#!/usr/bin/env python3
#ident $Id$ $Date$

from subprocess import run, check_output, CalledProcessError, call, Popen, PIPE
import sys, argparse, shlex
#from nbstreamreader import NonBlockingStreamReader as NBSR
import signal

def my_add_fn():
    if sys.version_info < (3,0,0):
        print ("SUM:%s"%sum(map(int,raw_input("Enter 2 numbers seperated by a space\n").split())))
    else:
        print ("SUM:%s"%sum(map(int,input("Enter 2 numbers seperated by a space\n").split())))

def my_quit_fn():
  raise SystemExit
  
def run_the_build():
    global run_the_build_cmd
    args = shlex.split(run_the_build_cmd)
    check_output(args)
    print("Done results should be ready on the server\n checkout {}.log on the server".format(executable_path))

def fetch_log_file():
    global get_log_file_cmd
    args = shlex.split(get_log_file_cmd)
    #res = 
    run(args)#.split('\n')
    #for line in res:
    #    print ("%r\n" % line)
    
def invalid():
  print ("INVALID CHOICE!")

rpm_builders={'gtt-fileloader':'build_voice_loader.sh'}
build_folder={'pbxdev.xcastlabs.com':'/home/ndarmoni/build'}
get_log_file_cmd=""
run_the_build_cmd=""
def main(host, rpm):
    global get_log_file_cmd
    global run_the_build_cmd
    
    connection_part="ssh ndarmoni@{}".format(host) 
    print("testing connection to build server {} and script for {}".format(host,rpm))
    build_rmp = rpm_builders[rpm]
    executable_path="{}/{}".format(build_folder[host],build_rmp)
    args = shlex.split("{} 'ls -l {}'".format(connection_part,executable_path))
    try:
        res=check_output(args)
    except CalledProcessError:
        print("Wrong/unknown rpm {}".format(rpm))
        raise SystemExit
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)
        print(__file__, 'Oops')
        raise SystemExit
    try:
        args=shlex.split(connection_part)
        p = Popen(args, stdin=PIPE, stdout=PIPE,stderr=PIPE, shell=False)
        #nbsr = NBSR(p.stdout)
        cmdline=p.stdin
        # running a build now
        get_log_file_cmd="{} 'cat {}.log'".format(connection_part,executable_path)
        run_the_build_cmd="{} 'cd {}; {} > {}.log 2>&1'".format(connection_part,build_folder[host],executable_path,executable_path)

        #cmdline.write("cat {}.log\n".format(executable_path))
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)
        print(__file__, 'Oops')
        raise SystemExit
        
    first = 0
    menu = {'1':("Run the build", run_the_build),
            '2':("Get the log file", fetch_log_file),
            '3':("Quit",my_quit_fn)
            }
    
    while True:
        options=menu.keys()
        for entry in sorted(options):
            print (entry, menu[entry][0])

        selection=input("Please Select:")
        menu.get(selection,[None,invalid])[1]()

def parse_args():
    parser = argparse.ArgumentParser(
        description='Creating test rpm')
    parser.add_argument('--host', type=str, required=False, default='pbxdev.xcastlabs.com',
                        help='builds hostname')
    parser.add_argument('--rpm', type=str, required=False, default='gtt-fileloader',
                        help='Rpm name to build')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, rpm=args.rpm)
