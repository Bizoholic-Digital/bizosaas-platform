<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";
if (isset($_POST['home_slider_news_submit'])) {

    $news_id = $_POST['news_id'];

    $news_slider_pos_id = 0;


//************ Slider News Already Exist Check Starts ***************


            $news_id_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "news_slider WHERE news_id='" . $news_id . "'");

            if (mysqli_num_rows($news_id_exist_check) > 0) {


                $_SESSION['status_msg'] = "The Selected News is Already Exist Try Other!!!";

                header('Location: news-home-sliders-add.php');
                exit;


            }

//************ Slider News Already Exist Check Ends ***************


        $sql = mysqli_query($conn, "INSERT INTO  " . TBL . "news_slider (news_id,news_slider_pos_id,news_slider_cdt)
VALUES ('$news_id','$news_slider_pos_id','$curDate')");
    

    if ($sql) {

        $_SESSION['status_msg'] = "Home Page Slider news has been Added Successfully!!!";


        header('Location: news-home-sliders.php');
        exit;

    } else {


        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: news-home-sliders.php');
        exit;
    }

}
?>