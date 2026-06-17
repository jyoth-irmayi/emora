from django.shortcuts import render,redirect
from .models import StoryChain,StoryContribution,ChatRoom,ChatMessage,Notification
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Post
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.http import require_POST
# Create your views here.
from datetime import timedelta

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


def start_chat(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    other_user = post.user

    # Prevent chatting with yourself
    if other_user == request.user:
        return redirect('feed')

    room = ChatRoom.objects.filter(
        post=post,
        is_active=True
    ).filter(
        Q(user1=request.user, user2=other_user) |
        Q(user1=other_user, user2=request.user)
    ).first()

    if not room:
        room = ChatRoom.objects.create(
            post=post,
            user1=request.user,
            user2=other_user,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

    return redirect('chat_room', room_id=room.id)


def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)

    # Only participants can enter
    if request.user not in [room.user1, room.user2]:
        return redirect('feed')

    is_active = timezone.now() < room.expires_at

    if not is_active and room.is_active:
        room.is_active = False
        room.save()

    other_user = (
        room.user2
        if room.user1 == request.user
        else room.user1
    )

    messages = room.messages.order_by('created_at')

    remaining_seconds = max(
        0,
        int((room.expires_at - timezone.now()).total_seconds())
    )

    return render(
        request,
        "interactions/chat_room.html",
        {
            "room": room,
            "messages": messages,
            "other_user": other_user,
            "is_active": is_active,
            "remaining_seconds": remaining_seconds,
        }
    )

@login_required
def notifications(request):

    notifications = (
        request.user.notifications
        .order_by("-created_at")
    )
    notifications.filter(
        is_read=False
    ).update(is_read=True)
    return render(
        request,
        "interactions/notifications.html",
        {
            "notifications": notifications,
        }
    )


@login_required
def open_notification(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        receiver=request.user
    )

    notification.is_read = True
    notification.save()

    return redirect(
        "chat_room",
        room_id=notification.room.id
    )