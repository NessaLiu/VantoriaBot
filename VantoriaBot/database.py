import mysql.connector

config = {
    'host':'localhost',
    'user': 'root',
    'password': 'NessaSql',
    'database': 'VANTORIA'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()


