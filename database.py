import mysql.connector
import os


url = os.environ['DATABASE_URL']

host = url.split('@')[1].split('/')[0] 
user = url.split('/')[2].split(':')[0] 
pwd = url.split(':')[2].split('@')[0] 
database = url.split('/')[-1].split('?')[0]

config = {
    'host': host,
    'user': user,
    'password': pwd,
    'database': database
}
print(config)

db = mysql.connector.connect(**config)
cursor = db.cursor()
