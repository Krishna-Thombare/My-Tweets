from django import forms
from .models import Tweet, Profile, CustomUser
from django.contrib.auth.forms import UserCreationForm

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

class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'register-input'})
    )
    handle = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'register-input', 'placeholder': '@yourhandle'})
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'register-file'})
    )
    city = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'register-input', 'placeholder': 'e.g. Pune'})
    )
    country = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'register-input', 'placeholder': 'e.g. India'})
    )

    class Meta:   # Meta class is used to specify the model and fields that will be used in the form
        model = CustomUser   # Specify the model that this form is associated with
        fields = ('username', 'email', 'password1', 'password2') # Specify the fields that will be included in the form
        widgets = {
            'username': forms.TextInput(attrs={'class': 'register-input'}),
        }

    
