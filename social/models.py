import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.userprofile_set.create().save()

post_save.connect(create_user_profile, sender=User)

def generate_random_username():
    return uuid.uuid4().bytes.encode('base64').replace('/', '@').rstrip('\n=')

class UserProfileView(object):
    def __init__(self, user_profile, request):
        self.user_profile = user_profile
        self.request = request

    @property
    def user(self):
        return self.user_profile.user

    @property
    def profile_thumbnail(self):
        return self.user_profile.profile_thumbnail

    @property
    def friends(self):
        return self.user_profile.get_friends(self.request)

class UserProfileManager(models.Manager):
    def get_recent_users(self):
        return self.all()

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    profile_thumbnail = models.URLField(verify_exists=False)

    objects = UserProfileManager()

    def get_friends(self, request):
        pass

    def __unicode__(self):
        return 'Profile for %s' % self.user

class FacebookUserManager(models.Manager):
    def create_profile(self, fb_user):
        user = User(username=generate_random_username())
        user.first_name = fb_user['first_name']
        user.last_name = fb_user['last_name']
        user.save()

        user_profile = UserProfile.objects.get(user=user)
        user_profile.profile_thumbnail = 'http://graph.facebook.com/%s/picture?type=square' % fb_user['id']
        user_profile.save()

        return self.attach_profile(user, fb_user)

    def attach_profile(self, user, fb_user):
        facebook_user = user.facebook_profiles.create(uid=fb_user['id'])
        facebook_user.save()
        return facebook_user

class FacebookUser(models.Model):
    user = models.ForeignKey(User, related_name='facebook_profiles')
    uid = models.CharField(max_length=50, unique=True, db_index=True)

    objects = FacebookUserManager()

    def __unicode__(self):
        return 'Facebook profile uid %s' % self.uid

class TwitterUserManager(models.Manager):
    def create_profile(self, twitter_user):
        user = User(username=generate_random_username())
        user.first_name = twitter_user['name']
        user.save()

        user_profile = UserProfile.objects.get(user=user)
        user_profile.profile_thumbnail = 'http://api.twitter.com/1/users/profile_image/%s.json' % twitter_user['screen_name']
        user_profile.save()

        return self.attach_profile(user, twitter_user)

    def attach_profile(self, user, twitter_user):
        twitter_profile = user.twitter_profiles.create(screen_name=twitter_user['screen_name'])
        twitter_profile.save()
        return twitter_profile

class TwitterUser(models.Model):
    user = models.ForeignKey(User, related_name='twitter_profiles')
    screen_name = models.CharField(max_length=20, unique=True, db_index=True)

    objects = TwitterUserManager()

    def __unicode__(self):
        return 'Twitter profile screen name %s' % self.screen_name

class GithubUserManager(models.Manager):
    def create_profile(self, github_user):
        user = User(username=generate_random_username())
        user.first_name = github_user.name
        user.save()

        user_profile = UserProfile.objects.get(user=user)
        user_profile.profile_thumbnail = ''
        user_profile.save()

        return self.attach_profile(user, github_user)

    def attach_profile(self, user, github_user):
        github_profile = user.github_profiles.create(login=github_user.login)
        github_profile.save()
        return github_profile

class GithubUser(models.Model):
    user = models.ForeignKey(User, related_name='github_profiles')
    login = models.CharField(max_length=100, unique=True, db_index=True)

    objects = GithubUserManager()

    def __unicode__(self):
        return 'Github profile login %s' % self.login

class GoogleUserManager(models.Manager):
    def create_profile(self, google_user):
        user = User(username=generate_random_username())
        user.first_name = github_user.name
        user.save()

        user_profile = UserProfile.objects.get(user=user)
        user_profile.profile_thumbnail = ''
        user_profile.save()

        return self.attach_profile(user, google_user)

    def attach_profile(self, user, google_user):
        google_profile = user.github_profiles.create(login=google_user.login)
        google_profile.save()
        return google_profile

class GoogleUser(models.Model):
    user = models.ForeignKey(User, related_name='google_profiles')
    login = models.CharField(max_length=100, unique=True, db_index=True)

    objects = GoogleUserManager()

    def __unicode__(self):
        return 'Google profile login %s' % self.login
