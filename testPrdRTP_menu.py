#!/usr/bin/env python

import argparse, sys
import shlex
from subprocess import call, Popen, check_call, check_output, PIPE, CalledProcessError
from weakref import WeakValueDictionary
import os
import signal

def sig_handler(sig, frame):
    print "got sig({})\n".format(sig)
    safe_exit(sig)

signal.signal(signal.SIGUSR1,sig_handler)
signal.signal(signal.SIGUSR2,sig_handler)
signal.signal(signal.SIGINT,sig_handler)
signal.signal(signal.SIGTERM,sig_handler)
signal.signal(signal.SIGHUP,sig_handler)

def safe_exit(level):
    # save stuff
    print("Exiting ...\n")
    exit(0)

class Counter:
    _instances = WeakValueDictionary()
    @property
    def Count(self):
        return len(self._instances)

    def __init__(self, name):
        self.name = name
        self._instances[id(self)] = self
        print 'created'

    def __del__(self):
        print 'deleted'
        if self.Count == 0:
            print 'Last Counter object deleted'
        else:
            print self.Count, 'Counter objects remaining'

g_chunk = None
g_agents_num = 0
def main(host, chunk, uname):
    global g_chunk
    global g_agents_num
    g_agents_num = 0
    g_chunk = chunk
    counters = []
    if('localhost' == host): ssh_cmd ='bash -c '
    else: ssh_cmd = "ssh " + uname + "@"+host
    mydir=os.path.dirname(__file__)

    def start_baresip():
        args = shlex.split(ssh_cmd + " 'ps -ef | grep -v grep | grep baresip | grep root'")
        #print (args)
        try:
            check_output(args)  # if service is not running, we will skip to execute except CalledProcessError

        except CalledProcessError:
            sudo = " sudo " if('localhost' != host) else ""
            args = shlex.split(ssh_cmd + sudo +" '/usr/local/bin/baresip'")
            p = Popen(args, stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False)
            if (p):
                counters.append(Counter(p))
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'

    def start_RTP_test():
        global g_chunk
        try:
            cmd = " '~/bin/test_RTPLoad.sh "+str(g_chunk) +" ' "
            args = shlex.split(ssh_cmd +cmd)
            print(args)
            print (check_output(args))
        except CalledProcessError:pass
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'

    def stop_RTP_test():
        global g_chunk
        try:
            cmd = " '~/bin/stoptest_RTPLoad.sh "+str(g_chunk) +" ' "
            args = shlex.split(ssh_cmd +cmd)
            print(args)
            print (check_output(args))
        except CalledProcessError:pass
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'

    def quit_baresip():
        global g_agents_num
        try:
            while len(counters) > 0 and len(Counter._instances) > 0:
                for id in counters:
                    id.name.stdin.write("q")
                    counters.remove(id)
                    break
            g_agents_num=0
            sudo = " sudo " if('localhost' != host) else ""
            args = shlex.split(ssh_cmd + sudo +" ~/bin/kill_baresip.sh")
            print (check_output(args))
        except CalledProcessError:pass
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'

    def count_agents():
        global g_agents_num
        if(0 == g_agents_num):
            cmd = ' ~/bin/countAgents.sh 2> /dev/null'
            args = shlex.split(ssh_cmd +cmd)
            res=check_output(args)
            if(len(res) > 0): g_agents_num=int(res)
        if (g_agents_num):
            print ("Number of Agents is {}\n".format(g_agents_num))

    def update_chunk():
        global g_chunk
        print ("current chunk = " + str(g_chunk) +  "\n")
        if sys.version_info < (3,0,0):
            _chunk = int(raw_input("Enter the new Chunk value\n"))
        else:
            _chunk = int(input("Enter the new Chunk value\n"))
        if (_chunk and 0 < _chunk):
            print ("current chunk = " + str(_chunk) +  "\n")
            g_chunk=_chunk
        else:
            print ("accepting positive numbers only\n")

    def my_quit_fn():
        try:
            if(len(counters) > 0):
                quit_baresip()
                #print (counters)
            raise SystemExit
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'

    def invalid():
      print ("INVALID CHOICE!")

    first = 0
    fmt = '{0:>3} => {1:<16}'
    while True:
        chunk_agents_report="[Chunk/Agents:{}/{}]".format(g_chunk,"???" if (0 == g_agents_num) else g_agents_num)
        if(0 == len(Counter._instances)): menu = {"1":("Start barsip on "+host, start_baresip)}
        else:
            menu = {} if (0 < g_agents_num) else {"1":("Count Agents (!!! only before calls are running !!!) ", count_agents)}
        menu.update({
                '2':("{} Run RTP Test calls".format(chunk_agents_report),start_RTP_test),
                '3':("{} Stop RTP Test".format(chunk_agents_report),stop_RTP_test),
                '4':("Quit baresip",quit_baresip),
                '5':("Chunk = {}".format(g_chunk) ,update_chunk),
                '6':("Exit",my_quit_fn)
                })
        options=menu.keys()
        for entry in sorted(options):
          print (fmt.format(entry, menu[entry][0]))

        if sys.version_info < (3,0,0):
            selection=raw_input("Please Select:")
        else:
            selection=input("Please Select:")
        menu.get(selection,[None,invalid])[1]()

def parse_args():
    parser = argparse.ArgumentParser(
        description='running RTP Testing using baresip')
    parser.add_argument('--host', type=str, required=False,
                        default='sbc11n2-la.siptalk.com',
                        help='hostname for RTP Testing')
    #parser.add_argument('--port', type=int, required=False, default=33000,
    #                    help='port of RTP Testing')
    parser.add_argument('--chunk', type=int, required=False, default=7,
                        help='Number of calls in a chunk')
    parser.add_argument('--uname', type=str, required=False, default='xcast',
                        help='User Name on the server')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    #dump(args)
    try:
        main(host=args.host, chunk=args.chunk, uname=args.uname)
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        print __file__, 'Oops'
