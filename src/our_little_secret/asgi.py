"""
ASGI config for our_little_secret project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'our_little_secret.settings')
application = get_asgi_application()
