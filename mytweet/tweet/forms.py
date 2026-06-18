from django import forms
from .models import Tweet

# Default Syntax
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet   # model name
        fields = ['text', 'photo']   # Mention model fields that are going to be used
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'tweet-form-textarea',
                'placeholder': "What's on your mind?",
                'rows': 4,
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'tweet-form-file',
            }),
        }


