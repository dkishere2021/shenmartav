# Django settings for shenmartav project - should be the same for every instance

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_URLCONF = 'shenmartav.urls'

USE_TZ = True
USE_I18N = True
USE_L10N = True

import os, sys
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_PATH, 'apps'))

MEDIA_ROOT = os.path.join(PROJECT_PATH, '..', 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATIC_ROOT = os.path.join(PROJECT_PATH, '..', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
#    'django.contrib.messages.context_processors.messages',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.multilingual.MultilingualURLMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
#    'cms.middleware.toolbar.ToolbarMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates')
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.comments',
    'django.contrib.markup',

    # third-party
    'south',
    'reversion',
    'mptt',
    'menus',
    'sekizai',
    'haystack',
    'sorl.thumbnail',
    'modeltranslation',

    # cms
    'cms',
    'cms_search',
    'cms.plugins.file',
    'cms.plugins.link',
    'cms.plugins.picture',
    #'cms.plugins.snippet',
    'cms.plugins.teaser',
    'cms.plugins.text',
    #'cms.plugins.flash',
    #'cms.plugins.googlemap',
    #'cms.plugins.video',
    #'cms.plugins.twitter',

    # mysociety.org
    'popit',
    #'mapit',

    # blog
    'basic.inlines',
    'basic.blog',
    'tagging',
    'markdown',

    # in-house
    'api',
    'representative',
    'votingrecord',
    'incomedeclaration',
    'draftlaw',
    'question',
    'contact',
)



###########################################################
# testing-related
###########################################################
SOUTH_TESTS_MIGRATE = False
if 'test' in sys.argv:
    from settings import DATABASES
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}



###########################################################
# login
# after login (which is handled by django.contrib.auth), redirect to the
# dashboard rather than 'accounts/profile' (the default).
###########################################################
LOGIN_REDIRECT_URL = '/'



###########################################################
# logging
#
# the default log settings are very noisy.
###########################################################
LOG_LEVEL = "DEBUG"
LOG_FILE = "log/shenmartav.log"
LOG_FORMAT = "[%(name)s]: %(message)s"
LOG_SIZE = 65536  # 8192 bits = 8 kb
LOG_BACKUPS = 32  # number of logs to keep


###########################################################
# markdown
###########################################################
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})
MARKITUP_SET = 'markitup/sets/markdown'



###########################################################
# mapit
###########################################################
#MAPIT_AREA_SRID = 27770
#MAPIT_AREA_SRID = 4326
#MAPIT_COUNTRY = 'uk'
#MAPIT_RATE_LIMIT = ()



###########################################################
# CMS
###########################################################
gettext = lambda s: s
CMS_TEMPLATES = (
    ('simple.html', gettext('Simple Template')),
    ('3col.html', gettext('3 Column Template')),
)
CMS_LANGUAGE_CONF = {
    'ka': ['en'],
}
CMS_FRONTEND_LANGUAGES = ('ka', 'en', 'ka')



###########################################################
# haystack
###########################################################
HAYSTACK_SITECONF = 'search_sites'
HAYSTACK_SEARCH_ENGINE = 'xapian'
HAYSTACK_XAPIAN_PATH = os.path.join(PROJECT_PATH, '..', 'xapian_index')
#import xapian
#HAYSTACK_XAPIAN_FLAGS = xapian.QueryParser.FLAG_DEFAULT | xapian.QueryParser.FLAG_PARTIAL
# FIXME: This is a complete hack to get around circular imports in 
# django-haystack and other apps such as django-endless-pagination
SKIP_COMMANDS = ['syncdb', 'migrate', 'schemamigration', 'datamigration', 'reset',
    'import_draftlaws', 'import_incomedeclarations', 'import_representatives',
    'import_votingrecords',
    'update_attendance', 'update_assets', 'update_votingrecordresults',
    'update_votingrecords']
if any([command in sys.argv for command in SKIP_COMMANDS]):
        HAYSTACK_ENABLE_REGISTRATIONS = False



###########################################################
# modeltranslation
###########################################################
MODELTRANSLATION_TRANSLATION_REGISTRY = 'shenmartav.translation'



###########################################################
# piecharts
###########################################################
PIECHART_DIR = os.path.join(MEDIA_ROOT, 'representatives/piecharts')