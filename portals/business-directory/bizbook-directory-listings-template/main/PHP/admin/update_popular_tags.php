<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['popular_tags_submit'])) {

        $popular_tags_id = $_POST['popular_tags_id'];

        $popular_tags_name = $_POST['popular_tags_name'];
        $popular_tags_link = $_POST['popular_tags_link'];


        $sql = mysqli_query($conn,"UPDATE  " . TBL . "popular_tags SET  popular_tags_name='" . $popular_tags_name. "'
        ,popular_tags_link='" . $popular_tags_link. "'
        where popular_tags_id='" . $popular_tags_id . "'");


        if ($sql) {

            $_SESSION['status_msg'] = "Popular Tags has been Updated Successfully!!!";


            header('Location: admin-footer-popular-tags.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-footer-popular-tags.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-footer-popular-tags.php');
    exit;
}
?>