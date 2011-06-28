import oauth2
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

BASE_URL = 'https://github.com/login/oauth/'
CLIENT_ID = getattr(settings, 'GITHUB_CLIENT_ID')
CLIENT_SECRET = getattr(settings, 'GITHUB_CLIENT_SECRET')

def github_login(request):
    client = oauth2.Client2(CLIENT_ID, CLIENT_SECRET, BASE_URL)
    authorization_url = client.authorization_url()
    return HttpResponseRedirect(authorization_url)

def github_login_done(request):
    client = oauth2.Client2(CLIENT_ID, CLIENT_SECRET, BASE_URL)
    data = client.access_token(request.GET['code'])
    access_token = data.get('access_token')

    user = authenticate(access_token=access_token)

    if not user:
        login_url = getattr(settings, 'LOGIN_URL', '/')
        return HttpResponseRedirect(login_url)

    login(request, user)

    return HttpResponseRedirect(request.GET.get('redirect_uri', '/'))
