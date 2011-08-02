from django.conf import settings
from social.views import OAuth2View, OAuth2LoginMixin, OAuth2CallbackMixin

class FacebookOAuthView(OAuth2View):
    app_id = getattr(settings, 'FACEBOOK_APP_ID')
    app_secret = getattr(settings, 'FACEBOOK_APP_SECRET')
    base_url = 'https://graph.facebook.com/oauth/'
    callback_name = 'social:facebook-login-done'
    authenticate_arg = 'fb_access_token'

class FacebookLoginView(OAuth2LoginMixin, FacebookOAuthView):
    pass

class FacebookCallbackView(OAuth2CallbackMixin, FacebookOAuthView):
    pass
