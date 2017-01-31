#!/usr/bin/php -e
<?php
function killme () {
    die ("I just killed my caller\n");
}
$load = sys_getloadavg();
$dat = getrusage();
print_r ($load);
//    killme();
print_r($dat);
if ($load[0] > 0.10) {
    print "Too busy, try again later\n";
    killme();
if($load[0] > 0.80)
        die('Server too busy. Please try again later.');
}
?>
