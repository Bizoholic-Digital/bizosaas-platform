<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['seo_submit'])) {
        
        $path = $_POST["path"];
        $id = $_POST["id"];
        $seo_title = $_POST["seo_title"];
        $seo_description = $_POST["seo_description"];
        $seo_keywords= $_POST["seo_keywords"];


        if($path == 'listing'){

            $sql = mysqli_query($conn,"UPDATE  " . TBL . "listings SET seo_title='" . $seo_title. "', seo_description='" . $seo_description . "'
     ,seo_keywords='" . $seo_keywords . "'
     where listing_id='" . $id . "'");
            
        }elseif ($path == 'event'){
            
            $sql = mysqli_query($conn,"UPDATE  " . TBL . "events SET seo_title='" . $seo_title. "', seo_description='" . $seo_description . "'
     ,seo_keywords='" . $seo_keywords . "'
     where event_id='" . $id . "'");
            
        }elseif ($path == 'blog'){
            
            $sql = mysqli_query($conn,"UPDATE  " . TBL . "blogs SET seo_title='" . $seo_title. "', seo_description='" . $seo_description . "'
     ,seo_keywords='" . $seo_keywords . "'
     where blog_id='" . $id . "'");
            
        }elseif ($path == 'product'){
            
            $sql = mysqli_query($conn,"UPDATE  " . TBL . "products SET seo_title='" . $seo_title. "', seo_description='" . $seo_description . "'
     ,seo_keywords='" . $seo_keywords . "'
     where product_id='" . $id . "'");
            
        }else{
            
            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: db-seo');
            exit;
        }

        

        if ($sql) {

            $_SESSION['status_msg'] = $BIZBOOK['USER_SEO_UPDATE_SUCCESS_MESSAGE'];

            header('Location: db-seo');
            exit;

        } else {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: db-seo');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: db-seo');
    exit;
}
?>