import urllib

import urllib.request
import urllib.parse
from urllib.parse import urlparse, urlsplit
import http.client, urllib.parse

url = 'https://www.w3schools.com/python/demopage.php'
url = 'http://10.10.10.55:8010/2/detail'
#print(urlparse(url))
#with urllib.request.urlopen(url) as f:
#	print(f.read().decode('utf-8'))
	#print(f.headers.keys())

#print(f.status, f.reason)
headers = {}

#exit(0)
def post_to_url(url, cookies, data):
	print("post_to_url ({}, {}, {})".format(url, cookies, data))
	params = urllib.parse.urlencode(data)
	params = params.encode('ascii')
	req = urllib.request.Request(url)
	req.add_header("User-Agent", "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")
	for key in headers.keys():
		print(key, headers[key])
		req.add_header(key, headers[key])
	print('nirwasHere', req.header_items())
	try:
		if len(cookies) > 0:
			urllib.request.HTTPCookieProcessor(cookies)
			#with request.urlopen(url, params) as f:
		with urllib.request.urlopen(url, params) as f:
			print(f.status, f.reason)
			print(f.read().decode('utf-8'))
	except urllib.error.HTTPError as inst:
		print("Error in reading url = '{}', params = {}".format(url, params))
		print (type(inst))
		print (inst.args)
		print (inst)
		print (__file__, 'Oops')
		exit()
#form = requests.get(url)


session_token = "csrfmiddlewaretoken"
csrf = {}
form = urllib.request.urlopen(url)

print("nirwasHere", form)
#exit(0)
#print('Cookies = {}'.format(form.cookies))

#print("Cookie keys = {}".format(form.cookies.keys()))
#print("Cookie csrftoken = '{}'".format(form.cookies['csrftoken']))
#print("{} = '{}'".format(session_token, form.cookies[session_token]))


#cookies = form.headers['Set-Cookie']
#print('Cookies = {}'.format(cookies))

#print(form.session)
#lines = form.content.splitlines()
lines = form.read().splitlines()
for x in lines:
	line = x.decode().replace("<","").replace(">","").replace("input","")
	if line.find(session_token) > -1:
		#print (line)
		elements = line.split()
		counter = 0
		for element in elements:
			#print(element)
			token = element.split("=")
			#print("{} {}".format(token, len(token)))
			name = token[0]
			value = token[1]
			csrf[name] = value.replace('"',"")
			#print("{} {}".format(name, value))
	else:
		next

print(csrf)
#print(form.iter_lines)
#print("Returned form", form.text, form.cookies)
#print("Returned form", form.text, form.body.table.input[session_token])
#print("Sending a request using POST")
myobj = {'somekey': 'somevalue'}
myobj = {'choice' :'MonitorCores'}
myobj = [('id',"choice1"), ('value',"822")]
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
#params = urllib.parse.urlencode({'@' + csrf['name']: csrf['value'], '@id' : 'choice1', '@value' :'822'})
cookies = {} #'name' : session_token, 'value': csrf['value']}
params = {session_token : csrf['value'], 'id' : 'choice1', 'value' :'822'}
print("Before calling post_to_url: params = ",params)
#print(cookies)
post_to_url(url, cookies, params)
exit(0)

#print (url, myobj, "cookies = {}".format(cookies))

#x = requests.post(url, headers, cookies)
#conn = http.client.HTTPConnection(url, 8010)
#conn.request("POST", "", params, headers)
#response = conn.getresponse()
#print(response.status, response.reason)
#data = response.read()
#conn.close()
#print(data)
