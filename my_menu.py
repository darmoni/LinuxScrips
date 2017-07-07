#!/usr/bin/env python3
import sys

def my_add_fn():
    if sys.version_info < (3,0,0):
        print ("SUM:%s"%sum(map(int,raw_input("Enter 2 numbers seperated by a space\n").split())))
    else:
        print ("SUM:%s"%sum(map(int,input("Enter 2 numbers seperated by a space\n").split())))

def my_quit_fn():
  raise SystemExit

def invalid():
  print ("INVALID CHOICE!")

'''
menu = {
  '1':"Add Student.",
  '2':"Delete Student.",
  '3':"Find Student",
  '4':"Exit"
  }
'''
first = 0
menu = {"1":("SUM", my_add_fn),
        '2':("Quit",my_quit_fn)
        }
for entry in sorted(menu.keys()):
    print ("{},{}".format(str(chr(first+ord('a')))[0],entry))
    first +=1

while True:
  options=menu.keys()
  for entry in sorted(options):
      print (entry, menu[entry][0])

  if sys.version_info < (3,0,0):
    selection=raw_input("Please Select:")
  else:
    selection=input("Please Select:")
  menu.get(selection,[None,invalid])[1]()
  '''
  if selection =='1':
      print ("add")
  elif selection == '2':
      print ("delete")
  elif selection == '3':
      print ("find")
  elif selection == '4':
      break
  else:
      print ("Unknown Option Selected!")
  '''
