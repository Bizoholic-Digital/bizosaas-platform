<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if(isset($_GET['newssubscribersnewssubscribersnewssubscribersnewssubscribersnewssubscribersnewssubscribers'])){

    $news_subscribers_id = $_GET['newssubscribersnewssubscribersnewssubscribersnewssubscribersnewssubscribersnewssubscribers'];


    $news_subscribers_qry =
        "DELETE  FROM " . TBL . "news_subscribers  where news_subscribers_id='" . $news_subscribers_id . "'";

    $news_subscribers_res = mysqli_query($conn,$news_subscribers_qry);


        if ($news_subscribers_res) {

            $_SESSION['status_msg'] = "News Subscriber has been Permanently Deleted!!!";


            header('Location: news-subscribers.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: news-subscribers.php');
        }
    
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: news-subscribers.php');
}