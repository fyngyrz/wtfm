# aa_tablelib.py
# --------------

import pgdb
import time
import re
import os
import sys

class table(object):
	"""This class allows you to easily produce HTML table displays
of data. Default values are set for reasonable table production.
The returned value is a string that is appropropriate for aggregation
into other text output destined for a web page, or output via
sys.stdout.write() rather than print because of EOL issues.
Typical use:

	import sys
    from aa_tablelib import *
	from aa_pgsqlib import *
    qs = "SELECT trim(znumber),trim(trim(zdesc)||' '||trim(zdesc2))"
    qs+= " FROM momstock"
    qs+= " WHERE znumber ILIKE 'ABC%'"
    qs+= " ORDER BY znumber"
    a = dbo("sondb",qs,"dserver")
    header("table demo")
    if a.rows > 0:
        b = table("Part #","Description")
        for partnumber,description in a.tuples:
            sys.stdout.write(b.line(partnumber,description))
        sys.stout.write(b.finish())
    else:
        print 'No data found for: '+qs
    footer("")

This will produce properly formatted HTML output
for inclusion in a live web output stream.

If the string [linenumber] is present in any cell, the
string will be replaced with the actual line number for
that line in the table. The first line below the first header
is counted as one.
	"""
	def __init__(self,*headerline):
		self.headerline = headerline # "column title","column title"
		self.linenumber = 0
		self.options()

	def options(self,
				tparms="CELLSPACING=0 CELLPADDING=0 BORDER=1",	# " BORDER=0" or "" or whatever
				hparms="",			# "align=right|align=left"
				lparms="",			# "align=right|align=left"
				hc="FFFFDD",		# header line color
				oc="DDFFDD",		# ODD line color
				ec="DDDDFF",		# EVEN line color
				alt=True,			# alternate line colors (otherwise use EVEN)
				sepchar="|",		# separates the hparms and lparms strings
				hdrrepeat=0):		# how many lines until header repeats (0=never)
		self.sepchar = sepchar
		self.hdrrepeat = hdrrepeat
		self.hc = hc
		self.oc = oc
		self.ec = ec
		self.alt = alt
		if tparms != "":
			tparms = " "+tparms
		self.tparms = tparms
		self.hparms = hparms.split(self.sepchar)
		self.lparms = lparms.split(self.sepchar)

# .update() can be used instead of .options() in order to avoid
# disturbing other settings.
# ----------------------------------------------------------------
	def update(self,
				lparms="",			# "align=right|align=left"
				oc="",				# ODD line color
				ec="",				# EVEN line color
				hdrrepeat=-1):		# how many lines until header repeats (0=never)
		if lparms != '':	self.lparms = lparms
		if oc != '':		self.oc = oc
		if ec != '':		self.ec = ec
		if hdrrepeat != -1:	self.hdrrepeat = hdrrepeat

	def line(self,*linedata):	# "celldata","celldata"
		op = ""
		self.linedata = linedata
		if self.linenumber == 0:
			op += '<table'+self.tparms+'>\n'
		if self.linenumber == 0 or (self.hdrrepeat != 0 and (self.linenumber % self.hdrrepeat == 0)):
			op += '<tr bgcolor="#'+self.hc+'">'
			celldex = 0
			for cell in self.headerline:
				try:
					cp = self.hparms[celldex]
					if cp != "":
						cp = " " + cp
				except:
					cp = ""
				op += "<TH"+cp+">"+cell+"</TH>"
				celldex += 1
			op += '</tr>\n'
		if self.linenumber & 1 == 0 or self.alt == False:
			op += '<tr bgcolor="#'+self.ec+'">'
		else:
			op += '<tr bgcolor="#'+self.oc+'">'
		celldex = 0
		for cell in self.linedata:
			tdcontent = ''
			if type(cell) == list:
				cx = cell
				cell = cx[1]
				tdcontent = cx[0]
			try:
				if tdcontent != '':
					cp = tdcontent
				else:
					cp = self.lparms[celldex]
				if cp != "":
					cp = " " + cp
			except:
				cp = ""
			cell = re.sub("\[linenumber\]",str(self.linenumber+1),cell)
			op += "<TD"+cp+">"+cell+"</TD>"
			celldex += 1
		op += '</tr>\n'
		self.linenumber += 1
		return op
	
	def finish(self):
		return '</table>\n'

	def __str__(self):
		rval = ""
		rval += "    header line=\""+str(self.headerline)+"\"\n"
		rval += "         tparms=\""+self.tparms+"\"\n"
		rval += "         hparms=\""+str(self.hparms)+"\"\n"
		rval += "         lparms=\""+str(self.lparms)+"\"\n"
		rval += "   header color=\""+self.hc+"\"\n"
		rval += " odd line color=\""+self.oc+"\"\n"
		rval += "even line color=\""+self.ec+"\"\n"
		rval += "          lines="+str(self.linenumber)+"\n"
		rval += "  header repeat="+str(self.hdrrepeat)+"\n"
		return rval

