import xml.sax.saxutils
import string
import httplib
from HTMLParser import HTMLParser
global zero
zero = ord('0')
def getpage(name, header):
	conn = httplib.HTTPConnection("hl.glenbrook225.org",80)
	conn.request("GET", "/homelogic/" + name, None, header)
	response = conn.getresponse()
	body = response.read()
	return body
def escape(name):
	escapedname = ""
	name = name.replace(u'__AMPERSAND12121',u'& ')
	for c in name:
		if ord(c) >= 32:
			escapedname += c
	return escapedname
def class0(self, tag, attrs):
	if len(attrs) >= 1 and len(attrs[0]) >= 2 and "javascript:Redirect('taskgradesreport'" in attrs[0][1]:
		link = "";
		for c in attrs[0][1]:
			test = ord(c) - zero
			if test >= 0 and test <= 9:
				link += c
		self.link = link
		self.s = 1
def class1(self, tag, attrs):
	self.s = 2
def class2(self, tag, attrs):
	self.s = 0
class_switch = {0:class0, 1:class1, 2:class2}


class ClassListParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.ndata = []
		self.s = 0
		self.name = None
		self.link = None
	def handle_starttag(self, tag, attrs):
		class_switch[self.s](self, tag, attrs)
	def handle_endtag(self,tag):
		return
	def handle_data(self, data):
		if self.s == 2:
			self.name = data
			self.ndata.append((self.name, self.link))
			self.name = None
			self.link = None
			self.s = 0
def grade_1(self, tag, attrs):
	self.s = 0
def checkclass(attrs, name):
	return (len(attrs) == 1 and len(attrs[0]) == 2 and name in attrs[0][1])
graden = {0:"caption2", 1:"even", 2:"odd"}
gradetmp = {0:"Major period", 1:"Minor Period", 2:"Assignment Group"}
gradecat = {0:u"Name:", 1:u"Date", 2:u"Weight", 3:u"Points Recieved", 4:u"Points Total", 5:u"Percent"}
class GradeListParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.ndata = []
		self.cursec = []
		self.s = -1
		self.c = 0
	def handle_starttag(self, tag, attrs):
		if checkclass(attrs, "caption2"):
			print "Major Reporting Period"
			self.s = 0
			self.c = 0
		if checkclass(attrs, "even"):
			print "	Minor Reporting Period"
			self.s = 1
			self.c = 0
		if checkclass(attrs, "odd"):
			print "		Assignment Group"
			self.s = 2
			self.c = 0
				
	def handle_endtag(self, tag):
		return
	def handle_data(self, data):
		if(self.s != -1):
			todisp = escape(data)
			if(len(todisp) != 0):
				out = '	'*self.s
				out += gradecat[self.c]
				out += ": "
				out += todisp
				out.replace('?', "__QUESTION_MARK__")
				print out.encode('ascii','replace').replace('?',' ').replace('__QUESTION_MARK__', '?')
				self.c += 1
				self.c %= 6
				if(self.s == 2 and self.c == 0):
					self.s = 3
				if(self.c == 0):
					print '~'*60

		
			

conn = httplib.HTTPConnection("hl.glenbrook225.org",80)
user = raw_input("input username ")
import getpass
pword = getpass.getpass("input password ")
print "logging in..."
params = r"SLPath=&AllowEmailPassword1=True&AllowNewUser1=True&School=1&str_Username_req=" + user + r"&str_Password_req=" + pword
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn.request("POST", "/homelogic/sDefault_validate.asp", params, headers)
response = conn.getresponse()
cookie_info = response.getheaders()
cookie = cookie_info[2][1]
header = {"Cookie: ":cookie}
conn.close()
body = getpage("Menu_Side.asp?main=marks", header)
if "Please login again" in body:
	print "bad pass"
	exit()
else:
	print "logged in"
classparser = ClassListParser()
classparser.feed(body)
classlist = []
for name in classparser.ndata:
	classlist.append((escape(name[0]), name[1]))
import sys
oldout = sys.stdout
f = open('homelogic dump', 'w')
for name,link in classlist:
	gradeparser = GradeListParser()
	print "retrieving class ", name
	sys.stdout = f
	abody = getpage("taskgradesreport.asp?cid=" + link, header)
	print "Class: ",name
	print '-'*60
	if "No Grade Details recorded" in abody:
		print "	No grades recorded for this class....\n" + ('-' * 60)
	else:
		gradeparser.feed(gradeparser.unescape(abody).replace(u'& ', u'__AMPERSAND12121'))
	sys.stdout = oldout
	print "finished retrieving class ",  name
#print gradeparser.ndata


