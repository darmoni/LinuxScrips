#!/usr/bin/env python3

# $Id$ $Date$

'''
Makefile command:
make all -f protobufs.mak
'''
from threading import Thread
from queue import Empty, Queue
import signal, time

import ACD_pb2, sys, os
from ACD_pb2 import RqstAgentStatus, RspAgentStatus, DynamicQueueRecord, AccID, StringValue

def handle_event(q):
    if not q:
        print("There is no Queue")
        safe_exit()
    print("VERBOSE printer")
    while True:
        record=q.get()
        print(record[0])
        if(record):
            if 'agent_id_request' == record[0]:
                status_request=RqstAgentStatus()
                status_request.ParseFromString(record[1])
                if status_request:
                    #print(status_request.GetTypeName())
                    print(GetAgentStatus(status_request.id).value.value)
            else:
                print(record[0])
            q.task_done()

def main(argv):
    print(argv)
    #exit(0)
    events_q = Queue(maxsize=0)
    printer = Thread(target=handle_event, args=(events_q,))
    printer.setDaemon(True)
    printer.start()

    queue = DynamicQueueRecord()
    if len(argv) > 0:
        try:
            f = open(argv[0], "rb")
            #queue.ParseFromIstream(f)
            queue.ParseFromString(f.read())
            f.close()
            print("Read {} Calls".format(len(queue._mapped_iors)))
            ListCalls(queue)
        except IOError:
            print (argv[0] + ": Could not open file.  Creating a new one.")

    ask_agent_status(25529,events_q)
    time.sleep(0.3)

def read_req_from_file():
    agent_id_request_fname='agent_id_request'
    if os.path.isfile(agent_id_request_fname):
        try:
            status_request=RqstAgentStatus()
            f = open(agent_id_request_fname, "rb")
            #status_request.ParseFromIstream(f)
            status_request.ParseFromString(f.read())
            f.close()
            if status_request:
                print(GetAgentStatus(status_request.id).value.value)
        except:
            pass

def ask_agent_status(id,events_q):
    status_request=RqstAgentStatus()
    status_request.id.id=id
    data=['agent_id_request',status_request.SerializeToString()]
    #print(data)
    events_q.put(data)
    #f = open('agent_id_request_', "wb")
    #f.write(data[1])
    #f.close()
    #exit(0)

def GetAgentStatus(agent_id):
    answer = RspAgentStatus()
    q="SELECT call_status FROM agent_data WHERE account_id = {};".format(agent_id.id)
    answer.value.value = q
    return (answer)

# Iterates though all people in the AddressBook and prints info about them.
def ListCalls(DynamicQueueRecord):
    for call in DynamicQueueRecord._mapped_iors:
#        print("call ={}\tqueue_record ={}\ttemp_queue_id ={}\tagent_account_id ={}\tflag ={}\ttime ={}\tname ={}\tnumber ={}\tcall_id ={}"
#              .format(call.call,call.queue_record,call.temp_queue_id,call.agent_account_id,call.flag,call._time,call.name,call.number,call.cid))
        print("call ={}".format(call.call), end ='\t')
        print("queue_record ={}".format(call.queue_record), end ='\t')
        print("temp_queue_id ={}".format(call.temp_queue_id), end ='\t')
        print("agent_account_id ={}".format(call.agent_account_id), end ='\t')
        print("flag ={}".format(call.flag), end ='\t')
        print("time ={}".format(call._time), end ='\t')
        print("name ={}".format(call.name), end ='\t')
        print("number ={}".format(call.number), end ='\t')
        print("call_id ={}".format(call.cid))

if __name__ == '__main__':
    main(sys.argv[1:])
