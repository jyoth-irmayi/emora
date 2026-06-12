from django.db import models

# Create your models here.
MOOD_CHOICES = (
    ('happy', 'Happy'),
    ('sad', 'Sad'),
    ('healing', 'Healing'),
    ('motivated', 'Motivated'),
    ('calm', 'Calm'),
)

class MoodQuestion(models.Model):

    question = models.CharField(
        max_length=255
    )

    def __str__(self):
        return self.question
    
    
class MoodOption(models.Model):

    question = models.ForeignKey(
        MoodQuestion,
        on_delete=models.CASCADE,
        related_name='options'
    )

    option_text = models.CharField(
        max_length=100
    )

    mood = models.CharField(
        max_length=20,
        choices=MOOD_CHOICES
    )

    score = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return self.option_text