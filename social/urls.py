from django.conf.urls.defaults import *

urlpatterns = patterns('social.views',
    url(r'^facebook-login/$', 'facebook.facebook_login', name='facebook-login'),
    url(r'^facebook-login/done/$', 'facebook.facebook_login_done', name='facebook-login-done'),
    url(r'^github-login/$', 'github.github_login', name='github-login'),
    url(r'^github-login/done/$', 'github.github_login_done', name='github-login-done'),
    url(r'^twitter-login/$', 'twitter.twitter_login', name='twitter-login'),
    url(r'^twitter-login/done/$', 'twitter.twitter_login_done', name='twitter-login-done'),
)
