#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import sys
import re
import urllib2
class mytool(object):
	def __init__(self,url,selects):
		self.url=url
		self.selects=selects
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
			try:
				newurl='%s%s'%(self.url[:self.url[:self.url.rstrip('/').rindex('/')].rindex('/')],self.entryurl)
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
			except Exception,e:
				print str(e)
			finally:			
				newf.close()
				self.display()

		else:
			print '\033[31m%s\033[0m'%('First get Entry Url plez')
	def display(self):
		if self.status:
			for k,v in self.finalresult.items():
				print '\033[32m%s\tBuy:%s\tSell:%s\033[0m'%(k,v['buy'],v['sell'])
		else:
			print '\033[31m%s\033[0m'%('First get Entry Url plez')
if __name__=='__main__':
	url='http://www.icbc.com.cn/ICBC/%s/'%urllib2.quote('网上黄金')
	selects=['人民币账户黄金','人民币账户白银','人民币账户铂金','人民币账户钯金']
	t=mytool(url,selects)
	t.start()

