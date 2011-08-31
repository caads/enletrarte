#!/usr/bin/env python
import os, sys

sys.path.append('/home/django')
sys.path.append('/home/django/enletrarte')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
