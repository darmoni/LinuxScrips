#!/usr/bin/awk -f

#15:36:33.619670|position_in_queue()

BEGIN {
    syslog_delimiter ="]: [";
    syslog = 0
    counter =0;
    name="qman"
    printf "measurement\ttime\tproc\tsubject\tinfo\n"
}
{
    if((0 == counter) && (0==syslog)){
        syslog = index($0,syslog_delimiter);
        if (syslog > 0) {
            counter += 1
            $0 = substr($0, syslog+3);
        }

    }
    else if (syslog > 0) {
            $0 = substr($0, syslog+3);
    }
    gsub("\t"," ",$0);
    if( $0 ~ /^([[:digit:]]{2}.){3}[[:digit:]]{6}/) {
        $0 =$0;
        pipe=index($0,"|")
        timetsamp=substr($0, 0,pipe-1);
        info = substr($0,pipe+1)
        subject = "Master"
        if(( timetsamp ~ /([[:digit:]]{2}.){3}[[:digit:]]{6}/ ) && (length(info) > 0)){
            printf "%s\t%s\t%s\t%s\t%s\n", name,timetsamp,name,subject,info
        }
    }
}
