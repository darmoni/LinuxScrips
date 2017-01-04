#!/usr/bin/php
<?php


declare(ticks = 1);

$cmdline;
$process;
function safe_exit() {
global $cmdline;
global $process;
# save stuff
    print("writing 'q' into " .$cmdline . "\n");
            fwrite($cmdline, "q");

            sleep(10);
            fclose($cmdline);

            // It is important that you close any pipes before calling
            // proc_close in order to avoid a deadlock
            $return_value = proc_close($process);
            $status = proc_get_status($process);

            echo "command returned $return_value\n";
            $exitcode = $status['exitcode'];
            exit($exitcode);
}

function sig_handler($sig) {
    switch($sig) {
        case 1:
        case SIGINT:
        # one branch for signal...
    }
        print "got sig($sig)\n";
        safe_exit();
}

pcntl_signal(1,  "sig_handler");
pcntl_signal(SIGINT,  "sig_handler");
pcntl_signal(SIGTERM, "sig_handler");
pcntl_signal(SIGHUP,  "sig_handler");






/*
function print_query($query)
{
	echo $query . "\n";
}

class db_connect {
    function db_connect() {
        static $doConnect = true;
        static $dbrc;

        if ($doConnect) {
            $host = "localhost";
            $user = "guest";
            $passwd = "n0b0dy";
            $db = "sip";
            $dbrc = mysql_connect($host, $user, $passwd)
                 or die("Cannot connect\n");
            mysql_select_db($db, $dbrc) or die("Cannot select $db\n");
            $doConnect = false;
        }
    }
}
function db_execute( $proc, $query, $err )
{
    $db = new db_connect();
    print_query($proc.": ".$query);
    $res = mysql_query($query) or die ($proc.": ".$err.":\n "
				 . mysql_error(). "<br>\n$query\n<br>");
	return $res;
}

function db_query( $proc, $query, $err )
{
	$res = db_execute( $proc, $query, $err );
    return mysql_fetch_array($res, MYSQL_ASSOC);
}

function db_insert( $proc, $query, $err, &$newid )
{
	db_execute( $proc, $query, $err );
    $newid = mysql_insert_id();
}

function db_quote( $val )
{
	return "'" . mysql_escape_string($val) . "'";
}

function dbexecute( $query )
{
	return db_execute( "", $query, "" );
}
function dbquery( $query )
{
	return db_query( "", $query, "" );
}
function dbinsert( $query, &$id )
{
	return db_insert( "", $query, "", $id );
}
function dbnext($res)
{
    return mysql_fetch_array($res, MYSQL_ASSOC);
}

function reload_cache($port, $message)
{
	$fp = fsockopen("udp://127.0.0.1", $port, $errno, $errstr);
    if (!$fp) {
	echo "ERROR: $errno - $errstr<br>\n";
	} else {
	fwrite($fp,"$message");
	fclose($fp);
	//echo "<script> alert('Sending socket update command'); </script>";
	print_query("SENDING UDP UPDATE MSG: $message");
	}
}
function updateaccount($id)
{
	$msg = sprintf("RELOAD %010d", $id);
	reload_cache(7555, $msg);
}

function dbupdateaccounts($query)
{
	$recs = dbexecute($query);
	while($rec=dbnext($recs))
	{
		updateaccount($rec['id']);
	}
}
*/
/* END of DB Interface  */

/*
echo exec('baresip -edsip:7160@siptalk64.xcastlabs.com');
    sleep(10);
*/

const TIMEOUT_SECONDS = 120;
$duration = TIMEOUT_SECONDS;
$calls = 100;
$shortopts  = "";
$shortopts .= "c:";  // text config file
//$shortopts .= "v::"; // Optional value
//$shortopts .= "abc"; // These options do not accept values

$longopts  = array(
    "config:",     // text config file
//    "optional::",    // Optional value
//    "option",        // No value
//    "opt",           // No value
);
$options = getopt($shortopts, $longopts);
//var_dump($options);
$output = "/tmp/error-output.txt";
$cfg_file = "cfg.txt";
if (isset($options['c'])) $cfg_file = $options['c'];

if(isset($cfg_file)) $configs=file($cfg_file);

while (list($tmp,$line) = each ($configs))
{
    list($cfg,$value) = explode('=', trim($line));
    print "$cfg=$value\n";
    if("output" == strtolower($cfg)) $output = $value;
    else if("duration" == strtolower($cfg)) $duration = $value;
    else if("calls" == strtolower($cfg)) $calls = $value;
}

function testing($count, $dial, $agents)
{
    global $output, $duration;
    stream_set_blocking(STDIN, 0);
global $cmdline;
global $process;
    $timeoutStarted = false;
    $timeout = null;
    $break = false;
    $calls = 0;

    $descriptorspec = array(
       0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
       1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
       2 => array("file", $output, "a") // stderr is a file to write to
    );

    // $cwd = '/tmp';
    //$cwd = '.';
    //$env = array('some_option' => 'aeiou');


    $process = proc_open('/usr/local/bin/baresip', $descriptorspec, $pipes/*, $cwd, $env*/);
    if (is_resource($process)) {
            // $pipes now looks like this:
            // 0 => writeable handle connected to child stdin
            // 1 => readable handle connected to child stdout
            // Any error output will be appended to /tmp/error-output.txt

    $cmdline = $pipes[0];

            stream_set_blocking($pipes[1], 0);
            stream_set_blocking($cmdline, 1);
                for ($i=0 ; $i < $count; $i++) {
                    $who = $dial[$i % count($dial)];
          //          $dial ="dsip:acdtst@siptalk64.xcastlabs.com\n";
                    echo "Call # $i, $who\n";
                    fwrite($cmdline, "dsip:$who@siptalk64.xcastlabs.com\n");
                    usleep(100000);
                    fwrite($cmdline, "T");  // switch agent
                    echo stream_get_contents($pipes[1]);
                }
                usleep(150);

            while (1) {
                while (false !== ($line = fgets(STDIN))) {
                    echo $line;
                    if('q' == $line[0]) {
                        $calls = intval(substr($line,1));
                        if(is_numeric($calls)){
                            if (0 == $calls) $calls = 100;
                            echo "Number of calls to close is $calls\n";
                            $break = true;
                        }
                    }
                    else
                    fwrite($cmdline, rtrim($line));

                    if ($timeoutStarted) {
                        $timeoutStarted = false;
                        $timeout = null;
                    }
                }
                if($break) {
                    for ($agent = 0 ; $agent < count($agents); $agent++) {
                        if(is_numeric($calls)) {
                            echo "Number of calls to close is $calls\n";
                            for ($a_calls= $calls;$a_calls >=0; $a_calls--){
                                fwrite($cmdline, "bT");
                                usleep(300);
                            }
                        }
/*                        fwrite($cmdline, "T");  
                        echo "switching agent\n";
                        usleep(300);
*/
                    }
                    break;
                }
                if (feof(STDIN)) {
                    echo "feof\n";
                    break;
                }
                if (null === $timeout) {
                    $timeout = time();
                    $timeoutStarted = true;
                    continue;
                }

                if (time() > $timeout + TIMEOUT_SECONDS){
                    echo "timeout\n";
                    break;
                } 
                for ($agent = 0 ; $agent < count($agents); $agent++){
                        echo "cycling\n";
                        for ($i= count($dial);$i >=0; $i--){
                            $who = $dial[$i % count($dial)];$count--;
                            echo "Call # $count, $who\n";
                            fwrite($cmdline, "bT");
                            usleep(300);
                            echo "Call # $count, $who\n";$count++;
                            fwrite($cmdline, "dsip:$who@siptalk64.xcastlabs.com\n");
                            if (time() > $timeout + TIMEOUT_SECONDS){
                                echo "timeout\n";
                                break;
                            }
                        }
                }
            }
            safe_exit();
/*            
            print("writing 'q' into " .$cmdline . "\n");
            fwrite($cmdline, "q");

            echo stream_get_contents($pipes[1]);
            $status = proc_get_status($process);
            // check retval
            if ($status === FALSE) {
                throw new Exception("Failed to obtain status information for $pid");
            }
            if ($status['running'] === FALSE) {
                $exitcode = $status['exitcode'];
                $pid = -1;
                echo "Process exited with code: $exitcode\n";

            //fclose($pipes[1]);

            sleep(10);
            fclose($cmdline);

            // It is important that you close any pipes before calling
            // proc_close in order to avoid a deadlock
            $return_value = proc_close($process);

            echo "command returned $return_value\n";
            exit($exitcode);

        }
*/   }
}
echo "dialing - ";
$dial = array("8601", "8600", "9801");
$agents = 2;
print_r($dial);
echo "cat /tmp/error-output.txt\n";
    testing($calls, $dial, $agents);

?>
