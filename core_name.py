#!/usr/bin/env python3

from subprocess import check_output
import shlex
from sys import stdin
import glob#, pandas as pd

core_modules = {}
processed_cores_notes = {}
hashes = {}
new_cores = {}
processed = []
filter = 'pbxsm-production'

def read_processed(file):
	try:
		with open(file) as f:
			for aline in f.readlines():
				line = aline.strip()
				processed.append(line)
	except Exception:
		print("problem with file {}".format(file))
		exit()

'''
def read_processed_cores(file):
	matrix = file
	matrix_data = pd.read_csv(matrix)
	if not matrix_data.empty:
			for (_, core, comment) in matrix_data.itertuples():
				processed.append("{},{}".format(core.strip(),comment.strip()))
				#print("DEBUG {:10},{}".format(comment, core))
'''
def core_parts(new_core, platform):
    pos = new_core.find(platform)

def read_cores(lines):
	for acore in lines:
		core = acore.strip()
		if core.find(filter) >= 0:
			basename = core.split()[-1:][0]
			#print(core, basename)
			if core not in processed:
				new_cores.update({basename: core})

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
                        print("[{}] {}".format( hash, log_name))

read_processed('checked_cores_list.doc')
#for p in processed:
#	print("DEBUG in after read_processed, line in processed = '{}'")


#read_processed_cores('checked_cores_list.doc')
#for p in processed:
#	print("DEBUG in after read_processed_cores, line in processed = '{}'".format(p))
#print("found in processed list ", processed)

temp = stdin.read().splitlines()
read_cores (temp)

for p in processed:
	if len(p) > 2:
		(path, note) = p.split(',')
		if path.find(filter) >= 0:
			processed_cores_notes.update({path.strip(): "{}".format(note.strip())})
		#print("Processed core: {:2} '{}','{}'".format(process_counter, note, path))
#print("found in new cores list ", new_cores)

for key in new_cores.keys():
	line = new_cores[key]
	if line not in processed_cores_notes.keys():
		print("New core: '{}'".format(line))
		line_parts = line.split("/")
		if len(line_parts) < 5:
			next
		name_parts = line_parts[:-1][0].split(".")
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

process_counter = 0
for path in processed_cores_notes.keys():
	process_counter += 1
	print("Processed core: {:>3} '{:10}','{}'".format(process_counter, processed_cores_notes[path] , path))
suggest_logs(hashes)
