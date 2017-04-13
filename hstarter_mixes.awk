#!/usr/bin/awk -f

# join.awk --- join an array into a string

function join(array, start, end, sep,    result, i)
{
    if (sep == "")
       sep = " "
    else if (sep == SUBSEP) # magic value
       sep = ""
    result = array[start]
    for (i = start + 1; i <= end; i++)
        result = result sep array[i]
    #print result
    return result
}

BEGIN {
	counter =0;
}
{
	
    FS=" ";
    OFS=","
    $0=$0;
    #print
  
    n= split($0,header,FS);
    datetime=header[2];
    for (i = 3; i<= n; ++i){
        if (header[i] ~ /AddPoint|VOICE_|attaching|cancelled|CLD_AddPoint|CLD_RemovePoint|\
                defined|DoAddPoint|DoAttachPoint|DoRemovePoint|DTMFProcessor|external|external-source|\
                ExternalSource| GenericAudioDecoder|GenericAudioEncoder|HT_RTPSTACK-queue|InitRTP|MediaCloud|\
                MediaNotify|ofs+data|OnStart|OutboundPin|packets|payload|prototype|ReadTransport|receiver|RemovePoint|\
                RTPJitter|RTPMediaPoint|RTPRender|scheduled|sending|SendPacket|SetPayload|SetupDTMF|\
                telephone-event\/Params|transfers|trn-in\/out/){
            result =0
            fields = 0
            line = join(header,3,n, SUBSEP);
            #print line 
            #break
            hstarter_activity_value[datetime] = line;
            break;
            }
        }
    #print n, datetime
}
END{
    $0="";
    report_sp = "|";
    event_type["AttachPoint"] = "Attach Point";
    event_type["RemovePoint"] = "Remove Point";
    event_type["CLD_AddPoint"] = "Add Point";
    odd_prefix= "Odd ";

    n = asorti(hstarter_activity_value, sorted)
    for (i = 1; i <= n; i++){
        key = sorted[i];
        printf("%s: %s\n", key,hstarter_activity_value[key]);
    }
}
