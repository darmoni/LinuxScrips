<?php
// mysqli
function msqli () {
    $mysqli = new mysqli("xdev64.xcastlabs.com", "guest", "n0b0dy", "sip");
    $result = $mysqli->query("SELECT 'mysqli says: Hello, dear MySQL user!' AS _message FROM DUAL\n");
    $row = $result->fetch_assoc();
    echo htmlentities($row['_message']);
}
// PDO
function pdo () {
$pdo = new PDO('mysql:host=xdev64.xcastlabs.com;dbname=sip', 'guest', 'n0b0dy');
$statement = $pdo->query("SELECT 'PDO says: Hello, dear MySQL user!' AS _message FROM DUAL\n");
$row = $statement->fetch(PDO::FETCH_ASSOC);
echo htmlentities($row['_message']);
}
// mysql
function old_mysql () {
    $c = mysql_connect("xdev64.xcastlabs.com", "guest", "n0b0dy");
    mysql_select_db("sip");
    $result = mysql_query("SELECT 'old_mysql says: Hello, dear MySQL user!' AS _message FROM DUAL\n");
    $row = mysql_fetch_assoc($result);
    echo htmlentities($row['_message']);
}
$nl = "\n";
try {
msqli ();
echo $nl;
pdo ();
echo $nl;
old_mysql();
}
finally {
    echo "Done\n";
}
?>
