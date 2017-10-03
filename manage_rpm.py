#!/usr/bin/env python3
#ident $Id$Date$

from subprocess import run, check_output, CalledProcessError, call, Popen, PIPE
import sys, argparse, shlex

import signal

class manage_rpm:
    def __init__(self, _host, _rpm):
        self.host=_host
        self.rpm =_rpm
        self.rpm_builders={}
        self.commands={}
        self.servers={
            'old':'xdev64.xcastlabs.com',
            'new':'pbxdev.xcastlabs.com'
            }
        self.build_folder={
            'pbxdev.xcastlabs.com':'/home/ndarmoni/build',
            'xdev64.xcastlabs.com':'/net/home/ndarmoni/w1/build'
        }
        self.set_commands()

    def invalid(self):
        print ("\n{:*>30}\n".format("INVALID CHOICE!"))

    def select_rpm(self):
        menu={}
        i=0
        for gtt in sorted(self.rpm_builders):
            script=self.rpm_builders[gtt]
            menu.update({chr(ord('a')+i):[gtt,script]})
            i=i+1

        while True:
            print(30*'-',' '*6,'-'*30)
            options=menu.keys()
            for entry in sorted(options):
                print ("{}:     {:-<30} {:30}".format(entry, menu[entry][0], menu[entry][1]))
            print(30*'-',' '*6,'-'*30)
            selection=input("Please Select:")
            try:
                rpm=menu[selection][0]
                script=menu[selection][1]
                print("selected {} building by {} ".format(rpm,script))
                if(0<=script.find("build_")):
                    break
            except:
                self.invalid()
        self.rpm=rpm
        self.set_commands()
        return self.rpm

    def push_rpm_2gitlab(self):
        print("in push_rpm_2gitlab")
        try:
            new_rpm=self.get_rpm_name()
            push_rpm_2gitlab_cmd=self.mv_rpm_2rpm_pbx_cmd.format(new_rpm)
            #print(push_rpm_2gitlab_cmd)
            push_rpm_2gitlab_cmd=push_rpm_2gitlab_cmd + " && " + self.push_rpm_2gitlab_cmd.format(new_rpm,"Adding {} for testing".format(new_rpm))
            #print(push_rpm_2gitlab_cmd)
            push_rpm_2gitlab_cmd="{} '{}' ".format(self.connection_part,push_rpm_2gitlab_cmd)
            #print(push_rpm_2gitlab_cmd)
            args = shlex.split(push_rpm_2gitlab_cmd)
            #print(push_rpm_2gitlab_cmd)
            run(args)
        except:throw()

    def run_the_build(self):
        run_the_build_cmd=self.commands['run_the_build_cmd']
        print(run_the_build_cmd);
        args = shlex.split(run_the_build_cmd)
        try:
            run(args)
        except:pass

    def fetch_rpm_spec(self):
        try:
            args = shlex.split(self.commands['get_rpm_spec_cmd'])
            run(args)
        except:pass

    def get_rpm_name(self):
        try:
            args = shlex.split(self.commands['get_rpm_name_cmd'])
            new_rpm=check_output(args, universal_newlines=True).strip()
            print (new_rpm)
            return new_rpm
        except:pass

    def get_rpm_and_script_names(self):
        try:
            get_rpm_n_script_names_cmd=self.commands['get_rpm_and_script_names_cmd']
            print(get_rpm_n_script_names_cmd)
            args = shlex.split(get_rpm_n_script_names_cmd)
            run(args)
        except:pass

    def fetch_log_file(self):
        get_log_file_cmd=self.commands['get_log_file_cmd']
        print(get_log_file_cmd)
        args = shlex.split(get_log_file_cmd)
        run(args)#.split('\n')

    def push_build_file(self):
        push_build_file_cmd=self.commands['push_build_file_cmd']
        print(push_build_file_cmd)
        args = shlex.split(push_build_file_cmd)
        run(args)#.split('\n')

    def pull_build_file(self):
        pull_build_file_cmd=self.commands['pull_build_file_cmd']
        args = shlex.split(pull_build_file_cmd)
        run(args)#.split('\n')

    def get_latest_cvs_tags(self):
        get_latest_cvs_tags_cmd=self.commands['get_latest_cvs_tags_cmd']
        print(get_latest_cvs_tags_cmd)
        args = shlex.split(get_latest_cvs_tags_cmd)
        run(args)#.split('\n')

    def populate_rpm_builders(self):
        if (self.commands.get('get_rpm_and_script_names_cmd')):
            try:
                i=0;
                get_rpm_n_script_names_cmd=self.commands['get_rpm_and_script_names_cmd']
                print(get_rpm_n_script_names_cmd)
                args = shlex.split(get_rpm_n_script_names_cmd)

                data=check_output(args, universal_newlines=True)
                for line in data.splitlines():
                    #i=i+1
                    [gtt,script] = line.split(":")
                    self.rpm_builders[gtt]=script
            except:throw

    def set_commands(self):
        host=self.servers[self.host.lower()]
        rpm=self.rpm
        host_account="ndarmoni@{}".format(host)
        connection_part="ssh {}".format(host_account)
        self.connection_part=connection_part
        self.commands['get_rpm_and_script_names_cmd']= "{} 'cd {} && source ./rpm_names.sh'".format(connection_part,self.build_folder[host])
        if((len(rpm) > 3) and (rpm in self.rpm_builders) ):
            print("testing connection to build server {} and script for {}".format(host,rpm))
        else:
            self.populate_rpm_builders()
            if(len(rpm) > 3):
                self.build_rpm = self.rpm_builders[rpm]
            else:
                self.select_rpm()
                return
        try:
            #populate_rpm_builders()
            self.build_rpm = self.rpm_builders[rpm]
            executable_path="{}/{}".format(self.build_folder[host],self.build_rpm)

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
            commands={}
            commands['get_log_file_cmd']="{} 'cat {}.log'".format(connection_part,executable_path)
            commands['get_rpm_spec_cmd']="{} 'cd {} && cat {}.spec'".format(connection_part,self.build_folder[host],rpm)
            commands['run_the_build_cmd']="{} 'cd {} && {} > {}.log 2>&1'".format(connection_part,self.build_folder[host],executable_path,executable_path)
            commands['pull_build_file_cmd']="scp -p {}:{} {}".format(host_account,executable_path,self.build_rpm)
            commands['push_build_file_cmd']="scp -p {} {}:{} ".format(self.build_rpm, host_account,executable_path)
            commands['get_latest_cvs_tags_cmd']="{} 'cd {} && {} {}'".format(connection_part,self.build_folder[host],'./rpm_builds_newest_tags.sh',self.build_rpm)
            commands['get_rpm_name_cmd']="{} 'cd {} && ls -1tr {}*rpm | tail -1'".format(connection_part,self.build_folder[host],rpm)
            self.mv_rpm_2rpm_pbx_cmd="cd {} && cp -p {} ../rpms/rpm.pbx/".format( self.build_folder[host],"{}")
            self.push_rpm_2gitlab_cmd="cd {}/../rpms/rpm.pbx/ && git add {} && git commit -m \"{}\" && git push -u origin uploader".format(self.build_folder[host],"{}","{}")
            #cmdline.write("cat {}.log\n".format(executable_path))
            self.commands = commands
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print(__file__, 'Oops')
            raise SystemExit
