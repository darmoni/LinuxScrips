import shlex, subprocess, time, sys, getopt, inspect, csv
from time import sleep
from subprocess import call, Popen, check_output, PIPE
from nbstreamreader import NonBlockingStreamReader as NBSR
from decimal import *

class configure:
    def get_parameters(self,argv):


        callerframerecord = inspect.stack()[1]    # 0 represents this line
                                            # 1 represents line at caller
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)
        caller = info.filename
        command_line_elements = ['','',False,False]
        param_test_case_matrix={}
        test_case_matrix={}
        this_configuration=''

        try:
            with open('param_test_case_matrix.csv') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    param_test_case_matrix.update({row['test_case'].strip():row['name'].strip()})

                csvfile.close()
            print 'param_test_case_matrix ={\n',
            for key in sorted(param_test_case_matrix.keys()):
                print "\t'"+key+"':\t'"+param_test_case_matrix[key]+"',\n",
                '''
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
                '''
            print '\t}'

            with open('test_case_matrix.csv','rb') as csvfile:
                testreader = csv.reader(csvfile, dialect='excel')
                for row in testreader:
                    key = row[0]
                    counter =0
                    matrix=[]
                    for cell in row:
                        counter +=1
                        if counter < 2: continue
                        matrix.append(cell.strip())
                    test_case_matrix.update({key.strip():matrix})
                csvfile.close()
            '''
            test_case_matrix ={
                'qman_dev_local_logs':[ 'xdev64.xcastlabs.com', 'bairsip.xcastlabs.com', 'dev_bsTestQman.py', 'xdev64.xcastlabs.com', '/qman.log', '/home/nir/bin/qman_events.awk', 'False', '40', 'dev', 'qman' ],
                'qman_staging_log_server':[ 'stage1n1-la.siptalk.com', 'bairsip.xcastlabs.com', 'staging_bsTestQman.py', 'logserver3-la.siptalk.com', '/qman.log', '/home/nir/bin/qman_events.awk', 'True', '20', 'staging', 'qman' ],
                'qman_production_log_server':[ '', '', '', 'logserver3-la.siptalk.com', '/<Pbx_node_qman.log  file name>', '/home/nir/bin/qman_events.awk', 'True', '20', 'production', 'qman' ],
                'conf_staging':[ 'stage1n1-la.siptalk.com', 'bairsip.xcastlabs.com', 'staging_bsTestConf.py', '', '', '', 'False', '0', 'staging', 'conf' ],
                'qman_production_local_logs_log_only':[ 'tswitch3.siptalk.com', 'bairsip.xcastlabs.com', 'sleeper.sh 4', 'tswitch3.siptalk.com', '/qman.log', '', 'False', '0', 'production', 'qman' ],
                'qman_staging_local_logs':[ 'stage1n1-la.siptalk.com', 'bairsip.xcastlabs.com', 'staging_bsTestQman.py', 'stage1n1-la.siptalk.com', '/qman.log', '/home/nir/bin/qman_events.awk', 'False', '20', 'staging', 'qman' ],
                'qman_dev_local_logs_log_only':[ 'xdev64.xcastlabs.com', 'bairsip.xcastlabs.com', 'sleeper.sh 4', 'xdev64.xcastlabs.com', '/qman.log', '', 'False', '40', 'dev', 'qman' ],
                'conf_dev':[ 'xdev64.xcastlabs.com', 'bairsip.xcastlabs.com', 'dev_bsTestConf.py', '', '', '', 'False', '0', 'dev', 'conf' ],
                'qman_staging_log_server_log_only':[ 'stage1n1-la.siptalk.com', 'bairsip.xcastlabs.com', 'staging_bsTestQman.py', 'logserver3-la.siptalk.com', '/qman.log', '', 'True', '20', 'staging', 'qman' ],
                'qman_production_local_logs':[ 'tswitch3.siptalk.com', 'bairsip.xcastlabs.com', 'sleeper.sh 4', 'tswitch3.siptalk.com', '/qman.log', '/home/nir/bin/qman_events.awk', 'False', '20', 'production', 'qman' ],
                'qman_staging_local_logs_log_only':[ 'stage1n1-la.siptalk.com', 'bairsip.xcastlabs.com', 'staging_bsTestQman.py', 'stage1n1-la.siptalk.com', '/qman.log', '', 'False', '20', 'staging', 'qman' ],
                }
            '''
            print 'test_case_matrix ={\n',
            for key in sorted(test_case_matrix.keys()):
                matrix = test_case_matrix[key]
                limit = len(matrix)
                values =0
                end = "'"
                middle = "',"
                print "\t'"+key+"':[",
                for value in test_case_matrix[key]:
                    values +=1
                    print "'"+value+(end,middle)[values < limit],
                print '],'
            print '\t}'
            exit()
        except Exception as inst:
            print type(inst)
            print inst.args
            print inst
            print __file__, 'Oops'
            exit()

        return what_2do



def main(argv):
        what_2do = configure().get_parameters(argv)


if __name__ == "__main__":
       main(sys.argv[1:])

   