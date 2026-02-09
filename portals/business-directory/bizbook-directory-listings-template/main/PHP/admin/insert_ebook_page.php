<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['ebook_submit'])) {

// Basic Personal Details
        $page_name = $_POST["page_name"];
        $page_name_2 = $_POST["page_name_2"];
        $page_download_link = $_POST["page_download_link"];

        $page_description = addslashes($_POST["page_description"]);
        $page_css = addslashes($_POST["page_css"]);
        $page_js = addslashes($_POST["page_js"]);

        $page_seo_title = $_POST["page_seo_title"];
        $page_seo_keyword = addslashes($_POST["page_seo_keyword"]);
        $page_seo_description = addslashes($_POST["page_seo_description"]);
        $page_seo_schema = addslashes($_POST["page_seo_schema"]);

        $page_status = $_POST["page_status"];
        $page_visibilty = $_POST["page_visibilty"];

        $page_type = 3;


        if (!empty($_FILES['page_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['page_image']['name'];
            $file_loc = $_FILES['page_image']['tmp_name'];
            $file_size = $_FILES['page_image']['size'];
            $file_type = $_FILES['page_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/services/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image_1 = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image_1);
                $page_image = compressImage($event_image_1, $file_loc, $folder, $new_size);
            } else {
                $page_image = '';
            }
        }

        function checkPageSlug($link, $counter = 1)
        {
            global $conn;
            $newLink = $link;
            do {
                $checkLink = mysqli_query($conn, "SELECT page_id FROM " . TBL . "pages WHERE page_slug = '$newLink' AND page_type = 3");
                if (mysqli_num_rows($checkLink) > 0) {
                    $newLink = $link . '' . $counter;
                    $counter++;
                } else {
                    break;
                }
            } while (1);

            return $newLink;
        }


        $page_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $page_name));
        $page_slug = checkPageSlug($page_name1);


//    Ebook Insert Part Starts


        $sql_qry = "INSERT INTO " . TBL . "pages 
					(page_type, page_name, page_name_2,page_download_link,page_description,page_css, page_js
					,page_seo_title, page_seo_keyword, page_seo_description, page_seo_schema, page_image, page_status, page_visibilty, page_slug, page_last_edit, page_cdt) 
					VALUES 
					('$page_type', '$page_name', '$page_name_2', '$page_download_link', '$page_description', '$page_css'
					, '$page_js', '$page_seo_title', '$page_seo_keyword', '$page_seo_description',  '$page_seo_schema', '$page_image', '$page_status', '$page_visibilty', '$page_slug', '$curDate', '$curDate')";

        $sql_res = mysqli_query($conn, $sql_qry);

        if ($sql_res) {

            $_SESSION['status_msg'] = "New E-Book has been created Successfully!!! ";

            header('Location: seo-ebook-all-pages.php');


        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: seo-ebook-all-pages.php');
        }

        //    E-Book Insert Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: seo-ebook-all-pages.php');
}