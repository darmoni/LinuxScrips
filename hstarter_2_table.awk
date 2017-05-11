#!/usr/bin/awk -f

#select * from conf where "proc" = 'T3680'
#select * from conf where "subject" = 'CLOUD'
#select * from conf group by subject

BEGIN {
    syslog_delimiter ="]: [";
    syslog = 0
    counter =0;
    #this_second =systime();
    printf "measurement\ttime\tproc\tsubject\tinfo\n"
    #print this_second
    #exit(0)
}
{
    #print $0
    if((0 == counter) && (0==syslog)){
        syslog = index($0,syslog_delimiter);
        if (syslog > 0) {
            counter += 1
            #print "again?"
            $0 = substr($0, syslog+3);
        }

    }
    else if (syslog > 0) {
            $0 = substr($0, syslog+3);
    }
    #print counter, syslog, $0
    if( $0 ~ /\[.{6}\] .{15} .*$/) {
        $0 =$0;
    }
    timetsamp=$2;
    n = split($1,front,"[");
    #print "DEBUG",front[2]
    if(0 < n){
        n = split(front[2],values,"]");
        if(0 < n) { value = values[1]; }
    #    print "DEBUG",value
    }
    proc = value

    info = $3
    if (index($3,"[") == 1){
        subject = substr($3,2,index($3,"]")-2);
        #print "DEBUG", subject
        info = substr($3,index($3,"]")+1);
        i=4
    }
    else {
        i=4
        subject = "Master"
    }
    if( subject ~ /RTP-.+/ ) subject = "RTP"
    #inserter = "conf,proc=" proc ",subject=" subject
    #inserter = "logs,proc=" proc ",subject=" subject

    if( timetsamp ~ /([[:digit:]]{2}.){3}[[:digit:]]{6}/){
        for (; i <= NF; i++)
            info = info " " $i
        printf "%s\t%s\t%s\t%s\t%s\n", "conf", timetsamp,proc,subject,info
        #print inserter " info=\"" info "\"", timetsamp
    }
}
