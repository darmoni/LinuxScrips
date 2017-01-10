#!/usr/bin/php -e
<?php

function _get_source_file_name()
{
    global $res_file;
    global $argv;
    if (($options = getopt("i:"))==TRUE)
    {
        $res_file = $options['i'];
        return $res_file;
    }
    else
    {
        echo "Usage: $argv[0] -i <input file name>\n";
        exit(0);
    }
}

$res_file = _get_source_file_name();
$data = fopen($res_file,"r");
if(!is_resource($data)) die ("Can not open results file $res_file!\n");
$topics = array("Time", "Queues", "Agents", "Conferences","% Idle", "Load", "Busy");
$headers = array("Time", "num_queues", "num_agents", "waiting", "logged_in", "available", "diff", "bridges", "participants", "idle", "load 1", "load 5", "load 15", "busy");
require_once 'Spreadsheet/Excel/Writer.php';

// Creating a workbook
$workbook = new Spreadsheet_Excel_Writer("$res_file.xls");
// Creating a worksheet
$worksheet =& $workbook->addWorksheet('results');
$topics_row = 0;
$row = 1;

$format_bold =& $workbook->addFormat();
$format_bold->setBold();

$format_header = array('bordercolor' => 'blue',
                'left' => 1,
                'bottom' => 1,
                'right' => 1,
                'top' => 1,
                'bold'=>'1',
              );
$format_title =& $workbook->addFormat($format_header);
$format_title->setColor('blue');
$format_title->setPattern(1);
$format_title->setFgColor('yellow');
$format_title->setAlign('center');

// topics
$topic = 0;
$worksheet->write($topics_row, 0, $topics[$topic++], $format_title);
$worksheet->write($topics_row, 1, $topics[$topic++], $format_title);
$worksheet->mergeCells($topics_row,1,$topics_row,3);
$worksheet->write($topics_row, 4, $topics[$topic++], $format_title);
$worksheet->mergeCells($topics_row,4,$topics_row,6);
$worksheet->write($topics_row, 7, $topics[$topic++], $format_title);
$worksheet->mergeCells($topics_row,7,$topics_row,8);
$worksheet->write($topics_row, 9, $topics[$topic++], $format_title);
$worksheet->write($topics_row, 10, $topics[$topic++], $format_title);
$worksheet->mergeCells($topics_row,10,$topics_row,12);
$worksheet->write($topics_row, 13, $topics[$topic++], $format_title); // last one, 

// Header
$worksheet->writeRow($row++, 0, $headers, $format_title);
// The actual data
while ($line = fgets($data, 2048)) {
    //$measurements = preg_split("/[\s,]+/",$line);
    $measurements = explode("\t",$line);
    $worksheet->writeRow($row, 0, $measurements);
    $the_row = $row+1;
    $formula="=100-J$the_row";
    $worksheet->writeFormula($row,13,$formula);
    $row++;
}
fclose($data);

/*
$worksheet->write(0, 0, 'Name');
$worksheet->write(0, 1, 'Age');
$worksheet->write(1, 0, 'John Smith');
$worksheet->write(1, 1, 30);
$worksheet->write(2, 0, 'Johann Schmidt');
$worksheet->write(2, 1, 31);
$worksheet->write(3, 0, 'Juan Herrera');
$worksheet->write(3, 1, 32);
*/
// Let's send the file
$workbook->close();
?>
