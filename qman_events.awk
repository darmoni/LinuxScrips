#!/usr/bin/awk -f
#find the traces of ior in log files
# cat qman.log | awk -f $0
# sample data
# 09:13:24.462595|XCastAgrSender::send snding event 0,8043,7747 [AV]
# 09:13:16.482618|XCastAgrSender::send snding event 1,13613,7747 [0]
# 09:13:16.474456|XCastAgrSender::send snding event 2,13613,7747 [size:1  timestamp:1489068796.474404


BEGIN {
    counter =0;
}
{
    if( $0 ~ /XCastAgrSender::send snding event [012],/ ) {
        FS=" ";
        OFS=","
        $0=$0;
        n= split($1,header,"|");
        datetime=header[1];
        n = split($4,parts,",");
        if(2<n){
            type=parts[1];
            account=parts[2];
            pbx=parts[3];
        }
        n = split($5,message_parts,"[");
        if(0 < n){
            n = split(message_parts[2],values,"]");
            if(0 < n) { value = values[1]; }
        }
        if(0 < pbx){
            #event[counter++]=datetime OFS type OFS account OFS pbx OFS value;
            pbx_last_value[sprintf("%s" OFS "%06d" OFS "%s",pbx,account,type)]=value;
        }
    }
}
END{
#    FS="[";
    $0="";
    report_sp = "|";
    event_type["0"] = "Agent Call Status";
    event_type["1"] = "Queued Calls";
    event_type["2"] = "Queue Records";
    odd_prefix= "Odd ";

    n = asorti(pbx_last_value, sorted)
    for (i = 1; i <= n; i++){
        key = sorted[i];
        f=split(key,fields,OFS);
        if(3==f){
            type = fields[3];
            event_header = event_type[type];
            value = pbx_last_value[key];
            switch(type) {
            case 0:
                agent_state[key]=value;
                if(value != "AV") {
                report[event_header report_sp key]=value;
                }
                break
            case 1:
                queued_calls[key]=value;
                if(value != 0) {
                report[event_header report_sp key]=value;
                }
                break
            case 2:
                queue_records[key]=value;
                if(value != "size:0") {
                report[event_header report_sp key]=value;
                }
                break
            }
        }
    }
    n = asorti(agent_state, sorted)
    if(0 < n) print event_type[0]":"
    for (i = 1; i <= n; i++){
        printf ("%s=%s\n",sorted[i],agent_state[sorted[i]]);
    }
    n = asorti(queued_calls, sorted)
    if(0 < n) print "\n"event_type[1]":"
    for (i = 1; i <= n; i++){
        printf ("%s=%s\n",sorted[i],queued_calls[sorted[i]]);
    }
    n = asorti(queue_records, sorted)
    if(0 < n) print "\n"event_type[2]":"
    for (i = 1; i <= n; i++){
        printf ("%s=%s\n",sorted[i],queue_records[sorted[i]]);
    }
    n = asorti(report, sorted)
    if(0 < n){
        print ;
        print odd_prefix "Report:"
        report_header ="";
        for (i = 1; i <= n; i++){
            f = split(sorted[i],parts,report_sp);
            if(2==f){
                this_header = parts[1];
                if(report_header != this_header){
                    report_header = this_header;
                    format = "%-18s\t%s=%9s\n";
                    printf ("%-18s\t%s=%9s\n",report_header,parts[2],report[sorted[i]]);
                    }
                else
                printf ("%-18s\t%s=%9s\n","",parts[2],report[sorted[i]]);
            }
        }
    }
    else
        print "\nLooks great to me!!!"
}
