from django.shortcuts import render

# Create your views here.
def create_post(request):
    return render(request,'posts/create_post.html')

def edit_post(request):
    return render(render,'posts/edit_post.html')

def feed(request):
    return render(request,'posts/feed.html')