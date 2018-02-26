#!/usr/bin/env python
import shlex, time, select
from subprocess import call, Popen, check_output, PIPE
from multiprocessing import Process, Pipe, current_process

from sys import stdin, stderr, stdout
from reg_event_listener import collect_middle_events
from Queue import Queue
from threading import Thread
import signal
from socket import socket, AF_INET, SOCK_DGRAM
import inspect

#from nbstreamreader import NonBlockingStreamReader as NBSR

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def sig_handler(sig, frame):
    print ("got sig({})\n".format(sig))
    safe_exit(sig)

def safe_exit(level):
    # save stuff
    print("Exiting ...\n")
    kill_cmd="pkill -9 -f '{}'".format(__file__)
    check_output(shlex.split(kill_cmd))
    exit(0)

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

def cleanup():
    kill_cmd="pkill -9 -f '{}'".format(__file__)
    global trd_workers
    for w in trd_workers:
        try:
            del w#trd_workers.remove(w)
        except:
            trd_workers.remove(w)
            #check_output(shlex.split(kill_cmd))
            continue

def use_pipe_to_send_cmd(sock,r, addr):
    try:
        while True:
            msg = r.recv().encode('utf-8')
            print(msg)
            sock.sendto(msg,addr)
    except Exception as inst:
        print ('{}'.format(lineno()), 'dying')
        print (type(inst))
        print (inst.args)
        print (inst)
'''
class clickhouse_client:
    def __init__(self, connection):
        if(connection):
            self.connection=connection
            self.os=connection.stdin
            self.iss=connection.stdout
        else:
            return None
    def ping(self):
        print(self.connection.communicate(input="show tables;\n")[0])
    def write(self, msg):
        print(self.os.write(msg))
'''
'''
def err_log_machine(ins):
    print("err_log_machine: starting ",current_process().name)
    while True:
        try:
            msg = ins.readline()
            if not msg:
                time.sleep(3)
                continue
        except EOFError:
            continue
        else:
            print("{}: {}".format(current_process().name, msg))

'''
#cmd= "pkill -f '/home/nir/bin/reg_event_listener.py'"
cmd="ssh ndarmoni@bdsupportdb-02.siptalk.com pkill -f '/home/ndarmoni/bin/clicking.py'"
try:
    check_output(shlex.split(cmd))
except:
    pass

try:
    PORT = 32802
    sock = socket(AF_INET,SOCK_DGRAM)
    msg = "Hello UDP server"
    addr=('bdsupportdb-02.siptalk.com', PORT)

    r, w = Pipe(duplex=False)
    p = Process(target=use_pipe_to_send_cmd, args=(sock,r, addr))
    if(p):
        p.start()
    print ('{}'.format(lineno()), 'so far, so good')
    if(True):
        time.sleep(0.3)
        middle_worker = Thread(target=collect_middle_events, args=(w,))
        middle_worker.setDaemon(False)
        middle_worker.start()
        print ('{}'.format(lineno()), 'so far, so good')
        while True:
            time.sleep(3)
    else:
        cleanup()
        print ('{}'.format(lineno()), 'leaving now')
        print ("could not start reg_event_listener. Bye!!")
        sys.exit(-1)

except Exception as inst:
    print ('{}'.format(lineno()), 'dying')
    print (type(inst))
    print (inst.args)
    print (inst)
    #print (__file__, 'Oops')
    #if(db_writer):
    #    db_writer.kill()
