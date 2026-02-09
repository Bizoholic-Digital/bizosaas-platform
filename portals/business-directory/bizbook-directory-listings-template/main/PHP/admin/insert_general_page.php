<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";

if ($_SERVER['REQUEST_METHOD']=='POST') {

    if (isset($_POST['general_submit'])) {

// Basic Personal Details
        $page_name = $_POST["page_name"];

        $page_template = $_POST["page_template"];
        $page_show_listings = $_POST["page_show_listings"];
        $page_show_products = $_POST["page_show_products"];
        $page_show_events = $_POST["page_show_events"];
        $page_show_blogs = $_POST["page_show_blogs"];
        $page_show_enquiry = $_POST["page_show_enquiry"];

        $page_description = addslashes($_POST["page_description"]);
        $page_css = addslashes($_POST["page_css"]);
        $page_js = addslashes($_POST["page_js"]);

        $page_seo_title = $_POST["page_seo_title"];
        $page_seo_keyword = addslashes($_POST["page_seo_keyword"]);
        $page_seo_description = addslashes($_POST["page_seo_description"]);
        $page_seo_schema = addslashes($_POST["page_seo_schema"]);

        $page_status = $_POST["page_status"];
        $page_visibilty = $_POST["page_visibilty"];

        $page_type = 2;

        $page_listings123 = $_POST["page_listings"];

        $prefix3 = '';
        foreach ($page_listings123 as $fruit3)
        {
            $page_listings .= $prefix3 .  $fruit3 ;
            $prefix3 = ',';
        }

        $page_products123 = $_POST["page_products"];

        $prefix = '';
        foreach ($page_products123 as $fruit)
        {
            $page_products .= $prefix .  $fruit ;
            $prefix = ',';
        }

        $page_events123 = $_POST["page_events"];

        $prefix1 = '';
        foreach ($page_events123 as $fruit1)
        {
            $page_events .= $prefix1 .  $fruit1 ;
            $prefix1 = ',';
        }

        $page_blogs123 = $_POST["page_blogs"];

        $prefix2 = '';
        foreach ($page_blogs123 as $fruit2)
        {
            $page_blogs .= $prefix2 .  $fruit2 ;
            $prefix2 = ',';
        }


        function checkPageSlug($link, $counter=1){
            global $conn;
            $newLink = $link;
            do{
                $checkLink = mysqli_query($conn, "SELECT page_id FROM " . TBL . "pages WHERE page_slug = '$newLink' AND page_type = 2");
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
					(page_type, page_name, page_template, page_show_listings
					,page_show_products, page_show_events, page_show_blogs, page_show_enquiry
					,page_description,page_css, page_js
					,page_seo_title, page_seo_keyword, page_seo_description, page_seo_schema
					,page_listings, page_products, page_events, page_blogs
					, page_status, page_visibilty, page_slug, page_last_edit, page_cdt) 
					VALUES 
					('$page_type', '$page_name', '$page_template', '$page_show_listings'
					,'$page_show_products', '$page_show_events', '$page_show_blogs', '$page_show_enquiry'
					, '$page_description', '$page_css', '$page_js'
					, '$page_seo_title', '$page_seo_keyword', '$page_seo_description',  '$page_seo_schema'
					, '$page_listings', '$page_products', '$page_events',  '$page_blogs'
					, '$page_status', '$page_visibilty', '$page_slug', '$curDate', '$curDate')";

        $sql_res = mysqli_query($conn,$sql_qry);

        if ($sql_res) {

            $_SESSION['status_msg'] = "New General Page has been created Successfully!!! ";

            header('Location: seo-general-all-pages.php');


        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: seo-general-all-pages.php');
        }

        //    General Insert Part Ends

    }
}else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: seo-general-all-pages.php');
}