#!/usr/bin/env python

import argparse, sys
import shlex
from subprocess import call, Popen, check_call, check_output, PIPE, CalledProcessError
from weakref import WeakValueDictionary
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

def main(host, port, chunk):
    counters = []
    def start_baresip():
        args = shlex.split("ssh xcast@"+host+ " 'ps -ef | grep -v grep | grep baresip'")
        print (args)
        try:
            print (check_output(args))
        except CalledProcessError:
            args = shlex.split("ssh xcast@"+host+ " 'sudo /usr/local/bin/baresip'")
            counters.append(Counter(Popen(args, stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False)))
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'

    def start_RPM_test():
        args = shlex.split("ssh xcast@"+host+ " ~/bin/test_RPMLoad.sh "+str(chunk))
        print (check_output(args))

    def stop_RPM_test():
        args = shlex.split("ssh xcast@"+host+ " ~/bin/stoptest_RPMLoad.sh "+str(chunk))
        try:
            print (check_output(args))
        except CalledProcessError:pass
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'

    def quit_baresip():
        args = shlex.split("ssh xcast@"+host+ " ~/bin/kill_baresip.sh")
        try:
            print (check_output(args))
        except CalledProcessError:pass
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'

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
    menu = {"1":("Start barsip:", start_baresip),
            '2':("Run RPM",start_RPM_test),
            '3':("Stop RPMs",stop_RPM_test),
            '4':("Quit baresip",quit_baresip),
            '5':("Exit",my_quit_fn)
            }
    for entry in sorted(menu.keys()):
        print ("{},{}".format(str(chr(first+ord('a')))[0],entry))
        first +=1

    while True:
      options=menu.keys()
      for entry in sorted(options):
          print (entry, menu[entry][0])

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
    parser.add_argument('--port', type=int, required=False, default=33000,
                        help='port of RTP Testing')
    parser.add_argument('--chunk', type=int, required=False, default=56,
                        help='Number of calls in a chunk')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    #dump(args)
    try:
        main(host=args.host, port=args.port, chunk=args.chunk)
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        print __file__, 'Oops'
