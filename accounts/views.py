from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import  login as auth_login,authenticate,logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from posts.models import Post
import random
# Create your views here.

User = get_user_model()
colors=[
    "#4f46e5", "#ef4444", "#10b981",
    "#f59e0b", "#a855f7", "#06b6d4"
]
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        firstname = request.POST.get('fname', '').strip()
        lastname = request.POST.get('lname', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        re_password = request.POST.get('repassword', '')

        if not username or not password or not firstname or not lastname or not email:
            return render(request,'accounts/register.html',{'error':'All fields are required'})
        
        if password!=re_password:
            return render(request,'accounts/register.html',{'error':'Password didnt match'}) 
        
        if len(username) < 3:
            return render(request, "accounts/register.html", {
                "error": "Username must be at least 3 characters"
            })
        
        if len(password) < 6:
            return render(request, "accounts/register.html", {
                "error": "Password must be at least 6 characters"
            })
        
        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {
                "error": "Username already taken"
            })
        
        if User.objects.filter(email=email).exists():
            return render(request, "accounts/register.html", {
                "error": "Email already registered"
            })
        
        user = User.objects.create_user(
            first_name = firstname,
            last_name = lastname,
            username = username,
            email = email,
            password = password
        )
        user.avatar_color = random.choice(colors)
        user.save()
        return redirect('login')
    return render(request,'accounts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            return render(request,'accounts/login.html',{'error':'Both field are required'})
        user = authenticate(request,username=username,password=password)

        if user is not None:
            auth_login(request,user)
            return redirect('home')
        else:
            return render(request,'accounts/login.html',{'errors':'ivalied email or password'})
    return render(request,'accounts/login.html')


def forgot_password(request):
    return render(request,'accounts/forgot_password.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request,'home.html')

def profile(request):
    user_data = request.user
    post_type = request.GET.get('type')

    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    if post_type:
        posts = posts.filter(
            post_type=post_type
        )

    return render(request,'accounts/profile.html',{'user_data':user_data,'posts':posts,'current_type': post_type})

def post_detail(request,id):
    post = get_object_or_404(Post,id=id)

    return render(
        request,
        'posts/post_detail.html',
        {
            'post': post
        }
    )

def edit_profile(request):
    return render(request,'accounts/edit_profile.html')