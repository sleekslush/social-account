import facebook
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from social.models import FacebookUser

class FacebookBackend(object):
    def authenticate(self, fb_access_token):
        graph_api = facebook.GraphAPI(fb_access_token)
        
        try:
            user_info = graph_api.get_object('me')
        except:
            if settings.DEBUG:
                raise
            return None

        try:
            return FacebookUser.objects.get(uid=user_info['id']).user
        except FacebookUser.DoesNotExist:
            """User hasn't been created yet"""

        return FacebookUser.objects.create_profile(user_info).user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
