#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import sys
import re
import urllib2
import time
from ConfigParser import ConfigParser
sys.path.append('.')
from getdiff import getdiffthread,getdiff
from watchcounts import watchcountsthread,watchcounts
class mytool(object):
	def __init__(self,url,selects,standards):
		self.url=url
		self.selects=selects
		self.standards=standards
		self.status=None
		self.finalresult={}
	def start(self):
		self.firstrun()
		if self.status:
			self.secondrun()
		else:
			print '\033[31m%s\033[0m'%('Get Entry Url Failed')
	def firstrun(self):
		try:
			f=urllib2.urlopen(self.url)
			self.content=f.read()
			pat=re.compile(r'<h2>贵金属行情</h2>.*?src="(.*?)"',re.S)
			result=pat.findall(self.content)
		except Exception,e:
			print str(e)
		finally:
			if len(result):
				self.status=True
				self.entryurl=result[0]
			f.close()
	def secondrun(self):
		if self.status:
			newf=None
			try:
				newurl='%s%s'%(self.url[:self.url[:self.url.rstrip('/').rindex('/')].rindex('/')],self.entryurl)
				mailinfo=self.getmailinfo()
				
				statuscounts=self.setcounts()
				while True:
					newf=urllib2.urlopen(newurl)
					newcontent=newf.read()
					for s in self.selects:
						newpatstr=r'[^=]%s.*?<td.*?<td.*?>(.*?)</td>.*?<td.*?>(.*?)</td>'%s
						newpat=re.compile(newpatstr,re.S)
						newresult=newpat.findall(newcontent)
						if not len(newresult):break
						if self.finalresult.get(s,{})=={}:
							self.finalresult[str(s)]={}
							buy=newresult[0][0].strip('\r\n ')
							sell=newresult[0][1].strip('\r\n ')
							self.finalresult[s]['buy']=buy
							self.finalresult[s]['sell']=sell
					t1=getdiff(self.finalresult,self.standards,statuscounts)
					t1.start()
					t2=watchcounts(statuscounts,mailinfo,self.standards,self.finalresult)
					t2.start()
					time.sleep(5)
			except Exception,e:
				print '\033[31m%s\033[0m'%str(e)
			finally:
				if newf!=None:			
					newf.close()
				self.display()

		else:
			print '\033[31m%s\033[0m'%('First get Entry Url plez')
	def setcounts(self):
		tmp={}
		for s in self.selects:
			tmp[s]=tmp.get(s,{})
			tmp[s]['buycount']=1
			tmp[s]['sellcount']=1
		return tmp
	def display(self):
		if self.status:
			for k,v in self.finalresult.items():
				print '\033[32m%s\tBuy:%s\tSell:%s\033[0m'%(k,v['buy'],v['sell'])
		else:
			print '\033[31m%s\033[0m'%('First get Entry Url plez')
	def getmailinfo(self):
		config=ConfigParser()
		config.read('config.txt')
		user=config.get('mail','user').strip()
	
		passwd=config.get('mail','password').strip()
		host=config.get('mail','host').strip()
		port=config.getint('mail','port') if config.has_option('mail','port') and config.get('mail','port')!='' else 25
		to=[f.strip() for f in config.get('mail','to').split(',')]
		
		return {'user':user,'password':passwd,'host':host,'tolist':to,'port':port}
'''		
if __name__=='__main__':
	url='http://www.icbc.com.cn/ICBC/%s/'%urllib2.quote('网上黄金')
	selects=['人民币账户黄金','人民币账户白银','人民币账户铂金','人民币账户钯金']
	warnings=[]
	t=mytool(url,selects,warning)
	t.start()
'''

