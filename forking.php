#!/usr/bin/php -f
<?PHP
/*
(PHP 5.2.4) 

This is an example of multithreading keeping different connections to a mysql database: when children exit they close the connection and others can't use it any more generating problems. In this example I used variable variables to make a different connection per each child. 

This scripts loops forever with one mother detached from the terminal and five children 'named' from 1 to 5. When one children sees it's name in the database (one table 'test.tb' with only one field 'test') he lets himself die. To kill children insert their value in the db. The mother suicides only when all children are dead.

What a sad but interesting story...

    $npid = pcntl_fork(); // DETACH FROM TERMINAL AND BE REAPED BY INIT

    if ($npid==-1) die("Error: impossible to pcntl_fork()\n");
    else if ($npid) exit(0); // THE GRANPA DIES
    else // MOTHER GOES ON TO MAKE CHILDREN
    {
        $children = 5;
        for ($i=1; $i<=$children; $i++)
        {
            $pid = pcntl_fork();
            if ($pid==-1) die("Error: impossible to pcntl_fork()\n");
            else if ($pid)
            {
                 $pid_arr[$i] = $pid;
            }
            if (!$pid) // CHILDREN
            {
                global $vconn;
                $vconn = "vconn$i";
                global $$vconn;
                $$vconn = @mysql_connect("mydbhost","mydbuser","mydbpwd");
                if (!($$vconn)) echo mysql_error();
                if (!($$vconn)) exit;

                while (1)
                {
                    $query = "SELECT test FROM test.tb";
                    $rs = mysql_query($query,$$vconn);
                    $rw = mysql_fetch_row($rs);
                    if ($rw[0]==$i) exit;
                    else
                    {
                        echo "Database is $rw[0] and I am $i, it's not my time, I will wait....\n";
                        sleep(1);
                    }
                }
            }
        }

        foreach ($pid_arr as $pid)
        {
            // we are the parent and we wait for all children to die
            pcntl_waitpid($pid, $status);
        }
        echo "All my children died, I will suicide...\n";
        exit();
    }
*/
?>

<?php
declare(ticks=1);
ini_set("auto_detect_line_endings", true);

// setup signal handlers
pcntl_signal(SIGUSR1, "sig_handler");
pcntl_signal(SIGTERM, "sig_handler");
pcntl_signal(SIGHUP, "sig_handler");

global $counter;
global $pid;
global $sockets;

function sig_handler($signo) 
{

     switch ($signo) {
         case SIGTERM:
             // handle shutdown tasks
             exit;
             break;
         case SIGHUP:
         case SIGUSR1:
            global $counter;
            global $pid;
            global $sockets;
            $counter ++;
            echo "$pid $counter\n";            
            fwrite($sockets[1],"die\n");
            fflush($sockets[1]);
             // handle restart tasks
             break;
         default:
             // handle all other signals
     }

}

function mother() {
    global $childs;
    $mypid = getmypid();
    echo "mother $mypid\n";
    while(count($childs) > 0) {
        foreach($childs as $key => $pid) {
            $res = pcntl_waitpid($pid, $status, WNOHANG);
            
            // If the process has already exited
            if($res == -1 || $res > 0)
                unset($childs[$key]);
        }
        sleep(1);
    }
    exit();
}


function child_fork()
{
    global $sockets;
    fclose($sockets[1]);
    $pid = getmypid();
        $counter = 0;
        // loop forever performing tasks
        echo "child $pid $counter\n";
        while (1) {
            $what = trim(fgets($sockets[0]));
            fwrite($sockets[0], "child $pid got $what\n");
            echo "child $pid $what\n";
            if("die" == strtolower($what)) break;
            // do something interesting here
            sleep(1);
        }
        fclose($sockets[0]);
        exit();
}

$sockets = stream_socket_pair(STREAM_PF_UNIX, STREAM_SOCK_STREAM, STREAM_IPPROTO_IP);
$npid = pcntl_fork(); // DETACH FROM TERMINAL AND BE REAPED BY INIT

if ($npid==-1) die("Error: impossible to pcntl_fork()\n");
else if ($npid) exit(0); // THE GRANPA DIES
else // MOTHER GOES ON TO MAKE CHILDREN
{
    $count = 1;
    $childs = array();
    for ($i = 0 ; $i < $count; $i++){
        $pid = pcntl_fork();
        if ($pid == -1) {
            die("could not fork"); 
        }
        else if ($pid) {
            $childs[] = $pid;
        } else {
             // we are the child
             child_fork();
        }
    }
    mother();
}
?>
