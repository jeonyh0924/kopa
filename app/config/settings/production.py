import requests

from .base import *

PRODUCTION_JSON = json.load(open(os.path.join(SECRET_DIR, 'production.json')))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [

    '.amazonaws.com',

]

STATIC_ROOT = os.path.join(ROOT_DIR, '.static')

WSGI_APPLICATION = 'config.wsgi.production.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = PRODUCTION_JSON['DATABASES']

# Health Check 도메인을 허용하는 코드
try:
    EC2_IP = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4').text
    ALLOWED_HOSTS.append(EC2_IP)
except requests.exceptions.RequestException:
    pass
