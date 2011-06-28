import oauth2
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

FACEBOOK_APP_ID = getattr(settings, 'FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = getattr(settings, 'FACEBOOK_APP_SECRET')
BASE_URL = 'https://graph.facebook.com/oauth/'

def facebook_login(request):
    client = oauth2.Client2(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, BASE_URL)

    authorization_url = client.authorization_url(
            redirect_uri=request.build_absolute_uri(reverse('social:facebook-login-done')))

    return HttpResponseRedirect(authorization_url)

def facebook_login_done(request):
    client = oauth2.Client2(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, BASE_URL)

    data = client.access_token(
            request.GET['code'],
            request.build_absolute_uri(reverse('social:facebook-login-done')))

    user = authenticate(fb_access_token=data.get('access_token'))

    if not user:
        login_url = getattr(settings, 'LOGIN_URL', '/')
        return HttpResponseRedirect(login_url)

    login(request, user)

    return HttpResponseRedirect(request.GET.get('next', '/'))
