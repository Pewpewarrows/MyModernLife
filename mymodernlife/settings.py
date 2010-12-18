# Django settings for mymodernlife project.

import os.path
import socket

# The only settings that ever need to be in a separate file are passwords
# and Secret Key info. All other local/dev/staging/production logic can just
# stay in this file.
try:
    from settings_auth import *
except:
    pass

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

DEFAULT_FROM_EMAIL = 'webmaster@marcosmodernlife.com'

ADMINS = (
    ('Marco Chomut', 'marco.chomut+modernlife@gmail.com'),
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
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

# Quick hack to get HttpOnly cookies until changeset 14707 is in the next release,
# adding the SESSION_COOKIE_HTTPONLY variable.
SESSION_COOKIE_PATH = '/;HttpOnly'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
)

if USE_I18N:
    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.i18n',)

# DO NOT modify the order of these, they have to wrap in a specific order
MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware', # Must be first
    'django.middleware.gzip.GZipMiddleware',
    # 'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.doc.XViewMiddleware',
    # 'django.middleware.transaction.TransactionMiddleware',    # Needed?
    'trackback.middleware.PingbackUrlInjectionMiddleware',
    'xframeoptions.middleware.Header',
)

ROOT_URLCONF = 'mymodernlife.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

# Alternative:
"""
TEMPLATE_DIRS = ()
for root, dirs, files in os.walk(PROJECT_PATH):
    if 'templates' in dirs: TEMPLATE_DIRS += (os.path.join(root, 'templates'),)
"""

INSTALLED_APPS = (
    # Included in Django
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    # 'django.contrib.databrowse', # read-only version of the admin
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.markup', # includes textile, markdown, ReST
    'django.contrib.messages',
    'django.contrib.redirects', # db-level redirects, as opposed to urlconfs
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.syndication',
    'django.contrib.webdesign', # lorem ipsum generator
    
    # Third-Party
    'django_extensions',
    'easy_thumbnails',
    'indexer',
    'mailer',
    'mediagenerator',
    'notification',
    'oembed',
    'paging',
    'sentry',
    'sentry.client',
    'south',
    'taggit',
    'taggit_templatetags',
    'trackback',
    'xframeoptions',
    
    # Prometheus
    'blog',
    
    # Project-specific
)

# Custom Application Settings

LOGIN_REDIRECT_URL = '/'
# ACCOUNT_ACTIVATION_DAYS = 7

# AUTH_PROFILE_MODULE = 'profiles.UserProfile'

# COMMENTS_APP = 'my_comment_app'

THUMBNAIL_SUBDIR = 'thumbs'

X_FRAME_OPTIONS = 'SAMEORIGIN'

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

MEDIA_BUNDLES = (
    ('main.css',
        'css/reset.css',
        'css/scaffold.css',
        # 'css/base_theme.css',
        'css/mymodernlife.css',
    ),
    ('main.js',
        'js/lib/modernizr-1.5.min.js',
        'js/utils.js',
        'js/mymodernlife.js',
    ),
    ('belatedpng.js',
        'js/lib/dd_belatedpng.js',
    ),
)

GLOBAL_MEDIA_DIRS = (os.path.join(MEDIA_ROOT, 'static'),)

ROOT_MEDIA_FILTERS = {
    'css': 'mediagenerator.filters.yuicompressor.YUICompressor',
    'js': 'mediagenerator.filters.yuicompressor.YUICompressor',
}

YUICOMPRESSOR_PATH = os.path.join(MEDIA_ROOT, 'static', 'java', 'yuicompressor-2.4.2.jar')

# Hostname lists for local/dev/staging/production machines
SERVERS = (
    # ('foo', 'DEV'),
    # ('bar', 'STAGING'),
    # ('baz', 'PROD'),
)

if SERVERS:
    (SERVER_TYPE,) = [v for k, v in SERVERS if socket.gethostname() == k]
else:
    SERVER_TYPE = 'LOCAL'
    
# Seems like bad idea to default to LOCAL, which exposes DEBUG info, rather than PROD?

if SERVER_TYPE == 'LOCAL':
    DEBUG = True
    USE_ETAGS = False
    CACHE_BACKEND = 'dummy:///'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # How much does this fuck up toolbar rendering? Might have to just hardcode
    # where it needs to be in the middleware chain.
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
else:
    DEBUG = False
    USE_ETAGS = True
    # CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

PREPEND_WWW = False
TEMPLATE_DEBUG = True # Now that we have sentry, we always want that debug info
MEDIA_DEV_MODE = DEBUG
PRODUCTION_MEDIA_URL = '/media/'
