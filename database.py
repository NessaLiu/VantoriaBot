import mysql.connector
import os
from urllib.parse import urlparse, uses_netloc
import sys

uses_netloc.append('mysql')
DATABASES = {}
url = urlparse(os.environ['DATABASE_URL'])

config = {
    'HOST': url.path[1:],
    'USER': url.username,
    'PASSWORD': url.password,
    'PORT': url.port,
}

db = mysql.connector.connect(**config)
cursor = db.cursor()
