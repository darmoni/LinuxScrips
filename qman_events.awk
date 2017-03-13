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
            pbx_last_value[pbx OFS account OFS type]=value;
        }
    }
}
END{
#    FS="[";
    n = asorti(pbx_last_value, sorted)
        for (i = 1; i <= n; i++){
                printf ("last sent value of %s=%s\n",sorted[i],pbx_last_value[sorted[i]]);
        }
}
