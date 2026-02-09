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

        $news_id = $_POST['news_id'];
        $news_slider_id = $_POST['news_slider_id'];

        $country_qry =
            " DELETE FROM  " . TBL . "news_slider WHERE news_slider_id='" . $news_slider_id . "'";


        $country_res = mysqli_query($conn,$country_qry);


        if ($country_res) {

            $_SESSION['status_msg'] = "Home News Slider has been Permanently Deleted!!!";

            header('Location: news-home-sliders.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: news-home-sliders-delete.php?row=' . $news_slider_id);
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: news-home-sliders.php');
}