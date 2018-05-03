import os

from server.settings import GOOGLE, MICROSOFT

ENV = 'dev'
SECRET_KEY = os.getenv('OK_SESSION_KEY', 'changeinproductionkey')
CACHE_TYPE = 'simple'

DEBUG = True
ASSETS_DEBUG = True
TESTING_LOGIN = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
INSTANTCLICK = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
db_url = os.getenv('DATABASE_URL')
if db_url:
    if 'mysql' in db_url:
        db_url = db_url.replace('mysql://', 'mysql+pymysql://')
        db_url += "&sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"
    SQLALCHEMY_DATABASE_URI = db_url
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../oksqlite.db'
# SQLALCHEMY_ECHO = True

# If using sqlite use absolute path (otherwise we break migrations)
sqlite_prefix = 'sqlite:///'
if SQLALCHEMY_DATABASE_URI.startswith(sqlite_prefix):
    SQLALCHEMY_DATABASE_URI = (sqlite_prefix + 
            os.path.abspath(SQLALCHEMY_DATABASE_URI[len(sqlite_prefix) + 1:]))

sql_ca_cert = os.getenv('SQL_CA_CERT')
azure_uri = "azure"
if sql_ca_cert and azure_uri in SQLALCHEMY_DATABASE_URI:
    SQLALCHEMY_ENGINE_OPTS = {'connect_args': {'ssl': {'ca': sql_ca_cert}}}

RQ_DEFAULT_HOST = REDIS_HOST = 'localhost'
REDIS_PORT = 6379
RQ_POLL_INTERVAL = 2000

MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # Max Upload Size is 20MB

STORAGE_PROVIDER = os.environ.get('STORAGE_PROVIDER',  'LOCAL')
STORAGE_SERVER = False
STORAGE_CONTAINER = os.environ.get('STORAGE_CONTAINER',
                                   os.path.abspath("./local-storage"))
STORAGE_KEY = os.environ.get('STORAGE_KEY', '')
STORAGE_SECRET = os.environ.get('STORAGE_SECRET', '').replace('\\n', '\n')

if STORAGE_PROVIDER == 'LOCAL' and not os.path.exists(STORAGE_CONTAINER):
    os.makedirs(STORAGE_CONTAINER)

GOOGLE_CONSUMER_KEY = ''

APPLICATION_INSIGHTS_KEY = os.getenv('APPLICATION_INSIGHTS_KEY')
