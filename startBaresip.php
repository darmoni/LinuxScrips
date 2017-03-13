<?php
$last_line = system("/sbin/start-stop-daemon -S -x /usr/local/bin/baresip -- -d", $retval);
echo '<pre>';

// Outputs all the result of shellcommand "ls", and returns
// the last output line into $last_line. Stores the return value
// of the shell command in $retval.
//$last_line = system("curl http://localhost:8000/?l", $retval);

// Printing additional info
echo '
</pre>
<hr />Last line of the output: ' . $last_line . '
<hr />Return value: ' . $retval;
?>
