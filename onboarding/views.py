from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify

from .models import *


def index(request):
    return render(request, 'onboarding/index.html')


def step_one(request):
    energy_choice = request.GET.get('energy_choice')
    if energy_choice:
        return redirect('step-two', energy_choice=energy_choice)

    return render(request, 'onboarding/step-one.html')


def step_two(request, energy_choice):
    formatted_choice = reverse_slug(energy_choice)
    emotion_group = get_object_or_404(
        EmotionGroup.objects.prefetch_related('emotions'),
        name=formatted_choice
    )
    emotions = emotion_group.emotions.all()
    if request.method == 'POST':
        selected_emotion = request.POST.get('emotion')
        if selected_emotion:
            return redirect('step-three', energy_choice=energy_choice, emotion=selected_emotion.lower())
        else:
            error_message = "Please select an emotion before continuing."
            return render(request, 'onboarding/step-two.html', {
                'emotion_group': emotion_group,
                'emotions': emotions,
                'error_message': error_message,
                'selected_emotion': selected_emotion,
            })

    return render(request, 'onboarding/step-two.html', {
        'emotion_group': emotion_group,
        'emotions': emotions
    })


def step_three(request, energy_choice, emotion):
    formatted_choice = reverse_slug(energy_choice)

    if request.method == 'POST':
        user_name = request.POST.get('user_name', '').strip()
        emotion_reason = request.POST.get('emotion_reason', '').strip()
        selected_emotion = get_object_or_404(Emotion, emotion__iexact=emotion)
        if len(emotion_reason) < 257:
            UserEmotionData.objects.create(
                name=user_name,
                reason=emotion_reason,
                energy_choice=energy_choice,
                emotion=selected_emotion
            )
            return redirect('main:emotions')
        else:
            error_message = 'Your Reason is more then 256 letters.'
            return render(request, 'onboarding/step-three.html', {
                'energy_choice': formatted_choice,
                'emotion': emotion.title(),
                'energy_choice_slug': slugify(formatted_choice),
                'error_message': error_message
            })

    return render(request, 'onboarding/step-three.html', {
        'energy_choice': formatted_choice,
        'emotion': emotion.title(),
        'energy_choice_slug': slugify(formatted_choice)
    })


def reverse_slug(text: str) -> str:
    result = text.replace('-', ' ').title()
    return result
