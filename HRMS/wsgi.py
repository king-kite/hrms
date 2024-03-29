import environ
import os

from django.core.wsgi import get_wsgi_application
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

env = environ.Env()

DEBUG = bool(int(env('DEBUG')))

if DEBUG:
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HRMS.settings.dev')
else:
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HRMS.settings.prod')

application = get_wsgi_application()
