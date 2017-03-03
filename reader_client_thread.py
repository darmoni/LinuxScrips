import shlex
from subprocess import Popen, PIPE
from time import sleep
from nbstreamreader import NonBlockingStreamReader as NBSR


args = shlex.split('/bin/netcat -u 127.0.0.1 5565')
p = Popen(args, stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False)

# run the shell as a subprocess:
#p = Popen(['python', 'shell.py'],
#        stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)
# wrap p.stdout with a NonBlockingStreamReader object:
nbsr = NBSR(p.stdout)
# issue command:
dials = shlex.split('dsip:55560 dsip:3000 dsip:3001 dsip:70062 dsip:4703 dsip:67892 dsip:4701 dsip:713300 dsip:55560 dsip:3000 dsip:3001 dsip:70062')

p.stdin.write('lTlT')
for call in dials:
    print call
    p.stdin.write('lTlT')
    p.stdin.write(call)
# get the output
    while True:
        output = nbsr.readline(0.1)
        # 0.1 secs to let the shell output the result
        if not output:
            print '[No more data]'
            break
        print output
