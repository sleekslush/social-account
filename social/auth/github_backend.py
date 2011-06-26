from django.conf import settings
from django.contrib.auth.models import User

class GithubBackend(object):
    CLIENT_ID = getattr(settings, 'GITHUB_CLIENT_ID')
    CLIENT_SECRET = getattr(settings, 'GITHUB_CLIENT_SECRET')
    
    def authenticate(self, access_token):
        pass

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
