import sqlite3
import os

if not os.path.exists('data'):
    os.mkdir('data')

sqlconnection = sqlite3.connect('data/data.db')

sql = sqlconnection.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS urls 
                (url text, lap int);''')

sql.execute('''INSERT INTO urls VALUES ('www.google.com', 0);''')

sqlconnection.commit()