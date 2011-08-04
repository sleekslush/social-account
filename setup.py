from distutils.core import setup
from social import __version__

setup(
        name='DZ Social Account',
        description='A badass authentication app for django websites that uses social networks',
        version=__version__,
        author='Craig Slusher',
        author_email='craig@disorderlyzen.com',
        packages=['social']
        )
