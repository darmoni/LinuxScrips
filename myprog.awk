BEGIN {
for (i = 1; i < ARGC; i++) {
        if (ARGV[i] == "-v")
            verbose = 1
        else if (ARGV[i] == "-q")
            debug = 1
        else if (ARGV[i] ~ /^-./) {
            e = sprintf("%s: unrecognized option -- %c",
                    ARGV[0], substr(ARGV[i], 2, 1))
            print e > "/dev/stderr"
        } else
            break
        delete ARGV[i]
    }
printf "A=%d, B=%d\n", A, B
printf "debug=%d verbose=%d\n",  debug, verbose
for (arg in ARGV) {
    print ARGV[arg]
}
#    printf "A=%d, B=%d\n", A, B
#    for (i = 0; i < ARGC; i++)
#        printf "\tARGV[%d] = %s\n", i, ARGV[i]
}
#END   {
#    }
