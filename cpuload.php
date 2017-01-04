#!/usr/bin/php -e
<?php
    $load = sys_getloadavg();
    $dat = getrusage();
    print_r ($load);
    print_r($dat);
    if ($load[0] > 0.10) {
        print "Too busy, try again later\n";
    if($load[0] > 0.80) 
            die('Server too busy. Please try again later.');
}
?>
