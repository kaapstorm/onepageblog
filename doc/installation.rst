Installing onepageblog
======================

Clone the source code, configure settings specific to your server, and create 
initial database entries. ::

    $ git clone https://github.com/kaapstorm/onepageblog.git
    $ cd src/onepageblog/
    $ cp setings.py settings_local.py
    $ vim settings_local.py
    $ python manage.py syncdb

settings_local.py does not need all the settings that are configured in 
settings.py, just those settings you want to override. These will include 
DATABASES, SECRET_KEY, TEMPLATE_DIRS, MEDIA_ROOT, BLOG_TITLE and BLOG_FOOTER.
For more information, see the `Django settings`_ documentation.

When you have finished, how you need to deploy your blog will depend on your 
server configuration. You can find comprehensive details at the
`Django deployment`_ documentation.


.. _Django settings: https://docs.djangoproject.com/en/dev/topics/settings/
.. _Django deployment: https://docs.djangoproject.com/en/dev/howto/deployment/
