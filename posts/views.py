from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Like,Comment

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

    return redirect('feed')

def comment_post(request,post_id):
    
    if request.method == 'POST':
        post = get_object_or_404(Post,id=post_id)
        comment = request.POST.get('comment')
        if comment:
            Comment.objects.create(user=request.user,post=post,content=comment)
    return redirect('feed')

def delete_comment(request,id):
    comment=get_object_or_404(Comment,id=id,user=request.user)
    if comment:
        comment.delete()
    return redirect('feed')