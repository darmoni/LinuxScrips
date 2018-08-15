#!/usr/bin/env python3
import pandas as pd

package_names2builders=pd.read_table('package_names2builders')
#print(package_names2builders.values)

builder2package_name={}
for lines in package_names2builders.values:
    #print(lines[0])
#exit(0)
    for line in lines:
        [gtt,builder]=line.split(' ')
        builder2package_name[builder]= gtt

#print (builder2package_name)

project_data_xls=pd.read_csv('~/Documents/RegistratorProjects.csv',sep="\t",header=0)
corrected_project_data_xls = ""
header = '\t'.join(project_data_xls.axes[1])

if not project_data_xls.empty:
    for row in project_data_xls.itertuples():
        (index, project,builder,package,tag) = row
        if not isinstance(package,str):
            package=builder2package_name[builder.strip()]
        #print((index, project,builder,package,tag))
        corrected_project_data_xls += "\t". join((project, builder, package, tag)) + "\n"

#print(corrected_project_data_xls)
with open('new_package_names2builders.csv','w') as new_project_data_xls:
    new_project_data_xls.write("{}\n{}".format(header,corrected_project_data_xls))
    new_project_data_xls.close()
