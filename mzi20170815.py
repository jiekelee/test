import requests
from bs4 import BeautifulSoup
import os
import sqlite3

class mzi:
	def __init__(self):
		self.headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}

	def getconn(self):
		self.conn = sqlite3.connect('mzi.db')
		self.cur = self.conn.cursor()

	def closeconn(self):
		self.cur.close()
		self.conn.close()



	def createtable(self):
		self.getconn()
		allurlexists = 'drop table if exists allurl'
		detailexists = 'drop table if exists detail'
		create_allurl = 'create table allurl(hurl text primary key not null,hpath text not null)'
		create_detail = 'create table detail(hurl text not null,hpath text not null,durl text not null,isdown bool default 0)'

		self.cur.execute(allurlexists)
		self.cur.execute(detailexists)
		self.cur.execute(create_allurl)
		self.cur.execute(create_detail)
		
		self.conn.commit()
		self.closeconn()

	def getallurl(self):
		
		all_url = 'http://www.mzitu.com/all'
		start_html = requests.get(all_url,headers=self.headers)

		Soup = BeautifulSoup(start_html.text,'html.parser')

		all_a = Soup.find('div',class_='all').find_all('a')

		self.getconn()
		for a in all_a:
			head_url = a['href']
			aa = head_url.split('/')
			h_path = aa[-1]


			sql = 'insert into allurl values ("%s","%s")'%(head_url,h_path)
			self.cur.execute(sql)
		self.conn.commit()
		self.closeconn()
			# print head_url
			# print h_path[-1]

	# def create_table_detail(self):
	# 	self.getconn()
	# 	drop_t = 'drop table if exists detail'
	# 	sql = 'create table detail(hurl text not null,hpath text not null,durl text not null,isdown bool default 0)'
	# 	self.cur.execute(drop_t)
	# 	self.cur.execute(sql)
	# 	self.conn.commit()
	# 	self.closeconn()

	def getpicurl(self):
		self.getconn()
		sql = 'select hurl,hpath from allurl'
		self.cur.execute(sql)
		hurl_list = self.cur.fetchall()
		num = 0
		for hurl in hurl_list:
			href = hurl[0]
			hpath = hurl[1]
			html = requests.get(href,headers=self.headers)
			html_Soup = BeautifulSoup(html.text,'html.parser')
			max_page = html_Soup.find('div',class_='pagenavi').find_all('span')[-2].get_text()
			# print href,hpath, max_page
			num +=1
			if num == 4:
				break

			for page in range(1,int(max_page)+1):
				page_url = href + '/' + str(page)
				# print href,hpath,max_page,page_url
				try:
					sql = 'insert into detail(hurl,hpath,durl,isdown)values("%s","%s","%s",0)'%(href,hpath,page_url)
					# print sql
					self.cur.execute(sql)
					# print href,hpath,page_url,'insert success'
				except:
					print 'insert fail'

			self.conn.commit()
		self.closeconn()

	def print_allurl(self):
		self.getconn()
		sql = 'select * from allurl'
		self.cur.execute(sql)
		print self.cur.fetchall()
		self.closeconn()

	def print_detail(self):
		self.getconn()
		sql = 'select * from detail'		
		self.cur.execute(sql)
		print self.cur.fetchall()
		
		self.closeconn()

	def deletedata(self):
		self.getconn()
		dele_allurl = 'delete from  allurl'
		dele_detail = 'delete from detail'
		self.cur.execute(dele_allurl)
		self.cur.execute(dele_detail)
		self.conn.commit()
		self.closeconn()



mm = mzi()
# mm.getallurl()
mm.createtable()
mm.getallurl()
mm.getpicurl()
# mm.create_table_detail()
# mm.getpicurl()
# mm.print_allurl()
mm.print_detail()