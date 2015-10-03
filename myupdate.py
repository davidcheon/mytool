#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import sys
import urllib2
import getopt
import re
import signal
sys.path.append('.')
from mytool import mytool
class myexception(Exception):pass
def showversion():
	print 'Version:1.0'
def showhelp():
	print '''
	-s or --selects To set selects (dot seperator to set more selects),e.g. '人民币账户黄金','人民币账户白银','人民币账户铂金','人民币账户钯金'
	-w or --warnings To set selects's warnings value(double length as  selects),e.g. buy,sell,buy,sell
	-v or --version To show version
	-h or --help To show more help
	'''
def checkselects(selects):
	orig=['人民币账户黄金','人民币账户白银','人民币账户铂金','人民币账户钯金']
	for s in selects:
		if s not in orig:
			return False
	return True
def checkwarnings(warnings):
	for w in warnings:
		if w<=0:
			return False
	return True
#def checkmail(mail):
#	mailpat=re.compile(r'\w+@\w+(\.\w+){1,}')
#	return False if len(mailpat.findall(mail))==0 else True
def handler(signum,frame):
	print '\033[31mReceived a signal %s.\033[0m'%(signum)
	sys.exit()
if __name__=='__main__':
	signal.signal(signal.SIGINT,handler)
	signal.signal(signal.SIGTERM,handler)
	url='http://www.icbc.com.cn/ICBC/%s/'%urllib2.quote('网上黄金')
	selects=[]
	warnings=[]
	mail=None
	try:
		opt,val=getopt.getopt(sys.argv[1:],'vh:s:w:',['version','help','warnings=','selects='])
		for o in opt:
			if o[0] in ['-w','--warnings']:
				warnings=map(lambda a:float(a),o[1].split(','))
			elif o[0] in ['-s','--selects']:
				selects=map(lambda a:a.strip(),o[1].split(','))
			elif o[0] in ['-v','--version']:
				showversion()
			elif o[0] in ['-h','--help']:
				showhelp()
		if len(selects)*2!=len(warnings):
			raise myexception('\033[31m Must be have right args counts\033[0m')
		if not (checkselects(selects) and checkwarnings(warnings)):
			raise myexception('\033[31m Must enter the right selects or warnings\033[0m')
		
	except getopt.GetoptError,e:
		print str(e)
	except myexception,e:
		print str(e)
	else:
		tmp={}
		for s in selects:
			tmp[s]=tmp.get(s,{})
			tmp[s]['buy']=warnings[selects.index(s)*2]
			tmp[s]['sell']=warnings[selects.index(s)*2+1]
		t=mytool(url,selects,tmp)
		t.start()
		

