import oauth2
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import View

class OAuth2View(View):
    def __init__(self):
        self.client = oauth2.Client2(self.app_id, self.app_secret, self.base_url)

class OAuth2LoginMixin(OAuth2View):
    def get(self, request, *args, **kwargs):
        authorization_url = self.client.authorization_url(
                redirect_uri=request.build_absolute_uri(reverse(self.callback_name)))

        return HttpResponseRedirect(authorization_url)

class OAuth2CallbackMixin(OAuth2View):
    def get(self, request, *args, **kwargs):
        data = self.client.access_token(
                request.GET['code'],
                request.build_absolute_uri(reverse(self.callback_name)))

        user = authenticate(**{self.authenticate_arg: data['access_token']})

        if not user:
            login_url = getattr(settings, 'LOGIN_URL', '/')
            return HttpResponseRedirect(login_url)

        login(request, user)

        return HttpResponseRedirect(getattr(settings, 'LOGIN_SUCCESS_URL', '/'))
