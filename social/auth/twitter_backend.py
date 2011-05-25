from django.conf import settings
from django.contrib.auth.models import User
from social.models import TwitterUser
from social.networks.oauthtwitter import OAuthApi

class TwitterBackend(object):
    CONSUMER_KEY = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
    CONSUMER_SECRET = getattr(settings, 'TWITTER_CONSUMER_SECRET', '')

    def authenticate(self, access_token):
        twitter = OAuthApi(
                self.__class__.CONSUMER_KEY,
                self.__class__.CONSUMER_SECRET,
                access_token['oauth_token'],
                access_token['oauth_token_secret'])

        try:
            user_info = twitter.VerifyCredentials()
        except:
            if settings.DEBUG:
                raise
            return None
        else:
            if isinstance(user_info, Exception):
                if settings.DEBUG:
                    raise user_info
                return None

        try:
            return TwitterUser.objects.get(screen_name=user_info['screen_name']).user
        except TwitterUser.DoesNotExist:
            """User hasn't been created yet"""

        return TwitterUser.objects.create_profile(user_info).user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
