#!/usr/bin/env python3
#ident $Id$ $Date$

my_text_signature='''
Nir Darmoni
Senior Software Engineer
XCast Labs Inc.
(847) 666-5460 Phone
(847) 716-5132 Fax
(800) 254-3109 Customer Support
191 Waukegan Rd <b>Suite 310</b> Northfield, IL 60093
ndarmoni@xcastlabs.com
'''
#print(my_text_signature)
top_line='<table style="font-size:10.0pt;font-family:&quot;Courier New&quot;;color:black">'
closing_line="</table>"
lines=my_text_signature.split("\n")
print (top_line)

for i in range (len(lines)):
    if(len(lines[i]) > 0):
        print ("<tr><td>{}</td></tr>".format(lines[i]))

print (closing_line)

