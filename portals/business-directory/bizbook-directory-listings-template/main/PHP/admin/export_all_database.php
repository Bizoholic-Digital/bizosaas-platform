<?php

/* Backup Database Using PHP Function */
include "config/info.php";

//ENTER THE RELEVANT INFO BELOW
$mysqlUserName = DB_USERNAME;                    //DB Username
$mysqlPassword = DB_PASSWORD;                        //DB Password
$mysqlHostName = DB_HOSTNAME;               //DB Hostname
$DbName = DB_NAME;                //DB Name

$backup_name = "Directory_Finder_Database";                //Backup Download file Name
//$tables             = "Your tables";
$tables = array('vv_admin', 'vv_advertisement', 'vv_all_ads_enquiry', 'vv_all_ads_price', 'vv_all_featured_filters', 'vv_all_listing_filters', 'vv_all_texts', 'vv_blogs', 'vv_categories', 'vv_cities', 'vv_countries', 'vv_enquiries', 'vv_events', 'vv_featured_cities'
, 'vv_featured_listings', 'vv_footer', 'vv_index_ad', 'vv_listing_likes', 'vv_listing_other_info', 'vv_listings', 'vv_messages', 'vv_notifications', 'vv_page_views', 'vv_plan_type', 'vv_price_table'
, 'vv_reviews', 'vv_services', 'vv_states', 'vv_sub_categories', 'vv_top_categories', 'vv_top_events', 'vv_top_service_providers', 'vv_transactions', 'vv_trend_categories', 'vv_trending_listings', 'vv_users'); //add all table names here


//or add 5th parameter(array) of specific tables:    array("mytable1","mytable2","mytable3") for multiple tables

Export_Database($mysqlHostName, $mysqlUserName, $mysqlPassword, $DbName, $tables = false, $backup_name);

function Export_Database($host, $user, $pass, $name, $tables = false, $backup_name)
{
    $mysqli = new mysqli($host, $user, $pass, $name);
    $mysqli->select_db($name);
    $mysqli->query("SET NAMES 'utf8'");

    $queryTables = $mysqli->query('SHOW TABLES');
    while ($row = $queryTables->fetch_row()) {
        $target_tables[] = $row[0];
    }
    if ($tables !== false) {
        $target_tables = array_intersect($target_tables, $tables);
    }
    foreach ($target_tables as $table) {
        $result = $mysqli->query('SELECT * FROM ' . $table);
        $fields_amount = $result->field_count;
        $rows_num = $mysqli->affected_rows;
        $res = $mysqli->query('SHOW CREATE TABLE ' . $table);
        $TableMLine = $res->fetch_row();
        $content = (!isset($content) ? '' : $content) . "\n\n" . $TableMLine[1] . ";\n\n";

        for ($i = 0, $st_counter = 0; $i < $fields_amount; $i++, $st_counter = 0) {
            while ($row = $result->fetch_row()) { //when started (and every after 100 command cycle):
                if ($st_counter % 100 == 0 || $st_counter == 0) {
                    $content .= "\nINSERT INTO " . $table . " VALUES";
                }
                $content .= "\n(";
                for ($j = 0; $j < $fields_amount; $j++) {
                    $row[$j] = str_replace("\n", "\\n", addslashes($row[$j]));
                    if (isset($row[$j])) {
                        $content .= '"' . $row[$j] . '"';
                    } else {
                        $content .= '""';
                    }
                    if ($j < ($fields_amount - 1)) {
                        $content .= ',';
                    }
                }
                $content .= ")";
                //every after 100 command cycle [or at last line] ....p.s. but should be inserted 1 cycle earlier
                if ((($st_counter + 1) % 100 == 0 && $st_counter != 0) || $st_counter + 1 == $rows_num) {
                    $content .= ";";
                } else {
                    $content .= ",";
                }
                $st_counter = $st_counter + 1;
            }
        }
        $content .= "\n\n\n";
    }
    $backup_name = $backup_name ? $backup_name . "__(" . date('d-m-Y') . ")" . ".sql" : $name . "__(" . date('d-m-Y') . ")" . ".sql";
    // $backup_name = $backup_name ? $backup_name : $name.".sql";
    header('Content-Type: application/octet-stream');
    header("Content-Transfer-Encoding: Binary");
    header("Content-disposition: attachment; filename=\"" . $backup_name . "\"");
    echo $content;
    exit;

}

header("location:admin-export.php");

?>
