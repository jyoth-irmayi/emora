from django.shortcuts import render,redirect
from .models import StoryChain,StoryContribution
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def create_story_chain(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        starter_content = request.POST.get('starter_content')
        StoryChain.objects.create(
            title=title,
            starter_content = starter_content,
            created_by=request.user

        )    
    return render(request,'interactions/create_story_chain.html')

def continue_story(request,story_id):
    story = get_object_or_404(
        StoryChain,
        id=story_id
    )

    if request.method == "POST":

        content = request.POST.get(
            'content'
        )

        if content:

            StoryContribution.objects.create(
                story=story,
                user=request.user,
                content=content
            )

        return redirect(
            'post_detail',
            story_id=story.id
        )

    contributions = story.contributions.all().order_by(
        'created_at'
    )

    return render(
        request,
        'interactions/continue_story.html',
        {
            'story': story,
            'contributions': contributions
        }
    )

@login_required
def story_detail(request,pk):
    story = get_object_or_404(
        StoryChain.objects.prefetch_related('contributions__user'),
        pk=pk
    )

    contributions = story.contributions.all().order_by('created_at')

    return render(request,'interactions/story_detail.html',{
        'story': story,
        'contributions': contributions
    })