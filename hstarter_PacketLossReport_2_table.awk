#!/usr/bin/awk -f
# SAMPLE:
# [T4337] 10:41:43.573466 [RTP][Process] PACKET LOSS !!! - 0002:HT_RTPSTACK : 1 packet(s) lost, new pkt 35ffb:HT_RTPBUFFER ofs+data(alloc) bytes: 12+  80(  92), seqno 56795, ssrc 2111032157, ts 652469389, pld 0, mrk 0, tsi 160
#
# 1 [T4337]
# 2 10:41:43.573466
# 3 [RTP][Process]
# 4 PACKET
# 5 LOSS
# 6 !!!
# 7 -
# 8 0002:HT_RTPSTACK
# 9 :
#10 1
#11 packet(s)
#12 lost,
#13 new
#14 pkt
#15 35ffb:HT_RTPBUFFER
#16 ofs+data(alloc)
#17 bytes:
#18 12+
#19 80(
#20 92),
#21 seqno
#22 56795,
#23 ssrc
#24 2111032157,
#25 ts
#26 652469389,
#27 pld
#28 0,
#29 mrk
#30 0,
#31 tsi
#32 160

BEGIN {
    if(length(name) == 0) {
        name ="PacketLoss"
    }
#    subjects_filter = "";
#    if(length(subject) > 0) {
#        subjects_filter = subject;
#        #printf ("subject ='%s' \n", subject);
#        n = split(subjects_filter, subjects, "|");
#        #printf ("i have %d subjects in '%s' \n", n, subjects_filter);
#        #for (_s in subjects) {
#        #    printf ("%d subject = %s\n",_s,subjects[_s]);
#        #}
#    }
    syslog_delimiter ="]: [";
    syslog = 0
    counter =0;
    info_packets_lost_item=8;

    printf "measurement\ttime\tproc\tsubject\tinfo\tdrp\n"
}

{
    if(! ($0 ~ / PACKET LOSS !!! /)) {next;}
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
            if (info_packets_lost_item <= n) {
                drp = infos[info_packets_lost_item];
            }
            if(0 < drp)
                printf "%s\t%s\t%s\t%s\t%s\t%s\n", name, timetsamp,proc,subject,info,drp;
        }
    }
}
