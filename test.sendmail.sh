#!/bin/sh
TO=nd.arm.oni@gmail.com
FROM=nd.arm.oni@gmail.com

/usr/sbin/sendmail -v -Ac -i -f$FROM -- $TO <<END
subject: test
to: $TO
from: $FROM

test
END
