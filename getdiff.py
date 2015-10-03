#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import threading
import sys
sys.path.append('.')
class getdiffthread(threading.Thread):
	def __init__(self,results,standards,statuscounts):
		threading.Thread.__init__(self)
		self.results=results
		self.standards=standards
		self.statuscounts=statuscounts
	def run(self):
		for key,value in self.results.items():
			if value['buy']<=self.standards[key]['buy']:
				self.statuscounts[key]['buycount']+=1
				print '\033[32m <Warning:%s\tCurrent BoughtPrice:%s\tStandard BoughtPrice:%s>\n\033[0m'%(key,value['buy'],self.standards[key]['buy'])
			elif value['sell']>=self.standards[key]['sell']:
				self.statuscounts[key]['sellcount']+=1
				print '\033[32m <Warning:%s\tCurrent SellPrice:%s\tStandard SellPrice:%s>\n\033[0m'%(key,value['sell'],self.standards[key]['sell'])
class getdiff(object):
	def __init__(self,results,standards,statuscounts):
		self.results=results
		self.standards=standards
		self.statuscounts=statuscounts
	def start(self):
		for key,value in self.results.items():
			if value['buy']<=self.standards[key]['buy']:
				self.statuscounts[key]['buycount']+=1
				print '\033[32m <Warning Count:%d\tProduct:%s\tCurrent BoughtPrice:%s\tStandard BoughtPrice:%s>\033[0m'%(self.statuscounts[key]['buycount'],key,value['buy'],self.standards[key]['buy'])
			elif value['sell']>=self.standards[key]['sell']:
				self.statuscounts[key]['sellcount']+=1
				print '\033[32m <Warning Count:%d\tProduct:%s\tCurrent SellPrice:%s\tStandard SellPrice:%s>\033[0m'%(self.statuscounts[key]['sellcount'],key,value['sell'],self.standards[key]['sell'])
					
