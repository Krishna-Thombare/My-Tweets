from django.apps import AppConfig


class TweetConfig(AppConfig):
    name = 'tweet'

    def ready(self):
        from django.contrib.auth.models import User
        from django.core.validators import RegexValidator

        username_field = User._meta.get_field('username')
        username_field.validators = [RegexValidator(
            regex=r'^[\w\s.@+-]+$',
            message='Username can contain letters, numbers, spaces, and @/./+/-/_ only.'
        )]
