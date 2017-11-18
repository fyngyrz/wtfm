#
# Contains routines to make building and reading forms much simpler
# -----------------------------------------------------------------

import time
import re

months = ['Jan','Feb','Mar','Aprl','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
fmonths = ['January','February','March','April','May','June','July','August','September','October','November','December']

# d is date in form: "YYYYMMDD"
def hrdate(d):
	global fmonths
	year = d[:4]
	month = int(d[4:6])
	day = int(d[6:8])
	sfx = 'th'
	if day == 1: sfx = 'st'
	if day == 2: sfx = 'nd'
	if day == 3: sfx = 'rd'
	if day == 21: sfx = 'st'
	if day == 22: sfx = 'nd'
	if day == 23: sfx = 'rd'
	if day == 31: sfx = 'st'
	return fmonths[month-1]+' '+str(day)+sfx+', '+year

# date is in form: "YYYYMMDD"
def getweekday(date):
	if type(date) != str:
		return 1
	if len(date) != 8:
		return 1
	wd = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	try:
		yr = int(date[0:4])
		mo = int(date[4:6])
		da = int(date[6:8])
		tp = (yr,mo,da,12,0,0,0,0,0)
		foo = time.mktime(tp)
		swatch = time.localtime(foo)
		bar = wd[swatch[6]]
		return bar,(swatch[6]+2)%7
	except:
		print 'date is a '+str(type(date))+'. date="'+str(date)+'" of length '+str(len(date))

# sy,ey in form 'YYYY'
# sm,em in form 'MM'
# sd,ed in form 'DD'
# --------------------
def makedatesorderly(sy,sm,sd,ey,em,ed):
	if ey < sy:	# oh, backwards years, eh? Not happening...
		t = sy
		sy = ey
		ey = t

	if sy == ey:
		if em < sm:	# backwards months in same year?  Oy vey, you got de bad genes
			t  = sm
			sm = em
			em = t
		if sm == em:
			if ed < sd:	# backwards days in same year, same month? Nope...
				t  = sd
				sd = ed
				ed = t
	return sy,sm,sd,ey,em,ed

# ll = [[sValue,textDesc],[sValue,textDesc]]
def buildDds(name,ll,selected=None):
	t = '<SELECT NAME="'+name+'">\n'
	for el in ll:
		kick = ''
		if selected != None and selected != '':
			if str(el[0]) == str(selected):
				kick = ' SELECTED'
		t += '<OPTION VALUE="'+str(el[0])+'"'+kick+'>'+str(el[1])+'\n'
	t += '</SELECT>\n'
	return t

# use builddropdown(), not this:
# ------------------------------
def lowbuilddropdown(name,ps,ad,sy):
	ad = ad[0:4]
	if ps == None or ps == '':
		ps = str(ad)
	t = '<SELECT NAME="'+name+'">'
	for i in range(int(sy),int(ad)+1):
		kick = ''
		if str(i) == ps:
			kick = ' SELECTED'
		t += '<Option VALUE="'+str(i)+'"'+kick+'>'+str(i)
	t += '</select>\n'
	return t

# Builds a drop-down list of years from sy to this 'ad'
# and if ps == one of those years, will PreSelect that year
# input element is named 'name'
# ------------------------------------------------------------
def builddropdown(name,ps,ad=None,sy=None):
	if ad == None:
		ad = str(time.localtime()[0])
	ad = ad[:4]
	if sy == None:
		sy = '1900'
	if sy > ad:
		ad = sy
	# label, preselect, last selectable year, start year
	return lowbuilddropdown(name,ps,ad,sy)

def builddaydropdown(name,ps):
	if ps == None:
		ps = str(time.localtime()[2])
	t = '<SELECT NAME="'+name+'">'
	for i in range(1,32):
		kick = ''
		if int(i) == int(ps):
			kick = ' SELECTED'
		rv = str(i)
		if i < 10:
			rv = '0'+rv
		t += '<Option VALUE="'+rv+'"'+kick+'>'+str(i)
	t += '</select>\n'
	return t

def buildmondropdown(name,ps):
	if ps == None:
		ps = str(time.localtime()[1])
	tt = ['January','February','March','April','May','June','July','August','September','October','November','December']
	t = '<SELECT NAME="'+name+'">'
	for i in range(1,13):
		kick = ''
		if int(i) == int(ps):
			kick = ' SELECTED'
		rv = str(i)
		if i < 10:
			rv = '0'+rv
		t += '<Option VALUE="'+rv+'"'+kick+'>'+tt[i-1]
	t += '</select>\n'
	return t

# The four 'make' methods following default to producing table rows
# with two cells: A right-justified cell with the lable content,
# and a right justified cell with the unput element(s), and if
# you use this default, you'll only have to provide a table wrapper.
#
# However, you can supply format strings that allow you to embed
# the label and element any way you like. Since the lable and elements
# are returned as one string, if you would prefer to parse them
# yourself, just call this way...
#
#     (...,lfmt='%s'+sepString,efmt='%s')
#
# ...then in your code, you can break them apart for later mucking about
# this way:
#
#     label,element = result.split(sepString)
#
# Of course sepString has to NOT appear in the results anywhere.
# I suggest something like: sepString = '@#$K-J;U+H=5@#$'
# it's not pretty, but it sure isn't likely to break, lol.
# Make up your own, of course.
# --------------------------------------------------------------------------

# Year, month, date selector
#
# retrieve with getadatefield()
# -----------------------------
# label describes the widget's purpose
#
# yl is ( year) NAME="yl"
# ml is (month) NAME="ml"
# dl is (  day) NAME="dl"
#
# yv is the year preset
# mv is the month preset
# dv is the day preset
#
# ad is
#
# lfmt and efmt control how the widget is presented.
# --------------------------------------------------
def makedrow(label,yl,ml,dl,yv,mv,dv,ad,lfmt='',efmt=''):
#	ad = ad[0:4]
	if lfmt == '':
		lfmt = '<tr><td align="right">%s</td>'
	o = lfmt % (label)
	# label
	# preselect
	# last selectable year (this year if unset)
	# start year (1900 if unset)
	s = ''
	s += buildmondropdown(ml,mv)
	s += builddaydropdown(dl,dv)
	s += builddropdown(yl,yv,ad)
	if efmt == '':
		efmt = '<td>%s</td></tr>'
	o += efmt % (s)
	return o

# year, month selector (good for credit card expiry)
#
# retrieve with getadate6field()
# --------------------------------------------------
def make6drow(label,yl,ml,yv,mv,ad,lfmt='',efmt=''):
	ad = ad[0:4]
	if lfmt == '':
		lfmt = '<tr><td align="right">%s</td>'
	o = lfmt % (label)
	s  = builddropdown(yl,yv,ad)
	s += buildmondropdown(ml,mv)
	if efmt == '':
		efmt = '<td>%s</td></tr>'
	o += efmt % (s)
	return o

# Bulleted selector:
# ------------------
# makeselector(label,list-of-2-tuples,cgi-name,default-selected,left-format,right-format)

def makeselector(label,ll,cginame,defs=None,lfmt=None,rfmt=None):
	if lfmt == None: lfmt = '<tr><td align="right">%s</td>'
	if rfmt == None: rfmt = '<td>%s</td></tr>'
	boil = '<INPUT TYPE="radio" NAME="[CGINAME]" VALUE="[DATA]"[SELECTOR]>[LABEL]<br>'
	thing = ''
	for el in ll:
		item = boil
		item = item.replace('[CGINAME]',cginame)
		item = item.replace('[DATA]',   el[0])
		item = item.replace('[LABEL]',  el[1])
		selector = ''
		if defs != None:
			if el[0] == defs:
				selector = ' CHECKED'
		item = item.replace('[SELECTOR]',selector)
		thing += item
	line  = lfmt % (label,)
	line += rfmt % (thing,)
	return line

# value selector as row
#
# retrieve with any of
# getannfield(),getnfield(),getsafefield(),getfield()
# ---------------------------------------------------
def makevrow(label,tag,variable,length,lfmt='',efmt='',olimit=64,tt=1):
	l = str(length)
	tts = ''
	tte = ''
	if tt == 1:
		tts = '<font face="courier">'
		tte = '</font>'
	fl = int(l)
	if fl > olimit:
		fl = olimit
		l = str(olimit)
	fl = str(fl)
	key = '['+tag.upper()+']'
	if lfmt == '':
		lfmt = '<tr><td align="right">'+tts+'%s'+tte+'</td>'
	o = lfmt % (label)
	if 0:
		sty = 'style="font-size: 16px; font-family:Courier;" '
	else:
		sty = ''
	s = '<INPUT '+sty+'TYPE="TEXT" SIZE='+fl+' MAXLENGTH='+l+' NAME="'+tag+'" VALUE="'+key+'">'
	s = s.replace(key,str(variable))
	if efmt == '':
		efmt = '<td>'+tts+'%s'+tte+'</td></tr>'
	o += efmt % (s)
	return o

# value selector as cell
#
# retrieve with any of
# getannfield(),getnfield(),getsafefield(),getfield()
# ---------------------------------------------------
def makevcell(label,tag,variable,length,lfmt='',efmt='',olimit=64,tt=1):
	l = str(length)
	tts = ''
	tte = ''
	if tt == 1:
		tts = '<font face="courier">'
		tte = '</font>'
	fl = int(l)
	if fl > olimit:
		fl = olimit
		l = str(olimit)
	fl = str(fl)
	key = '['+tag.upper()+']'
	if lfmt == '':
		lfmt = '<td align="right">'+tts+'%s'+tte+'</td>'
	o = lfmt % (label)
	if 0:
		sty = 'style="font-size: 16px; font-family:Courier;" '
	else:
		sty = ''
	s = '<INPUT '+sty+'TYPE="TEXT" SIZE='+fl+' MAXLENGTH='+l+' NAME="'+tag+'" VALUE="'+key+'">'
	s = s.replace(key,str(variable))
	if efmt == '':
		efmt = '<td>'+tts+'%s'+tte+'</td>'
	o += efmt % (s)
	return o

def maketextarea(label,tag,variable,lfmt='',efmt='',rows=8,cols=40,tt=1,pid='',mno=0):
	tts = ''
	tte = ''
	if tt == 1:
		tts = '<font face="courier">'
		tte = '</font>'
	if mno != 0:
		sty = 'style="font-size: 16px; font-family:Courier new,Monospace;" '
	else:
		sty = ''
	key = '['+tag.upper()+']'
	if lfmt == '':
		lfmt = '<tr><td align="right">'+tts+'%s'+tte+'</td>'
	o = lfmt % (label)
	s = '<TEXTAREA '+pid+sty+'NAME="'+tag+'" ROWS='+str(rows)+' COLS='+str(cols)+'>'
	s+= key
	s+= '</TEXTAREA>'
	s = s.replace(key,str(variable))
	if efmt == '':
		efmt = '<td>'+tts+'%s'+tte+'</td></tr>'
	o += efmt % (s)
	return o

# Checked option selector
#
# retrieve with getacheckfield()
# ------------------------------
def makecheckrow(label,tag,variable,lfmt='',efmt=''):
	key = '['+tag.upper()+']'
	if lfmt == '':
		lfmt = '<tr><td align="right">%s</td>'
	o = lfmt % (label)
	s = '<input type="checkbox" name="'+tag+'" value="ON"'+key+'>'
	if variable == 'ON':
		s = s.replace(key,' CHECKED')
	else:
		s = s.replace(key,'')
	if efmt == '':
		efmt = '<td>%s</td></tr>'
	o += efmt % (s)
	return o

# Checked option selector in cell
#
# retrieve with getacheckfield()
# ------------------------------
def makecheckcells(label,tag,variable,lfmt='',efmt=''):
	key = '['+tag.upper()+']'
	if lfmt == '':
		lfmt = '<td align="right">%s</td>'
	o = lfmt % (label)
	s = '<input type="checkbox" name="'+tag+'" value="ON"'+key+'>'
	if variable == 'ON':
		s = s.replace(key,' CHECKED')
	else:
		s = s.replace(key,'')
	if efmt == '':
		efmt = '<td>%s</td>'
	o += efmt % (s)
	return o

def makecrow(label,tag,variable,lfmt='',efmt=''):
	return makecheckrow(label,tag,variable,lfmt,efmt)

# These are retrieval functions from the above type input widgets
# ---------------------------------------------------------------

def getfield(form,fieldname,default):
	try:
		result = str(form[fieldname].value)
	except:
		result = default
	return result

def safer(result):
	if type(result) == str:
		result = result.replace("'","&#39;")
		result = result.replace("\\","&#92;")
		result = result.replace('"',"&quot;")
	if result.lower().find('<script') != -1:
		p = re.compile(r'<script.*?>')	# kill <script> tags outright
		result = p.sub('', result)
		p = re.compile(r'</script.*?>')	# kill </script> tags outright
		result = p.sub('', result)
	return result

def getsafefield(form,fieldname,default):
	result = safer(getfield(form,fieldname,default))
	if type(result) == None:
		result = ''
	return result

def getnfield(form,fieldname,default):
	x = getsafefield(form,fieldname,default)
	if x == '': return default
	try:
		x = int(x)
	except:
		return default
	return x

def getannfield(form,label,default,minimum,maximum):
	v = getnfield(form,label,default)
	if minimum != None:
		if v < minimum: v = minimum
	if maximum != None:
		if v > maximum: v = maximum
	return v

def getacheckfield(form,label,default):
	v = getsafefield(form,label,default)
	if v != 'ON':
		v = default
	return v

def getachecknfield(form,label,default): # default is 0 or 1
	default = str(default)
	if default == '0':	default = ''
	else:				default = 'ON'
	v = getsafefield(form,label,default)
	if v == 'ON':
		v = '1'
	else:
		v = '0'
	return v

def getadatefield(form,xly,xlm,xld,dy,dm,dd):
	try:
		xsy = str(getsafefield(form,xly,'')).strip()
		xsm = str(getsafefield(form,xlm,'')).strip()
		xsd = str(getsafefield(form,xld,'')).strip()
	except:
		xsy = dy
		xsm = dm
		xsd = dd
	if len(xsy) == 0: xsy = dy
	if len(xsm) == 0: xsm = dm
	if len(xsd) == 0: xsd = dd
	return xsy,xsm,xsd

def getnormdate(form,xly,xlm,xld):
	dy = str(time.localtime()[0])
	dm = str(time.localtime()[1])
	dd = str(time.localtime()[2])
	ray = getadatefield(form,xly,xlm,xld,dy,dm,dd)
	return ray[0]+ray[1]+ray[2]

def getadate6field(form,xly,xlm,dy,dm):
	try:
		xsy = str(getsafefield(form,xly,'')).strip()
		xsm = str(getsafefield(form,xlm,'')).strip()
	except:
		xsy = dy
		xsm = dm
	if len(xsy) == 0: xsy = dy
	if len(xsm) == 0: xsm = dm
	return xsy,xsm

