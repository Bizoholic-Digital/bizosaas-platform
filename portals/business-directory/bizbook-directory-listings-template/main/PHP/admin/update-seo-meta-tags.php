<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['seo_page_submit'])) {

        $seo_page_id = $_POST['seo_page_id'];

        $seo_page_title = $_POST["seo_page_title"];
        $seo_page_description = addslashes($_POST["seo_page_description"]);
        $seo_page_keywords = addslashes($_POST["seo_page_keywords"]);



        $sql = mysqli_query($conn, "UPDATE  " . TBL . "seo SET seo_page_title='" . $seo_page_title . "'
        , seo_page_description='" . $seo_page_description . "', seo_page_keywords='" . $seo_page_keywords . "'
        , seo_page_edit_cdt='" . $curDate . "'
     where seo_page_id='" . $seo_page_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "SEO Meta Tags been Updated Successfully!!!";

                header('Location: seo-meta-tags.php');
                exit;


        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location:seo-meta-tags-edit.php?row=' . $seo_page_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: seo-meta-tags.php');
    exit;
}
?>