# This file is part of onepageblog.
#
# onepageblog is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# onepageblog is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with onepageblog.  If not, see <http://www.gnu.org/licenses/>.
#

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = False

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'posts',
    'posts.templatetags',
    'standalone',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'posts.urls'

WSGI_APPLICATION = 'standalone.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'posts.context_processors.blog_settings',
            ),
        }
    }
]
TEMPLATE_DIRS = (
    BASE_DIR + '/posts/templates/',
    BASE_DIR + '/standalone/templates/',
)

# Internationalization
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = False

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'standalone', 'static')

SITE_ID = 1

# Disqus website shortname for Disqus comments.
# Set "DISQUS_SHORTNAME = None" to disable Disqus comments.
DISQUS_SHORTNAME = os.environ.get('DISQUS_SHORTNAME')

# Disallow raw HTML in posts. Valid values are of "remove", "replace" or
# "escape". Set to False to support markup not supported by Markdown, but risk
# cross-site scripting.
MARKDOWN_SAFE_MODE = 'escape'

# The title to use as the page heading and the text in title bar.
BLOG_TITLE = 'onepageblog'

if os.environ['DEPLOY_ENV'] == 'dev':
    DEBUG = True
    TEMPLATE_DEBUG = True

    SECRET_KEY = os.environ['SECRET_KEY']

    ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(' ')

    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }

    STATIC_URL = '/static/'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }

else:
    raise ValueError(f"Unknown deploy environment {os.environ['DEPLOY_ENV']}")
