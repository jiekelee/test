import sqlite3

aa = 'http://wwww.baidu.com/abc/123/009'
bb = '99999'

# sp = aa.split('/')
# print sp[-2]

conn = sqlite3.connect('mzi.db')
cur = conn.cursor()

droptable = 'drop table allurl'
sql = 'create table allurl(hurl text primary key not null,hpath text not null)'
cur.execute(droptable)
cur.execute(sql)

# sql = 'insert into allurl values("%s","%s")'%(aa,bb)
# print sql


conn.commit()

# sql = 'select * from allurl'
# cur.execute(sql)
# print cur.fetchall()

cur.close()
conn.close()