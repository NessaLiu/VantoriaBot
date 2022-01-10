import mysql.connector
import os


url = os.environ['DATABASE_URL']


config = {
    'host': url,
    'user': None,
    'password': None,
    'database': None
}

db = mysql.connector.connect(**config)
cursor = db.cursor()
