# -*- coding: utf-8 -*-

import requests , re , sys , json , random , string , time
from results import *

site = "http://rich.test/"
url = "%swp-admin/admin-ajax.php" % site
action = "wp_pro_quiz_admin_ajax"
authCookie = {}

def printFuncName ( frame ):
	print frame.f_code.co_name

def getPage ( cookie = {} ):
	printFuncName ( sys._getframe() )

	resp = requests.get("%s?test = minecraft" % site, cookies = cookie)
	return resp

def login ( username , password ):
	printFuncName ( sys._getframe() )

	resp = requests.post ( "%swp-login.php" % site
		, { "log": username
		, "pwd": password
		, "wp-submit": "Войти"
		, "redirect_to": "http://rich.test/wp-admin/"
		, "testcookie": 1 }
		, allow_redirects = False)
	return resp

def getCookie ( resp ):
	printFuncName ( sys._getframe() )

	token = resp.cookies.get("wordpress_677030e17c6dca5bcd9a6fe68cc8a1b9"
	, path='/wp-admin')
	cookies = dict(wordpress_677030e17c6dca5bcd9a6fe68cc8a1b9=token,
	wordpress_test_cookie="WP+Cookie+check")
	global authCookie
	authCookie = cookies
	return cookies

def getAuthPage ( username , password ):
	printFuncName ( sys._getframe() )

	result = getPage ( getCookie ( login ( username , password ) ) )
	result.isAuth = isAuth ( result._content )
	return result

def isAuth ( content ):
	printFuncName ( sys._getframe() )

	return True if "Выход" in content else False

#print getAuthPage ( "test0" , "test" ).isAuth

#for p in r.cookies: print p.path


def postQuizLoadData ( quizId ):
	printFuncName ( sys._getframe() )
	
	func = "quizLoadData"
	resp = requests.post ( url , { 'action' : action
		, 'func' : func 
		, 'data[quizId]' : quizId}, cookies = authCookie )
	return resp

def postLoadQuizData ( quizId ):
	printFuncName ( sys._getframe() )

	func = "loadQuizData"
	resp = requests.post ( url , { 'action' : action
		, 'func' : func 
		, 'data[quizId]' : quizId}, cookies = authCookie )
	return resp

def postMinecraftResult (  ):
	printFuncName ( sys._getframe() )

	data = getMinecraftResults()
	resp = requests.post ( url , data, cookies = authCookie )
	return resp

def postCounterStrikeResult (  ):
	printFuncName ( sys._getframe() )

	data = getCounterStrikeResults()
	resp = requests.post ( url , data, cookies = authCookie )
	return resp

def postAddInToplist ( quizId , name , email , totalPoints , token ):
	printFuncName ( sys._getframe() )

	func = "addInToplist"
	captcha = ''
	prefix = 0
	points = totalPoints

	resp = requests.post ( url , {'action': action
		,'func' : func
		,'data[quizId]' : quizId
		,'data[token]' : token
		,'data[name]' : name
		,'data[email]' : email
		,'data[captcha]' : captcha
		,'data[prefix]' : prefix
		,'data[points]' : points
		,'data[totalPoints]' : totalPoints}, cookies = authCookie )
	return resp

def postShowFrontToplist ( quizId ):
	printFuncName ( sys._getframe() )

	func = "showFrontToplist"
	resp = requests.post ( url , { 'action' : action
		,'func' : func , 'data[quizId]' : quizId
		,'data[quizIds][]' : quizId}, cookies = authCookie )
	return resp

def getToken ( input ):
	return json.loads ( input._content )[ 'toplist' ][ 'token' ]

def runMinecraftTest ( i ):
	printFuncName ( sys._getframe() )

	print getPage()
	print 'auth is %s' % getAuthPage ( getRandomLogin () , 'test' ).isAuth
	print postQuizLoadData ( 9 )
	topList = postLoadQuizData ( 9 )
	print topList
	print postMinecraftResult()
	print postAddInToplist ( 9 , 'MC_%d_%s' %( i , getRnd())
		, 'mc_%d_%s@tst.ru' %( i , getRnd())
		, 30
		, getToken ( topList ))._content
	print postShowFrontToplist ( 9 )

def runCounterStrikeTest ( i ):
	printFuncName ( sys._getframe() )
	
	print getPage()
	print 'auth is %s' % getAuthPage ( getRandomLogin () , 'test' ).isAuth
	print postQuizLoadData ( 12 )
	topList = postLoadQuizData ( 12 )
	print topList
	print postCounterStrikeResult()
	print postAddInToplist ( 12 , 'CS_%d_%s' % ( i ,getRnd() )
		, 'cs_%d_%s@tst.ru' % ( i , getRnd() )
		, 20
		, getToken ( topList ))._content
	print postShowFrontToplist ( 12 )

def runTest ( i ):
	if i % 2 == 1:
		runMinecraftTest ( i )
	else:
		runCounterStrikeTest ( i )

def getRnd():
	return genRandomString()

def genRandomString ( size = 5 , chars = string.ascii_uppercase + string.digits ):
	return ''.join ( random.choice ( chars ) for _ in range ( size ))

def getRandomLogin():
	return 'test%d' % random.randint ( 0 , 9 )
#print login('test0','test').__dict__

if len ( sys.argv )>1:
	if str ( sys.argv[ 1 ]) == 'minecraft':
		runMinecraftTest()
		
	if str ( sys.argv[ 1 ]) == 'cs':
		runCounterStrikeTest()