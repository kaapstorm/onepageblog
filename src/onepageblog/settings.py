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
"""
Django settings for onepageblog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import django.conf.global_settings as DEFAULT_SETTINGS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^#fo)6kwyk2bda1u8od@i$xiwhu2tjoxac=rx4u1p(%p6!pbcc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'posts',
    'posts.templatetags',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'onepageblog.urls'

WSGI_APPLICATION = 'onepageblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/static/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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

TEMPLATE_DIRS = (BASE_DIR + '/templates/',)

SITE_ID = 1

# Disqus website shortname for Disqus comments.
# Set "DISQUS_SHORTNAME = None" to disable Disqus comments.
DISQUS_SHORTNAME = 'onepageblog'

# Disallow raw HTML in posts. Valid values are of "remove", "replace" or
# "escape". Set to False to support markup not supported by Markdown, but risk
# cross-site scripting.
MARKDOWN_SAFE_MODE = 'escape'

# The title to use as the page heading and the text in title bar.
BLOG_TITLE = 'onepageblog'

# Blog footer appears at the bottom of all pages, including the 404 and 500
# error pages. It is wrapped in HTML5 "<footer>" tags.
BLOG_FOOTER = """
        <p class="blurb">
          <em><span xmlns:dct="http://purl.org/dc/terms/"
                    href="http://purl.org/dc/dcmitype/Text"
                    property="dct:title"
                    rel="dct:type">onepageblog</span></em>
          content by <span xmlns:cc="http://creativecommons.org/ns#"
                           property="cc:attributionName"
                           rel="cc:attributionURL">Norman Hooper</span>
          is licensed under a
          <a rel="license"
             href="http://creativecommons.org/licenses/by-sa/3.0/">Creative
          Commons Attribution-ShareAlike 3.0 Unported License</a>.

          The source code is released under the
          <a href="https://www.gnu.org/licenses/agpl.html">GNU Affero General
          Public License</a>, and is available at
          <a href="https://github.com/kaapstorm/onepageblog">GitHub</a>.

          The lightbulb icon is by
          <a href="http://tango.freedesktop.org/The_People">the people from
          the Tango! project</a>. The favicon is from the
          <a href="http://www.famfamfam.com/lab/icons/silk/">famfamfam Silk
          icon set</a> by Mark James.
        </p>
"""

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'posts.context_processors.blog_settings',
)

# Import local overrides
try:
    from onepageblog.settings_local import *
except ImportError:
    pass
