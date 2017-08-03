#!/usr/bin/php -f
<?
#ident "$Id:$"

$phpfile = pathinfo(__FILE__);
chdir($phpfile['dirname']);
include("./mappemail_utils.php");

function build_table($rows){
    $tbody = array_reduce($rows, function($a, $b){return $a.="<tr><td>".implode("</td><td>",$b)."</td></tr>";});
    $thead = "<tr><th>" . implode("</th><th>", array_keys($rows[0])) . "</th></tr>";

    return "<table border=\"1\">\n<thead>$thead\n</thead><tbody>$tbody\n</table>";
}

$me='ndarmoni@xcastlabs.com';
$html = True;
$cr = $html ? "<br>" : "\r\n";
$agents_id_list='';
$list_count=0;
$results = array();

$recs = dbexecute("select distinct (agent_data.id)/*, call_status*/ from agent_data where agent_data.call_status in ('WU','NA') and agent_data.next_call_can_start between 1 and UNIX_TIMESTAMP() -1 limit 30;");

while ($rec=dbnext($recs))  {
    $list_count +=1;
    if($html) array_push($results,array('id' => $rec['id']/*,'call_status'=>$rec['call_status']*/));
    else $agents_id_list .= $rec['id'] . ($html ? "</b>" : "") . $cr ;
}
$wrapping_agents_exist = ($list_count === 0) ? (($html ? "<b>" : "") . "no " . ($html ? "</b>" : "")) : '';
$urgent = ($list_count > 0);
$body = "There are " . $wrapping_agents_exist. "agents in wrapup state for long time" . $cr . $cr;
if($list_count > 0) {
    if ($html) $agents_id_list = build_table($results);
    $body .= 'Agent IDs:' . $cr ;
    $body .= $agents_id_list;
    sendEmail($me, $me, (($list_count === 0) ? "no ": "")."agents are stuck in wrapup state", $body, $html, '','' , $urgent, '');
}

