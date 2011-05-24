from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from social.networks.oauthtwitter import OAuthApi

CONSUMER_KEY = getattr(settings, 'TWITTER_CONSUMER_KEY', '')
CONSUMER_SECRET = getattr(settings, 'TWITTER_CONSUMER_SECRET', '')
REQUEST_TOKEN_SESSION_ID = 'twitter:request_token'

def twitter_login(request):
    twitter = OAuthApi(CONSUMER_KEY, CONSUMER_SECRET)
    request_token = twitter.getRequestToken()
    request.session[REQUEST_TOKEN_SESSION_ID] = request_token
    login_url = twitter.getAuthenticationURL(request_token)
    return HttpResponseRedirect(login_url)

def twitter_login_done(request):
    twitter = OAuthApi(CONSUMER_KEY, CONSUMER_SECRET)
    request_token = request.session[REQUEST_TOKEN_SESSION_ID]
    access_token = twitter.getAccessToken(request_token)

    user = authenticate(access_token=access_token)

    if not user:
        login_url = getattr(settings, 'LOGIN_URL', '/')
        return HttpResponseRedirect(login_url)

    login(request, user)

    return HttpResponseRedirect(request.GET.get('next', '/'))
