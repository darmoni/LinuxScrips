import shlex, subprocess, time, sys, getopt, inspect, csv
from time import sleep
from subprocess import call, Popen, check_output, PIPE
from nbstreamreader import UnexpectedEndOfStream, NonBlockingStreamReader as NBSR

def PrintFrame(index =2):
    callerframerecord = inspect.stack()[1]    # 0 represents this line
                                            # 1 represents line at caller
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    if 0 == index:
        print info.filename                       # __FILE__     -> Test.py
    elif 1 == index:
        print info.function                       # __FUNCTION__ -> Main
    elif 2 == index:
        print info.lineno                         # __LINE__     -> 13


class configure:
    def get_parameters(self,argv):
        command_line_elements = ['','','']
        param_test_case_matrix={}
        test_case_matrix={}
        '''test_case_matrix =  {
                'conf_dev':['xdev64.xcastlabs.com','bairsip.xcastlabs.com','dev_bsTestConf.py','','','',False,0,'dev','conf'],
                'qman_dev':['xdev64.xcastlabs.com','bairsip.xcastlabs.com','dev_bsTestQman.py','xdev64.xcastlabs.com','/qman.log','/home/nir/bin/qman_events.awk',False,40,'dev','qman'],
                'conf_staging':['stage1n1-la.siptalk.com','bairsip.xcastlabs.com','staging_bsTestConf.py','','','',False,0,'staging','conf'],
                'qman_staging_local_logs':['stage1n1-la.siptalk.com','bairsip.xcastlabs.com','staging_bsTestQman.py','stage1n1-la.siptalk.com','/qman.log','/home/nir/bin/qman_events.awk',False,20,'staging','qman'],
                'qman_staging_log_server':['stage1n1-la.siptalk.com','bairsip.xcastlabs.com','staging_bsTestQman.py','logserver3-la.siptalk.com','/qman.log','/home/nir/bin/qman_events.awk',True,20,'staging','qman'],
                'qman_production_local_logs':['tswitch3.siptalk.com','bairsip.xcastlabs.com','sleeper.sh 4','tswitch3.siptalk.com','/qman.log','',False,0,'production','qman'],
                'qman_production_log_server':['','','','logserver3-la.siptalk.com','/<Pbx_node_qman.log  file name>','/home/nir/bin/qman_events.awk',True,20,'production','qman'],
                }
        '''
        '''param_test_case_matrix ={
                '-s dev -t conf':           'conf_dev',
                '-s dev -t conf -l':        'conf_dev',
                '-s dev -t qman':           'qman_dev',
                '-s dev -t qman -l':        'qman_dev',
                '-s staging -t conf':       'conf_staging',
                '-s staging -t conf -l':    'conf_staging',
                '':                         'qman_staging_local_logs',  # default
                '-s staging -t qman':       'qman_staging_local_logs',
                '-s staging -t qman -l':    'qman_staging_log_server',
                '-s production -t qman':    'qman_production_local_logs',
                }
                   
        with open('param_test_case_matrix.csv','w') as csvfile:
            fieldnames = ['test_case', 'name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key in param_test_case_matrix:
                writer.writerow({'test_case':key, 'name':param_test_case_matrix[key]})
            csvfile.close()
        exit(0)  '''  


        with open('param_test_case_matrix.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                param_test_case_matrix.update({row['test_case'].strip():row['name'].strip()})
            
            csvfile.close()

        with open('test_case_matrix.csv','rb') as csvfile:
            testreader = csv.reader(csvfile, dialect='excel')
            for row in testreader:
                key = row[0]
                counter =0
                matrix=[]
                for cell in row:
                    counter +=1
                    if counter < 2: continue
                    matrix.append(cell)
                test_case_matrix.update({key:matrix})
            csvfile.close()

        try:
            opts, args = getopt.getopt(argv,"lhs:t:",["setup=","target="])
        except getopt.GetoptError:
            print __file__, ' -s <setup> -t <target>'
            exit(2)
        command_line_elements = ['staging','qman','']
        for opt, arg in opts:
            if opt == '-h':
                print __file__, ' -s <setup> -t <target>'
                print 'For Dev Testing:', __file__, '-s dev'
                print 'For Staging Testing:', __file__, '-s staging'
                print 'For Qman Testing:', __file__, '-t qman'
                print 'For Conference Testing:', __file__, '-t conf'
                exit()
            if opt == '-l':
                command_line_elements[2]='syslog'
            elif opt in ("-t", "--target"):
                command_line_elements[1]=arg.strip()
            elif opt in ("-s", "--setup"):
                command_line_elements[0]=arg.strip()

        this_test = ' '.join(['-s',command_line_elements[0],
                        '-t',command_line_elements[1],
                        ('','-l')['syslog' == command_line_elements[2]]])
        this_test_case = param_test_case_matrix.get(this_test.strip(),'qman_staging_local_logs')
        print __file__, "'"+this_test+"'\n",this_test_case
        return test_case_matrix[this_test_case]


class tester:
    def __init__(self, tester):
        self._test_obj = tester

    def test(self,user,testserver,command,sleep_time):
        return self._test_obj.test(user,testserver,command,sleep_time)

class logger:
    def __init__(self,server,path,setup,target,use_logserver,command, logserver = 'logserver3-la.siptalk.com'):
        #print __file__, server,path,setup,target,use_logserver,command
        self._server= server
        self._logserver= server
        self._path = path
        self._command = command
        self._setup = setup
        self._target = target
        self._use_logserver = use_logserver
        if 'dev' == self._setup:
            pass
        elif self._use_logserver: self._logserver = logserver
        if 'staging' == self._setup:
            if self._use_logserver:
                self._path += '/servers/'+self._server+'/'+time.strftime("%Y%m%d")
        self._logs_command = self._command[0]+self._path+self._command[1]
        #print __file__, self._logserver,self._path,self._setup,self._target,self._use_logserver,self._logs_command

    def which_server_to_monitor_logs_on(self):
        return (self._logserver,self._logs_command)


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
        self._we_log = False
        self._we_filter = False
        if(('' != self._logserver) and('' != self._log_command)):
            self._we_log = True

        if('' != filter_command):
            self._filter_command = filter_command
            self._we_filter = True

    def test(self,user,testserver,command,sleep_time):
        try:
            if(self._we_log):
                (logs,killme) = self.start_log(self._logserver)
                if(self._we_filter):
                    _filter = self.apply_filter()

                baresip_test.test(self,user,testserver,command,sleep_time)

                if(self._we_filter):
                    self.copy_results(logs,_filter)
                    print _filter.communicate()[0]
                    #del logs
                    killme.kill()
                else:
                    if(self._we_log):
                        self.read_results(logs)
                        killme.kill()

        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'
            print 'could not run test'
            exit(0)

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
            line =results.readline(0.3).strip()
            if(None == line):
                break
            print line
          except:
            break

    def copy_results(self,results, output):
        #print 'copy_results(results, output)\n'
        while True:
          try:
            line =results.readline(0.3)
            if(None == line):
                break
            output.stdin.write(line+"\n")
          except:
            break
