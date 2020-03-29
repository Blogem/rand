
import sqlite3

db_name = 'covid_data.db'

conn = sqlite3.connect(db_name)
c = conn.cursor()

t = ('2020-03-27',)
c.execute('SELECT count(*) FROM covid WHERE report_date = ?',t)
l = c.fetchall()

print(l)

# c.execute('PRAGMA table_info("covid")')
# print(c.fetchall())