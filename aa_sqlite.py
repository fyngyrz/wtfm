import sqlite3

class dbl(object):
	"""Class to simplify access to sqlite3.
      Author: fyngyrz  (Ben)
     Contact: fyngyrz@gmail.com
              (bugs, feature requests, kudos, bitter rejections)
     Project: aa_sqlite.py
    Homepage: https://github.com/fyngyrz/aa_sqlite
     License: None. It's free. *Really* free.
              Defy invalid social and legal norms.
 Disclaimers: 1) Probably completely broken. Do Not Use.
                 You were explicitly warned. Phbbbbt.
              2) My code is blackbox, meaning I wrote it without reference
                 to OPC (other people's code.)
              3) I can't check other people's contributions effectively,
                 so if you use any version of aa_sqlite.py that incorporates
                 accepted commits from others, you are risking the use of
                 OPC, which may or may not be protected by copyright,
                 patent, and the like, because our intellectual property
                 system is pathological. The risks and responsibilities and
                 any subsequent consequences are entirely yours. Have you
                 written your congresscritter about patent and copyright
                 reform yet?
      Incep Date: February 1st, 2015
         LastRev: January 15th, 2017
      LastDocRev: January 15th, 2017
     Tab spacing: 4 (set your editor to this for sane formatting while reading)
     Dev Env: OS X 10.6.8, Python 2.6.1
   Add'l Env: Debian 8.6, Python 2.7.9
   Add'l Env: Ubuntu 12.04.5 LTS, Python 2.7.3
	  Status: BETA
    Policies: 1) I will make every effort to never remove functionality or
                 alter existing functionality once past BETA stage. Anything
                 new will be implemented as something new, thus preserving all
                 behavior. The only intentional exceptions to this are if a
                 bug is found that does not match the intended behavior,
                 or I determine there is some kind of security risk. Remember,
                 this only applies to production code. Until the BETA status
                 is removed, ANYTHING may change.
       Usage: Run examples in shell like so:    python aa_sqlite.py
              Otherwise, it's an import library. See details below.
     1st-Rel: 1.0.6
     Version: 1.0.9
     History:
	    1.0.9 - case-sensitivity issues with sqlite addressed
		1.0.8 - bugfixes
		1.0.7 - bugfixes
		1.0.6 - first public release
	
	The circumstances underlying why you would want to use this are:
	
		1: You want your DB code to be REALLY easy to write
	
		2: You want extensive diagnostics and error handing,
		   but you don't want it in your face unless you need it
	
	If that sounds like your situation, then I think you're
	going to really like class dbl.
	
	This class creates simplified mechanisms for common sqlite3 uses.
	If a COMMAND, then it is executed and the instance may be deleted
	to recover memory. If a QUERY, then the instance returns containing
	.tuples, or can be iterated for each tuple, which are the query data,
	and .rows which tells how many (if any) rows were, or have been, retreived.
	
	In addition, there are three very handy utility functions that serve to
	keep DB data just the way you want (details above each function, below)::
	
		def sqclean2html(string):        # cleans up single quotes for HTML use
		def sqclean2esc(string):         # cleans up single quotes for literal use
		def launder(string,alsothis=''): # can clean up anything. :)
	
	As for the main tool, class dbl, you have a choice with queries,
	either heavy or light memory use:
	
	Returning all the tuples is memory-heavy, as they all have to be
	fetched and stored within the object. Benefit: You know how many
	rows you have before you process them. This is "heavy" use of class
	dbl. memory is cheap, and this is very effective if you are going to
	process all rows anyway.
	
	Returning one tuple at a time is memory-light, as only one tuple has
	to be stored in the object at one time. Issue: You don't know how
	many rows will be retrieved, although object.rows is always set to
	how many rows have been retrieved *thus far* as you retrieve
	additional rows. This  is "light" use of class dbl.
	
	The object is printable, like so...
	
		a = dbl(dbname,sql)
		print str(a)
	
	...a wealth of information including accrued diagnostics, error
	messages, state information, query string and so forth will be
	displayed in a nicely formatted manner with the console in mind.
	
	If you'd prefer the information in HTML, just do this instead:
	
		print a.html()
	
	Integrally committed one-op cmds are one-liners. (do)
	Getting data back from a query requires two lines. (open,do,[,,,])
	Deferred commit ops require minimum 3 lines (open,do,[...],commit)

	Deferred reads prior to commit work normally, but read back
	UNcommited data. Examples provided of deferred operations below.
	
	Built-in instance variables of interest are:
	
	------------- functional------------------------
	
	instance.tuples = database tuples in HEAVY mode
	
	------------- informative ----------------------
	
	instance.ec     = error count (normally 0)
	instance.err    = error message(s), if any, or None
	instance.dbn    = database name
	instance.diag   = diagnostic message(s), if any, or None
	instance.mode   = "query" or "cmd"
	instance.qs     = query string
	instance.rows   = query rows retrieved
	
	------------- access ----------------------------
	
	import aa_sqlite [ then, a = aa_sqlite.dbl(dbname,querystring) ]
	    ...or...
	from aa_sqlite import dbl [then, a = dbl(dbname,querystring) ]
	    ...or...
	from aa_sqlite import * [then, a = dbl(dbname,querystring) ]
	
	------------- Outline of Use ---------------------
	
	Basic memory heavy query operation with case sensitive like:
	
	    a = dbl(dbname,sqlSELECT,cs=True) # db is closed upon object creation
	    for tup in a.tuples:              # all SELECTed data is now in object
	        # do things with tup[0...n]   # db already closed
	
	Basic memory light query operation:
	
	    a = dbl(dbname,sqlSELECT,lean=1) # db open upon object creation
	    for tup in a.tup():              # fetch, one tuple at a time
	        # do things with tup[0...n] - db closes automatically when done
	
	Basic command operation with immediate commit:
	
	    a = dbl(dbname,sqlCMD)         # will commit on completion
	
	Basic deferred commit operation:
	
		a = dbl(dbname,'',True,False)  # set up deferred commit mode
	    a.dbl(sqlCMD)                  # first deferred db-changing operation
	    a.dbl(sqlCMD)                  # 2nd...n deferred db-changing operation
	    a.cmt()                        # actual commit and close

	Basic deferred commit operation with intentional abandonment:
	
		a = dbl(dbname,'',True,False)  # set up deferred commit mode
	    a.dbl(sqlCMD)                  # first deferred db-changing operation
	    a.dbl(sqlCMD)                  # 2nd...n deferred db-changing operation
	    a.close()                      # close without commit: db changes lost
	
	Deferred commit with atomic readback of change(s), heavy version:
	
		Basic Form:
		===========
		a = dbl(dbname,'',True,False)		# opens the DB in deferred commit, HEAVY
		a.dbl(sqlCMD)						# does something deferred
		a.dbl(sqlSELECT)					#  this reads back ALL UNcommited rows
		for tup in a.tuples:				# fetch it/them from object
			print str(tup)					# and do something with it/them
		a.cmt()								# commits the changes
	
	Deferred commit with atomic readback of change(s), light version:
	
		Basic Form:
		===========
		a = dbl(dbname,'',True,False,True)	# opens DB in deferred commit, LIGHT
		a.dbl(sqlCMD)						# does something deferred
		a.dbl(sqlSELECT)					# this sets up to read back
		for tup in a.tup():					# reads back one UNcommitted row
			print str(tup)					# do something with each as fetched
		a.cmt()								# commits the changes
		
		Some explanation about deferred operations:
		-------------------------------------------
		The deferred forms of use allow you to atomically change data
		without anyone else getting in between you and the change on
		read OR write operations. The DB is read/write locked for any
		other accessing code other than YOUR object until you commit (so
		don't hold on to that commit too long!) You can read the changes
		you have made back with a deferred mode read, as shown just
		above. This is ideal for utilizing a guaranteed monotonically
		increasing index or serial number. Locked databases will wait a
		little bit to see if the lock goes away before they return an
		error. So quick operations as shown here don't interfere with
		other users.
	
	*** Diagnostics normally accrue during deferred commit operations.
		Because of this, you may wish to reset them prior to each op...
	
			a = dbl(dbname,'',True,False)
			for x in range(0,10):
				a.diag = None
				a.dbl(sqlCMDxTimes)
			a.cmt()
	
		...in this way, only the diags for the most recent deferred command will
		be stored in the object at any one time.
		
		Case Sensitivity
		================
		
		sqlite is, inexplicably, not case-sensitive with LIKE();
		PostgreSQL LIKE is case-sensitive, and its ILIKE is
		case-insensitive. Which makes sense. sqlite's default
		approach... does not make sense. sqlite is both missing ILIKE
		and has the sense of LIKE backwards. So that's kind of a mess.
		There is a way to coerce sqlite's LIKE into being
		case-sensitive, and I've implemented it as a flag: cs=True.
		
		With cs=True either in the class instantiation or in a call to
		dbl() with an extant object, LIKE is or becomes case-sensitive.
		But now you don't have case INsensitivity. But there's an easy
		way to make that happen in the query SQL.
		
		Say you have a db where the names column contains one name 'ben'
		and one name 'Ben':
		
		case sensitive:
		---------------
		SELECT name FROM names WHERE name LIKE('ben)
		result: 'ben'
		
		case INsensitive:
		-----------------
		SELECT name FROM names WHERE lower(name) LIKE('ben')
		SELECT name FROM names WHERE upper(name) LIKE('BEN')
		result: 'ben','Ben'
		
		Informational pragmas (but see note):
		=====================================
		dbl() knows how to return rows for:
		
			PRAGMA table_info(TableName)
	
		NOTE: If you need other read pragmas supported, just let me know.
	
		At the end of this module are some concrete examples that demonstrate
		how to run commands and queries (both light and heavy), execute
		deferred operations, demonstrate case-sensitivity,  and so on.
		
		You can actually run them. Just execute this file directly instead
		of importing it, like this...
	
			python aa_sqlite.py
	
		...and the examples will run. Examining them and their outputs may
		be enlightening.
"""

# Accumulates errors in user-reportable form
# ------------------------------------------
	def qerr(self,estr):
		self.ec += 1
		if self.err == None:
			self.err = estr
		else:
			self.err += '\n           : '+estr

# Accumulates diagnostics in user-reportable form
# -----------------------------------------------
	def qdiag(self,dstr):
		if self.diag == None:
			self.diag = dstr
		else:
			self.diag += '\n           : '+dstr

# dbl.close() -- used to terminate deferred write
# operations, abandoning changes since the deferred
# state was opened. See class docs for example of use.
# ----------------------------------------------------
	def close(self):
		self.qs = ''
		self.diag = None
		self.lean = False
		if self.conn == None:
			self.qerr('connection is not open')
			self.c = None
			return
		if self.c == None:
			self.qerr('cursor is not valid')
			return

		try: self.c.close()
		except:
			self.qerr('failure to close cursor in close()')
		else:
			self.qdiag('c.close() OK')
		self.c = None

		try: self.conn.close()
		except:
			self.qerr('failure to close connection in close()')
		else:
			self.qdiag('conn.close() OK')
		self.conn = None
		return

# dbl.cmt() -- deferred commit for DB operations that need
# to occur all at once, or not at all. See class docs for
# example of use.
# --------------------------------------------------------
	def cmt(self):
		self.qs = ''
		self.diag = None
		if self.conn == None:
			self.qerr('connection is not open')
			self.c = None
			return
		if self.c == None:
			self.qerr('cursor is not valid')
			return

		try: self.conn.commit()
		except:
			self.qerr('failure to commit in deferred commit')
		else:
			self.qdiag('self.conn.commit() OK')

		try: self.c.close()
		except:
			self.qerr('failure to close cursor in deferred commit')
		else:
			self.qdiag('c.close() OK')
		self.c = None

		try: self.conn.close()
		except:
			self.qerr('failure to close connection in deferred commit')
		else:
			self.qdiag('conn.close() OK')
		self.conn = None
		return

# instance.dbl() -- SQL query and command manager
# See class documentation for examples of use.
# -----------------------------------------------
	# lean SELECTS

	def cleanup(self):
		try:
			self.c.close()
		except:
			self.qerr('unable to close cursor\n')
		else:
			self.c = None
			self.qdiag('c.close() OK')
		try:
			self.conn.close()
		except:
			self.qerr('unable to close connection\n')
		else:
			self.qdiag('conn.close() OK')
			self.conn = None
		return None

	def tupcleanup(self):
		self.cleanup()
		self.lean = None
		self.row = None

	def tup(self):
		self.looping = 1
		self.rows = 0
		while self.looping == 1:
			if self.conn == None:
				self.qerr('tup: no connection')
				self.tupcleanup()
				return
			if self.c == None:
				self.qerr('tup: no cursor')
				self.tupcleanup()
				return
			try:
				self.row = self.c.fetchone()
			except:
				self.row = None
				self.tupcleanup()
				self.qerr('tup: c.fetchone() failed')
				return
			if self.row == None:
				self.looping = 0
			else:
				self.rows += 1
				yield self.row
		self.qdiag('fetchone() sequence completed normally')
		if self.defer == True:
			self.lean = False # just exit lean query mode, don't close
		else:
			self.tupcleanup() # close connection normally

#
# This is used instead of dbl if lean mode is True
# only opens connection if connection not present,
# so can work with deferred commits
#
	def ldbl(self):
		if self.conn == None: # then we must open the db
			self.err = None
			self.row = None
			self.qdiag('lean query="'+self.qs+'"')
			try: self.conn = sqlite3.connect(self.dbn)
			except:
				self.qerr('sqlite3.connection exception thrown, check database name')
				return
			else:
				self.qdiag('connect('+self.dbn+') OK')
			# now open cursor if things are sane
			if self.conn == None:
				self.qerr('connection is not open, cannot proceed')
				self.tupcleanup()
			else:
				if self.c == None:
					try: self.c = self.conn.cursor()
					except:
						self.qerr('conn.cursor exception thrown, connection bad?')
						self.tupcleanup()
				else:
					self.qerr('FAIL: conn.cursor already open!')
		if self.c == None:
			self.qdiag('Cursor not open, cannot execute')
		else:
			if self.cs == True and self.csset == False:
				try:
					self.c.execute('PRAGMA CASE_SENSITIVE_LIKE = On')
				except Exception,e:
					self.qerr('Unable to set CASE_SENSITIVE_LIKE: "'+str(e)+'"')
					self.qdiag('Case sensitivity failed to set')
				else:
					self.qdiag('Case sensitivity set')
					self.csset = True
			else:
				self.qdiag('Case insensitive mode')
			try: self.c.execute(self.qs)
			except:
				self.qerr('Execute exception thrown, check query/cmd string')
				self.tupcleanup()
			else:
				self.qdiag('conn.execute OK')

	def dbl(self,qs='',defer=None,commit=None,lean=None,cs=None):
		if defer != None: self.defer = defer
		if commit != None: self.commit = commit
		if lean != None: self.lean = lean
		if qs != '': self.qs = qs
		if cs != None: self.cs = cs

		if self.lean == True:
			self.qdiag('lean detected true')
			if self.qs[0:6].upper() == "SELECT": # then do it in lean mode
				self.qdiag('lean query detected, calling ldbl')
				self.mode = "Query mode"
				self.ldbl()
				return
			else:
				self.qdiag('query? "'+self.qs[0:6]+'"')

		self.err = None
		self.qdiag('initial commit='+str(self.commit))
		self.qdiag('initial defer='+str(self.defer))
		self.qdiag('initial qs='+str(self.qs))

		if self.defer == True and self.commit == True:
			if self.qs == '':	# setting up?
				try: self.conn = sqlite3.connect(self.dbn)
				except:
					self.qerr('sqlite3.connection exception thrown, check database name')
					return
				else:
					self.qdiag('connect('+self.dbn+') OK')
				if self.conn == None:
					self.qerr('connection is not open, cannot proceed')
					return
				else:
					if self.c == None:
						try: self.c = self.conn.cursor()
						except:
							self.qerr('conn.cursor exception thrown, connection bad?')
							self.conn.close()
							self.conn = None
							return
						else:
							self.qdiag('conn.cursor() OK')
				return

		if self.conn == None or self.defer == False:
			try: self.conn = sqlite3.connect(self.dbn)
			except:
				self.qerr('sqlite3.connection exception thrown, check database name')
				return
			else:
				self.qdiag('connect('+self.dbn+') OK')
		if self.conn == None:
			self.qerr('connection is not open, cannot proceed')
			return
		else:
			if self.c == None:
				try: self.c = self.conn.cursor()
				except:
					self.qerr('conn.cursor exception thrown, connection bad?')
					self.conn.close()
					self.conn = None
					return
				else:
					self.qdiag('conn.cursor() OK')

			if self.cs == True and self.csset == False:
				try:
					self.c.execute('PRAGMA CASE_SENSITIVE_LIKE = On')
				except Exception,e:
					self.qerr('Unable to set CASE_SENSITIVE_LIKE: "'+str(e)+'"')
				else:
					self.qdiag('Case sensitivity set')
					self.csset = True
			else:
				self.qdiag('Case insensitive mode')

			try: self.c.execute(self.qs)
			except:
				self.qerr('Execute exception thrown, check query/cmd string')
			else:
				self.qdiag('conn.execute OK')
#
# we only have selects here if we're not in lean mode
#
				sel1  = "SELECT"
				prag1 = "PRAGMA TABLE_INFO"
				prag2 = 'PRAGMA CASE_SENSITIVE_LIKE'

				if	self.qs[0:len(sel1)].upper() == sel1 or \
					self.qs[0:len(prag1)].upper() == prag1:
#					self.qs[0:len(prag2)].upper() == prag2:

					if self.qs[0:6].upper() == "SELECT":
						self.mode = "Query mode"
					else:
						self.mode = "Pragma mode"
					try: self.tuples = self.c.fetchall()
					except:
						self.tuples = []
						self.qerr('c.fetchall() exception thrown, check connection')
					else:
						self.rows = len(self.tuples)
						self.qdiag('c.fetchall() OK')
				else:
					self.mode = "CMD mode"
					if self.defer == False and self.commit == True:
						try: self.conn.commit()
						except:
							self.qerr('conn.commit() exception thrown, check command string')
						else:
							self.qdiag('c.commit() OK')
			if self.defer == False:
				try:
					self.c.close()
				except:
					self.qerr('unable to close cursor\n')
				else:
					self.qdiag('c.close() OK')
				self.c = None
		if self.defer == False:
			try:
				self.conn.close()
			except:
				self.qerr('unable to close connection\n')
			else:
				self.qdiag('conn.close() OK')
				self.conn = None

# instance: this performs class instantiation. This can
# do the whole shbang for you: connect to the DB, issue
# SQL commands or a query, and return it to you with
# detailed reporting on what went on, row count and so
# forth. See class documentation for examples of use.
# -----------------------------------------------------

	def __init__(self,dbn='',qs='',defer=False,commit=True,lean=False,cs=False):
		self.dbn    = dbn
		self.qs     = qs
		self.rows   = 0
		self.defer  = defer
		self.commit = commit
		self.lean   = lean
		self.tuples = []
		self.mode   = None
		self.conn   = None
		self.row    = None
		self.c      = None
		self.err    = None
		self.ec     = 0
		self.cs     = cs
		self.csset	= False
		self.diag   = None
		self.dbl()

# instance.__str__() -- this returns lots of information about
# what went on during class instantiation and other use. You
# could use this in any case where you're getting results you
# didn't expect. It'll tell you if your query failed, or the
# connection isn't in the epected state and so on. It'll even
# dump a detailed step-by-step report about successful operations.
# ----------------------------------------------------------------
	def __str__(self):
		if self.qs == '':
			sm  = "      Query: '""'\n"
		else:
			sm  = '      Query: "'+str(self.qs)+'"\n'
		sm += '   Database: '+str(self.dbn)+'\n'
		if self.conn == None:
			sm += ' Connection: Closed\n'
		else:
			sm += ' Connection: Open\n'
		if self.c == None:
			sm += '     Cursor: Closed\n'
		else:
			sm += '     Cursor: Open\n'
		sm += '       mode: '+str(self.mode)+'\n'
		sm += '       rows: '+str(self.rows)+'\n'
		sm += '     commit: '+str(self.commit)+'\n'
		sm += '       lean: '+str(self.lean)+'\n'
		sm += '      defer: '+str(self.defer)+'\n'
		sm += '   error(s): '+str(self.err)+'\n'
		sm += 'diagnostics: '+str(self.diag)+'\n'
		return sm

	def html(self):
		return('<tt>'+self.__str__().replace('\n','<br>\n').replace(' ','&nbsp;')+'</tt><br>')

# launder() -- a simple, plain-text based mechanism for
# cleaning up user input in order to make it DB-safe.
# -----------------------------------------------------

# launder() works by whitelisting characters, so you can rest assured
# that nothing harmful will come back.
#
# Space ( ), 3 ranges and 2 single characters are normally whitelisted:
#
#                  A-Z    a-z    0-9    _    -
#
# Having said that, you can set the optional "alsothis" parameter
# for any additional characters you want to permit, or other more
# complex cases. For instance, if you want to launder foo such that
# it may contain the standard whitelisted chars, and additionaly
# the % and $ characters, you would do it like this:
#
#     foo = launder(foo,'%$')
#
# Whereas for normally whitelisted characters, if you do NOT want them,
# include respectively the character or 2x starting character from the
# range: AA,aa,00 and  or _,- and they will not make it through either
#
#     foo = launder(foo,'AA')   # no capital letters
#              or
#     foo = launder(foo,'AAaa+_. ') # ONLY digits, +, -, and decimal point
#
# If you want a subset of an allowed range, say 0-5 of the digits only,
# This would accomplish that...
#
#     foo = launder(foo,'AAaa00 -_012345')
#
# ...it works by disallowing the standard ranges and characters, then
# re-allowing 0...5
#
# This example would pass through only digits and periods:
#
#     foo = launder(foo,'AAaa_- .')
#
# Both of these additionally allow single quotes (apostrophes):
#
#     foo = launder(foo,"'")
#     foo = launder(foo,'\'')
#
# And both of these additionally allow both single quotes and double quotes:
#
#     foo = launder(foo,'"\'')
#     foo = launder(foo,"'\"")
#
# --------------------------------------------------------------------

# Local utility for launder:
# --------------------------
def lau_flag(string,cc,putflag=False):
	if cc in string:
		string = string.replace(cc,'')
		return putflag,string
	return not putflag,string

def launder(string,alsothis=''):
	if string == None: string = ''
	string = str(string) # coercion. It's what's for dinner.
	out = ''
	mflag = sflag = nflag = cflag = lflag = uflag = True
	if alsothis != '':
		uflag,alsothis = lau_flag(alsothis,'_')
		mflag,alsothis = lau_flag(alsothis,'-')
		sflag,alsothis = lau_flag(alsothis,' ')
		cflag,alsothis = lau_flag(alsothis,'AA')
		lflag,alsothis = lau_flag(alsothis,'aa')
		nflag,alsothis = lau_flag(alsothis,'00')
		
	for cc in string:
		if   uflag and cc == '_': out += cc
		elif mflag and cc == '-': out += cc
		elif sflag and cc == ' ': out += cc
		elif nflag and cc >= '0' and cc <= '9': out += cc
		elif cflag and cc >= 'A' and cc <= 'Z': out += cc
		elif lflag and cc >= 'a' and cc <= 'z': out += cc
		else:
			 for dd in alsothis:
				if cc == dd:
					out += cc
	return out

# ===============================================================
# Single quotes. What a pain in database operations. So. Fixit!

# Single quotes are often used as apostophes; we don't want them
# live in query/cmd text; generally, in HTML, the best way to handle
# that is to convert them to numbered character entities.
# ------------------------------------------------------------------
def sqclean2html(string):
	string = str(string) # a little coercion never hurt anyone
	string.replace("'","&#39;")
	return string

# If you're not working in HTML, though, then you probably just
# want to escape them so the DB doesn't see them:
# -------------------------------------------------------------
def sqclean2esc(string):
	string = str(string) # a little coercion never hurt anyone
	string.replace("'","\\'")
	return string

# If you'd prefer to eliminate them entirely, you should probably
# be looking at launder(), above.
# ---------------------------------------------------------------

# Here are some demos that run if you execute the library directly
# instead of importing it as it is normally used. Note this creates
# a small database to work with in the current directory, so make
# sure you have write priviliges in the directory where you try
# this out:
#
#		python aa_sqlite.py
#
# =================================================================
if __name__ == "__main__":
	thedb = 'mytestsernumb.db'

	# if demo db doesn't exist, create it
	# -----------------------------------
	try:
		fh = open(thedb)
	except:
		a = dbl(thedb,"create table thesn(unibase integer)")
		b = dbl(thedb,"insert into thesn (unibase) VALUES (0)")
	else:
		fh.close()

	# HEAVY way
	# =========
	# You get all the tuples at once in a.tuples
	# a.rows tells you how many tuples you got
	# ------------------------------------------

	# LIGHT way (lean=True)
	# =====================
	# b.rows is a *counter* that increments
	# as you get tuples, not a total. You
	# get one tuple every time you call
	# object.tup()
	# ---------------------------------

	# Heavy deferred commit example:
	# -------------------------------
	print 'Heavy:'
	a = dbl(thedb,'',True,False)							# open, deferred commit
	a.dbl("UPDATE thesn SET unibase = unibase + 1")			# increment SN
	a.dbl("SELECT unibase FROM thesn LIMIT 1")				# read back
	for tup in a.tuples:
		print 'pre-commit THIS object reads: '+str(tup[0])	# output

	b = dbl(thedb,"SELECT unibase FROM thesn LIMIT 1")
	for tup in b.tuples:
		print 'pre-commit OTHER objects read: '+str(tup[0])	# output

	a.cmt()													# DB closed,committed here

	# Light deferred example:
	# -----------------------
	print 'Light:'
	a = dbl(thedb,'',True,False,lean=True)					# open, deferred commit, lean
	a.dbl("UPDATE thesn SET unibase = unibase + 1")			# increment SN
	a.dbl("SELECT unibase FROM thesn LIMIT 1")				# read back
	for tup in a.tup():
		print 'pre-commit THIS object reads: '+str(tup[0])	# output

	b = dbl(thedb,"SELECT unibase FROM thesn LIMIT 1",lean=True)
	for tup in b.tup():
		print 'pre-commit OTHER objects read: '+str(tup[0])	# output

	a.cmt()													# DB committed,closed here

# ...don't mix light and heavy techniques on the same object!

	# Here are light and heavy query examples
	# Also demonstrations of case-sensitity management
	# Note the distinction between mode and method
	# ------------------------------------------------
	thedb = 'mytestnames.db'
	# if demo db doesn't exist, create it
	# -----------------------------------
	try:
		fh = open(thedb)
	except:
		nt = ('Ben','haben','mobendar','benjy','ben','Sheila')
		a = dbl(thedb,"create table names(uname text)")
		for tup in nt:
			b = dbl(thedb,"insert into names (uname) VALUES ('"+tup+"')")
	else:
		fh.close()

	print "heavy, case-insensitive mode"
	sql = "SELECT uname FROM names WHERE uname LIKE('ben')"
	a = dbl(thedb,sql)
	for tup in a.tuples:
		print str(tup)

	print "light, case-insensitive mode"
	sql = "SELECT uname FROM names WHERE uname LIKE('ben')"
	a = dbl(thedb,sql,lean=True)
	for tup in a.tup():
		print str(tup)
	a.close()

	print "heavy, case-sensitive mode, case-sensitive method"
	sql = "SELECT uname FROM names WHERE uname LIKE('ben')"
	a = dbl(thedb,sql,cs=True)
	for tup in a.tuples:
		print str(tup)

	print "heavy, case-sensitive mode, case-insensitive method"
	sql = "SELECT uname FROM names WHERE lower(uname) LIKE('ben')"
	a = dbl(thedb,sql,cs=True)
	for tup in a.tuples:
		print str(tup)

	print "light, case-sensitive mode, case-sensitive method"
	sql = "SELECT uname FROM names WHERE uname LIKE('ben')"
	a = dbl(thedb,sql,lean=True,cs=True)
	for tup in a.tup():
		print str(tup)
	a.close()

	print "light, case-sensitive mode, case-insensitive method"
	sql = "SELECT uname FROM names WHERE lower(uname) LIKE('ben')"
	a = dbl(thedb,sql,lean=True,cs=True)
	for tup in a.tup():
		print str(tup)
	print 'demonstrating cs=True is sticky with connection open:'
	sql = "SELECT uname FROM names WHERE uname LIKE('ben%')"
	a = dbl(thedb,sql,lean=True,cs=True)
	for tup in a.tup():
		print str(tup)
	a.close()
