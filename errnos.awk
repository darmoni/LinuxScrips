#!/usr/bin/awk -f
{
    if ($0 ~ /#define/ ) {
        if("" != $3) {
            literal=$2;
            code=$3;
            $1="";
            $2="";
            $3="";
            $4="";
            $(NF)="";
            print "errors[" code "]=\"" literal " " $0 "\";";
        }
    }
}
