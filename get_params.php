#! /usr/bin/php -f
<?php
//$line = '/usr/local/registrator/lib/mserver/app/mappemail_acdrecording.php 22094 1046332 15817 "7117" 8003 "3000" "7160" "Nir Darmoni" "message-center@xcaststaging.voippbxsite.net" "ndarmoni@xcastlabs.com" "/usr/local/registrator/callrecordings//xcaststaging.voippbxsite.net/fc/acdcallrec-8003-1046329.mp3" wav';
//$line2 = '/usr/local/registrator/lib/mserver/app/mappemail_acdrecording.php 22094 1046332 15817 "7117" 8003 "3000" "7160" "Nir Darmoni" """Message Center"" "message-center@xcaststaging.voippbxsite.net" "ndarmoni@xcastlabs.com" "/usr/local/registrator/callrecordings//xcaststaging.voippbxsite.net/fc/acdcallrec-8003-1046329.mp3" wav';
//$line3 = '/usr/local/registrator/lib/mserver/app/mappemail_acdrecording.php 30320 109050 25518 "7160" 15999 "9801" "7161" "Near Darmoni 61" ""Message Center" <message-center@xcastlabs.com>" "ndarmoni@xcastlabs.com" "/usr/local/registrator/callrecordings//siptalk64.xcastlabs.com/71/acdcallrec-15999-109049.mp3" wav';

function log_notify($a){
    printf("%s \n", $a);
}

//print escapeshellarg($line2);
//print "\n";
//parse_str("$line\n");
//print "$line3\n";


$processId = intval($argv[1]);
$callId = strval($argv[2]);
$agentAcc = intval($argv[3]);
$agentCallerId = strval($argv[4]);
$queueAcc = intval($argv[5]);
$queueCallerId = strval($argv[6]);
$fromPhone = intval($argv[7]);
$fromDisplayName = strval($argv[8]);
$fromEmail = strval($argv[9]);
$toEmail = strval($argv[10]);
$file = strval($argv[11]);
$filetype = strval($argv[12]);

log_notify("Starts");
log_notify("    processId = $processId");
log_notify("    callId = $callId");
log_notify("    agentAcc = $agentAcc");
log_notify("    agentCallerId = $agentCallerId");
log_notify("    queueAcc = $queueAcc");
log_notify("    queueCallerId = $queueCallerId");
log_notify("    fromPhone = $fromPhone");
log_notify("    fromDisplayName = $fromDisplayName");
log_notify("    fromEmail = $fromEmail");
log_notify("    toEmail = $toEmail");
log_notify("    file = $file");
log_notify("    filetype = $filetype");



?>
