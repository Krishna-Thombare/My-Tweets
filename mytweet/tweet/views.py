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
from django.core.paginator import Paginator

# Create your views here.

# Home page listing all recent tweets
def tweet_list(request):
    tweets = Tweet.objects.select_related('user', 'user__profile').order_by('-created_at')

    paginator = Paginator(tweets, 20)
    page = request.GET.get('page', 1)
    all_tweets = paginator.get_page(page)

    user_tweets = []
    if request.user.is_authenticated:
        user_tweets = Tweet.objects.select_related('user', 'user__profile').filter(user=request.user).order_by('-created_at')

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
    query = request.GET.get('q', "").strip()
    tweets = []

    if query:
        search_query = SearchQuery(query, config='english', search_type='plain')

        # Tweet text (higher priority) and username (lower priority)
        search_vector = (
            SearchVector('text', config='english', weight='A') + 
            SearchVector('user__username', config='english', weight='B')
        )

        # Split query into words to match any word (OR search)
        words = query.split()
        or_query = SearchQuery(' | '.join(words), config='english', search_type='raw') if len(words) > 1 else search_query

        tweets = list(
            Tweet.objects.select_related('user', 'user__profile').annotate(
                rank=SearchRank(search_vector, or_query)
            ).filter(rank__gt=0).order_by('-rank', '-created_at')
        )

        # Compile the regex once to reuse it for all matching tweets
        pattern = re.compile(re.escape(query), re.IGNORECASE)

        for tweet in tweets:
            tweet.highlighted_text = mark_safe(
                pattern.sub(r"<mark>\g<0></mark>", tweet.text)
            )

    return render(request, 'search.html', {'tweets': tweets, 'query': query})

# User profile page
def profile(request, handle):
    user_profile = get_object_or_404(Profile, handle=handle)
    profile_user = user_profile.user
    profile_tweets = Tweet.objects.select_related('user', 'user__profile').filter(user=profile_user).order_by('-created_at')

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
    


    



    

        
