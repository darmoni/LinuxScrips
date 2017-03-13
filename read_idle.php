<?php
//$idle= popen("mpstat|tail -1 | awk '{print $13;}'","r");
$read= popen("mpstat|tail -2", "r");
//$read = fread($idle, 256);
$line = fgets($read, 1024);
$fields = preg_split("/[\s,]+/",$line);
for($i = 0 ; $i<count($fields); ++$i) {
    echo $fields[$i] ."\n";
    if ('%idle' == $fields[$i]) {
        echo "Found idle $i\n";
        break;
    }
}

$line = fgets($read, 1024);
$fields = preg_split("/[\s,]+/",$line);
echo $fields[$i]. "<=idle[$i]\n";
pclose($read);
?>
