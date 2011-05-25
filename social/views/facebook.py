import urllib
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def facebook_login(request):
    params = {
            'client_id': getattr(settings, 'FACEBOOK_APP_ID'),
            'redirect_uri': request.build_absolute_uri(reverse('social:facebook-login-done'))
            }

    facebook_authorize_url = 'https://graph.facebook.com/oauth/authorize?%s' % urllib.urlencode(params)

    return HttpResponseRedirect(facebook_authorize_url)

def facebook_login_done(request):
    user = authenticate(request=request)

    if not user:
        login_url = getattr(settings, 'LOGIN_URL', '/')
        return HttpResponseRedirect(login_url)

    login(request, user)

    return HttpResponseRedirect(request.GET.get('next', '/'))
