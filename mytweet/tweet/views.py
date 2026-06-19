from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse

# Create your views here.

def tweet_list(request): 
    all_tweets = Tweet.objects.all().order_by('-created_at')

    user_tweets = []

    if request.user.is_authenticated:
        user_tweets = all_tweets.filter(user=request.user)
    
    return render(request, 'tweet_list.html', {'all_tweets': all_tweets, 'user_tweets': user_tweets})

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


    


    



    

        
