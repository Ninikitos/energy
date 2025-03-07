from collections import deque
from datetime import timedelta

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count, Q
from django.shortcuts import render
from django.utils.timezone import now

from onboarding.models import UserEmotionData


class EmotionTracker:
    def __init__(self):
        self.hour_blocks = deque(maxlen=24)
        self.initialize_blocks()

    def initialize_blocks(self):
        """Initialize 24 hours of empty blocks with newest first"""
        current_time = now().replace(minute=0, second=0, microsecond=0)

        # Create blocks starting with current hour first
        for hour_offset in range(0, 24):
            block_time = current_time - timedelta(hours=hour_offset)
            self.hour_blocks.append({
                'start_time': block_time,
                'intervals': {
                    i: [] for i in range(0, 60, 10)
                }
            })

    def update_blocks(self, current_time):
        """Update blocks when a new hour starts"""
        if not self.hour_blocks:
            self.initialize_blocks()
            return

        newest_block = self.hour_blocks[0]
        while newest_block['start_time'] + timedelta(hours=1) <= current_time:
            # Add new hour at the beginning
            new_block = {
                'start_time': newest_block['start_time'] + timedelta(hours=1),
                'intervals': {i: [] for i in range(0, 60, 10)}
            }
            self.hour_blocks.appendleft(new_block)
            newest_block = new_block

    def add_emotion_data(self, emotion_data):
        """Add emotion entries to appropriate intervals"""
        for block in self.hour_blocks:
            block_end = block['start_time'] + timedelta(hours=1)

            # Filter data for current hour block
            hour_data = [
                entry for entry in emotion_data
                if block['start_time'] <= entry.created_on < block_end
            ]

            # Sort data into 10-minute intervals
            for entry in hour_data:
                interval_key = (entry.created_on.minute // 10) * 10
                block['intervals'][interval_key].append(entry)

    @staticmethod
    def calculate_trend(intervals):
        """Calculate trend based on the last 3 non-empty intervals"""
        non_empty_intervals = [
                                  interval for interval in intervals
                                  if interval['dominant'] is not None
                              ][-3:]

        if len(non_empty_intervals) < 2:
            return None

        # Count transitions
        positive_transitions = 0
        negative_transitions = 0

        for i in range(len(non_empty_intervals) - 1):
            current = non_empty_intervals[i]['dominant']
            next_emotion = non_empty_intervals[i + 1]['dominant']

            if current == 'negative' and next_emotion in ['equal', 'positive']:
                positive_transitions += 1
            elif current == 'equal' and next_emotion == 'positive':
                positive_transitions += 1
            elif current == 'positive' and next_emotion in ['equal', 'negative']:
                negative_transitions += 1
            elif current == 'equal' and next_emotion == 'negative':
                negative_transitions += 1

        # Determine overall trend
        if positive_transitions > negative_transitions:
            return 'improving'
        elif negative_transitions > positive_transitions:
            return 'declining'
        elif positive_transitions == negative_transitions and positive_transitions > 0:
            return 'fluctuating'
        return 'stable'

    def get_formatted_data(self):
        """Format data for frontend display"""
        formatted_blocks = []

        for block in self.hour_blocks:
            formatted_intervals = []

            for interval_start in range(0, 60, 10):
                entries = block['intervals'][interval_start]
                positive_count = sum(1 for e in entries if e.emotion.type == 'Positive')
                negative_count = sum(1 for e in entries if e.emotion.type == 'Negative')

                dominant = None
                if positive_count > negative_count:
                    dominant = 'positive'
                elif negative_count > positive_count:
                    dominant = 'negative'
                elif negative_count == positive_count and positive_count > 0:
                    dominant = 'equal'

                formatted_intervals.append({
                    'interval': f"{interval_start:02d}:{00:02d}-{interval_start:02d}:10",
                    'positive': positive_count,
                    'negative': negative_count,
                    'dominant': dominant
                })

            trend = self.calculate_trend(formatted_intervals)

            formatted_blocks.append({
                'hour': block['start_time'].strftime('%Y-%m-%d %H:00'),
                'intervals': formatted_intervals,
                'trend': trend
            })

        return formatted_blocks


def emotions(request):
    current_time = now()
    last_24_hours = current_time - timedelta(hours=24)
    last_7_days = current_time - timedelta(days=7)

    # Get the filter parameter from the request
    emotion_filter = request.GET.get('filter', 'all')

    # Base queryset with select_related to reduce database hits
    base_queryset = UserEmotionData.objects.filter(created_on__gte=last_24_hours).select_related('emotion')

    # Apply filtering based on the emotion filter early to reduce data processed
    if emotion_filter == 'positive':
        user_data_queryset = base_queryset.filter(emotion__type='Positive')
    elif emotion_filter == 'negative':
        user_data_queryset = base_queryset.filter(emotion__type='Negative')
    else:
        user_data_queryset = base_queryset

    # Get unique emotion types in one query
    emotion_types = set(base_queryset.values_list('emotion__type', flat=True).distinct())
    has_positive = 'Positive' in emotion_types
    has_negative = 'Negative' in emotion_types

    # Use annotate to perform counts in a single query rather than multiple aggregates
    emotion_counts = base_queryset.aggregate(
        total=Count('id'),
        positive=Count('id', filter=Q(emotion__type='Positive')),
        negative=Count('id', filter=Q(emotion__type='Negative'))
    )
    total_count = emotion_counts['total']

    # Calculate percentages only if needed
    if total_count:
        positive_percentage = (emotion_counts['positive'] / total_count * 100)
        negative_percentage = (emotion_counts['negative'] / total_count * 100)
    else:
        positive_percentage = negative_percentage = 0

    # Use first() directly on querysets - avoid redundant orderings
    most_recent_emotion = base_queryset.order_by('-created_on').first()

    # Reuse annotated queries for most popular emotions
    most_popular_24_hours = (
        base_queryset
        .values('emotion__emotion')
        .annotate(count=Count('id'))
        .order_by('-count')
        .first()
    )

    most_popular_7_days = (
        UserEmotionData.objects.filter(created_on__gte=last_7_days)
        .select_related('emotion')
        .values('emotion__emotion')
        .annotate(count=Count('id'))
        .order_by('-count')
        .first()
    )

    # Paginate after filtering to improve efficiency
    user_data_queryset = user_data_queryset.order_by('-created_on')
    paginator = Paginator(user_data_queryset, 8)

    # Safer page number conversion
    try:
        page_number = int(request.GET.get('page', 1))
        page_number = max(1, min(page_number, paginator.num_pages))
    except (ValueError, TypeError):
        page_number = 1

    page_obj = paginator.page(page_number)

    # Initialize tracker and add data only once
    tracker = EmotionTracker()
    tracker.update_blocks(current_time)
    tracker.add_emotion_data(page_obj)
    formatted_blocks = tracker.get_formatted_data()

    # Choose template based on request type
    template = 'main/partials/emotion-data.html' if request.headers.get('HX-Request') else 'main/main.html'

    return render(request, template, {
        'user_data': page_obj,
        'has_positive': has_positive,
        'has_negative': has_negative,
        'hour_blocks': formatted_blocks,
        'current_filter': emotion_filter,
        'most_recent_emotion': most_recent_emotion.emotion if most_recent_emotion else None,
        'most_popular_24_days': most_popular_24_hours['emotion__emotion'] if most_popular_24_hours else None,
        'most_popular_7_days': most_popular_7_days['emotion__emotion'] if most_popular_7_days else None,
        'positive_percentage': round(positive_percentage, 1),
        'negative_percentage': round(negative_percentage, 1)
    })


def emotions_all(request):
    current_time = now()
    last_24_hours = current_time - timedelta(hours=24)

    user_data_queryset = (UserEmotionData.objects.filter(created_on__gte=last_24_hours)
                          .order_by('-created_on')
                          .select_related('emotion'))
    has_positive = user_data_queryset.filter(emotion__type="Positive").exists()
    has_negative = user_data_queryset.filter(emotion__type="Negative").exists()

    return render(request, 'main/partials/emotion-data.html', {
        'user_data': user_data_queryset,
        'has_positive': has_positive,
        'has_negative': has_negative,
    })


def emotions_positive(request):
    current_time = now()
    last_24_hours = current_time - timedelta(hours=24)

    positive_user_data = UserEmotionData.objects.filter(created_on__gte=last_24_hours, emotion__type='Positive')

    return render(request, 'main/partials/emotion-data.html', {
        'user_data': positive_user_data,
        'current_filter': 'positive',
        'has_positive': True
    })


def emotions_negative(request):
    current_time = now()
    last_24_hours = current_time - timedelta(hours=24)

    negative_user_data = UserEmotionData.objects.filter(created_on__gte=last_24_hours, emotion__type='Negative')

    return render(request, 'main/partials/emotion-data.html', {
        'user_data': negative_user_data,
        'current_filter': 'negative',
        'has_negative': True,
    })


def comments(request, comment_id):

    context = {}
    return render(request, 'main/comments.html', context)