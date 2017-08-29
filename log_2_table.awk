#!/usr/bin/awk -f
BEGIN {
    if(length(name) == 0) {
        name ="conf"
    }
    subjects_filter = "";
    if(length(subject) > 0) {
        subjects_filter = subject;
        #printf ("subject ='%s' \n", subject);
        n = split(subjects_filter, subjects, "|");
        #printf ("i have %d subjects in '%s' \n", n, subjects_filter);
        #for (_s in subjects) {
        #    printf ("%d subject = %s\n",_s,subjects[_s]);
        #}
    }
    syslog_delimiter ="]: [";
    syslog = 0
    counter =0;
    printf "measurement\ttime\tproc\tsubject\tinfo\n"
}
{
    #print subjects_filter;
    gsub("\t"," ",$0);
    $0 = $0;
    if((length(subjects_filter) > 0) && ( 0 == index($0 , subjects_filter))) {next;}
    else if((0 == counter) && (0==syslog)) {
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
    if((length(subjects_filter) > 0) && ( 0 == index($0 , subjects_filter))){}
    else if ($0 ~ / ([[:digit:]]{2}.){3}[[:digit:]]{6} /) {
        $0 =$0;

        timetsamp=$2;
        n = split($1,front,"[");
        if(0 == n) value = $1;
        if(0 < n){
            n = split(front[2],values,"]");

            if(0 < n) { value = values[1]; }
        }
        proc = value

        info = $3
        if (index($3,"[") == 1) {
            subject = substr($3,2,index($3,"]")-2);
            info = substr($3,index($3,"]")+1);
            i=4
        }
        else {
            i=4
            subject = "Master"
        }
#corrections
        if( subject ~ /RTP-.+/ ) subject = "RTP";
        if(( "" == proc ) && (subject ~ /^[0-9]+$/ )) {
            proc = subject;
            subject = "Master";
            }

#validating time field is set
        if( timetsamp ~ /([[:digit:]]{2}.){3}[[:digit:]]{6}/) {
            for (; i <= NF; i++)
                info = info " " $i
            if (subject ~ /^[0-9]+$/ ) {
                subject ="";
                info = $3 "" info;
            }
            if(length(subjects_filter) > 0) {
                for (_s in subjects) {
                    if(subjects[_s] == subject) {
                        printf "%s\t%s\t%s\t%s\t%s\n", name, timetsamp,proc,subject,info;
                        break;
                    }
                }
            }
            else printf "%s\t%s\t%s\t%s\t%s\n", name, timetsamp,proc,subject,info ;
        }
    }
}
