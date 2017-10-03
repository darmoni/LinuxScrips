#!/usr/bin/env python3
#ident $Id$ $Date$

#from subprocess import run, check_output, CalledProcessError, call, Popen, PIPE
import argparse

#import signal
from manage_rpm import manage_rpm
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

def chr_index(i,base='a'):
    return chr(ord(base)+i)

def main(host, rpm):
    manager=manage_rpm(host,rpm)
    i=0
    menu = {'q':(6*'* '+"Quit"+7*' *',my_quit_fn)}
    menu[chr_index(i)]=("Run the build", manager.run_the_build)
    i+=1;    menu[chr_index(i)]=("Read the log file", manager.fetch_log_file)
    i+=1;    menu[chr_index(i)]=("Read the spec file", manager.fetch_rpm_spec)
    i+=1;    menu[chr_index(i)]=("Pull the script file", manager.pull_build_file)
    i+=1;    menu[chr_index(i)]=("Push the script file", manager.push_build_file)
    i+=1;    menu[chr_index(i)]=("Get latest CVS tags", manager.get_latest_cvs_tags)
    i+=1;    menu[chr_index(i)]=("Get last Rpm name", manager.get_rpm_name)
    i+=1;    menu[chr_index(i)]=("Upload last Rpm to GitLab", manager.push_rpm_2gitlab)
    i+=1;    menu[chr_index(i)]=("Refresh Rpm Builds",manager.populate_rpm_builders)
    i+=1;    menu[chr_index(i)]=("Select Rpm",manager.select_rpm)

    while True:
        header="{: ^19}".format(manager.build_rpm)
        print("  {:-^33}".format(header))
        options=menu.keys()
        for entry in sorted(options):
            print("{: >3}: {:-^30}".format(entry, menu[entry][0]))

        selection=input("Please Select:")
        menu.get(selection,[None,manager.invalid])[1]()

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
