import sqlite3
import os
import requests
from bs4 import BeautifulSoup

def getURL(page):
    """

    :param page: html of web page (here: Python home page) 
    :return: urls in that page 
    """
    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote

if(os.path.exists('data/data.db')):
    os.remove('data/data.db')

if(os.path.exists('data')):
    os.rmdir('data')

if not os.path.exists('data'):
    os.mkdir('data')

sqlconnection = sqlite3.connect('data/data.db')

sql = sqlconnection.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS urls (url text, ref text, round int);''')

sql.execute('''INSERT INTO urls VALUES ('http://www.google.com', null, 0);''')

sqlconnection.commit()

round = 0

while True:
    nextround_count = sql.execute('SELECT count(*) FROM urls WHERE round = ?', (round,))
    print('MOST is ready. Round ' + str(round) + '. I will scan ' + str(nextround_count.fetchone()[0]) + ' urls. Press y to confirm and go.')

    choice = input()
    if choice == 'y':
        query = sql.execute('SELECT * FROM urls WHERE round = ?', (round,))
        results = query.fetchall()
        print(len(results))
        for row in results:
            print(row)
            try:
                response = requests.get(row[0])
            except:
                print('Maybe not a valid url? check more!')
            page = str(BeautifulSoup(response.content, features="html.parser"))
            url = 'starting'
            while url:
                url, n = getURL(page)
                page = page[n:]
                if url:
                    if url.startswith('/'):
                        url = row[0] + url
                    print(url)
                    sql.execute('INSERT INTO urls VALUES (?, ?, ?)', (url, row[0], round + 1))

        sqlconnection.commit()
        round += 1
    
    else: 
        break
