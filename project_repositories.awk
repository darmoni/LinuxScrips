#!/usr/bin/awk -f
#ident "$Id$" "$Date$"

function read_remote_url(project) {

    # reading latest tag from CVS
    cmd="cd " project " && git config remote.origin.url"
    cmd | getline remote_url;
    close(cmd);
    return remote_url;
}

BEGIN {
    $0=$0;
    OFS=", ";
}
{
    if ($0 ~ /cvs /) {
        if ( $0 ~ /cvs .+ / ) {
            project=$NF
            print "Project=" project
            remote_url=read_remote_url(project);
            if("" != remote_url) {
                projects[remote_url] = project;
            }
        }
    }
}
END {
    n = asorti(projects, sorted)
    for (i=1; i<= n; i++) {
        url = sorted[i];
        if("$" != substr(project,0,1))
            print "git clone " url " " projects[url] ;
    }
}
