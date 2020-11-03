#!/usr/bin/awk -f
#find the name of executable that crashed
# check_cores.sh 2> /dev/null | sort -u | awk -f ~/bin/core_name.awk | sort -u | grep -v errors.log | egrep 'container[[:digit:]]+-la.xcastlabs.net|[[:alpha:]]+-pbxsm-production-'

BEGIN{
	#print("check_cores.sh | egrep -v container | sort -u" )
    counter = 1;
}
{
    if( $0 ~ /[[:alpha:]]+-pbxsm-production-/ ) {
		print("# " counter++ " " $0);
		split($0,line_parts,"/");
		#print(line_parts[5])
		n = split(line_parts[5],name_parts, ".");
		for (i in name_parts) {
			if( name_parts[i] ~ /[[:alpha:]]+-pbxsm-production-/) {
				name = name_parts[i];
				nn = split(name, parts, "-");
				#print("nn = ", nn);
				if (4 == nn) {
					core_name = parts[1] "-" parts[2] "-" parts[3];
					flog = "ssh ndarmoni@logs-pbx-la.xcastlabs.net 'flog " core_name "'"
					print("# " counter++ " Get container of crashed service:\n" "# " counter++ " " flog);
					system(flog);
				}
			}
		}
    }
    else if ($0 ~ /^containe/) { print "#   " $0;
	}
}
