import shlex, subprocess
from subprocess import call, Popen, check_output, PIPE

#args = shlex.split('/bin/netcat -u 127.0.0.1 5565')
args = shlex.split("curl 'http://127.0.0.1:9010/?l'")
print check_output(args)

p1 = Popen(["dmesg"], stdout=PIPE)
p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]
print output
