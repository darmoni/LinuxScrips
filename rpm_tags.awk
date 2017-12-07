#!/usr/bin/awk -f
BEGIN {
    PACKAGE_NAME="";
    RPM_VERSION="";
    RPM_RELEASE="";
}
{
    if( $0 ~ /^PACKAGE_NAME=|^RPM_VERSION=|^RPM_RELEASE=/ ) {
        FS ="=";
        $0=$0;
        if("PACKAGE_NAME"==$1) {
  #          gsub("-","_",$2);
            PACKAGE_NAME = $2;
        }
        if("RPM_VERSION"==$1) RPM_VERSION=$2;
        if("RPM_RELEASE"==$1) RPM_RELEASE=$2;
    }
}
END{
#    print PACKAGE_NAME "-RPM_VERSION=" RPM_VERSION "\n" PACKAGE_NAME "-RPM_RELEASE=" RPM_RELEASE
    print "RPM_VERSION_" PACKAGE_NAME "=" RPM_VERSION "\n" "RPM_RELEASE_" PACKAGE_NAME "=" RPM_RELEASE    
}
