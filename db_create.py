import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
    c = connection.cursor()
    
    c.execute("""CREATE TABLE urls(url_id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL)""")
    
    c.execute(
       'INSERT INTO urls (url) VALUES("http://www.lds.org")' 
    )
    c.execute(
       'INSERT INTO urls (url) VALUES("http://www.mormon.org")' 
    )