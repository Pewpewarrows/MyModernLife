# Django settings for tomeofwow project.

import os.path
import socket
from settings_auth import *

DEVELOPMENT_MODE = (socket.gethostname() == "Marco-PC")

if DEVELOPMENT_MODE:
    DEBUG = TEMPLATE_DEBUG = True
    PREPEND_WWW = False
    USE_ETAGS = False
    CACHE_BACKEND = "dummy:///"
else:
    DEBUG = TEMPLATE_DEBUG = False
    PREPEND_WWW = True
    USE_ETAGS = True
    # CACHE_BACKEND = "memcached://127.0.0.1:11211/"

PROJECT_ROOT = os.path.dirname(__file__)

DEFAULT_FROM_EMAIL = 'webmaster@marcosmodernlife.com'

ADMINS = (
    ('Marco Chomut', 'marco.chomut+modernlife@gmail.com'),
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Note that sensitive information, such as username/password/secretkey,
# are all stored in a separate settings file that is not tracked in git
# Replace with DATABASES dictionary in 1.2
DATABASE_ENGINE = 'postgresql_psycopg2'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

INTERNAL_IPS = (
    '127.0.0.1',
)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware', # Must be first
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    # 'django.contrib.FetchFromCacheMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',     # Requires 1.2
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.doc.XViewMiddleware',
    # 'django.middleware.transaction.TransactionMiddleware',    # Needed?
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'mymodernlife.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.databrowse',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.markup',
    # 'django.contrib.messages',    # Requires 1.2
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.syndication',
    'django.contrib.webdesign',
)

# AUTH_PROFILE_MODULE = 'profiles.UserProfile'

LOGIN_REDIRECT_URL = '/'

# ACCOUNT_ACTIVATION_DAYS = 7

# COMMENTS_APP = 'my_comment_app'

#DEBUG_TOOLBAR_PANELS = (
#    'debug_toolbar.panels.version.VersionDebugPanel',
#    'debug_toolbar.panels.sql.SQLDebugPanel',
#)
