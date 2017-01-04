#!/usr/bin/php
<?php
declare(ticks = 1);
 
pcntl_signal(SIGTERM, 'signalHandler');// Termination ('kill' was called)
pcntl_signal(SIGHUP, 'signalHandler'); // Terminal log-out
pcntl_signal(SIGINT, 'signalHandler'); // Interrupted (Ctrl-C is pressed)
 
$pidFileName = basename(__FILE__) . '.pid';
$pidFile = @fopen($pidFileName, 'c');
if (!$pidFile) die("Could not open $pidFileName\n");
if (!@flock($pidFile, LOCK_EX | LOCK_NB)) die("Already running?\n");
ftruncate($pidFile, 0);
fwrite($pidFile, getmypid());
 
while (true) sleep(1);
 
function signalHandler($signal) {
  global $pidFile;
  ftruncate($pidFile, 0);
  exit;
}
?>
