#!/usr/bin/php -f
<?php
declare(ticks = 1);
if (!function_exists('pcntl_signal'))
{
    printf("Error, you need to enable the pcntl extension in your php binary, see http://www.php.net/manual/en/pcntl.installation.php for more info%s", PHP_EOL);
    exit(1);
}

function test_event_server ($cmdline,$count,$agents,$dial) {
    echo "cycling($count)\n";
    for ($i= $count;$i >=0; $i--)
    {
        $who = $dial[$i % count($dial)];$count--;
        fwrite($cmdline, "b\n");
        usleep (100000);
        $count++;
        fwrite($cmdline, "dsip:$who\n");
        usleep (100000);
        fwrite($cmdline, "T\n");  // switch agent
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

function cleanup ($calls, $cmdline) {
    global $agents;
	if(!is_resource($cmdline)) return;
    if(is_numeric($calls)) {
		echo "Number of calls to close is $calls\n";
		for ($a_calls= 2*$calls;$a_calls >=0; $a_calls--) {
			fwrite($cmdline, "b\n");
			usleep(10000);
	        if(1 < $agents) fwrite($cmdline, "T\n");  // switch agent
		}
	}
}
const TIMEOUT_SECONDS = 2*60;

function testing($count, $dial, $agents) {
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


//    $process = proc_open('/usr/local/bin/baresip', $descriptorspec, $pipes/*, $cwd, $env*/);
    $process = proc_open('netcat -u 127.0.0.1 5565', $descriptorspec, $pipes/*, $cwd, $env*/);

    if (is_resource($process)) {
            // $pipes now looks like this:
            // 0 => writeable handle connected to child stdin
            // 1 => readable handle connected to child stdout
            // Any error output will be appended to /tmp/error-output.txt

        $cmdline = $pipes[0];

        //stream_set_blocking($pipes[1], 0);
        stream_set_blocking($cmdline, 1);
        while (1) {
            test_event_server($cmdline,$count,$agents,$dial);
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
                echo "timeout\n";
                cleanup($count,$cmdline);
                break;
            }
            $status = proc_get_status($process);
            // check retval
            if ($status === FALSE) {
                throw new Exception("Failed to obtain status information for $pid");
            }
            if ($status['running'] === FALSE) {
                $exitcode = $status['exitcode'];
                $pid = -1;
                echo "Process exited with code: $exitcode\n";
                fclose($cmdline);

                // It is important that you close any pipes before calling
                // proc_close in order to avoid a deadlock
                $return_value = proc_close($process);

                echo "command returned $return_value\n";
                exit($exitcode);
            }
        }
    }
}
#$calls = 512;
#$calls = 256;
$calls = 128;
echo "dialing - calls\n";
$dial = array("55560", "3000", "3001", "70062", "4703","67892","4701","713300");
$agents = 5;
print_r($dial);
// echo "cat /tmp/error-output.txt\n";
testing($calls, $dial, $agents);
