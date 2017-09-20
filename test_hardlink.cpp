/*

cat /usr/include/asm-generic/errno-base.h /usr/include/asm-generic/errno.h | awk ' !/$^/' | awk '/#define/ {if("" != $3) print "errors[" $3 "]=\"" $0 "\";"}'
cat /usr/include/asm-generic/errno-base.h /usr/include/asm-generic/errno.h | awk ' !/$^/' | awk '/#define/ {if("" != $3) { literal=$2;code=$3;$1="";$2="";$3="";$4="";$(NF)="";print "errors[" code "]=\"" literal " " $0 "\";";}}' > errnos.txt
*/

#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string>
#include <map>
#include <iostream>

using namespace std;

int map_errors(map<int,string> & errs);
int main() {
    map<int,string> errs;
    map_errors(errs);
    string org(__FILE__);
    string temp("/tmp/_" + org);
    string error_text("");
    if(link (org.c_str(), temp.c_str())){
        int the_errno=errno;
        map<int,string>::iterator the_error_name=errs.find(the_errno);
        if(errs.end() != the_error_name) error_text.assign(the_error_name->second);

        cout << "link (" << org << "," << temp << ") failed with errno(" <<  the_errno << ")" << error_text << endl;

    }
}
int map_errors(map<int,string> & errors){
#include "errnos.txt"
}
