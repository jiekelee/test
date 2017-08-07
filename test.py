import sqlite3

conn = sqlite3.connect('mzi.db')
cur = conn.cursor()

sql = 'select * from detail'
cur.execute(sql)
aa = cur.fetchall()
# print '222'
print aa
for c in aa:
    print c

cur.close()
conn.close()
