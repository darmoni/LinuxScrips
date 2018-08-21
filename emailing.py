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
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
exit(0)
'''
import smtplib, os
import mimetypes

from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid

# Create the base text message.
msg = EmailMessage()
msg['Subject'] = "Ayons asperges pour le déjeuner"
msg.set_content("""\
Salut!

Cela ressemble à un excellent recipie[1] déjeuner.

[1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718

--Pepé
""")

# Add the html version.  This converts the message into a multipart/alternative
# container, with the original text message as the first part and the new html
# message as the second part.
asparagus_cid = make_msgid()
msg.add_alternative("""\
<html>
  <head></head>
  <body>
    <p>Salut!</p>
    <p>Cela ressemble à un excellent
        <a href="http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718">
            recipie
        </a> déjeuner.
    </p>
    <p>--Pepé</p>
  </body>
</html>
""", subtype='html')
# note that we needed to peel the <> off the msgid for use in the html.
directory='.'
filename = "callSetup_steps.txt"
# Now add the related image to the html part.
with open(filename, 'rb') as img:

    path = os.path.join(directory, filename)
    if not os.path.isfile(path):
        exit(0)
    # Guess the content type based on the file's extension.  Encoding
    # will be ignored, although we should check for simple things like
    # gzip'd or compressed files.
    ctype, encoding = mimetypes.guess_type(path)
    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed), so
        # use a generic bag-of-bits type.
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    with open(path, 'rb') as fp:
        msg.add_attachment(fp.read(),
                            maintype=maintype,
                            subtype=subtype,
                            filename=filename)
# Now send or store the message

# Make a local copy of what we are going to send.
with open('outgoing.msg', 'wb') as f:
    f.write(bytes(msg))
exit(0)
# Send the message via local SMTP server.
with smtplib.SMTP('localhost') as s:
    '
'''
