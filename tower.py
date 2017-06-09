#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from anoii import towers

def main(argv):

    number = "Number = "
    word ="המספר =".decode('UTF-8')
    rtl_number =''.join(reversed(word))

    if(len(argv)):
        _number = int(argv[0])
        if(1 > _number):
            print "\t\t\t",_number , "is invalid! Use posistive numbers only"
            sys.exit(0)
    else:
        _number = 1

    rtl = (_number%2)
    tower = towers(rtl)
    print "\n"
    if(rtl):
        print "\t\t\t",_number, rtl_number
    else:
        print number,_number
    tower.towers(_number,0,2,1)

if __name__ == "__main__":
    main(sys.argv[1:])
