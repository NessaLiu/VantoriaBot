import mysql.connector
import os
from urllib.parse import urlparse, uses_netloc
import sys

uses_netloc.append('mysql')

try:
    DATABASES = {}

    if 'DATABASE_URL' in os.environ:
        url = urlparse(os.environ['DATABASE_URL'])

        # Ensure default database exists.
        DATABASES['default'] = DATABASES.get('default', {})

        # Update with environment configuration.
        DATABASES['default'].update({
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        })
except Exception:
    print('Unexpected error:', sys.exc_info())

print(DATABASES)

db = mysql.connector.connect(DATABASES['default'])
cursor = db.cursor()


