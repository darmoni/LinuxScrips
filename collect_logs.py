import shlex, subprocess, socket, os, time, signal, sys, datetime
from time import sleep
from subprocess import call, Popen, check_output, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR

class log_collector:
    def __init__(self, log ='db', log_server = 'xdev64.xcastlabs.com', syslog=False, execute_cmd = None):
        self._server=log_server
        self._log=log
        self._p = -1
        self._execute_cmd = execute_cmd
        if syslog:self._params =self.add_syslog_log(self._log,self._server)
        else :self._params =self.add_local_log(self._log,self._server)

    def __del__(self):
        if(0 < self._p): self._p.kill()

    def collect_log(self):
        (remote_log_srv_cmd,log_srv_cmd,parser,influx_writer) = self._params
        self.setup()
        if(-1 != self._p):
            self._p.stdin.write(log_srv_cmd)
        return self._p

    def add_local_log(self, log, log_server):

        influx_writer='/home/nir/bin/table_2_db.py'
        logname = "~/logs/{}.log".format(log)
        parser = 'awk -v name={} -f /home/nir/bin/log_2_table.awk'.format(log)
        if('db' == log):
             parser = '/home/nir/bin/db_2_table.awk'
        elif('qman' == log):
            parser = '/home/nir/bin/qman_2_table.awk'
        elif('conf' == log):
            logname = "~/logs/{}.log".format('hstarter')

        remote_log_srv_cmd ="ssh xcast@{}".format(log_server)
        log_srv_cmd ="tail -0f {}\n".format(logname)
        return remote_log_srv_cmd,log_srv_cmd,parser,influx_writer

    def add_syslog_log(self, log, log_source, log_server = "logserver3-la.siptalk.com"):

        influx_writer='/home/nir/bin/table_2_db.py'
        logname = "~/logs/servers/{}/{}/{}.log".format(log_source, datetime.datetime.today().strftime("%Y%m%d"),log)
        parser = 'awk -v name={} -f /home/nir/bin/log_2_table.awk'.format(log)
        if('db' == log):
             parser = '/home/nir/bin/db_2_table.awk'
        elif('qman' == log):
            parser = '/home/nir/bin/qman_2_table.awk'
        elif('conf' == log):
            logname = "~/logs/servers/{}/{}/{}.log".format(log_source, datetime.datetime.today().strftime("%Y%m%d"),'hstarter')

        remote_log_srv_cmd ="ssh xcast@{}".format(log_server)
        log_srv_cmd ="tail -0f {}\n".format(logname)
        return remote_log_srv_cmd,log_srv_cmd,parser,influx_writer

    def setup(self):
        (remote_log_srv_cmd,log_srv_cmd,parser,influx_writer) = self._params
        print "{} '{}' | {} | {}".format(remote_log_srv_cmd,log_srv_cmd,parser,influx_writer)
        #return
        args = shlex.split(remote_log_srv_cmd)
        try:
            p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE,shell=False, bufsize=0)
            awk = Popen(shlex.split(parser), stdin=p.stdout, stdout=PIPE,stderr=PIPE, shell=False, bufsize=0)
            p.stdout.close()    # Allow awk to receive a SIGPIPE if p exits.
            uploader = Popen(shlex.split(influx_writer), stdin=awk.stdout, stdout=PIPE,stderr=PIPE, shell=False, bufsize=0)
            awk.stdout.close()  # Allow uploader to receive a SIGPIPE if awk exits.
            print "DEBUG. Made it through setup of log parsing"
            self._p = p
        except Exception as inst:
            self._p = -1
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'
            p.kill()

    def run(self, execute_cmd='/home/nir/bin/staging_qman_2_influxdb.sh'):
        (remote_log_srv_cmd,log_srv_cmd,parser,influx_writer) = self._params
        self.setup()
        try:
            if(-1 == self._p): return
            p = self._p
            p.stdin.write(log_srv_cmd)                      # start logging
            print "DEBUG. Strated logging. will run '%s' now..." % execute_cmd
            print check_output(shlex.split(execute_cmd))    # blocking call, wait until done
            #error = p.stderr.readlines()                   # blocking call, wait until done
            #time.sleep(30)
            self._p = -1
            p.kill()
        except Exception as inst:
            self._p = -1
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'
            p.kill()

    def execute(self):
        if (self._execute_cmd): self.run(self._execute_cmd)
        else : self.collect_log()
        if(-1 == self._p): return
        self._p.kill()
