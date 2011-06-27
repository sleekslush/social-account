import urllib
import urllib2
import urlparse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

CLIENT_ID = getattr(settings, 'GITHUB_CLIENT_ID')
CLIENT_SECRET = getattr(settings, 'GITHUB_CLIENT_SECRET')

AUTHORIZE_URL = 'https://github.com/login/oauth/authorize?client_id=' + CLIENT_ID
ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'

def github_login(request):
    return HttpResponseRedirect(AUTHORIZE_URL)

def github_login_done(request):
    parameters = {
            'code': request.GET['code'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
            }

    result = urllib2.urlopen(ACCESS_TOKEN_URL, urllib.urlencode(parameters))
    parsed_qs = urlparse.parse_qs(result.read())
    access_token = parsed_qs['access_token'][0]

    user = authenticate(access_token=access_token)

    if not user:
        login_url = getattr(settings, 'LOGIN_URL', '/')
        return HttpResponseRedirect(login_url)

    login(request, user)

    return HttpResponseRedirect(request.GET.get('redirect_uri', '/'))
