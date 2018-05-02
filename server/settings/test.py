import os

ENV = 'test'
SECRET_KEY = os.getenv('OK_SESSION_KEY', 'testkey')

DEBUG = False
ASSETS_DEBUG = True
TESTING_LOGIN = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
INSTANTCLICK = False

SQLALCHEMY_TRACK_MODIFICATIONS = False

db_url = os.getenv('DATABASE_URL')
if db_url and 'mysql' in db_url:
    db_url = db_url.replace('mysql://', 'mysql+pymysql://')
    db_url += "&sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
else:
    db_url = os.getenv('DATABASE_URL', 'sqlite:///../oktest.db')

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

WTF_CSRF_CHECK_DEFAULT = False
WTF_CSRF_ENABLED = False

STORAGE_PROVIDER = os.getenv('STORAGE_PROVIDER', 'LOCAL')
STORAGE_SERVER = False
STORAGE_CONTAINER = os.getenv('STORAGE_CONTAINER', os.path.abspath('./local-storage'))
STORAGE_KEY = os.getenv('STORAGE_KEY', '')
STORAGE_SECRET = os.environ.get('STORAGE_SECRET', '').replace('\\n', '\n')

if STORAGE_PROVIDER == 'LOCAL' and not os.path.exists(STORAGE_CONTAINER):
    os.makedirs(STORAGE_CONTAINER)

CACHE_TYPE = 'simple'

RQ_DEFAULT_HOST = REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
RQ_POLL_INTERVAL = 2000
RQ_DEFAULT_DB = 2  # to prevent conflicts with development

GOOGLE_CONSUMER_KEY = ''
