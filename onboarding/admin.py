from django.contrib import admin
from .models import *


@admin.register(EmotionGroup)
class EmotionGroupAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Emotion)
class EmotionAdmin(admin.ModelAdmin):
    list_display = ('emotion', 'type', 'group', )
    list_filter = ('group',)


@admin.register(UserEmotionData)
class UserEmotionDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'energy_choice', 'emotion', 'created_on',)