#!/usr/bin/php -e
<?php

$options = getopt("i:l:");
function _get_source_file_name()
{
    global $res_file;
    global $argv;
    global $options;
    if (isset($options['i']))
    {
        $res_file = $options['i'];
        //echo "Found input file name = $res_file \n";
        return $res_file;
    }
    else
    {
        echo "Usage: $argv[0] -i <input file name>\n";
        exit(0);
    }
}
$files = array();
$res_file = _get_source_file_name();
$load_threshold = 5;
if (isset($options['l']))
{
    $load_threshold = $options['l'];
    //echo "Found load_threshold = $load_threshold \n";
}

if(!is_file($res_file)) {
    //$files = glob($res_file);
    $last_line = exec("ls $res_file", $files);
    if(count($files)>1) {
        global $res_file;
        sort($files);
        $patterns = array('/\*/', '/\?/');
        $output_filename = preg_replace($patterns,'_',$res_file);
        $path_parts = pathinfo($output_filename);
        $path_parts['filename'] .= '.'.date("Ymdhis");
        $output_filename = $path_parts['dirname'].'/'.$path_parts['filename'];
        foreach($files as $res) {
            if (is_file($res)) system("cat $res >> $output_filename", $retval);
        }
        if(is_file($output_filename)) $res_file = $output_filename;
    }
}
$data = fopen($res_file,"r");
if(!is_resource($data)) die ("Can not open results file $res_file!\n");

$topics = array("Time", "Queues", "Agents", "Conferences","% Idle", "Load", "% Busy");
$headers = array("Time", "Number of queues", "Number of agents", "Waiting Calls", "Logged in", "Available", "Not Available", "Bridges", "Participants", "Idle",
    "1 Minute Average Load", "5 Minutes Average Load", "15 Minutes Average Load", "Busy");
require_once 'Spreadsheet/Excel/Writer.php';

// Creating a workbook
$filename = pathinfo($res_file, PATHINFO_DIRNAME);
$filename .= "/". basename($res_file, '.csv'). '.xls';
$workbook = new Spreadsheet_Excel_Writer($filename);
// Creating a worksheet
$worksheet =& $workbook->addWorksheet('results');
$topics_row = 0;
$row = 1;
$load_index = array_search("1 Minute Average Load", $headers);

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
$format_title->setTextWrap(true);

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
$has_high_load = false;
while ($line = fgets($data, 2048)) {
    $row++;
    $measurements = array_slice(explode("\t",$line), 0 , count($headers)-1);
    $formula="=100-J$row";
    $measurements [] = $formula;
    if(!$has_high_load && $measurements[$load_index] > $load_threshold)
        $has_high_load = true;
    $worksheet->writeRow($row-1, 0, $measurements);
}
fclose($data);
if($has_high_load) {
    $data = fopen($res_file,"r");
    if(!is_resource($data)) die ("Can not open results file $res_file!\n");

    $worksheet =& $workbook->addWorksheet('high load');
    $worksheet->select();
    $source_rows = $row;  // we will copy from source from 0 to $rows, into the new sheet
    $topics_row = 0;

    $row = 1;
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
        $measurements = array_slice(explode("\t",$line), 0 , count($headers)-1);
        if($measurements[$load_index] > $load_threshold) {
            $row++;
            $formula="=100-J$row";
            $measurements [] = $formula;
            $worksheet->writeRow($row-1, 0, $measurements);
        }
    }
    fclose($data);
}
$workbook->close();
?>
