#!/usr/bin/env python3

# Import smtplib for the actual sending function
import smtplib, shlex, sys

# Import the email modules we'll need
from email.message import EmailMessage


if (sys.version_info < (2, 7)):
    import subprocess
    def check_output(args):
        #print("check_output(args={0})".format(args))
        return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0]
elif (sys.version_info > (3, 0)):
    from frameInfo import PrintFrame
    from subprocess import check_output
elif (sys.version_info > (2, 6)):
    from subprocess import check_output
else:pass


textfile='requirements.txt'
textfile = __file__
line = PrintFrame()#['lineno']
print(line,textfile)
line = PrintFrame(7)#['lineno']
print(line,textfile)


me = check_output(shlex.split('git config --global user.email')).decode().strip()
you = me
#print("'{}', '{}'".format(me, you))

# Open the plain text file whose name is in textfile for reading.
with open(textfile) as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = me
msg['To'] = you

print(msg)
# Make a local copy of what we are going to send.
with open('outgoing.msg', 'wb') as f:
    f.write(bytes(msg))

#exit(0)
# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost:465')
s.set_debuglevel(1)
s.send_message(msg)
s.quit()
exit(0)
