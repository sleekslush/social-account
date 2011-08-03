from django.conf import settings
from social.views import OAuth2View, OAuth2LoginMixin, OAuth2CallbackMixin

class GithubOAuthView(OAuth2View):
    app_id = getattr(settings, 'GITHUB_CLIENT_ID')
    app_secret = getattr(settings, 'GITHUB_CLIENT_SECRET')
    base_url = 'https://github.com/login/oauth/'
    callback_name = 'social:github-login-done'
    authenticate_arg = 'github_access_token'

class GithubLoginView(OAuth2LoginMixin, GithubOAuthView):
    pass

class GithubCallbackView(OAuth2CallbackMixin, GithubOAuthView):
    pass
