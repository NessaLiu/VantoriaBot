import mysql.connector
import os


#url = os.environ['DATABASE_URL']

url = 'mysql://b933b28d9b839c:3cf3178c@us-cdbr-east-05.cleardb.net/heroku_f9c09781f41ef7b?reconnect=true'

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
