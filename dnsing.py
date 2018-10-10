#!/usr/bin/env python3

from nbstreamreader import NonBlockingStreamReader as NBSR
from threading import Thread
from queue import Empty, Queue
import signal, time
import os.path
# Import smtplib for the actual sending function
import shlex, sys

from frameInfo import PrintFrame
from subprocess import check_output, Popen, PIPE, TimeoutExpired
from socket import socket, AF_INET, SOCK_DGRAM
MAX_SIZE=4096

resources=[]
workers=[]

def safe_exit():
    counter=1
    for r in resources:
        print ("deleting {}\n".format(counter))
        del r
        counter +=1
    exit(0)

def sig_handler(sig, frame):
    print ("got sig(%d)\n" % sig)
    safe_exit()

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

def my_printer(q):
    if not q:
        print("There is no Queue")
        safe_exit()
    print("VERBOSE printer")
    while True:
        record=q.get()
        if(record):
            print(record)
            q.task_done()

def read_from_pbx(sock, events, p):
    while True:
        data, addr = sock.recvfrom(MAX_SIZE)
        if(data):
            print("read_from_pbx data = {}".format(data))
            #events = Queue(maxsize=0)
            worker = Thread(target=read_from_adns, args=(data, sock, addr, p, events))
            worker.setDaemon(False)
            worker.start()
            workers.append(worker)
            resources.append(worker)
            p.stdin.write(data)
    print("read_from_pbx Oops, I have died")


def read_from_adns(data, sock, addr, p, events):
    while True:
        response = events.readline(1.2)
        if response:
            print("response = ",response.decode())
            sock.sendto(response,addr)
        if not response:
            return

def main():
    adns_output_q = Queue(maxsize=0)
    printer = Thread(target=my_printer, args=(adns_output_q,))
    printer.setDaemon(True)
    printer.start()
    resources.append(printer)
    try:
        sock = socket(AF_INET,SOCK_DGRAM)
        sock.bind(('',32803))

        adns_exec="/home/nir/bin/adnshost"
        cmd="{} -a --config '{} options rotate' -f".format(adns_exec, "{}" )
        print(cmd)
        servers = ["10.10.10.226","8.8.8.8"]
        config_servers = []
        for server in servers:
            config = 'nameserver {}'.format(server)
            config_servers.append(config)
        print(config_servers)
        adns_cmd=cmd.format(' '.join(config_servers))
        print(adns_cmd)
        args = shlex.split(adns_cmd)
        print (args)
        p = Popen(args, stdin=PIPE, stdout=PIPE, stderr = PIPE, shell=False, bufsize=0)
        events = NBSR(p.stdout)
        p.stdin.write("www.thinkcompute.com\n".encode('utf-8'))

        worker = Thread(target=read_from_pbx, args=(sock, events, p))
        worker.setDaemon(True)
        worker.start()
        workers.append(worker)
        resources.append(worker)
    except Exception as inst:
            print (type(inst))
            print (inst.args)
            print (inst)
            print (__file__, 'Oops')
            safe_exit()
    while True:
        time.sleep(2)

    safe_exit()

if __name__ == '__main__':
    main()
