import os

from werkzeug.exceptions import (Forbidden, NotFound, Unauthorized,
                                 ClientDisconnected, MethodNotAllowed)

RAVEN_IGNORE_EXCEPTIONS = [Forbidden, NotFound, Unauthorized,
                           ClientDisconnected, MethodNotAllowed]


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
    tenent_id=os.getenv('MICROSOFT_TENANT_ID', 'common'),
    base_url='https://management.azure.com',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://login.microsoftonline.com/{tenant_id}/oauth2/token' \
        .format(tenant_id=os.getenv('MICROSOFT_TENANT_ID', 'common')),
    authorize_url='https://login.microsoftonline.com/{tenant_id}/oauth2/authorize' \
        .format(tenant_id=os.getenv('MICROSOFT_TENANT_ID', 'common')),
        request_token_params={
        'resource' : os.getenv('MICROSOFT_APP_ID'),
        'response_mode' : 'query',
        # 'scope': 'email profile',
        'prompt': 'login'
    }
)
