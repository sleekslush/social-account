from django.utils.functional import SimpleLazyObject
from social.models import UserProfileView

def user_profile(request):
    def get_user():
        get_profile = request.user.get_profile
        request.user.get_profile = lambda: UserProfileView(get_profile(), request)
        return request.user

    return {'user': SimpleLazyObject(get_user)}
