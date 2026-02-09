<?php
//database configuration
if (file_exists('config/info.php')) {
    include('config/info.php');
}


//get search term
//$searchTerm = $_GET['term'];

$display_json = array();
//get matched data from skills table
//$qry ="SELECT * FROM " . TBL . "cities WHERE state_id IN (663,664,665,666,667,668,669,670,671,672,673,674,675)  ORDER BY city_name ASC";
$qry ="SELECT * FROM " . TBL . "blogs ORDER BY blog_name ASC";
$query = mysqli_query($conn,$qry);
while ($row = mysqli_fetch_array($query)) {
   // $display_json[] = $row['blog_name'];
    $blogg_name = urlModifier($row['blog_slug']);
    $display_json[] = array( 'label'=> $row['blog_name'],'link'=> $webpage_full_link.'blog/'.$blogg_name);

}

echo json_encode($display_json);

?>