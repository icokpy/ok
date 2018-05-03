""" Do not put secrets in this file. This file is public.
    Production config.
"""
import os
import sys

from server.settings import RAVEN_IGNORE_EXCEPTIONS
from server.settings import GOOGLE, MICROSOFT

ENV = 'prod'
PREFERRED_URL_SCHEME = 'https'

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False
ASSETS_DEBUG = False
TESTING_LOGIN = False
DEBUG_TB_INTERCEPT_REDIRECTS = False
# The Google Cloud load balancer behaves like two proxies: one with the external
# fowarding rule IP, and one with an internal IP.
# See https://cloud.google.com/compute/docs/load-balancing/http/#target_proxies
# Including Nginx too makes 3 proxies.
NUM_PROXIES = 3

db_url = os.getenv('DATABASE_URL')
if db_url:
    db_url = db_url.replace('mysql://', 'mysql+pymysql://')
    db_url += "&sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
else:
    print("The database URL is not set!")
    sys.exit(1)

SQLALCHEMY_DATABASE_URI = db_url

# If using sqlite use absolute path (otherwise we break migrations)
sqlite_prefix = 'sqlite:///'
if SQLALCHEMY_DATABASE_URI.startswith(sqlite_prefix):
    SQLALCHEMY_DATABASE_URI = (sqlite_prefix +
            os.path.abspath(SQLALCHEMY_DATABASE_URI[len(sqlite_prefix) + 1:]))

sql_ca_cert = os.getenv('SQL_CA_CERT')
azure_uri = "azure"
if sql_ca_cert and azure_uri in SQLALCHEMY_DATABASE_URI:
    SQLALCHEMY_ENGINE_OPTS = {'connect_args': {'ssl': {'ca': sql_ca_cert}}}

SQLALCHEMY_TRACK_MODIFICATIONS = False
SENTRY_USER_ATTRS = ['email', 'name']
PREFERRED_URL_SCHEME = 'https'
OAUTH2_PROVIDER_TOKEN_EXPIRES_IN = 28800

WTF_CSRF_CHECK_DEFAULT = True
WTF_CSRF_ENABLED = True

MAX_CONTENT_LENGTH = 30 * 1024 * 1024  # Max Upload Size is 30MB

CACHE_TYPE = 'redis'
CACHE_KEY_PREFIX = 'ok-web'

RQ_DEFAULT_HOST = REDIS_HOST = CACHE_REDIS_HOST = \
    os.getenv('REDIS_HOST', 'redis-master')
REDIS_PORT = 6379
RQ_POLL_INTERVAL = 2000

STORAGE_PROVIDER = os.environ.get('STORAGE_PROVIDER',  'GOOGLE_STORAGE')
STORAGE_SERVER = False
STORAGE_CONTAINER = os.environ.get('STORAGE_CONTAINER',  'ok-v3-user-files')
STORAGE_KEY = os.environ.get('STORAGE_KEY', '')
STORAGE_SECRET = os.environ.get('STORAGE_SECRET', '').replace('\\n', '\n')

# TODO: NEW OAUTH SETTINGS

if "GOOGLE_ID" in os.environ or "GOOGLE_SECRET" in os.environ:
    OAUTH_PROVIDER='GOOGLE'
elif "MICROSOFT_APP_ID" in os.environ or "MICROSOFT_APP_SECRET" in os.environ:
    OAUTH_PROVIDER='MICROSOFT'
else:
    print("Please set the Google or Microsoft OAuth ID and Secret variables.")
    sys.exit(1)
        
########

SENDGRID_AUTH = {
    'user': os.environ.get("SENDGRID_USER"),
    'key': os.environ.get("SENDGRID_KEY")
}

APPLICATION_INSIGHTS_KEY = os.getenv('APPLICATION_INSIGHTS_KEY')
