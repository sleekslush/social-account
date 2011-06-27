import cgi
import facebook
import urllib
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from social.models import FacebookUser

class FacebookBackend(object):
    FACEBOOK_APP_ID = getattr(settings, 'FACEBOOK_APP_ID')
    FACEBOOK_APP_SECRET = getattr(settings, 'FACEBOOK_APP_SECRET')

    def authenticate(self, request=None):
        fb_user = None
        user_info = facebook.get_user_from_cookie(
                request.COOKIES,
                self.__class__.FACEBOOK_APP_ID,
                self.__class__.FACEBOOK_APP_SECRET)

        if not user_info:
            fb_user_details = self._oauth_authenticate(request)

            if not fb_user_details:
                return None

            fb_user = fb_user_details['fb_user']

            user_info = {
                    'uid': fb_user['id'],
                    'access_token': fb_user_details['access_token']
                    }

        try:
            return FacebookUser.objects.get(uid=user_info['uid']).user
        except FacebookUser.DoesNotExist:
            """No problem. This just means the user hasn't been created in our
            system yet. Move on. There's nothing to see here.
            """

        if not fb_user:
            graph_api = facebook.GraphAPI(user_info['access_token'])
            fb_user = graph_api.get_object('me')

        return FacebookUser.objects.create_profile(fb_user).user

    def _oauth_authenticate(self, request):
        params = {
                'client_id': self.__class__.FACEBOOK_APP_ID,
                'client_secret': self.__class__.FACEBOOK_APP_SECRET,
                'code': request.GET.get('code', ''),
                'redirect_uri': request.build_absolute_uri(reverse('social:facebook-login-done'))
                }

        url = 'https://graph.facebook.com/oauth/access_token?%s' % urllib.urlencode(params)
        response = cgi.parse_qs(urllib.urlopen(url).read())

        if 'access_token' not in response:
            return None

        graph_api = facebook.GraphAPI(response['access_token'][-1])

        return {
                'access_token': graph_api.access_token,
                'fb_user': graph_api.get_object('me')
                }

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
