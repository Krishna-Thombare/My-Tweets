from django.shortcuts import render
from .models import Tweet

# Create your views here.

def tweet_list(request): 
    all_tweets = Tweet.objects.all().order_by('-created_at')

    user_tweets = []

    if request.user.is_authenticated:
        user_tweets = all_tweets.filter(user=request.user)
    
    return render(request, 'tweet_list.html', {'all_tweets': all_tweets, 'user_tweets': user_tweets})


    


    



    

        
