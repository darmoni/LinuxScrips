#!/usr/bin/env python
'''
Example input:
Entering 'monitoring/EvService'
* master
../monitoring_EvService.git  67931e10a0753f58170f3336ceae8b79b56e3516

Entering 'monitoring/cfg'
* master
../monitoring_cfg.git  be49086ac5a9f7f4529d594ce52e80b049ee41b9

Entering 'Registrator/db'
* (detached from 5fa04af)
../db.git  5fa04af84585cfa4ee4247ad14fbb888a9b932c3

'''
import shlex
class my_manifest:
    def __init__(self, lines):
        self.set_lines(lines)
        #print("lines counter = {}".format(len(self.lines)))
    def set_lines(self,lines):
        self.valid=False
        self.folder=""
        self.branch=""
        self.path=""
        self.hash=""
        self.lines=lines
    def eval(self):
        for line in self.lines:
            parts=shlex.split(line)
            if (len(parts) == 2):
                #print("line '{}'\n => parts: '{}','{}'\n".format(line,parts[0],parts[1]))
                if ("Entering" == parts[0]):
                    self.folder=parts[1]
                elif ("*" == parts[0]):
                    self.branch=parts[1]
                    #self.branch='master'
                elif (".git" == parts[0][-4:]):
                    self.path=parts[0]
                    self.hash=parts[1]
                    if(4==len(self.lines)
                            and len(self.folder)>0
                            and len(self.branch)>0
                            and len(self.path)>0
                            and len(self.hash)>0):
                        self.valid=True
                        return self.valid
        return self.valid
    def get_record(self):
        return ("git clone {} {} && \n pushd {} && \n git checkout {} && \n git checkout -B {} && \n popd\n".format(
            self.path,self.folder,self.folder,self.hash,self.branch)
        )

def read_manifest(lines):
    counter=0
    #print("counter = {}".format(counter))
    manifest = my_manifest(lines[0:1]) # dummy starter
    for i in range(len(lines)/4):
        manifest.set_lines(lines[(i*4):(i*4+4)])
        #i+=1
        if (manifest.eval()):
            print (manifest.get_record())

from sys import stdin
temp = stdin.read().splitlines()
read_manifest (temp)
