#!/usr/bin/awk -f


BEGIN {
    counter =0;
}
{
    if( $0 ~ /AddPoint|VOICE_|MIXER|attaching|cancelled|CLD_AddPoint|CLD_RemovePoint|HND INFO|defined|DoAddPoint|DoAttachPoint|DoRemovePoint|DTMFProcessor|external|external-source| ExternalSource| GenericAudioDecoder|GenericAudioEncoder|HT_RTPSTACK-queue|InitRTP|MediaCloud|MediaNotify|ofs+data|OnStart|OutboundPin|packets|payload|prototype|ReadTransport|receiver|RemovePoint|RTPJitter|RTPMediaPoint|RTPRender|scheduled|sending|SendPacket|SetPayload|SetupDTMF|telephone-event\/Params|transfers|trn-in\/out|\[VID\]|[h|H]\.{0,1}264|G729/ ) {
    print
    }
}
END {
}
