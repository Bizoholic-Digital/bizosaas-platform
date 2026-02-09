<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['home_news_social_submit'])) {

        $social_media_id = $_POST['social_media_id'];
        
        $social_media_name = $_POST['social_media_name'];
        $social_media_count = $_POST['social_media_count'];
        $social_media_link = $_POST['social_media_link'];
        $social_media_status = $_POST['social_media_status'];
        


        $sql = mysqli_query($conn,"UPDATE  " . TBL . "news_social_media SET social_media_name ='" . $social_media_name . "'
        , social_media_count ='" . $social_media_count . "' , social_media_link ='" . $social_media_link . "'
        , social_media_status ='" . $social_media_status . "'
         where social_media_id='" . $social_media_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Home page Social Media news has been Updated Successfully!!!";


            header('Location: news-home-social-media.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: news-home-social-media-edit.php?row=' . $social_media_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: news-home-social-media.php');
    exit;
}
?>