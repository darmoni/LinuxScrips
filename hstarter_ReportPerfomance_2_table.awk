#!/usr/bin/awk -f
# SAMPLE:
# [T46d7] 10:13:59.966942 [MWK][ReportPerfomance] 0001:HT_WORKTHREAD queue 0x17c054d0 (rcv/drp/prc/tmr 4095/0/4095/2242), CPU info : wait/run (average 96.819%/3.077%, recent 97.8%/2.2%)
#
# 1 [ReportPerfomance]
# 2 0001:HT_WORKTHREAD
# 3 queue
# 4 0x17c054d0
# 5 (rcv/drp/prc/tmr
# 6 4095/0/4095/2242),
# 7 CPU
# 8 info
# 9 :
#10 wait/run
#11 (average
#12 96.819%/3.077%,
#13 recent
#14 97.8%/2.2%)

BEGIN {
    if(length(name) == 0) {
        name ="ReportPerfomance"
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
    info_queue_item=4;
    info_rcv_drp_prc_tmr_item=6;
    info_average_item=12;
    info_recent_item=14;
#    info_queue="4.0";
#    info_rcv="6.1"
#    info_drp="6.2"
#    info_prc="6.3"
#    info_tmr="6.4"
#    info_average_wait="12.1"
#    info_average_run="12.2"
#    info_recent_wait="14.1"
#    info_recent_run="14.2"
    printf "measurement\ttime\tproc\tsubject\tinfo\tqueue\trcv\tdrp\tprc\ttmr\taverage_wait\taverage_run\trecent_wait\trecent_run\n"
}

{
    if(! ($0 ~ /ReportPerfomance/)) {next;}
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
    if( 0 == index($0 , subjects_filter)) {}
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
            n = split(info, infos)
            if (0 < n) {
                for (item in infos) {
                    #print item,infos[item];
                    if(info_queue_item == item) queue = infos[item];
                    else if(info_rcv_drp_prc_tmr_item == item) {
                        n = split(infos[item],rcv_drp_prc_tmr,"/")
                            if(n > 3) {
                               rcv = rcv_drp_prc_tmr[1];
                               drp = rcv_drp_prc_tmr[2];
                               prc = rcv_drp_prc_tmr[3];
                               _tmr = rcv_drp_prc_tmr[4];
                               tmr = substr(_tmr,0, index(_tmr,")")-1);
                            }
                        }
                    else if(info_average_item == item) {
                        n = split(infos[item],averages,"/")
                            if(n > 1) {
                               average_wait = averages[1];
                               _average_run = averages[2];
                               average_run = substr(_average_run,0, index(_average_run,",")-1);
                            }
                        }
                    else if(info_recent_item == item) {
                        n = split(infos[item],recents,"/")
                            if(n > 1) {
                               recent_wait = recents[1];
                               _recent_run = recents[2];
                               recent_run = substr(_recent_run,0, index(_recent_run,")")-1);
                            }
                        }
                }
            }
            printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", name, timetsamp,proc,subject,info,
                    queue,rcv,drp,prc,tmr,average_wait,average_run,recent_wait,recent_run;
            if(length(subjects_filter) > 0) {
                for (_s in subjects) {
                    if(subjects[_s] == subject) {
                        printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", name, timetsamp,proc,subject,info,
                            queue,rcv,drp,prc,tmr,average_wait,average_run,recent_wait,recent_run;
                        break;
                    }
                }
            }
            else printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", name, timetsamp,proc,subject,info,
                    queue,rcv,drp,prc,tmr,average_wait,average_run,recent_wait,recent_run;

        }
    }
}
