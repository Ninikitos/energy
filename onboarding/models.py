from django.db import models


class EmotionGroup(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Emotion(models.Model):
    emotion = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=16, choices=[('Positive', 'Positive'), ('Negative', 'Negative')], db_index=True)
    group = models.ForeignKey(EmotionGroup, related_name='emotions', on_delete=models.CASCADE)

    def __str__(self):
        return self.emotion


class UserEmotionData(models.Model):
    name = models.CharField(max_length=32, default='Anonymous user', blank=True, null=True, db_index=True)
    energy_choice = models.CharField(max_length=32)
    emotion = models.ForeignKey(Emotion, related_name='user_emotions', on_delete=models.CASCADE)
    reason = models.TextField(max_length=256, default='Chose not to share.', blank=False, null=True)
    created_on = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name_plural = "User Emotion Data"

    def __str__(self):
        return f'{self.name} {self.energy_choice} {self.emotion}'

    def save(self,*args,**kwargs):
        if not self.reason:
            self.reason = 'Chose not to share.'
        if not self.name:
            self.name = 'Anonymous user'
        super().save(*args, **kwargs)