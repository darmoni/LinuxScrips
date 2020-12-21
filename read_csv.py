#!/usr/bin/env python

#Ident $Id$    $Date$

import pandas, argparse, os, sys

def parse_args():
	parser = argparse.ArgumentParser(
		description='read and prints csv file')
	parser.add_argument('--file', '-f', type=str, required=False,
					 help='path to csv file')
	return parser.parse_args()

def print_row(row):
	for item in row:
		print("{:<120}".format(item), end ='\t')
	print('')

if __name__ == '__main__':
	csv_file_path=''
	csv_file_path=''
	argc=len(sys.argv)
	if 1 == argc:
		sys.argv.append ('-h')
		#print(argc,sys.argv)
	if 2 == argc and os.path.isfile(sys.argv[1]):
		csv_file_path = sys.argv[1]
	elif argc > 2:
		try:
			args = parse_args()
			if args.file:
				csv_file_path = args.file
		except:
			exit(-1)
	elif 0 == len(csv_file_path):
		parse_args()
		print("Can't find csv file {}".format(csv_file_path))
		exit(-1)
	#print("--file={}".format(args.file))
	if os.path.isfile(csv_file_path):
		csv_file_path = csv_file_path
	else:
		print("Can't find csv file {}".format(csv_file_path))
		exit(-1)
	report=pandas.read_csv(csv_file_path)
	print(report.to_string())
	for row in report.itertuples(index=False):
		print_row(row)
