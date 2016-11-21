#!/usr/bin/python

def readDataFile(fn,toList=0,nolinecomments=0,allsettings=0):
	rdict = {}
	rlist = []
	try:
		fh = open(fn)
	except:
		pass
	else:
		switch = 1
		for line in fh:
			if line != "" and line[0] != '#' and line[:1] != '//': # elim dead lines
				if len(line) >= 2:
					if nolinecomments == 0:
						if line.find('#') > 0:
							line,junk = line.split('#',1)
					if line[0] == '/' and line[1] == '*':		# skip c-style comments...
						switch = 0
					if line[0] == '*' and line[1] == '/':		# ...because it's fun :)
						switch = 1
					if switch == 1:								# ok, just do it
						line = line.strip()
						if toList == 0:
							if line.find('=') > 0:				# THEN loadable entry
								line,datum = line.split('=',1)	#     get the data
								if allsettings == 1:
									rdict[line] = datum				#     store it in dict
								else:
									if (line[:5] != 'desc_' and
										line[:5] != 'grup_' and
										line[:5] != 'indx_' and
										line[:5] != 'type_'):
										rdict[line] = datum
							else:								# ELSE not loadable
								rdict[line] = 1					#     just make a note
						else:
							rlist += [line]
		fh.close()
	if toList == 0:
		return rdict
	return rlist
