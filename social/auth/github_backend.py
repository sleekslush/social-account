from django.conf import settings
from django.contrib.auth.models import User
from github2.client import Github
from social.models import GithubUser

class GithubBackend(object):
    CLIENT_ID = getattr(settings, 'GITHUB_CLIENT_ID')
    CLIENT_SECRET = getattr(settings, 'GITHUB_CLIENT_SECRET')
    
    def authenticate(self, access_token):
        github = Github(access_token=access_token)

        try:
            user_info = github.users.show(None)
        except:
            if settings.DEBUG:
                raise
            return None

        try:
            return GithubUser.objects.get(login=user_info.login).user
        except GithubUser.DoesNotExist:
            """User hasn't been created yet"""

        return GithubUser.objects.create_profile(user_info).user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
