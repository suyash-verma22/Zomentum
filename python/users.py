import sqlite3

db = 'zomentum.db'

con = sqlite3.connect(db)
c = con.cursor()

c.execute("""
CREATE TABLE users(
    id INTEGER PRIMARY KEY ,
    name VARCHAR(20) NOT NULL,
    phone VARCHAR(10)
)
""")

con.commit()
con.close()