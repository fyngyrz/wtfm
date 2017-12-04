#!/usr/bin/python

var = 'hello'

#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import cgi
import sys
import json
from aa_macro import *

def output(content):
	sys.stdout.write('Content-Type: text/plain\n\n')
	sys.stdout.write(content)
 
form = cgi.FieldStorage()
 
fail=0
try:
	myData = str(form['myData'].value) # expecting JSON encoded string
except:
	myData = json.dumps('no data?')
	fail=1
else:
	if myData == "":
		myData = json.dumps('empty data?')
		fail=1

try:
	pyObject = str(json.loads(myData)) # now you can use the data in Python
except:
	myData = 'Decode Fail'
	fail = 1

if fail == 1:
	output(json.dumps(myData))
	raise SystemExit
else:
	try:
		mod = macro(noshell=True,noembrace=True,noinclude=True,locklipath='/safebox/',lockwepath='/hpics/',xlimit=35,dlimit=4)
		if 1:
			oData = mod.do(pyObject)
		else:
			oData = mod.do('[i test]')
	except:
		oData = 'Cannot process'

output(json.dumps(oData)) # sends the Python variable content to javascript as JSON

raise SystemExit
