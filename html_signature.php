<?php
#ident $Id$ $Date: Tue Oct 3 14:48:49 2017 -0500$

$my_text_signature="
Nir Darmoni
Senior Software Engineer
XCast Labs Inc.
(847) 666-5460 Phone
(847) 716-5132 Fax
(800) 254-3109 Customer Support
191 Waukegan Rd Suite 310 Northfield, IL 60093
ndarmoni@xcastlabs.com
";
$lines=explode("\n",$my_text_signature);
print '<table style="font-size:10.0pt;font-family:&quot;Courier New&quot;;color:black">'. "\n";
foreach($lines as &$line) {
    if(strlen($line) > 0)
        print "<tr><td>" . $line. "</td></tr>\n";
}
print "</table>\n";
//echo explode("\n",$my_text_signature);
#echo htmlentities($my_text_signature, ENT_QUOTES, "UTF-8");
#echo htmlentities($my_text_signature, ENT_COMPAT, "UTF-8");
#echo htmlentities($my_text_signature, ENT_NOQUOTES, "UTF-8");
//print $my_text_signature;
/*
{
    echo "<table><tr><th></th><th></th></tr>";
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<tr><td>" . $row["id"]. "</td><td>" . $row["firstname"]. " " . $row["lastname"]. "</td></tr>";
    }
}
* 
*/
?>
