from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Like,Comment,SavedPost
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# Create your views here.
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post_type = request.POST.get('post_type')
        mood = request.POST.get('mood')
        background = request.POST.get('background')
        is_anonymous = request.POST.get('is_anonymous') == 'on'

        Post.objects.create(user=request.user,title=title,content=content,post_type=post_type,mood=mood,background=background,is_anonymous=is_anonymous)
        return redirect('create_post')
    
    return render(request,'posts/create_post.html')

def edit_post(request):
    return render(render,'posts/edit_post.html')

def feed(request):
    post_type = request.GET.get('type')
    posts = Post.objects.all().order_by('-created_at')
    if post_type:
        posts=posts.filter(post_type=post_type)

    return render(request,'posts/feed.html',{'posts': posts})

def like_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id
    )

    like = Like.objects.filter(
        user=request.user,
        post=post
    )

    if like.exists():

        like.delete()

    else:

        Like.objects.create(
            user=request.user,
            post=post
        )

    return redirect(request.META.get('HTTP_REFERER', 'feed'))

def comment_post(request,post_id):
    
    if request.method == 'POST':
        post = get_object_or_404(Post,id=post_id)
        comment = request.POST.get('comment')
        if comment:
            Comment.objects.create(user=request.user,post=post,content=comment)
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


def delete_comment(request,id):
    comment=get_object_or_404(Comment,id=id,user=request.user)
    if comment:
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


@require_POST
@login_required
def save_post(request,post_id):
    print("SAVE VIEW HIT", request.user, post_id)
    try:
        post = Post.objects.get(id=post_id)

        saved_obj = SavedPost.objects.filter(user=request.user, post=post)

        if saved_obj.exists():
            saved_obj.delete()
            saved = False
        else:
            SavedPost.objects.create(user=request.user, post=post)
            saved = True

        return JsonResponse({
            "saved": saved,
            "saved_count": SavedPost.objects.filter(post=post).count()
        })

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)


@login_required
@require_POST
def edit_post(request, post_id):

    try:
        post = Post.objects.get(id=post_id)

        # 🔒 Only owner can edit
        if post.user != request.user:
            return JsonResponse({"error": "Not allowed"}, status=403)

        # Get data from frontend
        title = request.POST.get("title")
        content = request.POST.get("content")
        mood = request.POST.get("mood")
        background = request.POST.get("background")

        # Update fields
        post.title = title
        post.content = content
        post.mood = mood

        # Only quote can change background
        if post.post_type == "quote":
            post.background = background

        post.save()

        return JsonResponse({
            "success": True,
            "message": "Post updated successfully"
        })

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    

@login_required
@require_POST
def delete_post(request, post_id):

    try:
        post = Post.objects.get(id=post_id)

        if post.user != request.user:
            return JsonResponse({"error": "Not allowed"}, status=403)

        post.delete()

        return JsonResponse({"success": True})

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)