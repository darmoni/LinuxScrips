#!/usr/bin/env python3

import glob, pandas as pd

max_cols = None
max_rows = None
def print_my_csv():
	data_files = glob.glob("./*.csv")
	for matrix in data_files:
		matrix_data = pd.read_csv(matrix)
		test_str = matrix_data.columns[0]
		if test_str.find('\t') >= -1:
			matrix_data = pd.read_table(matrix)
		print("{}\n{}".format(matrix, matrix_data))

def print_my_checked_cores():
	matrix = 'checked_cores_list.doc'
	matrix_data = pd.read_csv(matrix)
	if not matrix_data.empty:
		print(matrix_data.to_string(header = ['The Path','The Comment']))
		#for i, row in matrix_data.iterrows():
		for row in matrix_data.itertuples(name='Processed_core'):
		#for (_, core, comment) in matrix_data.itertuples(name='Processed_core'):
			print(row)
			#(core, comment) = row
			#print("Processed core: {:10} {}".format(comment, core))
			#title = row.title
			#print("Title = '{}".format(title))

print_my_checked_cores()
import pandas as pd
