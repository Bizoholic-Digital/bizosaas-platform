<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['home_news_slider_submit'])) {

        $news_id_old = $_POST['news_id_old'];
        $news_id = $_POST['news_id'];
        $news_slider_id = $_POST['news_slider_id'];



//************ News Title Already Exist Check Starts ***************

        if($news_id_old != $news_id) {
            $listing_name_exist_check = mysqli_query($conn,"SELECT * FROM " . TBL . "news_slider WHERE news_id='" . $news_id . "' ");


            if (mysqli_num_rows($listing_name_exist_check) > 0) {


                $_SESSION['status_msg'] = "The Given Home Slider News is Already Exist Try Other!!!";

                header('Location: news-home-sliders-edit.php?row=' . $news_slider_id);
                exit;


            }
        }

//************ News Title Already Exist Check Ends ***************


        $sql = mysqli_query($conn,"UPDATE  " . TBL . "news_slider SET news_id ='" . $news_id . "'
     where news_slider_id='" . $news_slider_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Home page Slider news has been Updated Successfully!!!";


            header('Location: news-home-sliders.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: news-home-sliders-edit.php?row=' . $news_slider_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: news-home-sliders.php');
    exit;
}
?>