<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['home_news_trend_submit'])) {

        $news_id_old = $_POST['news_id_old'];
        $news_id = $_POST['news_id'];
        $trending_news_id = $_POST['trending_news_id'];



//************ News Title Already Exist Check Starts ***************

        if($news_id_old != $news_id) {
            $listing_name_exist_check = mysqli_query($conn,"SELECT * FROM " . TBL . "news_trending WHERE news_id='" . $news_id . "' ");


            if (mysqli_num_rows($listing_name_exist_check) > 0) {


                $_SESSION['status_msg'] = "The Given Home Trending News is Already Exist Try Other!!!";

                header('Location: news-home-trending-edit.php?row=' . $trending_news_id);
                exit;


            }
        }

//************ Listing Name Already Exist Check Ends ***************


        $sql = mysqli_query($conn,"UPDATE  " . TBL . "news_trending SET news_id ='" . $news_id . "'
     where trending_news_id='" . $trending_news_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Home page Trending news has been Updated Successfully!!!";


            header('Location: news-home-trending.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: news-home-trending-edit.php?row=' . $trending_news_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: news-home-trending.php');
    exit;
}
?>