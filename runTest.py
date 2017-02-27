# -*- coding: utf-8 -*-

import requests, re, sys, json, random, string,time
from results import *


def getPage():
	func_name = sys._getframe().f_code.co_name
	print func_name
	url = "http://rich.test/?test=minecraft"
	resp = requests.get(url)
	return resp

def postQuizLoadData ( quizId ):
	func_name = sys._getframe().f_code.co_name
	print func_name
	url = "http://rich.test/wp-admin/admin-ajax.php"
	action = "wp_pro_quiz_admin_ajax"
	func = "quizLoadData"
	resp = requests.post(url, { 'action' : action, 'func':func , 'data[quizId]' : quizId})
	return resp

def postLoadQuizData ( quizId ):
	func_name = sys._getframe().f_code.co_name
	print func_name
	url = "http://rich.test/wp-admin/admin-ajax.php"
	action = "wp_pro_quiz_admin_ajax"
	func = "loadQuizData"
	resp = requests.post(url, { 'action' : action, 'func':func , 'data[quizId]' : quizId})
	return resp


def postMinecraftResult():
	func_name = sys._getframe().f_code.co_name
	print func_name
	url = "http://rich.test/wp-admin/admin-ajax.php"
	data = getMinecraftResults()
	resp = requests.post(url, data)
	return resp

def postCounterStrikeResult():
	func_name = sys._getframe().f_code.co_name
	print func_name
	url = "http://rich.test/wp-admin/admin-ajax.php"
	data = getCounterStrikeResults()
	resp = requests.post(url, data)
	return resp

def postAddInToplist ( quizId, name, email, totalPoints,token ):
	func_name = sys._getframe().f_code.co_name
	print func_name
	url = "http://rich.test/wp-admin/admin-ajax.php"
	action = "wp_pro_quiz_admin_ajax"
	func = "addInToplist"

	captcha=''
	prefix=0
	points=2

	resp = requests.post(url, {'action': action
		,'func':func
		,'data[quizId]':quizId
		,'data[token]':token
		,'data[name]':name
		,'data[email]':email
		,'data[captcha]':captcha
		,'data[prefix]':prefix
		,'data[points]':points
		,'data[totalPoints]':totalPoints})
	return resp

def postShowFrontToplist ( quizId ):
	func_name = sys._getframe().f_code.co_name
	print func_name
	url = "http://rich.test/wp-admin/admin-ajax.php"
	action = "wp_pro_quiz_admin_ajax"
	func = "showFrontToplist"

	resp = requests.post(url, {'action': action
		,'func':func,'data[quizId]':quizId
		,'data[quizIds][]':quizId})
	return resp

def getToken(input):
	return json.loads(input._content)['toplist']['token']

def runMinecraftTest(i):
	func_name = sys._getframe().f_code.co_name
	print func_name

	print getPage()
	print postQuizLoadData(9)
	topList = postLoadQuizData(9)
	print topList
	print postMinecraftResult()
	print postAddInToplist(9,'MC_%d_%s' %(i,getRnd()),'mc_%d_%s@tst.ru' %(i,getRnd()),30,getToken(topList))._content
	print postShowFrontToplist(9)

def runCounterStrikeTest(i):
	func_name = sys._getframe().f_code.co_name
	print func_name
	
	print getPage()
	print postQuizLoadData(12)
	topList = postLoadQuizData(12)
	print topList
	print postCounterStrikeResult()
	print postAddInToplist(12,'CS_%d_%s' %(i,getRnd()),'cs_%d_%s@tst.ru' %(i,getRnd()),20,getToken(topList))._content
	print postShowFrontToplist(12)

def runRandomTest(i):
	if i % 2 == 1:
		runMinecraftTest(i)
	else:
		runCounterStrikeTest(i)

def getRnd():
	return genRandomString()

def genRandomString(size=5, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

if len(sys.argv)>1:
	if str(sys.argv[1]) == 'minecraft':
		runMinecraftTest()
		
	if str(sys.argv[1]) == 'cs':
		runCounterStrikeTest()