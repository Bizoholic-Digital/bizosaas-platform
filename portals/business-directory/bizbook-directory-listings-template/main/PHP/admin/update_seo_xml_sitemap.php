<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['seo_xml_sitemap_submit'])) {
        

        $_FILES['sitemap_file']['name'];

        if (!empty($_FILES['sitemap_file']['name'])) {
            //$file = rand(1000, 100000) . $_FILES['sitemap_file']['name'];
            $file = 'sitemap.xml';
            $file_loc = $_FILES['sitemap_file']['tmp_name'];
            $file_size = $_FILES['sitemap_file']['size'];
            $file_type = $_FILES['sitemap_file']['type'];
            $allowed = array("application/xml","text/xml", "text/plain");
            if (in_array($file_type, $allowed)) {
                $folder = "../";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);

                if(file_exists("../$file")){
                    unlink("../$file");    //Delete old sitemap xml file
                }
                $upload_logic = move_uploaded_file($file_loc, $folder . $event_image);  //Uploading new file
               // $sitemap_file = compressImage($event_image, $file_loc, $folder, $new_size);

                if($upload_logic){
                    $_SESSION['status_msg'] = "XML file have been successfully uploaded";

                    header('Location: seo-xml-sitemap.php');
                    exit;
                }else{
                    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

                    header('Location: seo-xml-sitemap.php');
                    exit;
                }

            } else {
                $_SESSION['status_msg'] = "The Uploaded file was not supported format !! Please use XML file";

                header('Location: seo-xml-sitemap.php');
                exit;
            }
        } else {
            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: seo-xml-sitemap.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: seo-xml-sitemap.php');
    exit;
}
?>