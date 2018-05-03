""" Do not put secrets in this file. This file is public.
    For staging environment (Using Dokku)
"""
import os
import sys

from server.settings import RAVEN_IGNORE_EXCEPTIONS

ENV = 'staging'
PREFERRED_URL_SCHEME = 'https'

SECRET_KEY = os.getenv('SECRET_KEY')

CACHE_TYPE = 'simple'

DEBUG = False
ASSETS_DEBUG = False
TESTING_LOGIN = False
DEBUG_TB_INTERCEPT_REDIRECTS = False

SQLALCHEMY_TRACK_MODIFICATIONS = False
SENTRY_USER_ATTRS = ['email', 'name']

RQ_DEFAULT_HOST = REDIS_HOST = CACHE_REDIS_HOST = \
    os.getenv('REDIS_HOST', 'redis-master')
REDIS_PORT = 6379
RQ_POLL_INTERVAL = 2000
OAUTH2_PROVIDER_TOKEN_EXPIRES_IN = 28800

db_url = os.getenv('DATABASE_URL')
if db_url:
    db_url = db_url.replace('mysql://', 'mysql+pymysql://')
    db_url += "&sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"

else:
    db_url = os.getenv('SQLALCHEMY_URL', 'sqlite:///../oksqlite.db')

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

WTF_CSRF_CHECK_DEFAULT = True
WTF_CSRF_ENABLED = True
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # Max Upload Size is 10MB

STORAGE_PROVIDER = os.environ.get('STORAGE_PROVIDER',  'LOCAL')
STORAGE_SERVER = False
STORAGE_CONTAINER = os.environ.get('STORAGE_CONTAINER',  'ok-v3-user-files')
STORAGE_KEY = os.environ.get('STORAGE_KEY', '')
STORAGE_SECRET = os.environ.get('STORAGE_SECRET', '').replace('\\n', '\n')

if STORAGE_PROVIDER == 'LOCAL' and not os.path.exists(STORAGE_CONTAINER):
    os.makedirs(STORAGE_CONTAINER)

# TODO: NEW OAUTH SETTINGS

if "GOOGLE_ID" in os.environ or "GOOGLE_SECRET" in os.environ:
    OAUTH_PROVIDER='GOOGLE'
elif "MICROSOFT_APP_ID" in os.environ or "MICROSOFT_APP_SECRET" in os.environ:
    OAUTH_PROVIDER='MICROSOFT'
else:
    print("Please set the Google or Microsoft OAuth ID and Secret variables.")
    sys.exit(1)
        
# Service Keys
GOOGLE = dict(
    consumer_key=os.environ.get('GOOGLE_ID'),
    consumer_secret=os.environ.get('GOOGLE_SECRET'),
    base_url='https://www.googleapis.com/oauth2/v3/',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    profile_url="https://www.googleapis.com/plus/v1/people/me?access_token={}",
    userinfo_url="https://www.googleapis.com/oauth2/v3/userinfo?access_token={}",
    request_token_params={
        'scope': 'email',
        'prompt': 'select_account'
    },
    request_token_url=None,
    access_token_method='POST'
)

MICROSOFT = dict(
	consumer_key=os.getenv('MICROSOFT_APP_ID'), # TODO: make these generic across provider
	consumer_secret=os.getenv('MICROSOFT_APP_SECRET'),
    base_url='https://management.azure.com',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://login.microsoftonline.com/common/oauth2/token',
    authorize_url='https://login.microsoftonline.com/common/oauth2/authorize?resource=c0bbcec8-3f72-4e97-941c-1950300696b6' #?resource=https://management.azure.com/'
)

########

SENDGRID_AUTH = {
    'user': os.environ.get("SENDGRID_USER"),
    'key': os.environ.get("SENDGRID_KEY")
}

APPLICATION_INSIGHTS_KEY = os.getenv('APPLICATION_INSIGHTS_KEY')
