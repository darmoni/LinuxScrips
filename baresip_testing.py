import shlex, subprocess, time, sys
from time import sleep
from subprocess import call, Popen, check_output, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR

class baresip_test:

    def test(self,user,testserver,command,sleep_time):
        #print 'baresip_test.test (',user,testserver,command,sleep_time, ')'
        HOST=user+"@"+testserver
        self._ssh = subprocess.Popen(["ssh", "%s" % HOST, command],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        error = self._ssh.stderr.readlines()                 #blocking call, wait until done
        if(error != []):
            print >>sys.stderr, "ERROR: %s" % error

        print  "Done", (time.strftime("%H:%M:%S")),
        if(0< sleep_time):
            print 'sleeping', sleep_time, 'seconds'
            sleep(sleep_time) # let all settle down
        else:
            print ''

class baresip_test_with_logs(baresip_test):

    def __init__(self,logserver,log_command,filter_command):
        self._logserver = logserver
        self._log_command = log_command
        self._log_user = 'xcast'

        if('' != filter_command):
            self._filter_command = filter_command
            self._we_filter = True

    def test(self,user,testserver,command,sleep_time):
        try:
            if(('' != self._logserver) and('' != self._log_command)):
                (logs,killme) = self.start_log(self._logserver)
                if(self._we_filter):
                    _filter = self.apply_filter()

                baresip_test.test(self,user,testserver,command,sleep_time)

                if(self._we_filter):
                    self.copy_results(logs,_filter)
                    print _filter.communicate()[0]
                else:
                    self.read_results(logs)
        except:
            print 'could not run test'
            exit(0)
        if(self._we_filter):
            try:
                killme.kill()
            except:
                print 'could not stop log process'

    def start_log(self,logserver):
        try:
            _text ='ssh '+self._log_user+'@'+self._logserver
            #print _text
            args = shlex.split(_text)
            _log_server = Popen(args,stdin=PIPE,stdout=PIPE,stderr=PIPE, shell=False)
            events= NBSR(_log_server.stdout)
            _log_server.stdin.write(self._log_command)
            return (events,_log_server)
        except:
            print 'could not connect to log server'
            exit(0)

    def apply_filter(self):
        try:
            #print 'apply_filter: ',self._filter_command
            args = shlex.split(self._filter_command)
            return Popen(args, stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False)
        except:
            print 'could not run filter',filter
            exit(0)

    def read_results(self,results):
        while True:
          try:
            line =results.readline()
            if(None == line):
                break
            print line
          except:
            break

    def copy_results(self,results, output):
        #print 'copy_results(results, output)\n'
        while True:
          try:
            line =results.readline()
            if(None == line):
                del results
                break
            output.stdin.write(line+"\n")
          except:
            break
