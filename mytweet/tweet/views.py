from django.shortcuts import render
from .models import Tweet, Profile
from .forms import TweetForm, UserRegistrationForm, ProfileEditForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import re
from django.utils.safestring import mark_safe
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# Create your views here.

# Home page listing all recent tweets
def tweet_list(request): 
    all_tweets = Tweet.objects.all().order_by('-created_at')

    user_tweets = []

    if request.user.is_authenticated:
        user_tweets = all_tweets.filter(user=request.user)
    
    return render(request, 'tweet_list.html', {'all_tweets': all_tweets, 'user_tweets': user_tweets})

# Create new tweet
@login_required   # This decorator ensures that only authenticated users can access the view. Else redirected to the login page.
@xframe_options_exempt   # It allows the view to be embedded in an iframe, useful for the modal form functionality.
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            if request.GET.get('embed') == '1':
                return HttpResponse('<script>window.parent.location.reload();</script>')
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {
        'form': form,
        'embed': request.GET.get('embed') == '1',
    })

# Edit tweet
@login_required
@xframe_options_exempt
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            if request.GET.get('embed') == '1':
                return HttpResponse('<script>window.parent.location.reload();</script>')
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_form.html', {
        'form': form,
        'embed': request.GET.get('embed') == '1',
    })

# Delete tweet
@login_required
@xframe_options_exempt
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        tweet.delete()
        if request.GET.get('embed') == '1':
            return HttpResponse('<script>window.parent.location.reload();</script>')
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {
        'tweet': tweet,
        'embed': request.GET.get('embed') == '1',
    })

# User registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])   # Set the password for the user using the cleaned data from the form
            user.save()   # Save the user to the database

            Profile.objects.create(
                user=user,
                handle=form.cleaned_data['handle'],
                photo=form.cleaned_data.get('photo'),
                city=form.cleaned_data.get('city', ''),
                country=form.cleaned_data.get('country', ''),
            )

            login(request, user)   # Log the user in after successful registration
            return redirect('tweet_list')   # Redirect the user to the tweet list page after successful registration
    else:
        form = UserRegistrationForm() 

    return render(request, 'registration/register.html', {'form': form})

# Search tweets
def search_tweets(request):
    query = request.GET.get('q', "")
    tweets = []

    if query:
        search_query = SearchQuery(query, config='english')
        search_vector = SearchVector('text', config='english', weight='A') + SearchVector('user__username', config='english', weight='B')

        tweets = list(
            Tweet.objects.annotate(
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gt=0).order_by('-rank', '-created_at')
        )

        for tweet in tweets:
            highlighted = re.sub(
                f'({re.escape(query)})',
                r'<mark>\1</mark>',
                tweet.text,
                flags=re.IGNORECASE
            )
            tweet.highlighted_text = mark_safe(highlighted)

    return render(request, 'search.html', {'tweets': tweets, 'query': query})

# User profile page
def profile(request, handle):
    user_profile = get_object_or_404(Profile, handle=handle)
    profile_user = user_profile.user
    profile_tweets = Tweet.objects.filter(user=profile_user).order_by('-created_at')

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'user_profile': user_profile,
        'profile_tweets': profile_tweets,
    })

# Profile edit
@login_required
@xframe_options_exempt
def profile_edit(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            if request.GET.get('embed') == '1':
                return HttpResponse('<script>window.parent.location.reload();</script>')
            return redirect('profile', handle=user_profile.handle)
    else:
        form = ProfileEditForm(instance=user_profile)
    return render(request, 'profile_edit.html', {
        'form': form,
        'embed': request.GET.get('embed') == '1',
    })

# About us page
def aboutus(request):
    return render(request, 'aboutus.html')
    


    



    

        
