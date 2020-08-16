"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

path = '/home/kiran/Documents/Development/core/SACCHAI/Backend'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
