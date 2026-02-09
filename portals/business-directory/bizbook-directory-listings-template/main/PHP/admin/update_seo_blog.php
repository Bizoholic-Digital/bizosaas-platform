<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['blog-seo-submit'])) {

        $blog_id = $_POST['blog_id'];


        $seo_title = $_POST['seo_title'];
        $seo_keywords = $_POST['seo_keywords'];
        $seo_description = $_POST['seo_description'];


        $sql = mysqli_query($conn,"UPDATE  " . TBL . "blogs SET  seo_title='" . $seo_title. "'
        ,seo_keywords='" . $seo_keywords. "', seo_description='" . $seo_description . "'
        where blog_id='" . $blog_id . "'");


        if ($sql) {

            $_SESSION['status_msg'] = "Blog SEO options has been Updated Successfully!!!";


            header('Location: seo-all-blog-options.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: seo-all-blog-options.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: seo-all-blog-options.php');
    exit;
}
?>