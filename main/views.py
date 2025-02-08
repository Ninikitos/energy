from collections import deque
from datetime import timedelta

from django.core.paginator import Paginator, EmptyPage
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

            formatted_blocks.append({
                'hour': block['start_time'].strftime('%Y-%m-%d %H:00'),
                'intervals': formatted_intervals
            })

        return formatted_blocks


def emotions(request):
    current_time = now()
    last_24_hours = current_time - timedelta(hours=24)
    # Get the filter parameter from the request
    emotion_filter = request.GET.get('filter', 'all')
    # Get emotion data from database
    user_data_queryset = (UserEmotionData.objects.filter(created_on__gte=last_24_hours)
                          .order_by('-created_on')
                          .select_related('emotion'))

    emotion_types = set(user_data_queryset.values_list('emotion__type', flat=True))

    # Determine the presence of Positive/Negative emotions
    has_positive = 'Positive' in emotion_types
    has_negative = 'Negative' in emotion_types

    # Apply filtering based on the emotion filter
    if emotion_filter == 'positive':
        user_data_queryset = (user_data_queryset
                              .filter(emotion__type='Positive', created_on__gte=last_24_hours))
    elif emotion_filter == 'negative':
        user_data_queryset = (user_data_queryset
                              .filter(emotion__type='Negative', created_on__gte=last_24_hours))

    user_data_queryset = user_data_queryset.order_by('-created_on')
    paginator = Paginator(user_data_queryset, 8)

    page_number = max(1, min(int(request.GET.get('page', 1)), paginator.num_pages))

    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Initialize tracker
    tracker = EmotionTracker()
    tracker.update_blocks(current_time)

    # Process emotion data
    user_data = list(page_obj)
    tracker.add_emotion_data(user_data)

    # Get formatted data for template
    formatted_blocks = tracker.get_formatted_data()

    if request.headers.get('HX-Request'):
        template = 'main/partials/emotion-data.html'
    else:
        template = 'main/main.html'

    return render(request, template, {
        'user_data': page_obj,
        'has_positive': has_positive,
        'has_negative': has_negative,
        'hour_blocks': formatted_blocks,
        'current_filter': emotion_filter,
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
