#!/usr/home/myusername/venv/onepageblog/bin/python3
import os
import sys

sys.path.insert(0, '/usr/home/myusername/src/onepageblog/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onepageblog.settings')

from django.core.wsgi import get_wsgi_application
from onepageblog.cgi import run_with_cgi


application = get_wsgi_application()
run_with_cgi(application)
