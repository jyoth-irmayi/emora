from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import  login as auth_login,authenticate,logout
from django.contrib.auth import get_user_model
from .models import PasswordResetOTP
from django.contrib.auth.decorators import login_required
from posts.models import Post,SavedPost
from interactions.models import StoryChain
import random
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
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
    print('helloooo')
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)

            otp_obj = PasswordResetOTP.objects.create(user=user)
            print('hi',otp_obj.otp)
            send_mail(
                "Your Password Reset OTP",
                f"Your OTP is {otp_obj.otp}",
                "jyothirmayirani289@gmail.com",
                [email],
                fail_silently=False
            )

            request.session["reset_user_id"] = user.id
            return redirect("verify_otp")

        except User.DoesNotExist:
            error = "Email not found"
    return render(request,'accounts/forgot_password.html',{"error": error})


def verify_otp(request):
    user_id = request.session.get("reset_user_id")

    if not user_id:
        return redirect("forgot_password")
    
    user = User.objects.get(id=user_id)
    otp_obj = PasswordResetOTP.objects.filter(user=user).last()

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        if otp_obj and timezone.now() > otp_obj.created_at + timedelta(minutes=5):
            return render(request, "accounts/verify_otp.html", {
                "error": "OTP expired. Please resend OTP."
            })
        if not otp_obj or otp_obj.otp != entered_otp:
            return render(request, "accounts/verify_otp.html", {
                "error": "Invalid OTP"
            })
        
        return redirect("reset_password")
    return render(request,'accounts/verify_otp.html')


def resend_otp(request):
    user_id = request.session.get("reset_user_id")
    if not user_id:
        return redirect("forgot_password")

    user = User.objects.get(id=user_id)

    # delete old OTP
    PasswordResetOTP.objects.filter(user=user).delete()

    # create new OTP
    otp_obj = PasswordResetOTP.objects.create(user=user)

    send_mail(
        "Your New OTP",
        f"Your OTP is {otp_obj.otp}",
        "jyothirmayirani289@gmail.com",
        [user.email],
        fail_silently=False
    )

    return redirect("verify_otp")


def reset_password(request):
    user_id = request.session.get("reset_user_id")

    if not user_id:
        return redirect("forgot_password")

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, "accounts/reset_password.html", {
                "error": "Passwords do not match"
            })

        user.set_password(password)
        user.save()

        del request.session["reset_user_id"]

        return redirect("login")

    return render(request,'accounts/reset_password.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return render(request,'home.html')

@login_required
def profile(request):
    user_data = request.user
    post_type = request.GET.get('type')
    tab = request.GET.get('tab')
    posts = Post.objects.filter(user=request.user).order_by('-created_at')

    stories = None

    if post_type:
        posts = posts.filter(
            post_type=post_type
        )

    if tab == "saved":
        posts = Post.objects.filter(
            saved_posts__user=request.user
        ).order_by('-created_at')

        if post_type:
            posts = posts.filter(post_type=post_type)

    if tab == "my_stories":
        stories = StoryChain.objects.filter(
            created_by=request.user
        ).order_by('-created_at')

    
    return render(request,'accounts/profile.html',{'user_data':user_data,'posts':posts,'current_type': post_type,'tab': tab,'stories': stories})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.bio = request.POST.get('bio')
        user.avatar_color = request.POST.get("avatar_color")
        user.save()
        return redirect('profile')
    return render(request,'accounts/edit_profile.html')

@login_required
def post_detail(request,id):
    post = get_object_or_404(Post,id=id)

    return render(
        request,
        'posts/post_detail.html',
        {
            'post': post
        }
    )

