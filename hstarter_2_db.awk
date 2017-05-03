#!/usr/bin/awk -f

#select * from conf where "proc" = 'T3680'
#select * from conf where "subject" = 'CLOUD'
#select * from conf group by subject

BEGIN {
    counter =0;
    this_second =systime();
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
    for (; i <= NF; i++)
        info = info " " $i
    if( $2 ~ /([[:digit:]]{2}.){3}[[:digit:]]{6}/){
        #u = substr($2,index($2,".")+1)
        #seconds = substr($2,1,index($2,".")-1)
        #print $2, seconds,u
        #n = split(substr($2,1,index($2,".")-1),timeparts,":")
        #if(3 == n){
        #    seconds=timeparts[3] + 60 *timeparts[2] + 60*60*timeparts[1]
        #}
        #timestamp = sprintf("%010ld%06d000",this_second+seconds,u)
        #print this_second, seconds,u,timestamp
        print inserter " info=\"" info "\"", $2
    }
}
END {
}

