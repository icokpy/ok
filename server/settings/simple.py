""" Do not put secrets in this file. This file is public.
    Production config.
"""
import os
import sys

from server.settings import RAVEN_IGNORE_EXCEPTIONS

ENV = 'simple'
PREFERRED_URL_SCHEME = 'http'

SECRET_KEY = os.getenv('SECRET_KEY')
OAUTH_PROVIDER='NotSet'

DEBUG = False
ASSETS_DEBUG = False
TESTING_LOGIN = False
DEBUG_TB_INTERCEPT_REDIRECTS = False

db_url = os.getenv('DATABASE_URL')
if db_url:
    if 'mysql' in db_url:
        db_url = db_url.replace('mysql://', 'mysql+pymysql://')
        db_url += "&sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
else:
    print("The database URL is not set!")
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

SQLALCHEMY_TRACK_MODIFICATIONS = False
SENTRY_USER_ATTRS = ['email', 'name']
PREFERRED_URL_SCHEME = 'https'
OAUTH2_PROVIDER_TOKEN_EXPIRES_IN = 28800

WTF_CSRF_CHECK_DEFAULT = True
WTF_CSRF_ENABLED = True

CACHE_TYPE = 'simple'
CACHE_KEY_PREFIX = 'ok-web'

RQ_DEFAULT_HOST = REDIS_HOST = CACHE_REDIS_HOST = \
    os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = 6379
RQ_POLL_INTERVAL = 2000

STORAGE_PROVIDER = 'LOCAL'
STORAGE_SERVER = False
STORAGE_CONTAINER = os.path.abspath("./local-storage")

if not os.path.exists(STORAGE_CONTAINER):
    os.makedirs(STORAGE_CONTAINER)


def try_google_oauth():
    print('inside the google check..')
    try:
        os.environ["GOOGLE_ID"]
        os.environ["GOOGLE_SECRET"]
        return True
    except KeyError:
        print("Please set the google login variables.")
        return False
        

def try_microsoft_oauth():
    print('inside the microsoft check..')
    try:
        os.environ["MICROSOFT_APP_ID"]
        os.environ["MICROSOFT_APP_SECRET"]
        return True
    except KeyError:
        print("Please set the microsoft app ID and Secret variables.")
        return False


from flask_oauthlib.client import OAuth, OAuthException
oauth = OAuth()

if try_google_oauth():
    OAUTH_PROVIDER=oauth.remote_app('google', app_key = 'GOOGLE')
    pass
elif try_microsoft_oauth():
    OAUTH_PROVIDER=oauth.remote_app('microsoft', app_key = 'MICROSOFT')
    pass
else:
    sys.exit(1)
        
# Service Keys
# TODO put the rest of the google OAuth settings here that are now in Auth.py
GOOGLE = dict(
    consumer_key=os.environ.get('GOOGLE_ID'),
    consumer_secret=os.environ.get('GOOGLE_SECRET'),
    base_url='https://www.googleapis.com/oauth2/v3/',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_params={
        'scope': 'email',
        'prompt': 'select_account'
    },
    request_token_url=None,
    access_token_method='POST')

ms_access_token_url = 'https://login.microsoftonline.com/{Tenant}/oauth2/token'.format(Tenant=os.environ.get('MICROSOFT_TENENT_ID'))
ms_authorize__url = 'https://login.microsoftonline.com/{Tenant}/oauth2/authorize'.format(Tenant=os.environ.get('MICROSOFT_TENENT_ID'))

MICROSOFT = dict(
	consumer_key=os.getenv('MICROSOFT_APP_ID'),
	consumer_secret=os.getenv('MICROSOFT_APP_SECRET'),
	base_url='http://ignore',  # We won't need this
	access_token_url=ms_access_token_url,
	authorize_url=ms_authorize__url,
	request_token_params={
        'scope': 'email'
    },
	request_token_url=None,
	access_token_method='POST'
)


SENDGRID_AUTH = {
    'user': os.environ.get("SENDGRID_USER"),
    'key': os.environ.get("SENDGRID_KEY")
}

APPLICATION_INSIGHTS_KEY = os.getenv('APPLICATION_INSIGHTS_KEY')
