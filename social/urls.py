from django.conf.urls.defaults import *
from social.views.facebook import FacebookCallbackView, FacebookLoginView
from social.views.github import GithubCallbackView, GithubLoginView

urlpatterns = patterns('social.views',
    url(r'^facebook-login/$', FacebookLoginView.as_view(), name='facebook-login'),
    url(r'^facebook-login-done/$', FacebookCallbackView.as_view(), name='facebook-login-done'),
    url(r'^github-login/$', GithubLoginView.as_view(), name='github-login'),
    url(r'^github-login/done/$', GithubCallbackView.as_view(), name='github-login-done'),
    url(r'^twitter-login/$', 'twitter.twitter_login', name='twitter-login'),
    url(r'^twitter-login/done/$', 'twitter.twitter_login_done', name='twitter-login-done'),
)
