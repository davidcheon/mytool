#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import threading
import sys
import time
sys.path.append('.')
from sendwarns import sendwarnsthread
class watchcountsthread(threading.Thread):
	def __init__(self,statuscounts,mailinfo,standards,result):
		threading.Thread.__init__(self)
		self.statuscounts=statuscounts
		self.mailinfo=mailinfo
		self.standards=standards
		self.result=result
	def run(self):
		for key,value in self.statuscounts.items():
			if value['buycount']%20==0:
				t=sendwarnsthread(time.strftime('%Y-%m-%d %H:%M:%S'),self.mailinfo,key,'buy',self.standards[key]['buy'],self.result[key]['buy'])
				t.start()
			elif value['sellcount']%20==0:
				t=sendwarnsthread(time.strftime('%Y-%m-%d %H:%M:%S'),self.mailinfo,key,'sell',self.standards[key]['sell'],self.result[key]['sell'])
				t.start()
class watchcounts(object):
	def __init__(self,statuscounts,mailinfo,standards,result):
		self.statuscounts=statuscounts
		self.mailinfo=mailinfo
		self.standards=standards
		self.result=result
	def start(self):
		for key,value in self.statuscounts.items():
			if value['buycount']%20==0:
				t=sendwarnsthread(time.strftime('%Y-%m-%d %H:%M:%S'),self.mailinfo,key,'buy',self.standards[key]['buy'],self.result[key]['buy'])
				t.start()
			elif value['sellcount']%20==0:
				t=sendwarnsthread(time.strftime('%Y-%m-%d %H:%M:%S'),self.mailinfo,key,'sell',self.standards[key]['sell'],self.result[key]['sell'])
				t.start()
