from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate,logout,login
from django.urls import reverse,reverse_lazy
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from Post.forms import PostForm

def sign_up(request):
     form = CreateNewUserForm()
     registered = False
     if request.method == 'POST':
          form  = CreateNewUserForm(data = request.POST)
          if form.is_valid():
               user = form.save()
               registered = True
               user_profile = UserProfile(user = user)
               user_profile.save()
               return redirect('login_page')
     context = {
          'title':"Sign up.",
          'form':form,
     }
     return render(request,'Account/signup.html',context=context)

def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Post:home')

    return render(request, 'Account/login.html', context={'title':'Login . Social','form':form})

@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form = EditProfile(instance=current_user)
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = EditProfile(instance=current_user)
            return redirect('profile')
    return render(request, 'Account/profile.html', context={'form':form, 'title':'Edit Profile . Social'})

@login_required
def logout_user(request):
    logout(request)
    return redirect('login_page')


@login_required
def profile(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('Post:home')
    return render(request, 'Account/user.html', context={'title':'User', 'form': form})

@login_required
def user(request, username):
    user_other = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=request.user, following=user_other)
    
    if user_other == request.user:
        return redirect('profile')
    
    context={
        'user_other':user_other,
        'already_followed':already_followed
    }
    return render(request, 'Account/user_other.html', context=context)



@login_required
def follow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    if not already_followed:
        followed_user = Follow(follower=follower_user, following=following_user)
        followed_user.save()
    return redirect('user', username)

@login_required
def unfollow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    already_followed.delete()
    return redirect('user',username)