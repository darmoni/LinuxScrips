#!/usr/bin/awk -f
{
    if( $0 ~ /hstarter|[m|f|c]server\.cfg/ ) {
        FS =" ";
        $0=$0;
        #printf("%s %s %s\n",$2,$3,$8)
        n=split ($8,a,/\//);
        parent[$2] = $3 "-" a[n];
    }
}
END{
    for (i in parent){
        n = split(parent[i],a,/-/);
        #printf("%s child of %s %s\n",i,a[1],a[2]);
        if(n > 1 && 1 == a[1]){
            server[i] = a[2];
            #printf("server[%s]=%s\n",i,server[i]);
        }
        else proc[i] = a[1];
    }
    for (i in proc) {
        #printf("proc[%s]=%s\n",i,proc[i]);
        if (proc[i] in server){
            master[i] = server[proc[i]];
        }
        else
            child[proc[i]]++
    }
    if(0)
        for (i in server) {
            printf("server[%s]=%s\n",i,server[i]);
        }
    if(0)
        for (i in master) {
            printf("Master[%s]=%s\n",i, master[i]);
        }
        n = asorti(master, sorted)
        for(i in sorted){
            format = "Count of Children[%s]=%s\n"
                printf (format, master[sorted[i]],(sorted[i] in child) ? child[sorted[i]]:0);
        }
}
