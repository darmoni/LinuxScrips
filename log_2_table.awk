#!/usr/bin/awk -f
BEGIN {
    if(length(name) == 0)
    {
        name ="conf"
    }
    syslog_delimiter ="]: [";
    syslog = 0
    counter =0;
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
    if( $0 ~ / ([[:digit:]]{2}.){3}[[:digit:]]{6} /) {
        $0 =$0;

        timetsamp=$2;
        n = split($1,front,"[");
        if(0 < n){
            n = split(front[2],values,"]");
            if(0 < n) { value = values[1]; }
        }
        proc = value

        info = $3
        if (index($3,"[") == 1){
            subject = substr($3,2,index($3,"]")-2);
            info = substr($3,index($3,"]")+1);
            i=4
        }
        else {
            i=4
            subject = "Master"
        }
        if( subject ~ /RTP-.+/ ) subject = "RTP"
        if( timetsamp ~ /([[:digit:]]{2}.){3}[[:digit:]]{6}/){
            for (; i <= NF; i++)
                info = info " " $i
            printf "%s\t%s\t%s\t%s\t%s\n", name, timetsamp,proc,subject,info
        }
    }
}
