# social-account is an awesome django authentication app

## What does it do?
I was really surprised to see that there was no real simple way to handle OAuth-style authentication in Django, so I wrote social-account.
Basically it helps you easily integrate 3rd party authentication into your application, handling all the nasty details behind the scenes.
The app will seamlessly extend the User object and give you access to a custom UserProfile that contains extended information about the user
as provided by the 3rd party network.

## What networks does it support?

- Facebook
- Twitter
- Github
- Other (*easily extendable to support OAuth2-style logins*)

## Installation
Installing the app is super simple. You can use setuptools to get started.

    $ python setup.py install

## Configuration
Once the app is installed, there are a few settings you'll have to put into settings.py

1. Make sure you specify which social networks you can log into

        AUTHENTICATION_BACKENDS = (
                'social.auth.facebook_backend.FacebookBackend',
                'social.auth.twitter_backend.TwitterBackend',
                'social.auth.github_backend.GithubBackend',
                )

2. Specify the custom user profile to store additional information about the user

        AUTH_PROFILE_MODULE = 'social.UserProfile'

3. Configure the application key and application secret for each service you specify in `AUTHENTICATION_BACKENDS`

    **Facebook**

        FACEBOOK_APP_ID = '<app id>'
        FACEBOOK_APP_SECRET = '<app secret>'

    **Github**

        GITHUB_CLIENT_ID = '<client id>'
        GITHUB_CLIENT_SECRET = '<client secret>'

    **Twitter**

        TWITTER_CONSUMER_KEY = '<consumer key>'
        TWITTER_CONSUMER_SECRET = '<consumer secret>'

4. Create the database tables

        $ ./manage.py syncdb

## Who wrote this amazing piece of software?
social-account is a Disorderly Zen production written by [Craig Slusher](https://github.com/sleekslush) and released under a [BSD License](http://www.opensource.org/licenses/bsd-license.php).
