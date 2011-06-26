import oauth2
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

CLIENT_ID = getattr(settings, 'GITHUB_CLIENT_ID')
CLIENT_SECRET = getattr(settings, 'GITHUB_CLIENT_SECRET')

def github_login(request):
    client = oauth2.Client2(
            CLIENT_ID,
            CLIENT_SECRET,
            'https://github.com/login/oauth')

    authorization_url = client.authorization_url()
    return HttpResponseRedirect(authorization_url)

def github_login_done(request):
    pass
