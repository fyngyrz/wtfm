#!/usr/bin/python
# -*- coding: utf-8 -*-

# To-Do:
# --------------------------------------------------------------------------
# add stage_fn() and isplit() to aa_macro
# --------------------------------------------------------------------------

debug = ''
do_debug = False

doc ="""Documentation Generation System
      Author: fyngyrz  (Ben)
     Contact: fyngyrz@gmail.com (bugs, feature requests, kudos, bitter rejections)
     Project: doc_system.py
    Homepage: https://github.com/fyngyrz/wtfm
     License: None. It's free. *Really* free. Defy invalid social and legal norms.
 Disclaimers: 1) Probably completely broken. Do Not Use. You were explicitly warned. Phbbbbt.
              2) My code is blackbox, meaning I wrote it without reference to other people's code
              3) I can't check other people's contributions effectively, so if you use any version
                 of doc_system.py that incorporates accepted commits from others, you are risking
                 the use of OPC, which may or may not be protected by copyright, patent, and the
                 like, because our intellectual property system is pathological. The risks and
                 responsibilities and any subsequent consequences are entirely yours. Have you
                 written your congresscritter about patent and copyright reform yet?
  Incep Date: June 17th, 2015
     LastRev: December 4th, 2017
  LastDocRev: December 24th, 2015
 Tab spacing: 4 (set your editor to this for sane formatting while reading)
     Dev Env: Ubuntu 12.04.5 LTS, Python 2.7.3
      Status: BETA
    Policies: 1) I will make every effort to never remove functionality or
                 alter existing functionality once past BETA stage. Anything
                 new will be implemented as something new, thus preserving all
                 behavior and the API. The only intentional exceptions to this
                 are if a bug is found that does not match the intended behavior,
                 or I determine there is some kind of security risk. What I
                 *will* do is not document older and less capable versions of a
                 function, unless the new functionality is incapable of doing
                 something the older version(s) could do. So your use of older
                 API will always work (instead of being "deprecated" and then
                 yanked right out from under you), while the documentation
                 encourages new and (hopefully) better stuff. But remember,
                 this only applies to production code. Until the BETA status
                 is removed, ANYTHING may change. Having said that, if something
                 changes that seriously inconverniences you, let me know, and
                 I will try to do something about it if it is reasonably possible.
     1st-Rel: 0.0.1
     Version: 0.0.3 Beta
     History: See changes.md
"""

import cgi
import random

from aa_webpage		import *
from aa_formboiler	import *
from aa_sqlite		import *
from aa_tablelib	import *
from aa_macro		import *
from aa_datafile	import *

# global configuration
# --------------------
cfg = readDataFile('perdunkdoc_system.cfg')
xprefix	=	cfg['xprefix']
xsystem	=	cfg['xsystem']
dprefix	=	cfg['dprefix']
dname	=	cfg['dname']

# special chars
# -------------
qtard = 'j8g67f54dlll9f8f7f'
stard = 'jfjfjn76876juj54g4g'

warning = ''
cmd = ''
searchterm = ''
casesensitive = False

# various forms of web- and db-safety things
# ==========================================

# Prepares data, typically already text, for placement into CGI INPUT elements
# ----------------------------------------------------------------------------
def dequote(s):
	s = str(s)
	s = s.replace('&','&amp;')	# So we don't eat character entities on the web
	s = s.replace('"','&quot;')	# So we don't put quotes inside of quote-delimited CGI elements
	s = s.replace('<','&lt;')	# deactivate all of ...
	s = s.replace('>','&gt;')	# ...the tag delimiters
	return s

# Prepares data, typically already text, for insertion into SQLite statements
# ---------------------------------------------------------------------------
def clean(s):
	s = str(s)
	s = s.replace("'",qtard)	# no single quotes; save a placeholder instead
	s = s.replace("\\",stard)	# no backslashes; save a placeholder instead
	s = s.replace('\r','')		# no C/Rs, this is linux. EOL is 0x0a.
	return s

# When text data comes out of SQLite, replace the placeholders
# ------------------------------------------------------------
def unclean(s):
	s = str(s)
	s = s.replace(qtard,"'")	# put the single quotes back
	s = s.replace(stard,"\\")	# put the backslashes back
	return s

# philter() prevents characters above 127 from breaking
# the ASCII string CODEC, a common failing of
# Python. It also replaces those instances with an
# HTML-entity encoded version of themselves so that
# They will display as something visible on the web,
# and be easily visible within the context of CGI
# data entry/editing FORM elements. All CGI input comes
# here before going anywhere else; ergo, no way to
# feed illegal characters to the Python v2 CGI from
# the web. :P
# -----------------------------------------------------
def philter(rawstring):
	cleanstring = ''
	for rawc in rawstring:
		if ord(rawc) < 128:
			cleanstring += rawc
		else:
			cleanstring += '&#%d;' % (ord(rawc))
	return cleanstring

# set up meta tags and body colors
# --------------------------------
metags = '<meta name="robots" content="noindex,nofollow">\n'
colors = 'style="color: #000000; background-color: #FFFFFF;"'

# If DB does not exist, create it
# -------------------------------
dbname = "%s%s" % (dprefix,dname)

# This is used, occasionaly, when I need to add new columns
# It's a development thing, not part of normal operation
# ---------------------------------------------------------
if 0:
#	sql = "ALTER TABLE pages ADD COLUMN pageloc TEXT"
#	a = dbl(dbname,sql)
#	debug += str(a)
	pass

# The intent is to supply a starter database, with a starter
# project in it. But in case something untoward happens with
# SQLite3's compatability, or the database is lost, or you
# just want to start fresh, this will build a new, empty
# database when it finds that there isn't one available.
# ----------------------------------------------------------
try:
	fh = open(dbname)
except:
	psql = 'styles TEXT'		# one row, one column: global styles
	a = dbl(dbname,'CREATE TABLE globals(%s)') % (psql)

	psql  = 'previewpath TEXT,'	# path to actual HTML files are from web perspective
	psql += 'extension TEXT,'	# the default file extension for projects. Typically '.html'
	psql += 'name TEXT,'		# the name of the project
	psql += 'styles TEXT,'		# the styles specific to the project
	psql += 'target TEXT,'		# path to actual HTML files from filesystem perspective
	psql += 'parentname TEXT'	# parent project name
	a = dbl(dbname,'CREATE TABLE projects(%s)' % (psql))

	psql  =  'pagename TEXT'	# the name of the web page to be created
	psql  =  'pageloc TEXT'		# the non-default location of the file to be created
	psql += ',projectname TEXT'	# the name of the project which the page belongs to
	psql += ',pagestyle TEXT'	# the style that *wraps* this page
	psql += ',pagelocals TEXT'	# the styles local to this page
	psql += ',content TEXT'		# the actual page content
	psql += ',extension TEXT'	# if the page has a disfferent extension than the default
	psql += ',disable INTEGER'	# if the page is not to be generated
	psql += ',sequence INTEGER'	# the order in which the pages are built and linked
	a = dbl(dbname,'CREATE TABLE pages(%s)' % (psql))

	if do_debug == True: debug += str(a)
else:
	fh.close() # it's there

# CSS used on the doc system form page
# ------------------------------------
styles = """div#docwarn
{
	margin-right: 100px;
	margin-left: 80px;
	margin-bottom: 10px;
	clear: both;    
	padding-left: 10px;
	padding-right: 10px;
	padding-top: 5px;
	padding-bottom: 5px;
	border: 1px solid #000000;
	background: #ffddff;
	color: #000000;
}
div#docnote
{
	margin-right: 100px;
	margin-left: 80px;
	margin-bottom: 10px;
	clear: both;    
	padding-left: 10px;
	padding-right: 10px;
	padding-top: 5px;
	padding-bottom: 5px;
	border: 1px solid #000000;
	background: #ddddff;
	color: #000000;
}"""

# command lists used to populate the cmd bars on the three form types
# -------------------------------------------------------------------
rpacmds = ['save','generate','delete']
gpacmds = ['prev','next','list','search','load','resequence']

rprcmds = ['save','generate','delete']
gprcmds = ['list','load']

rstcmds = ['save','delete']
gstcmds = ['load']

# quick links to each of the three form types
# -------------------------------------------
palinks = [	['Project Editor','mode=project'],
			['Global Style Editor','mode=style'],
			['Page Editor','mode=page']
		  ]

# Here's the reference for the page form
# --------------------------------------
thereference = """<br>
<div id="docnote">

<b>Quick Reference:</b><br>
<br>

<i>Pre-defined locals</i><br>
<pre>
[v nextpage] = page and extension of the next page in sequence, or nothing
[v prevpage] = page and extension of the previous page in sequence, or nothing
[v current_page] = web page name from top of this form
</pre>

<i>Escapes</i><br>
<pre>
[lb] [rb] = [ ]
[ls] [rs] = { }
[sp] = space
[nl] or [lf] = newline
</pre>

</div>
"""

# These are the forms
# ===================

# Page form
# ---------
pabody  = """
[WARNING]
<h3 style="text-align: center;">Page Editor</h3>
<FORM METHOD="POST" ACTION="[XPREFIX][XSYSTEM]">
[MODE]
<table style="margin: auto; background-color: rgb(240,240,240);" width="90%" border=1>
[PROJECTNAME]
[WEBPAGENAME]
[PAGELOC]
[EXTENSION]
[PAGESEQ]
[PAGEDISABLE]
[PAGEALLOW]
[PAGESTYLE]
[PAGELOCAL]
[PAGECONTENT]
</table>
<table style="margin: auto; background-color: rgb(255,128,128);" width="80%" border=1>
<tr>[RCMDS]</tr>
</table>
<table style="margin: auto; background-color: rgb(128,255,128);" width="80%" border=1>
<tr>[GCMDS]</tr>
</table>
<table style="margin: auto; background-color: rgb(220,220,255);" width="70%" border=1>
<tr>[LINKS]</tr>
</table>
</FORM>
[DEBUG]
[REFERENCE]
"""

# Style form
# ----------
stbody  = """
<h3 style="text-align: center;">Global Style Editor - These apply to <i>all</i> documents</h3>
[WARNING]
<FORM METHOD="POST" ACTION="[XPREFIX][XSYSTEM]">
[MODE]
<table style="margin: auto; background-color: rgb(240,240,240);" width="90%" border=1>
[STYLEALLOW]
[GLOBALSTYLES]
</table>
<table style="margin: auto; background-color: rgb(255,128,128);" width="80%" border=1>
<tr>[RCMDS]</tr>
<table style="margin: auto; background-color: rgb(128,255,128);" width="80%" border=1>
<tr>[GCMDS]</tr>
</table>
<table style="margin: auto; background-color: rgb(220,220,255);" width="70%" border=1>
<tr>[LINKS]</tr>
</table>
</FORM>
<br>
<div id="docwarn">
<b>Note:</b><br>
Only the <b>global</b> style form can be used here: <tt><b>[<b style="color: red;">gstyle</b> StyleDefinition]</b></tt><br>
Only the <b>global</b> variable form can be used here: <tt><b>[<b style="color: red;">global</b> VariableDefinition]</b></tt><br>
These styles apply to <i>all</i> projects
</div>
</div>
[DEBUG]
"""

# Project form
# ------------
prbody  = """
[WARNING]
<h3 style="text-align: center;">Project Editor</h3>
<FORM METHOD="POST" ACTION="[XPREFIX][XSYSTEM]">
[MODE]
<table style="margin: auto; background-color: rgb(240,240,240);" width="90%" border=1>
[PROJECTNAME]
[PROJECTTARGET]
[PREVIEWPATH]
[PROJECTEXT]
[PROJECTALLOW]
[PARENTNAME]
[PROJECTSTYLES]
</table>
<table style="margin: auto; background-color: rgb(255,128,128);" width="80%" border=1>
<tr>[RCMDS]</tr>
</table>
<table style="margin: auto; background-color: rgb(128,255,128);" width="80%" border=1>
<tr>[GCMDS]</tr>
</table>
<table style="margin: auto; background-color: rgb(220,220,255);" width="70%" border=1>
<tr>[LINKS]</tr>
</table>
</FORM>
<br>
<div id="docwarn">
<b>Note:</b><br>
Only the <b>global</b> style form can be used here: <tt><b>[<b style="color: red;">gstyle</b> StyleDefinition]</b></tt><br>
Only the <b>global</b> variable form can be used here: <tt><b>[<b style="color: red;">global</b> VariableDefinition]</b></tt><br>
These styles are specific to this project
</div>
[DEBUG]
"""

# This produces a page listing all projects
# assuming there are any. Otherwise, sets
# mode to project and returns
# -----------------------------------------
def prolist():
	global xprefix
	global xsystem
	global dbname
	global mode
	global cmd
	global warning
	sql  = 'SELECT name FROM projects'
	a = dbl(dbname,sql)
	content = ''
	if a.rows != 0:
		b = table("Projects")
		for tup in a.tuples:
			content += b.line('&nbsp;<a href="%s%s?mode=project&amp;projectname=%s">%s</a>&nbsp;' % (xprefix,xsystem,str(tup[0]),str(tup[0])))
		content += b.finish()
		content += '<br><a href="%s%s?mode=project">Open Empty, Unnamed Project</a>' % (xprefix,xsystem)
		print thePage(	title   = 'Proj List',
						styles  = '',
						body    = content,
						valid   = 1,
						forhead = metags,
						forbody = colors,
						doctype = '4.01')
		exit()
	else:
		warning += '...No Projects Found<br>'
		cmd = ''
		mode = 'project'
	return

# This produces a page listing all pages in a project
# ---------------------------------------------------
def paglist(term=None):
	global xprefix
	global dbname
	global projectname
	global warning
#	a = dbl(dbname,'PRAGMA case_sensitive_like=ON')
#	warning += '<pre>\n'+str(a)+'\n</pre>'
	tcolors = 'style="color: #442200; background-color: #FFEEDD;"'
	ssql = ''
	if term != None:
		if casesensitive == True:
			ssql = " AND (pagelocals LIKE '"+term+"' OR content LIKE '"+term+"')"
		else:
			ssql = " AND (lower(pagelocals) LIKE lower('"+term+"') OR lower(content) LIKE lower('"+term+"'))"
	sql  = "SELECT pagename||'||||'||sequence FROM pages WHERE projectname='%s'%s ORDER BY sequence" % (projectname,ssql)
	a = dbl(dbname,sql)
	content = warning
	if a.rows != 0:
		seqlist = []
		for tup in a.tuples:
			seqlist.append(str(tup[0]))
		alplist = sorted(seqlist)
		n = len(seqlist)
		bgc = 'FFEEDD'
		ccc = 'ffeedd'
		b = table("#","</tt> Page Order "," "," Alpha Order ")
		b.options(	hparms = 'align=right||bgcolor=%s|' % (bgc),
					lparms = '||width=50 bgcolor=%s|' % (bgc))
		cpn = '%s <b><font color="#880000">==&gt;</font></b>' % (projectname)
		for i in range(0,n):
			tik = seqlist[i]
			tup,sn = tik.split('||||')
			tak = alplist[i]
			tap,discard = tak.split('||||')
			content += b.line(	sn,
								' <a href="%s%s?mode=page&amp;webpagename=%s&amp;projectname=%s">&nbsp;%s %s</a>&nbsp;'	%	(xprefix,xsystem,str(tup),projectname,cpn,str(tup)),
								'&nbsp;',
								' <a href="%s%s?mode=page&amp;webpagename=%s&amp;projectname=%s">&nbsp;%s %s</a>&nbsp;'	%	(xprefix,xsystem,str(tap),projectname,cpn,str(tap))
							)
		content += b.finish()
	else:
		content += '...No Pages Found<br>'
	print thePage(	title   = 'Pages List',
					styles  = '',
					body    = content,
					valid   = 1,
					forhead = metags,
					forbody = tcolors,
					doctype = '4.01')
	exit()

# defaults prior to reading CGI input
# -----------------------------------
mytitl = 'Untitled'
mybody = '<P>eh?</P>[DEBUG]'

# CGI defaults for page mode
# --------------------------
projectname = ''
parentname = ''
projectext = ''
webpagename = ''
extension = ''
pageseq = '10'
pagedisable = ''
pagestyle = ''
pageloc = ''
pagelocal = ''
pagecontent = ''

# cgi defalts for project mode
# ----------------------------
projectstyles = ''
projecttarget = ''
previewpath = ''

# cgi defaults for style mode
# ---------------------------
globalstyles = ''

# save a page
# -----------
def savepage():
	global webpagename
	global projectname
	global pagestyle
	global pageloc
	global pagelocal
	global pagecontent
	global extension
	global pagedisable
	global pageseq
	global debug

	try:	snum = int(pageseq)
	except:	snum = 10

	thedis = 0
	if pagedisable == 'ON':
		thedis = 1

	# insanity?
	# ---------
	if webpagename == '': return
	if projectname == '': return

	# does project exist?
	projectname = projectname.lower()
	sql =  "SELECT name from projects where name='%s'" % (clean(projectname))
	a = dbl(dbname,sql)
	if a.rows == 1: # only if project exists. Then, does page exist?
		sql = "SELECT pagename FROM pages WHERE projectname='%s' AND pagename='%s'" % (clean(projectname),clean(webpagename))
		a = dbl(dbname,sql)
		if a.rows == 0:	# then insert, page does not exist
			fields = 'pagename,pageloc,projectname,pagestyle,pagelocals,content,extension,disable,sequence'
			values = "'%s','%s','%s','%s','%s','%s','%s','%s','%s'"
			values = values % (	clean(webpagename),
								clean(pageloc),
								clean(projectname),
								clean(pagestyle),
								clean(pagelocal),
								clean(pagecontent),
								clean(extension),
								str(thedis),
								str(snum))
			icmd = 'INSERT INTO pages (%s) VALUES (%s)' % (fields,values)
		else:			# update, page exists - no need to update name or project
			values  =  "pagestyle='%s'"
			values += ",pagelocals='%s'"
			values += ",content='%s'"
			values += ",extension='%s'"
			values += ",disable=%s"
			values += ",sequence=%s"
			values += ",pageloc='%s'"
			values = values % (	clean(pagestyle),
								clean(pagelocal),
								clean(pagecontent),
								clean(extension),
								str(thedis),
								str(snum),
								clean(pageloc))
			icmd = "UPDATE pages SET %s WHERE projectname='%s' AND pagename='%s'" % (values,clean(projectname),clean(webpagename))
		a = dbl(dbname,icmd)
		if do_debug == True: debug += 'save command result:' + str(a)
	else:
		warning += 'Project Not Found - Unable to save<br>'

# save a style
# ------------
def savesty():
	global globalstyles
	global dbname
	global debug
	sql = "SELECT styles FROM globals"
	a = dbl(dbname,sql)
	if a.rows == 0:	# insert
		scmd = "INSERT INTO globals (styles) VALUES ('%s')" % (clean(globalstyles))
	else:			# update
		scmd = "UPDATE globals SET styles='%s'" % (clean(globalstyles))
	a = dbl(dbname,scmd)
	if do_debug == True: debug += str(a)

# save a project
# --------------
def savepro():
	global projectname
	global parentname
	global projectstyles
	global projecttarget
	global projectext
	global previewpath
	global extension
	global dbname
	global debug
	
	if do_debug == True: debug += 'Saving: "%s", "%s", "%s", "%s", "%s"\n' % (parentname,previewpath,projectname,projecttarget,projectext)

	# first, does project exist? If so, it's an update. Otherwise, an insert.
	# -----------------------------------------------------------------------
	projectname = projectname.lower()
	parentname = parentname.lower()
	sql =  "SELECT name from projects where name='%s'" % (clean(projectname))
	a = dbl(dbname,sql)
	if do_debug == True: debug += str(a)
	projectstyles = clean(projectstyles)
	if a.rows == 0:
		scmd = "INSERT INTO projects (parentname,previewpath,extension,styles,target,name) VALUES  ('%s','%s','%s','%s','%s','%s')"
	else:
		scmd = "UPDATE projects SET parentname='%s',previewpath='%s',extension='%s',styles='%s',target='%s' WHERE name='%s'"
	scmd = scmd % (clean(parentname),clean(previewpath),clean(projectext),clean(projectstyles),clean(projecttarget),clean(projectname))
	a  = dbl(dbname,scmd)
	if do_debug == True: debug += str(a)

# Builds the page sequence, so that sequence-relevant information
# such as previous and next page may be determined
# ---------------------------------------------------------------
def getseq():
	global dbname
	global webpagename
	global projectname
	sql = "SELECT pagename FROM pages WHERE projectname='%s' ORDER BY sequence" % (projectname)
	a = dbl(dbname,sql,lean=True)
	seqlist = []
	seqid = -1
	seqnm = -1
	nf = True
	ll = -1
	for tup in a.tup():
		ll += 1
		nam = str(tup[0])
		if nam == webpagename:
			seqid = nam
			seqnm = ll
			nf = False
		seqlist.append(nam)
	return seqlist,seqid,seqnm,ll

# Sets the previous page name
# ---------------------------
def prevpage():
	global webpagename
	slist,sid,sn,sl = getseq()
	if sn > 0 and sid != -1:
		webpagename = slist[sn-1]

# Sets the next page name
# -----------------------
def nextpage():
	global webpagename
	slist,sid,sn,sl = getseq()
	if sn < sl and sn >= 0 and sid != -1:
		webpagename = slist[sn+1]

# the sequence values on eah page determine the processing
# and editing order. You can put any values in there, which
# makes it easy to insert pages between, etc. But eventually,
# you can run out of room. This function renembers all pages,
# still in the sequence order you defined, starting with 10
# and incrementing by 10 per page. If you have inadvertntly
# duplicated a sequence number, they may come out AB or BA.
# But they will be renumbered. You can fix this manually.
# ----------------------------------------------------------
def resequence():
	global dbname
	global do_debug
	global debug
	global projectname
	sql = "SELECT pagename FROM pages WHERE projectname='%s' ORDER BY sequence" % (projectname)
	a = dbl(dbname,sql)
	num = 0
	for tup in a.tuples:
		num += 10
		nam = str(clean(tup[0]))
		sql = "UPDATE pages SET sequence = %d WHERE pagename='%s'" % (num,nam)
		b = dbl(dbname,sql)
	if do_debug == True: debug += 'reseq\n'

# preview()
# ---------
def preview():
	pass

# Generates all pages to target
# -----------------------------
def generate():
	global debug
	global do_debug
	global dbname
	global projectname
	global warning

	parentlist = {}
	obj = macro()
	obj.setMode('4.01s')
	if do_debug == True: debug += 'gen/1: have object\n'
	if projectname == '': return
	if do_debug == True: debug += 'gen/2: projectname=%s\n' % (projectname)

	slist,sid,sn,sl = getseq() # we'll use this for next/prev page data
	if do_debug == True: debug += 'gen/3: sequence ran len = %s\n' % (len(slist))

	# This processes the global styles
	# --------------------------------
	glostyles = ''
	sql = 'SELECT styles FROM globals'
	a = dbl(dbname,sql)
	if a.rows == 1:
		try:
			glostyles = unclean(str(a.tuples[0][0]))
			obj.theGlobals['vglobal_styles'] = glostyles
			discard = obj.do(str(glostyles))
		except Exception,e:
			warning += 'Processing failure with global styles: "%s"\n' % (e)
	if do_debug == True: debug += 'a.rows=%d of globals/styles\n' % (a.rows)

	# This sets up the filesystem location and the default page extension
	# -------------------------------------------------------------------
	sql = "SELECT target,extension FROM projects WHERE name='%s'" % (projectname)
	a = dbl(dbname,sql)
	if do_debug == True: debug += 'gen/4: tgt,ext query ran\n'
	if a.rows == 0: return
	if do_debug == True: debug += 'gen/5: nonzero result, good to go: %d\n' % (a.rows)
	tgt = a.tuples[0][0]
	if tgt != '':
		if tgt[-1:] != '/':
			tgt = tgt + '/'
	if do_debug == True: debug += 'target = "%s"\n' % (tgt)
	ext = str(a.tuples[0][1])
	if do_debug == True: debug += 'prjext = "%s" (%d)\n' % (ext,len(ext))
	if ext == 'None':
		ext = ''

	prostyles = ''
	sql = "SELECT styles,parentname FROM projects WHERE name='%s'" % (projectname)
	a = dbl(dbname,sql)
	if a.rows == 1:
		prstyles,paname = a.tuples[0]
		if prstyles == None: prstyles = ''	# these will be processed after the next step
		if paname == None: paname = ''		# resolve name of first parent project, if any

		# This brings in parent styles, and parents of parents, etc.
		# Each parent is brought in only once, so recursive looping
		# cannot occur.
		# ----------------------------------------------------------
		while paname != '': # There are parent styles to include
			sql = "SELECT styles,parentname FROM projects WHERE name='%s'" % (clean(paname))
			pa = dbl(dbname,sql)
			if pa.rows == 1:
				pastyles,paname = pa.tuples[0]
				if paname == None: paname = ''
				paname = str(paname)
				if paname != '':
					if parentlist.get(paname,'') == '':
						parentlist[paname] = 'x'
					else:
						paname = ''
				if pastyles == None: pastyles = ''
				pastyles = str(pastyles)
				if pastyles != '':
					pastyles = unclean(pastyles)
					try:
						obj.theGlobals['vparent_styles'] = pastyles
						discard = obj.do(str(pastyles))
					except Exception,e:
						warning += 'Failure with parent "%s" styles: "%s"\n' % (paname,e)

		# This processes the styles belonging to this
		# specific project:
		# -------------------------------------------
		try:
			parstyles = unclean(str(prstyles))
			obj.theGlobals['vproject_styles'] = parstyles
			discard = obj.do(str(parstyles))
		except Exception,e:
			warning += 'Failure: "%s"\n' % (e)
			parstyles = ''

	if do_debug == True: debug += 'a.rows=%d\n' % (a.rows)

	# Build list of next/prev links
	# -----------------------------
	seqlist = []
	fmt = "SELECT pagename,extension FROM pages WHERE coalesce(disable,0)=0 AND projectname='%s' ORDER BY sequence"
	sql = fmt % (projectname)
	a = dbl(dbname,sql,lean=True)
	slen = -1
	for tup in a.tup():
		slen += 1
		na = str(tup[0])	# page name
		ex = str(tup[1])	# page extension
		if ex == '':
			ex = ext
		pl = na + ex
		seqlist.append(pl)

	# Per-page generation (lean fetch mode)
	# -------------------------------------
	sql = "SELECT pagename,content,extension,pagelocals,pagestyle,pageloc FROM pages WHERE coalesce(disable,0)=0 AND projectname='%s' ORDER BY sequence" % (projectname)
	a = dbl(dbname,sql,lean=True)
	pnum = -1
	for tup in a.tup():
		pnum += 1
		obj.resetLocals()
		if do_debug == True: debug += 'gen/6A: tup loop pnum=%d\n' % (pnum)
		pn,co,ex,pl,ps,pagloc = tup
		ex = str(ex)
		ps = str(ps)
		pl = unclean(str(pl))
		if pagloc == None:
			pagloc = ''
		pagloc = unclean(pagloc)
		if ex == '' or ex == 'None': ex = ext
		fpn = pn + ex
		fn = tgt + fpn
		if pagloc != '':
			if pagloc[-1:] != '/':
				pagloc = pagloc + '/'
			fn = pagloc + fpn

		nextp = ''
		prevp = ''
		if pnum > 0:
			prevp = seqlist[pnum - 1]
		if pnum < slen:
			nextp = seqlist[pnum + 1]
		fmt  = '[local current_page %s]'
		cpp = fmt % (fpn)
		discard = obj.do(cpp)

		fmt = ''
		pagref = ''
		if nextp != '' and prevp != '':
			fmt += '[local prevpage %s]'
			fmt += '[local nextpage %s]'
			pagref = fmt % (prevp,nextp)
		elif nextp != '':
			fmt += '[local nextpage %s][local prevpage]'
			pagref = fmt % (nextp)
		elif prevp != '':
			fmt += '[local prevpage %s][local nextpage]'
			pagref = fmt % (prevp)
		else:
			pass

		if do_debug == True: debug += 'fn = "%s"\n' % (fn)
		try:
			fh = open(fn,'w')
		except:
			warning += 'Unable to save "%s" page. Project Target?, permissions?\n' % (fn)
			return
		pl = str(pl)
		if pl != '':
			try:
				discard = obj.do(str(pagref))
				discard = obj.do(str(pl))
			except Exception,e:
				fh.close()
				warning += 'Page %s; ERROR: "%s" Can\'t parse page locals. Aborted.\n' % (fpn,str(e))
				return
#		discard = obj.do(pagref)
		co = cpp + co
		if ps != '':
			co = '{%s %s}' %  (ps,co)
		try: # try
			pco = obj.do(str(unclean(co)))
		except Exception,e: # except
			fh.close()
			warning += 'Page %s; ERROR: "%s" Can\'t parse content. Aborted.\n' % (fpn,str(e))
			return
		pco = pco.replace('&#123;','{')
		pco = pco.replace('&#125;','}')
		pco = pco.replace('&#91;','[')
		pco = pco.replace('&#93;',']')
		pco = pco.replace('&#44;',',')
		try:
			fh.write(pco)
		except:
			warning += "Can't write to file!\n"
			try: fh.close()
			except:
				warning += "Can't close file!\n"
			return
		try:	fh.close()
		except:	return
		else:
			if do_debug == True: debug += 'gen/6B: save went ok\n'

# capture any incoming CGI for further manipulation
# -------------------------------------------------
form = cgi.FieldStorage()

# if you come in without a mode, or with a pathological mode, defaults to project mode
# ------------------------------------------------------------------------------------
mode = ''
override = 0
try: mode = philter(form['mode'].value)
except: pass
if mode not in ['page','style','project']:
	mode = 'project'
	override = 1

# Capture project CGI data
# ------------------------
try:	projectname		= philter(form['projectname'].value)
except:	projectname		= ''
try:	parentname		= philter(form['parentname'].value)
except:	parentname		= ''
try:	projectstyles	= philter(form['projectstyles'].value)
except:	projectstyles	= ''
try:	projecttarget	= philter(form['projecttarget'].value)
except:	projecttarget	= ''
try:	projectext	= philter(form['projectext'].value)
except:	projectext	= ''
try:	previewpath	= philter(form['previewpath'].value)
except:	previewpath	= ''

# Capture page CGI data
# ---------------------
try:	webpagename		= philter(form['webpagename'].value)
except:	webpagename		= ''
try:	extension		= philter(form['extension'].value)
except:	extension		= ''
try:	pageseq			= philter(form['pageseq'].value)
except:	pageseq			= ''
try:	pageloc			= philter(form['pageloc'].value)
except:	pageloc			= ''
try:	pagestyle		= philter(form['pagestyle'].value)
except:	pagestyle		= ''
try:	pagelocal		= philter(form['pagelocal'].value)
except:	pagelocal		= ''
try:	pagecontent		= philter(form['pagecontent'].value)
except:	pagecontent		= ''
try:	pagedisable		= philter(form['pagedisable'].value)
except:	pagedisable		= ''

# Capture style CGI data
# ----------------------
try:	globalstyles	= philter(form['globalstyles'].value)
except:	globalstyles	= ''

# capture delete information
# --------------------------
try:	deleteallow	= philter(form['deleteallow'].value)
except:	deleteallow	= ''
try:	delok		= philter(form['delok'].value)
except:	delok		= ''
try:	delyes		= philter(form['delyes'].value)
except:	delyes		= ''
try:	delsure		= philter(form['delsure'].value)
except:	delsure		= ''
try:	deleteset	= philter(form['deleteset'].value)
except:	deleteset	= ''
try:	delonetime	= philter(form['delonetime'].value)
except:	delonetime	= ''
try:	delrand		= philter(form['delrand'].value)
except:	delrand		= ''

# Execute the various commands in the context of the current mode
# ---------------------------------------------------------------
try:
	searchterm = form['searchterm'].value
except:
	searchterm = ''
else:
	searchterm = searchterm.replace('\'','\\\'')

try:
	cs = str(form['casesensitive'].value).lower()
except:
	casesensitive = False
else:
	if cs == 'on':
		casesensitive = True

dodelete = False
try:
	if override == 0:	# normal operation
		cmd = philter(form['perform'].value)
	else:
		cmd = 'LIST'	# came in with no mode - try to list projects
	if do_debug == True: debug += 'got cmd\n'
except:
	cmd = 'no command'
	if do_debug == True: debug += "didn't get command\n"
else:
	if do_debug == True: debug += 'checking command ("%s" in "%s" context)\n' % (cmd,mode)
	if mode == 'project':
		if cmd == 'SAVE':
			savepro()
		elif cmd == 'DELETE':
			dodelete = True
		elif cmd == 'GENERATE':
			savepro()
			generate()
		elif cmd == 'LIST':
			savepro()
			prolist()
		elif cmd == 'LOAD':
			pass
		else: # not in command mode
			pass
	elif mode == 'style':
		if cmd == 'SAVE':
			savesty()
		elif cmd == 'DELETE':
			savesty()
			dodelete = True
		else:
			cmd = 'No command in style mode'
	elif mode == 'page':
		if cmd == 'SAVE':
			savepage()
		elif cmd == 'GENERATE':
			savepage()
			generate()
		elif cmd == 'DELETE':
			savepage()
			dodelete = True
		elif cmd == 'PREV':
			savepage()
			prevpage()
		elif cmd == 'SEARCH':
			savepage()
			paglist(searchterm)
		elif cmd == 'LIST':
			savepage()
			paglist()
		elif cmd == 'NEXT':
			savepage()
			nextpage()
		elif cmd == 'LOAD':
			pass
		elif cmd == 'RESEQUENCE':
			savepage()
			resequence()
		else: # not in command mode
			pass
if do_debug == True: debug += cmd + '\n'

# Convenience functions to generate CGI form elements
# ===================================================

# text elements, one line
# -----------------------
def mvrow(body,label,name,content,length):
	fi = makevrow(label,name,content,length)
	body = body.replace('[' + name.upper() + ']',fi)
	return body

# checkmark elements
# ------------------
def mcrow(body,label,name,value):
	fi = makecheckrow(label,name,value)
	body = body.replace('[' + name.upper() + ']',fi)
	return body

# text box elements
# -----------------
def mtrow(body,label,name,content,rows,cols):
	fi = maketextarea(label,name,content,rows=rows,cols=cols)
	body = body.replace('[' + name.upper() + ']',fi)
	return body

# SUBMIT elements
# ---------------
def mcmd(name):
	name = name[:1].upper() + name[1:].lower()
	termy = ''
	if name == 'Search':
		termx = '<INPUT TYPE="checkbox" NAME="casesensitive"> Match Case'
		termx = ' Wildcards: % _'
		termy = ' <INPUT TYPE="text"  NAME="searchterm"  SIZE=10 MAXLENGTH=40 VALUE="">'+termx
	boil = '<td align="center"><INPUT TYPE="SUBMIT" VALUE="%s" NAME="perform">%s</td>' % (name.upper(),termy)
	return boil

# Builds all SUBMIT elements
# --------------------------
def mcmds(body,m1,m2):
	sub = ''
	if m1 != []:
		for el in m1:
			sub += mcmd(el)
		body = body.replace('[GCMDS]',sub)
	if m2 != []:
		sub = ''
		for el in m2:
			sub += mcmd(el)
		body = body.replace('[RCMDS]',sub)
	return body

# Page and Project DELETE permission processing when DELETE command received
# --------------------------------------------------------------------------
if dodelete == True:
	if (deleteallow == 'ON' and
		delok  == 'ON' and
		delyes == 'ON' and
		delsure== 'ON' and
		deleteset == 'yes' and
		delonetime == delrand):
		warning += 'I guess you meant it! <b>BUH BYE DATA!</b>\n'
		if mode == 'project':
			fmt = "DELETE FROM pages WHERE projectname='%s'"
			sql = fmt % (projectname)
			a = dbl(dbname,sql)
			fmt = "DELETE FROM projects WHERE name='%s'"
			sql = fmt % (projectname)
			a = dbl(dbname,sql)
		elif mode == 'style':
			sql = "DELETE FROM globals"
			a = dbl(dbname,sql)
		elif mode == 'page':
			fmt = "DELETE FROM pages WHERE projectname='%s' AND pagename='%s'"
			sql = fmt % (projectname,webpagename)
			a = dbl(dbname,sql)
			paglist()
	else:
		warning += 'Whew! That was close. Nothing Deleted.\n'

# Creates the intentionally difficult DELETE permissions HTML
# -----------------------------------------------------------
def delrow(page,text,checkone):
	checkonex = 'deleteallow'
	span = '<span style="color: red; font-weight: bold;">'
	s  = '<tr><td align="right">%s%s</span></td>' % (span,text)
	sub  = '<table border=1 width="100%"><tr>'
	cellf = '<td>%s</td>'

	sc = ''
	sc += '<input type="checkbox" name="%s" value="ON"> %sAllow</span><br>' % (checkonex,span)
	sc += '<input type="checkbox" name="delok" value="ON"> %sReally Allow</span><br>' % (span)
	sc += '<input type="checkbox" name="delyes" value="ON"> %sI\'m Sure</span><br>' % (span)
	sc += '<input type="checkbox" name="delsure" value="ON"> %sNo, really, I am!</span>' % (span)
	sub += cellf % (sc)
	
	sc = ''
	sc += '<input type="radio" name="deleteset" value="no" CHECKED> Decidedly not<br>'
	sc += '<input type="radio" name="deleteset" value="uhuh"> Oh, HECK no.<br>'
	sc += '<input type="radio" name="deleteset" value="yes"> %sYeah: Lose EVERYTHING.</span><br>' % (span)
	sc += '<input type="radio" name="deleteset" value="never"> I need to go home and rethink my life.'
	sub += cellf % (sc)

	cellf = '<td align="center">%s</td>'
	code = ''
	step = 0
	random.seed()
	for i in range(8):
		char = chr(65 + random.randint(0,25))
		if step & 1 == 0:
			code += char
		else:
			code += char.lower()
		step += 1
	sc = ''
	sc += '%sConfirm With Code:</span><br>%s<br>' % (span,code)
	sc += '<INPUT TYPE="HIDDEN" NAME="delonetime" VALUE="%s">' % (code)
	sc += '<INPUT TYPE="TEXT" SIZE=10 MAXLENGTH=10 NAME="delrand" VALUE="">'
	sub += cellf % (sc)

	sub += '</tr></table>'
	s += '<td>%s</td></tr>' % (sub)
	page = page.replace('[' + checkone.upper() + ']',s)
	return page

# Creates the various links within the various page modes of the doc system
# -------------------------------------------------------------------------
def mlnks(body):
	global xprefix
	global xsystem
	global projectname
	global projectext
	global dbname
	sub = ''
	for el in palinks:
		if projectname != '' and mode == 'project' and el[1] == 'mode=page':
			sql = "SELECT pagename FROM pages WHERE projectname='%s' LIMIT 1" % (clean(projectname))
			x = dbl(dbname,sql)
			if x.rows == 0:
				sub += '<td align="center"><a href="%s%s?%s&amp;projectname=%s">%s</a></td>' % (xprefix,xsystem,el[1],projectname,el[0])
			else:
				el[0] += ' List'
				sub += '<td align="center"><a href="%s%s?%s&amp;projectname=%s&amp;perform=LIST">%s</a></td>' % (xprefix,xsystem,el[1],projectname,el[0])
		elif projectname != '' and mode == 'page' and el[1] == 'mode=project':
			sub += '<td align="center"><a href="%s%s?%s&amp;projectname=%s">%s</a></td>' % (xprefix,xsystem,el[1],projectname,el[0])
		else:
			sub += '<td align="center"><a href="%s%s?%s">%s</a></td>' % (xprefix,xsystem,el[1],el[0])
	body = body.replace('[LINKS]',sub)
	return body

# Many times, I need a variable to be '' when it is None. This does that.
# -----------------------------------------------------------------------
def nonone(s):
	if s == None:
		s = ''
	return s

# Various page modes used to build appropriate forms here:
# --------------------------------------------------------
if mode == 'project':
	if projectname != '':
		sql = "SELECT styles,target,previewpath,extension,parentname FROM projects WHERE name='%s'" % (projectname)
		a = dbl(dbname,sql)
		if a.rows == 1:
			projectstyles = unclean(nonone(a.tuples[0][0]))
			projecttarget = nonone(a.tuples[0][1])
			previewpath = nonone(a.tuples[0][2])
			projectext = nonone(a.tuples[0][3])
			parentname = nonone(a.tuples[0][4])
		else:
			projectstyles = ''
			projecttarget = ''
			previewpath = ''
			parentname = ''
			if do_debug == True: debug += str(a)
	else:
		if do_debug == True: debug += 'projectname = ""\n'
	mytitl = 'DS Project'
	prbody = mvrow(prbody,'Project Name:',				'projectname',		dequote(projectname),	64)
	prbody = mvrow(prbody,'Project Target:',			'projecttarget',	dequote(projecttarget),	512)
	prbody = mvrow(prbody,'Preview Path:',				'previewpath',		dequote(previewpath),	512)
	prbody = mvrow(prbody,'Default Extension:',			'projectext',		dequote(projectext),	32)
	prbody = delrow(prbody,'Allow Delete','projectallow')
	hlp = '<br><br>(<i>Non-style, non-variable content is treated as commentary</i>)'
	prbody = mvrow(prbody,'Parent Project',				'parentname',	dequote(parentname),	64)
	prbody = mtrow(prbody,'Project Styles:%s' % (hlp),	'projectstyles',	dequote(projectstyles),	16, 80)
	prbody = mcmds(prbody,gprcmds,rprcmds)
	prbody = mlnks(prbody)
	mybody = prbody
elif mode == 'style':
	sql = "SELECT styles FROM globals"
	a = dbl(dbname,sql)
	if a.rows != 0:
		globalstyles = unclean(a.tuples[0][0])
	else:
		globalstyles = ''
	if do_debug == True: debug += str(a)
	mytitl = 'DS Style'
	stbody = delrow(stbody,'Allow Delete','styleallow')
	hlp = '<br><br>(<i>Non-style, non-variable content is treated as commentary</i>)'
	stbody = mtrow(stbody,'Global Styles:%s' % (hlp),		'globalstyles',	dequote(globalstyles),	16, 80)
	stbody = mcmds(stbody,gstcmds,rstcmds)
	stbody = mlnks(stbody)
	mybody = stbody
elif mode == 'page':
	pretgt = ''
	if projectname != '' and webpagename != '':
		fields = "previewpath,extension"
		sql = "SELECT %s FROM projects WHERE name='%s'" % (fields,clean(projectname))
		a = dbl(dbname,sql)
		if do_debug == True: debug += str(a)
		pretgt = ''
		preext = ''
		if do_debug == True: debug += 'Did the select from project\n'
		if a.rows == 1:
			if do_debug == True: debug += 'Got a row looking for ext\n'
			tup = a.tuples[0]
			pretgt = str(tup[0])
			preext = str(tup[1])
		else:
			if do_debug == True: debug += 'no rows. SQL = "%s"\n' % (sql)
		if do_debug == True: debug += 'ext from project = "%s"\n' % (preext)
		if len(pretgt) != 0:
			if do_debug == True: debug += 'pretgt > 0 length\n'
			if pretgt[-1:] != '/':
				if do_debug == True: debug += 'adding trailing "/"\n'
				pretgt += '/'

		#         0         1        2       3         4          5       6
		fields = "extension,sequence,disable,pagestyle,pagelocals,content,pageloc"
		sql = "SELECT %s FROM pages WHERE projectname='%s' AND pagename='%s'" % (fields,clean(projectname),clean(webpagename))
		a = dbl(dbname,sql)
		if a.rows == 1:
			tup = a.tuples[0]
			extension = tup[0]
			if extension != '':
				preext = tup[0]
			pageseq = str(tup[1])
			pagedisable = str(tup[2])
			if pagedisable == '1':
				pagedisable = 'ON'
			else:
				pagedisable = ''
			pagestyle = unclean(tup[3])
			pagelocal = unclean(tup[4])
			pagecontent = unclean(tup[5])
			pretgt += webpagename + preext
			pagloc = tup[6]
			if pagloc == None:
				pagloc = ''
			pageloc = unclean(pagloc)
		else:
			extension = ''
			preext = ''
			pageseq = '10'
			pagedisable = ''
			pagestyle = ''
			pagelocal = ''
			pagecontent = ''
			pretgt = ''
			if do_debug == True: debug += 'problem loading page\n'+str(a)
	else:
		if do_debug == True: debug += "can't load web page\n"
	mytitl = 'DS Page'
	pabody = mvrow(pabody,'Project Name:',			'projectname',	dequote(projectname),	32)
	pabody = mvrow(pabody,'Web Page Name:',			'webpagename',	dequote(webpagename),	32)
	pabody = mvrow(pabody,'Non-default location:',	'pageloc',		dequote(pageloc),		32)

	pabody = mvrow(pabody,'Non-default Extension:',	'extension',	dequote(extension),		32)
	pabody = mvrow(pabody,'Page Sequence:',			'pageseq',		dequote(pageseq),		32)
	pabody = mcrow(pabody,'Page Disable:',			'pagedisable',	dequote(pagedisable))
	pabody = delrow(pabody,'Allow Delete','pageallow')
	pabody = mvrow(pabody,'Page Style:',			'pagestyle',	dequote(pagestyle),		32)
	hlp = '<br><br>(<i>Non-style, non-variable content is treated as commentary</i>)<br>'
	if pretgt != '':
		hlp+= '<a href="%s" target="_blank">Page Preview</a>' % (pretgt)
	pabody = mtrow(pabody,'Page Locals:%s' % (hlp),	'pagelocal',	dequote(pagelocal),		6, 80)
	hlp = '<br><br>Do <i>not</i> define styles here!'
	pabody = mtrow(pabody,'Page Content:%s' % (hlp),			'pagecontent',	dequote(pagecontent),	10, 80)
	pabody = mcmds(pabody,gpacmds,rpacmds)
	pabody = mlnks(pabody)
	mybody = pabody

if do_debug == True: debug += 'mode=%s\n' % (mode)

# Generate the requested form
# ----------------------------
if do_debug == True and debug != '':
	debug = '<pre>'+debug+'</pre>'
else:
	debug = ''
if warning != '':
	warning = '<pre>'+warning+'</pre>'
mybody = mybody.replace('[WARNING]',warning)
mybody = mybody.replace('[DEBUG]',debug)
mybody = mybody.replace('[MODE]','<INPUT TYPE="HIDDEN" NAME="mode" VALUE="%s">' % (mode))
mybody = mybody.replace('[XPREFIX]',xprefix)
mybody = mybody.replace('[XSYSTEM]',xsystem)
mybody = mybody.replace('[REFERENCE]',thereference)
print thePage(	title   = mytitl,
				styles  = styles,
				body    = str(mybody),
				valid   = 1,
				forhead = metags,
				forbody = colors,
				doctype = '4.01')

# Done!
