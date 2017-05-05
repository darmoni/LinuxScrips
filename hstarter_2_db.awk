#!/usr/bin/awk -f

#select * from conf where "proc" = 'T3680'
#select * from conf where "subject" = 'CLOUD'
#select * from conf group by subject

BEGIN {
    counter =0;
    this_second =systime();
    printf "measurement\ttime\tproc\tsubject\tinfo\n"
    #print this_second
    #exit(0)
}
{
    if( $0 ~ /\[.{6}\] .{15} .*$/) {
        $0 =$0;
    }
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
    inserter = "conf,proc=" proc ",subject=" subject
    #inserter = "logs,proc=" proc ",subject=" subject

    if( $2 ~ /([[:digit:]]{2}.){3}[[:digit:]]{6}/){
        for (; i <= NF; i++)
            info = info " " $i
        printf "%s\t\t%s\t%s\t%s\t%s\n", "conf", $2,proc,subject,info
        #print inserter " info=\"" info "\"", $2
    }
}
END {
}

