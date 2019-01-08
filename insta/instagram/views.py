from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from instagram.forms import SignUpForm, LoginForm, NewPostForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from instagram.models import User, Post

login_url = reverse_lazy('login')


@login_required(login_url=login_url)
def newsfeed(request):
    user = request.user

    if user.is_authenticated():
        followers, following = get_followers_and_following(user)
        posts = get_posts(user)
        # posts = Post.objects.filter(user__username=user.username)
        return render(request, 'instagram/newsfeed.html',
                      {'user': user, 'followers': followers,
                       'following': following,
                       'posts':posts})
    else:
        return HttpResponseRedirect(reverse('login'))

def get_posts(user):
    posts = Post.objects.filter(user__username=user.username)
    followers, following = get_followers_and_following(user)
    following = get_user_objects(following, 'following')
    for followee in following:
        followee_posts = Post.objects.filter(user__username=followee.username)
        posts = posts | followee_posts
    return posts.order_by('-created_at')


def get_followers_and_following(user):
    followers = User.all_followers.get_queryset(user.username).all()
    following = User.all_following.filter(username=user.username)
    for followee in following:
        if followee['following'] is None:
            following = User.objects.none()
            break
    return followers, following



def index(request):
    return HttpResponseRedirect('login')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url=login_url)
def search(request):
    errors = []
    if 'query' in request.GET:
        query = request.GET['query']
        if not query:
            errors.append('Enter a search term')
        elif len(query) > 20:
            errors.append('Please enter at most 20 characters')
        else:
            users = User.objects.filter(Q(username__icontains=query) |
                                        Q(first_name__icontains=query) |
                                        Q(last_name__icontains=query))
            return render(request, 'instagram/search_results.html',
                          {'users': users, 'query': query})
    return render(request, 'instagram/search_form.html',
                  {'errors': errors})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('newsfeed'))
    form = LoginForm()
    return render(request, 'instagram/login.html', {'form': form,})


@login_required(login_url=login_url)
def profile(request, pk):
    errors = []
    if not pk:
        errors.append('ERROR')
        return render(request, 'instagram/profile.html',
                      {'errors': errors,
                      })
    else:
        profile_owner = get_object_or_404(User, pk=pk)
        user = request.user
        logged_in_profile = profile_owner.username == user.username
        if user.is_authenticated():
            followers, following = get_followers_and_following(user)
        else:
            followers, following = get_followers_and_following(profile_owner)
        already_followed = is_already_followed(profile_owner, following)
    return render(request, 'instagram/profile.html',
                  {'errors': errors,
                   'user': profile_owner,
                   'logged_in_profile': logged_in_profile,
                   'already_followed': already_followed,
                   'following': following,
                   'followers': followers,
                   })


def is_already_followed(profile_owner, following):
    for followee in following:
        if followee['following'] == profile_owner.pk:
            return True
    return False


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.bio = form.cleaned_data.get('bio')
            user.avatar = form.cleaned_data.get('avatar')
            user.save()
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('newsfeed'))
    else:
        form = SignUpForm()
    return render(request, 'instagram/signup.html', {'form': form})


@login_required(login_url=login_url)
def follow_profile(request, pk):
    errors = []
    user = request.user
    to_follow = get_object_or_404(User, pk=pk)
    user.following.add(to_follow)
    user.save()

    to_follow.refresh_from_db()
    followers, following = get_followers_and_following(to_follow)
    return render(request, 'instagram/profile.html',
                  {'errors': errors,
                   'user': to_follow,
                   'logged_in_profile': False,
                   'already_followed': True,
                   'following': following,
                   'followers': followers,
                   })


@login_required(login_url=login_url)
def unfollow_profile(request, pk):
    errors = []
    user = request.user
    to_unfollow = get_object_or_404(User, pk=pk)
    user.following.remove(to_unfollow)
    to_unfollow.refresh_from_db()

    followers, following = get_followers_and_following(to_unfollow)
    return render(request, 'instagram/profile.html',
                  {'errors': errors,
                   'user': to_unfollow,
                   'logged_in_profile': False,
                   'already_followed': False,
                   'following': following,
                   'followers': followers,
                   })


@login_required(login_url=login_url)
def show_followers(request, pk):
    target_profile = get_object_or_404(User, pk=pk)
    followers, following = get_followers_and_following(target_profile)
    return render(request, 'instagram/show_followers.html',
                        {'followers': followers})

@login_required(login_url=login_url)
def show_following(request, pk):
    target_profile = get_object_or_404(User, pk=pk)
    followers, following = get_followers_and_following(target_profile)
    following = get_user_objects(following, 'following')
    return render(request, 'instagram/show_followers.html',
                        {'followers': following})

def new_post(request):
    user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            post = form.save()
            post.refresh_from_db()
            post.user = user
            post.save()
            return HttpResponseRedirect(reverse('newsfeed'))
    else:
        form = NewPostForm(user=user)
        return render(request, 'instagram/new_post.html', {'form': form})


def get_user_objects(query_set, key):
    users = []
    for item in query_set:
        try:
            user = get_object_or_404(User, pk=int(item[key]))
            users.append(user)
        except KeyError:
            print('ERROR')
    return users
