"""
Excerpt from: https://code.djangoproject.com/attachment/ticket/2407/django.cgi

This is probably the slowest way to serve django pages, as the python
interpreter, the django code-base and your site code has to be loaded every
time a request is served. FCGI and mod_python solve this problem, use them if
you can.

In order to speed things up it may be worth experimenting with running
uncompressed zips on the sys.path for django and the site code, as this can be
(theorectically) faster. See PEP-0273 (specifically Benchmarks).
http://www.python.org/dev/peps/pep-0273/

Make sure all python files are compiled in your code base. See
http://docs.python.org/lib/module-compileall.html

"""
__author__ = 'Paul Sargent'

import os
import sys


def run_with_cgi(application):
    environ = dict(os.environ.items())
    environ['wsgi.input'] = sys.stdin
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.multithread'] = False
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once'] = True

    if environ.get('HTTPS', 'off') in ('on', '1'):
        environ['wsgi.url_scheme'] = 'https'
    else:
        environ['wsgi.url_scheme'] = 'http'

    headers_set = []
    headers_sent = []

    def write(data):
        if not headers_set:
            raise AssertionError("write() before start_response()")

        elif not headers_sent:
            # Before the first output, send the stored headers
            status, response_headers = headers_sent[:] = headers_set
            sys.stdout.write('Status: %s\r\n' % status)
            for header in response_headers:
                sys.stdout.write('%s: %s\r\n' % header)
            sys.stdout.write('\r\n')

        sys.stdout.write(data if isinstance(data, str) else data.decode())
        sys.stdout.flush()

    def start_response(status, response_headers, exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    # Re-raise original exception if headers sent
                    exc_type, exc_value, exc_traceback = exc_info
                    raise exc_type(exc_value).with_traceback(exc_traceback)
            finally:
                exc_info = None  # avoid dangling circular ref
        elif headers_set:
            raise AssertionError("Headers already set!")

        headers_set[:] = [status, response_headers]
        return write

    result = application(environ, start_response)
    try:
        for data in result:
            if data:  # don't send headers until body appears
                write(data)
        if not headers_sent:
            write('')  # send headers now if body was empty
    finally:
        if hasattr(result, 'close'):
            result.close()
