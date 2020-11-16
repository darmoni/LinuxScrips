#!/usr/bin/env python3


from subprocess import check_output
import shlex
from sys import stdin

core_modules = {}
hashes = {}
new_cores = []
processed = []
filter = 'pbxsm-production'

def read_processed(file):
	try:
		with open(file) as f:
			for aline in f.readlines():
				line = aline.strip()
				processed.append(line)
				#print("found in processed file ", processed)
	except Exception:
		print("problem with file {}".format(file))
		exit()
					
def core_parts(new_core, platform):
    pos = new_core.find(platform)

def read_cores(lines):
    for core in lines:
        if core.strip().find(filter) >= 0:
            if core.strip() not in processed:
                new_cores.append(core.strip())

def suggest_logs(hashes):
    existing_hashes = []
    cores = hashes.keys()
    for hash in cores:
        core_module = hashes[hash][0]
        #print("hash = '{}', module = '{}'".format(hash, core_module))

        flog_cmd = "ssh ndarmoni@logs-pbx-la.xcastlabs.net 'flog {}'".format(core_module)
        log_list = check_output(shlex.split(flog_cmd)).decode().splitlines()
        for log_name in log_list:
            if not ((log_name.find('ls -latr') > -1) or (log_name.find('errors.log') > -1)):
                for core_hash in cores:
                    if log_name.find(hash) > -1:
                        print(log_name)

read_processed('checked_cores_list.doc')
#print("found in processed list ", processed)

temp = stdin.read().splitlines()
read_cores (temp)

for p in processed:
	if len(p) > 2:
		print("Processed core: '{}'".format(p))
#print("found in new cores list ", new_cores)

for line in new_cores:
    print("New core: '{}'".format(line))
    line_parts = line.split("/")
    if len(line_parts) < 5:
        next
    name_parts = line_parts[4].split(".")
    for i in name_parts:
        if i.find(filter) >= 0:
            name = i
            parts = name.split('-')
            #print("parts are '{}'".format(parts))
            if 4 == len(parts):
                hash = parts[3]
                core_module = '-'.join( parts[0:4])
                #print("hash = '{}', core_module = '{}'".format(hash,core_module ))
                hashes.update({hash:[core_module]})

suggest_logs(hashes)
