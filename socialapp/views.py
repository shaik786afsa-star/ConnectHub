from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Post, Like, Comment, Follow, Profile
from .forms import PostForm, CommentForm, ProfileForm


# Home Page
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})


# Create Post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            return redirect('/')

    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})


# Like / Unlike Post
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()

    return redirect('/')


# Add Comment
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )

    return redirect('/')


# Register
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('/')

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


# Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('/')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# Logout
def user_logout(request):
    logout(request)
    return redirect('/')


# Profile Page
def profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)

    profile_obj, created = Profile.objects.get_or_create(
        user=profile_user
    )

    posts = Post.objects.filter(
        user=profile_user
    ).order_by('-created_at')

    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    is_following = False

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    return render(
        request,
        'profile.html',
        {
            'profile_user': profile_user,
            'profile_obj': profile_obj,
            'posts': posts,
            'followers_count': followers_count,
            'following_count': following_count,
            'is_following': is_following,
        }
    )


# Follow / Unfollow User
@login_required
def follow_user(request, user_id):
    user_to_follow = User.objects.get(id=user_id)

    if user_to_follow != request.user:

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        if not created:
            follow.delete()

    return redirect(f'/profile/{user_id}/')
@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()

            return redirect(
                f'/profile/{request.user.id}/'
            )

    else:
        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'edit_profile.html',
        {'form': form}
    )
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user == request.user:
        post.delete()

    return redirect('/')