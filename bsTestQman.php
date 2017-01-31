#!/usr/bin/php -f
<?php
declare(ticks = 1);
if (!function_exists('pcntl_signal'))
{
    printf("Error, you need to enable the pcntl extension in your php binary, see http://www.php.net/manual/en/pcntl.installation.php for more info%s", PHP_EOL);
    exit(1);
}

function test_event_server ($cmdline,$count,$agents,$dial) {
    echo "cycling($count,$agents)\n";
    for ($agent = 0 ; $agent < $agents; $agent++) {
        for ($i= count($dial);$i >=0; $i--)
        {
            $who = $dial[$i % count($dial)];$count--;
//            echo "Call # $count, $who\n";
            fwrite($cmdline, "b\n");
            sleep (1);
//            echo "Call # $count, $who\n";
            $count++;
            fwrite($cmdline, "dsip:$who\n");
            fwrite($cmdline, "T\n");  // switch agent
        }
        sleep (1);
    }
}


function safe_exit($level) {
global $cmdline;
global $calls;
global $process;
# save stuff
    print("Exiting ...\n");
    cleanup($calls, $cmdline);
/*    if($level === 1)
    for ($i=0;$i< 20; $i++)
    {
        echo "closing calls time $i\n";
        fwrite_stream($cmdline, "Tbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbl\n");
        sleep(1);
    }
*/
    exit(0);
}


function sig_handler($sig) {
       print "got sig($sig)\n";
        safe_exit($sig);
}

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
echo exec('baresip -edsip:7160@xcaststaging.voippbxsite.net');
    sleep(10);
*/
function cleanup ($calls, $cmdline){
    global $agents;
	if(!is_resource($cmdline)) return;
//    for ($agent = 0 ; $agent < $agents; $agent++){
        if(is_numeric($calls)) {
            echo "Number of calls to close is $calls\n";
            for ($a_calls= $calls;$a_calls >=0; $a_calls--){
                fwrite($cmdline, "b\n");
                usleep(100000);
                if(1 < $agents) fwrite($cmdline, "T\n");  // switch agent
            }
        }
        sleep(1);
//    }
//	sleep(3);
}
const TIMEOUT_SECONDS = 2*60;

function testing($count, $dial, $agents)
{

    stream_set_blocking(STDIN, 0);

    $timeoutStarted = false;
    $timeout = null;
    $break = false;
    $calls = 0;
    $pid = getmypid();

    $descriptorspec = array(
       0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
       //1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
       1 => array("file", "/dev/null","a"),  // stdout is a pipe that the child will write to
       2 => array("file", "/tmp/error-output$pid.txt", "a") // stderr is a file to write to
    );

    // $cwd = '/tmp';
    //$cwd = '.';
    //$env = array('some_option' => 'aeiou');


//    $process = proc_open('/usr/local/bin/baresip', $descriptorspec, $pipes/*, $cwd, $env*/);
    $process = proc_open('netcat -u 127.0.0.1 5555', $descriptorspec, $pipes/*, $cwd, $env*/);

    if (is_resource($process)) {
            // $pipes now looks like this:
            // 0 => writeable handle connected to child stdin
            // 1 => readable handle connected to child stdout
            // Any error output will be appended to /tmp/error-output.txt

    $cmdline = $pipes[0];

            //stream_set_blocking($pipes[1], 0);
            stream_set_blocking($cmdline, 1);
            for ($i=0 ; $i < $count; $i++) {
                $who = $dial[$i % count($dial)];
      //          $dial ="dsip:acdtst@xcaststaging.voippbxsite.net\n";
      //          echo "Call # $i, $who\n";
                //fwrite($cmdline, "dsip:$who@xcaststaging.voippbxsite.net\n");
                fwrite($cmdline, "d$who\n");
                usleep(10000);
                if($agents>1) fwrite($cmdline, "T\n");  // switch agent
                //echo stream_get_contents($pipes[1]);
            }
            sleep(1);

            while (1) {
                while (false !== ($line = fgets(STDIN))) {
                    echo $line;
                    if('q' == $line[0]) {
                        $calls = intval(substr($line,1));
                        if(is_numeric($calls)){
                            if (0 == $calls) $calls = $count;
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
                    cleanup($count,$cmdline);
		/* for ($agent = 0 ; $agent < count($agents); $agent++) {
                        if(is_numeric($calls)) {
                            echo "Number of calls to close is $calls\n";
                            for ($a_calls= $calls;$a_calls >=0; $a_calls--)
                            {
                                fwrite($cmdline, "b");
                                usleep(300);
                            }
                        }
                        fwrite($cmdline, "T");  // switch agent
                        usleep(300);
                    }*/
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

                if (time() > $timeout + TIMEOUT_SECONDS) {
                    //test_event_server($cmdline,$count/8,$agents,$dial);
                    echo "timeout\n";
                    cleanup($count,$cmdline);
                    break;
                } /*
                for ($agent = 0 ; $agent < count($agents); $agent++) {
                        echo "cycling\n";
                        for ($i= count($dial);$i >=0; $i--)
                        {
                            $who = $dial[$i % count($dial)];$count--;
                            echo "Call # $count, $who\n";
                            fwrite($cmdline, "b");
                            usleep(300);
                            echo "Call # $count, $who\n";$count++;
                            fwrite($cmdline, "dsip:$who@xcaststaging.voippbxsite.net\n");
                            fwrite($cmdline, "T");  // switch agent
                        }
                    } */
            };
            //print("writing 'q' into " .$cmdline . "\n");
            //fwrite($cmdline, "q");

            //echo stream_get_contents($pipes[1]);
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

            //sleep(3);
            fclose($cmdline);

            // It is important that you close any pipes before calling
            // proc_close in order to avoid a deadlock
            $return_value = proc_close($process);

            echo "command returned $return_value\n";
            exit($exitcode);
        }
    }
}
$calls = 99;
#$calls = 256;
#$calls = 128;
echo "dialing - calls\n";
$dial = array("55560", "3000", "3001", "70062", "4703","67892","4701","713300");
$agents = 2;
print_r($dial);
// echo "cat /tmp/error-output.txt\n";
    testing($calls, $dial, $agents);
