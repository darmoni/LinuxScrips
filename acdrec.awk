#!/usr/bin/awk -f
#find the traces of ior in log files
# cat mappemail_acdrecording.php.log | awk -f $0
BEGIN {
    counter =0;
}
{
    if( $0 ~ /received a .+ second/ ) {
        FS=" ";
        $0=$0;
    }
    date = $1;
    hour = substr($2,0,2);
    hour_minutetime = substr($2,0,5);
    time =substr($2,0,8)
    duration = $8;
    units =$9;

    recordings[counter++]=date " " time " " duration " " units;
    count_date[date]++;
    sum_date[date]+=duration
    count_hour_minute[hour_minutetime]++;
    sum_hour_minute[hour_minutetime]+=duration
    count_hour[hour]++;
    sum_hour[hour]+=duration
}
END{
    FS="[";
#    for(i in recordings){
#        print recordings[i],i;
#    }
    n = asorti(count_date, sorted)
    for(i in sorted){
        print "daily count:",sorted[i],count_date[sorted[i]];
    }
    n = asorti(sum_date, sorted)
    for(i in sorted){
        print "daily duration:",sorted[i],sum_date[sorted[i]];
    }
    n = asorti(count_hour, sorted)
    for(i in sorted){
        print "hourly count:",sorted[i],count_hour[sorted[i]];
    }
    n = asorti(sum_hour, sorted)
    for(i in sorted){
        print "hourly duration:",sorted[i],sum_hour[sorted[i]];
    }
}
