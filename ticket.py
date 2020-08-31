import sqlite3

db = 'zomentum.db'

con = sqlite3.connect(db)
c = con.cursor()

c.execute("""
CREATE TABLE ticket(
    id INTEGER PRIMARY KEY ,
    cid INTEGER NOT NULL,
   slot INETGER NOT NULL,
   CONSTRAINT ticket_of_user
   FOREIGN KEY (cid)
   REFERENCES users(id)
)
""")

con.commit()
con.close()