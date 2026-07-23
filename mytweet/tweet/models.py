from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.templatetags.static import static

# Customize the default username field to allow spaces while validating
class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w\s.@+-]+$',
            message='Username can contain letters, numbers, spaces, and @/./+/-/_ only.'
        )]
    )

class Tweet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # String representation of the model in Django Admin
    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'
    
    # Return the tweet image if available.
    # If the tweet has no image, return the user's profile photo.
    # If neither exists, return a default placeholder image.
    def get_image_url(self):
        if self.photo:
            return self.photo.url
        try:
            if self.user.profile.photo:
                return self.user.profile.photo.url
        except Profile.DoesNotExist:
            pass
        return static('images/default_profile.png')
    
class Profile(models.Model):
    # Create a one-to-one relationship so each user has exactly one profile.
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # Unique username/handle displayed on the user's profile.
    handle = models.CharField(max_length=15, unique=True, blank=False)
    
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, max_length=255)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)

    class Meta:
        # Ensure the profile handle is never stored as an empty string.
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(handle=''),
                name='profile_handle_not_empty'
            )
        ]
    # Return the user's handle as the string representation of the profile.
    def __str__(self):
        return f'@{self.handle}'
    
