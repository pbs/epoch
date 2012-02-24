import os

# This will activate the virtualenv. See activate_this file for more info.
path_to_activate = '/home/devel/deployed/current/ve/bin/activate_this.py'
execfile(path_to_activate, dict(__file__=path_to_activate))

# Now we need to configure the actual wsgi application
os.environ['DJANGO_SETTINGS_MODULE'] = 'epoch.settings'

import django.core.handlers.wsgi

_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    return _application(environ, start_response)
