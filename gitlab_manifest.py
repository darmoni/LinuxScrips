#!/usr/bin/env python
'''
Example input:
Entering 'monitoring/EvService'
* master
../monitoring_EvService.git  67931e10a0753f58170f3336ceae8b79b56e3516

Entering 'monitoring/cfg'
* master
../monitoring_cfg.git  be49086ac5a9f7f4529d594ce52e80b049ee41b9
'''
import shlex
class my_manifest:
    def __init__(self, lines):
        self.folder=""
        self.valid=False
        self.project=""
        self.checkout=""
        self.lines=lines
    def eval(self):
        pass
    def get_record(self):
        pass

def read_manifest(lines):
    counter=0
    manifest_lines={}
    #print("counter = {}".format(counter))
    
    for line in lines:
        #print("counter = {}".format(counter))
        parts=shlex.split(line)
        if (len(parts) == 2):
            #print("line '{}'\n => parts: '{}','{}'\n".format(line,parts[0],parts[1]))
            counter +=1
            if ("Entering" == parts[0]):
                manifest_lines.update({"folder":parts[1]})
            elif ("*" == parts[0]):
                manifest_lines.update({"branch":parts[1]})
            elif (".git" == parts[0][-4:]):
                manifest_lines.update({"path":parts[0]})
                manifest_lines.update({"hash":parts[1]})
                #print(manifest_lines)
                print ("git clone {} {} && \n pushd {} && \n git checkout -B branch_{} && \n git checkout {} && \n popd\n".format(
                    manifest_lines["path"],
                    manifest_lines["folder"],
                    manifest_lines["folder"],
                    manifest_lines["branch"],
                    manifest_lines["hash"]
                    )
                )
            else: counter=0
        else:
            if(""== line and counter > 0):
                #print manifest_lines
                counter=0

from sys import stdin
temp = stdin.read().splitlines()
read_manifest (temp)
