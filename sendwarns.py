#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import threading
import smtplib
from email.mime.text import MIMEText
class sendwarnsthread(threading.Thread):
	def __init__(self,timestr,mailinfo,prodname,status,standprice,nowprice):
		threading.Thread.__init__(self)
		self.timestr=timestr
		self.prodname=prodname
		self.status=status
		self.standprice=standprice
		self.nowprice=nowprice
		self.user=mailinfo['user']
		self.password=mailinfo['password']
		self.host=mailinfo['host']
		self.to=mailinfo['tolist']
		self.port=mailinfo['port']
	def run(self):
		try:
			if self.port==465:
				server=smtplib.SMTP_SSL(self.host,port=self.port)
			else:
				server=smtplib.SMTP(self.host,port=self.port)
			content='Date:%s\nProduct:%s\nCurrent %s price:%s\nStandard price:%s\n'%(self.timestr,self.prodname,self.status,self.nowprice,self.standprice)
			msg=MIMEText(content,_subtype='plain',_charset='utf-8')
			msg['Subject']='Letter From Product Warnings'
			msg['From']=self.user
			msg['To']=','.join(self.to)
			server.login(self.user,self.password)
			server.sendmail(self.user,self.to,msg.as_string())
			server.close()
			print '\033[33m%s\033[0m'%('Mail send succeed!')
		except Exception,e:
			print str(e)













