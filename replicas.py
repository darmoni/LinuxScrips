#!/usr/bin/env python

import sys,shlex
from subprocess import call, Popen, check_output, PIPE

client_node='pbxdev.xcastlabs.com'
server_node0=client_node
server_node1='pbxdev2.xcastlabs.com'
server_node2='pbxdev3.xcastlabs.com'
iors=['replica-0.ior','replica-1.ior','replica-2.ior']

server_cmd="ssh ndarmoni@{} 'pkill -10 -f 'RolyPoly/server';export LD_LIBRARY_PATH=/usr/local/ACE_wrappers/lib; cd ~/tao_examples/examples/FaultTolerance ; RolyPoly/server -o {} {}'"
relica0=server_cmd.format(server_node0,iors[0],' -c 2')
relica1=server_cmd.format(server_node1,iors[1],'')
relica2=server_cmd.format(server_node2,iors[2],'')

copy_cmd="scp ndarmoni@{}:tao_examples/examples/FaultTolerance/{} . && scp {} ndarmoni@{}:tao_examples/examples/FaultTolerance/{}"
copy_cmds=[]
if(client_node != server_node0):
    copy_cmds.append(copy_cmd.format(server_node0,iors[0],iors[0],client_node,iors[0]))
if(client_node != server_node1):
    copy_cmds.append(copy_cmd.format(server_node1,iors[1],iors[1],client_node,iors[1]))
if(client_node != server_node2):
    copy_cmds.append(copy_cmd.format(server_node2,iors[2],iors[2],client_node,iors[2]))

client_cmd="ssh {} 'export LD_LIBRARY_PATH=/usr/local/ACE_wrappers/lib; cd ~/tao_examples/examples/FaultTolerance ; RolyPoly/client -k file://replica-0.ior -k file://replica-1.ior -kfile://replica-2.ior'".format(client_node)
print ("\n".join([relica0, relica1, relica2, client_cmd]))
print ("\n".join(copy_cmds))

sys.exit()
try:
    replicas = []
    replicas.append (Popen(shlex.split(relica0), stdin=PIPE, stdout=PIPE, stderr=PIPE))
    replicas.append (Popen(shlex.split(relica1), stdin=PIPE, stdout=PIPE, stderr=PIPE))
    replicas.append (Popen(shlex.split(relica2), stdin=PIPE, stdout=PIPE, stderr=PIPE))
    
    #copying the IORs to the client area
    
    check_output(shlex.split(copy_cmd))
    check_output(shlex.split(client_cmd))
    for s in replicas:
        del s
except:
    for s in replicas:
        del s
