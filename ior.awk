#!/usr/bin/awk -f
#find the traces of ior in log files
BEGIN {
    counter =0;
    puts = "./ior_puts.log"
    use = "./ior_use_agent.log"
    pos = "./ior_get_position.log"
}
{
    if( $0 ~ /:/ ) {
        FS=":";
        $0=$0;
    }
    iors[counter++]=substr($2,160,5);
}
END{
    FS="[";
    for(i=0; i < counter; ++i){
        needle = iors[i];

        print needle, " ---Inserts -------", puts;
        while (getline < puts) {
            if($0 ~ needle){
                puts_counter[needle]++;
                print needle, $1;
                }
        }close (puts);
        if(0 == puts_counter[needle]) print "grep", needle, puts;
        print needle, " ---USAGE----------", use;
        while (getline < use ) {
            if($0 ~ needle){
                use_counter[needle]++;
                print needle, $1;
                }
        }close (use);
        if(0 == use_counter[needle]) print "grep", needle, use;
        print needle, " ---Position ----------", pos;
        while (getline < pos ) {
            if($0 ~ needle){
                pos_counter[needle]++;
                print needle, $1;
                }
        }close (pos);
        if(0 == pos_counter[needle]) print "grep", needle, pos;
    }
}
