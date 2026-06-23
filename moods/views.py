from django.shortcuts import render
from .models import MoodQuestion,MoodOption
from django.contrib.auth.decorators import login_required
from .audius_service import get_songs
# Create your views here.

@login_required
def mood_test(request):
    questions = MoodQuestion.objects.prefetch_related('options')
    if request.method == "POST":
        mood_scores = {
            'happy': 0,
            'sad': 0,
            'healing': 0,
            'motivated': 0,
            'calm': 0,
        }
        for key, value in request.POST.items():

            if key.startswith('question_'):

                option = MoodOption.objects.get(id=value)

                mood_scores[option.mood] += option.score
        final_mood = max(
            mood_scores,
            key=mood_scores.get
        )
        songs = get_songs(final_mood)
        return render(
            request,
            'moods/mood_result.html',
            {
                'mood': final_mood,
                'scores': mood_scores,
                'songs': songs
            }
        )
    return render(request,'moods/mood_test.html',{'questions':questions})

@login_required
def recommended_music(request):
    return render(request,'moods/mood_result.html')