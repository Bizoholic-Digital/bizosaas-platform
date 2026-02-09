<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";

if ($_SERVER['REQUEST_METHOD']=='POST') {

    if (isset($_POST['target_submit'])) {


// Basic Personal Details
        $page_name = $_POST["page_name"];

        $page_seo_title = $_POST["page_seo_title"];
        $page_seo_keyword = addslashes($_POST["page_seo_keyword"]);
        $page_seo_description = addslashes($_POST["page_seo_description"]);
        $page_seo_schema = addslashes($_POST["page_seo_schema"]);

        $page_type = 1;

        $page_listings123 = $_POST["page_listings"];

        $prefix3 = '';
        foreach ($page_listings123 as $fruit3)
        {
            $page_listings .= $prefix3 .  $fruit3 ;
            $prefix3 = ',';
        }


        function checkPageSlug($link, $counter=1){
            global $conn;
            $newLink = $link;
            do{
                $checkLink = mysqli_query($conn, "SELECT page_id FROM " . TBL . "pages WHERE page_slug = '$newLink' AND page_type = 1");
                if(mysqli_num_rows($checkLink) > 0){
                    $newLink = $link.''.$counter;
                    $counter++;
                } else {
                    break;
                }
            } while(1);

            return $newLink;
        }


        $page_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $page_name));
        $page_slug = checkPageSlug($page_name1);


//    General insert Part Starts


        $sql_qry = "INSERT INTO " . TBL . "pages 
					(page_type, page_name
					,page_seo_title, page_seo_keyword, page_seo_description, page_seo_schema
					,page_listings, page_slug, page_last_edit, page_cdt) 
					VALUES 
					('$page_type', '$page_name'
					, '$page_seo_title', '$page_seo_keyword', '$page_seo_description',  '$page_seo_schema'
					, '$page_listings', '$page_slug', '$curDate', '$curDate')";

        $sql_res = mysqli_query($conn,$sql_qry);

        if ($sql_res) {

            $_SESSION['status_msg'] = "New Target Promotion Page has been created Successfully!!! ";

            header('Location: seo-target-promotion-all-pages.php');


        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: seo-target-promotion-all-pages.php');
        }

        //    General Insert Part Ends

    }
}else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: seo-target-promotion-all-pages.php');
}