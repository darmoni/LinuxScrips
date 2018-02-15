#!/usr/bin/env python

def usage():
    print('client.py |  ~/Downloads/kafka_2.11-1.0.0/bin/kafka-console-producer.sh --broker-list localhost:9094 --topic my-replicated-topic')
import socket, time, sys, shlex
from threading import Thread
import signal
from subprocess import call, Popen, check_output, PIPE
from multiprocessing import Process, Pipe, current_process


def sig_handler(sig, frame):
    print "got sig(%d) \n" % sig
    safe_exit()

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

resources=[]

def safe_exit():
    for r in resources:
        del r
    exit(0)

PORT = 32802
BUFFER_SIZE = 4096

def read_from_middle(s,sout):
    try:
        while s:
            data, addr = s.recvfrom(BUFFER_SIZE)
            if(data):
                when=time.time()
                data += "Time: {:18.9f}\nServerIP: {}\n".format(when,addr[0])
                formated_data=repr(data.strip()).strip("'").encode('utf-8')+"\n"
                sout.write(formated_data)
                print(formated_data)
            else:
                time.sleep(1)
    except:
        sys.exit(-1)
    if(s):
        s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', PORT))

producer=shlex.split("/home/nir/Downloads/kafka_2.11-1.0.0/bin/kafka-console-producer.sh --broker-list localhost:9094 --topic my-replicated-topic")
p = Popen(producer, stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False, bufsize=0)
if not p:
    print("producer is not running")
    exit(-1)
resources.append(p)

middle_worker = Thread(target=read_from_middle, args=(s,p.stdin))
middle_worker.setDaemon(True)
middle_worker.start()
resources.append(middle_worker)


while p and middle_worker:
    time.sleep(3)

safe_exit()
#middle_worker.join()
