import oauth2
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import View

SOCIAL_LOGIN_SUCCESS_KEY = 'social_login_success_url'

def reset_next_url(request):
    """
    If the view was requested with ?next=/something/, store it in the session so we can
    redirect to it on a successful login. If ?next doesn't exist, delete any previous redirect
    URL from the session.
    """
    if 'next' in request.GET:
        request.session[SOCIAL_LOGIN_SUCCESS_KEY] = request.GET['next']
    else:
        delete_next_url(request.session)

def get_next_url(session):
    """
    Returns the redirect URL from the session if it exists. Otherwise, return the URL
    specified in settings. If all else fails, return '/'
    """
    return session.get(SOCIAL_LOGIN_SUCCESS_KEY, getattr(settings, 'LOGIN_SUCCESS_URL', '/'))

def delete_next_url(session):
    """
    Delete the ?next URL from session.
    """
    try:
        del session[SOCIAL_LOGIN_SUCCESS_KEY]
    except KeyError:
        pass

class OAuth2View(View):
    def __init__(self):
        self.client = oauth2.Client2(self.app_id, self.app_secret, self.base_url)

class OAuth2LoginMixin(OAuth2View):
    def get(self, request, *args, **kwargs):
        reset_next_url(request)

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

        next_url = get_next_url(request.session)

        return HttpResponseRedirect(next_url)
