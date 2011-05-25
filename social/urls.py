from django.conf.urls.defaults import *

urlpatterns = patterns('social.views',
    url(r'^facebook-login/$', 'facebook.facebook_login', name='facebook-login'),
    url(r'^facebook-login/done/$', 'facebook.facebook_login_done', name='facebook-login-done'),
    #url(r'^google-login/$', 'google.google_login', name='google-login'),
    #url(r'^google-login/done/$', 'google.google_login_done', name='google-login-done'),
    url(r'^twitter-login/$', 'twitter.twitter_login', name='twitter-login'),
    url(r'^twitter-login/done/$', 'twitter.twitter_login_done', name='twitter-login-done'),
)
