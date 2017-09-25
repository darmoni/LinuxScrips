#!/usr/bin/env python3
#ident $Id$ $Date$

from subprocess import run, check_output, CalledProcessError, call, Popen, PIPE
import sys, argparse, shlex

import signal
'''
def my_add_fn():
    if sys.version_info < (3,0,0):
        print ("SUM:%s"%sum(map(int,raw_input("Enter 2 numbers seperated by a space\n").split())))
    else:
        print ("SUM:%s"%sum(map(int,input("Enter 2 numbers seperated by a space\n").split())))
grep gtt- build*sh | awk -F":PACKAGE_NAME=" '/PACKAGE_NAME=/ {print $2 ":" $1;}' | sort |uniq

'''
def my_quit_fn():
  raise SystemExit

commands={
    'get_log_file_cmd':'',
    'run_the_build_cmd':''
}

def select_rpm():
    global rpm_builders
    menu={}
    i=0
    for gtt in sorted(rpm_builders):
        script=rpm_builders[gtt]
        menu.update({chr(ord('a')+i):[gtt,script]})
        i=i+1
    #print (menu)
    '''
    menu = {'1':("Run the build", run_the_build),
            '2':("Read the log file", fetch_log_file),
            '3':("Pull the script file", pull_build_file),
            '4':("Push the script file", push_build_file),
            '5':("Get latest CVS tags", get_latest_cvs_tags),
            '6':("Get last rpm name", get_rpm_name),
            '7':("Refresh Rpm Builds",populate_rpm_builders),
            '8':("Select rpm",select_rpm),
            'q':("Quit",my_quit_fn)
            }
    '''
    while True:
        print(30*'-',' '*6,'-'*30)
        options=menu.keys()
        for entry in sorted(options):
            print ("{}:     {:<30} {:30}".format(entry, menu[entry][0], menu[entry][1]))
        print(30*'-',' '*6,'-'*30)
        selection=input("Please Select:")
        try:
            _rpm=menu[selection][0]
            script=menu[selection][1]
            print("selected {} building by {} ".format(_rpm,script))
            if(0<=script.find("build_")):
                break
        except:
            invalid()

    return _rpm

def run_the_build():
    global commands
    run_the_build_cmd=commands['run_the_build_cmd']
    print(run_the_build_cmd);
    args = shlex.split(run_the_build_cmd)
    try:
        run(args)
        get_rpm_name()
    except:pass

def fetch_rpm_spec():
    global commands
    try:
        args = shlex.split(commands['get_rpm_spec_cmd'])
        run(args)
    except:pass

def get_rpm_name():
    global commands
    try:
        args = shlex.split(commands['get_rpm_name_cmd'])
        run(args)
    except:pass

def get_rpm_n_script_names():
    global commands
    try:
        get_rpm_n_script_names_cmd=commands['get_rpm_n_script_names_cmd']
        print(get_rpm_n_script_names_cmd)
        args = shlex.split(get_rpm_n_script_names_cmd)
        run(args)
    except:pass

def fetch_log_file():
    global commands
    get_log_file_cmd=commands['get_log_file_cmd']
    print(get_log_file_cmd)
    args = shlex.split(get_log_file_cmd)
    run(args)#.split('\n')

def push_build_file():
    global commands
    push_build_file_cmd=commands['push_build_file_cmd']
    print(push_build_file_cmd)
    args = shlex.split(push_build_file_cmd)
    run(args)#.split('\n')

def pull_build_file():
    global commands
    pull_build_file_cmd=commands['pull_build_file_cmd']
    args = shlex.split(pull_build_file_cmd)
    run(args)#.split('\n')

def get_latest_cvs_tags():
    global commands
    get_latest_cvs_tags_cmd=commands['get_latest_cvs_tags_cmd']
    print(get_latest_cvs_tags_cmd)
    args = shlex.split(get_latest_cvs_tags_cmd)
    run(args)#.split('\n')

def invalid():
  print ("INVALID CHOICE!")

rpm_builders={}

'''
rpm_builders={
    'gtt-db-qman':'build_db.sh',
    'gtt-fileloader':'build_voice_loader.sh'
    }
'''
build_folder={
    'pbxdev.xcastlabs.com':'/home/ndarmoni/build',
    'xdev64.xcastlabs.com':'/net/home/ndarmoni/w1/build',
}

def populate_rpm_builders():
    i=0;
    args = shlex.split(commands['get_rpm_n_script_names_cmd'])
    try:
        data=check_output(args, universal_newlines=True)
        for line in data.splitlines():
            #i=i+1
            [gtt,script] = line.split(":")
            rpm_builders[gtt]=script
    except:pass

def main(host, rpm):
    global commands,rpm_builders

    servers={
        'old':'xdev64.xcastlabs.com',
        'new':'pbxdev.xcastlabs.com'
            }
    host=servers[host.lower()]

    host_account="ndarmoni@{}".format(host)
    connection_part="ssh {}".format(host_account)
    commands['get_rpm_n_script_names_cmd']= "{} 'cd {} && source ./rpm_names.sh'".format(connection_part,build_folder[host])
    if(len(rpm) > 3):
        print("testing connection to build server {} and script for {}".format(host,rpm))
    else:
        populate_rpm_builders()
        rpm = select_rpm()


    #print(commands['get_rpm_n_script_names'])
    try:
        #populate_rpm_builders()
        build_rpm = rpm_builders[rpm]
        executable_path="{}/{}".format(build_folder[host],build_rpm)

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
        cmdline=p.stdin
        # running a build now

        commands['get_log_file_cmd']="{} 'cat {}.log'".format(connection_part,executable_path)
        commands['get_rpm_spec_cmd']="{} 'cd {}; cat {}.spec'".format(connection_part,build_folder[host],rpm)
        commands['run_the_build_cmd']="{} 'cd {}; {} > {}.log 2>&1'".format(connection_part,build_folder[host],executable_path,executable_path)
        commands['pull_build_file_cmd']="scp -p {}:{} {}".format(host_account,executable_path,build_rpm)
        commands['push_build_file_cmd']="scp -p {} {}:{} ".format(build_rpm, host_account,executable_path)
        commands['get_latest_cvs_tags_cmd']="{} 'cd {}; {} {}'".format(connection_part,build_folder[host],'./rpm_builds_newest_tags.sh',build_rpm)
        commands['get_rpm_name_cmd']="{} 'cd {}; ls -1tr {}*rpm | tail -1'".format(connection_part,build_folder[host],rpm)
        #cmdline.write("cat {}.log\n".format(executable_path))
    except Exception as inst:
        print(type(inst))
        print(inst.args)
        print(inst)
        print(__file__, 'Oops')
        raise SystemExit

    i=1
    menu = {'q':("Quit",my_quit_fn)}
    menu[str(i)]=("Run the build", run_the_build)
    i+=1;    menu[str(i)]=("Read the log file", fetch_log_file)
    i+=1;    menu[str(i)]=("Read the spec file", fetch_rpm_spec)
    i+=1;    menu[str(i)]=("Pull the script file", pull_build_file)
    i+=1;    menu[str(i)]=("Push the script file", push_build_file)
    i+=1;    menu[str(i)]=("Get latest CVS tags", get_latest_cvs_tags)
    i+=1;    menu[str(i)]=("Get last Rpm name", get_rpm_name)
    i+=1;    menu[str(i)]=("Refresh Rpm Builds",populate_rpm_builders)
    i+=1;    menu[str(i)]=("Select Rpm",select_rpm)

    while True:
        print(16*'-',' '*8,'-'*16)
        options=menu.keys()
        for entry in sorted(options):
            print (entry, menu[entry][0])

        selection=input("Please Select:")
        menu.get(selection,[None,invalid])[1]()

def parse_args():
    parser = argparse.ArgumentParser(
        description='Creating test rpm')
    parser.add_argument('--host', type=str, required=False, default='old',
                        help='builds hostname')
    parser.add_argument('--rpm', type=str, required=False, default='',
                        help='Rpm name to build')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, rpm=args.rpm)
