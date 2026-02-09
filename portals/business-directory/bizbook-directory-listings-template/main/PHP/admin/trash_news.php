<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['news_submit'])) {

        $news_id = $_POST["news_id"];

        $news_image_old = $_POST["news_image_old"];

        $news_qry =
            " DELETE FROM  " . TBL . "news WHERE news_id='" . $news_id . "'";


        $news_res = mysqli_query($conn,$news_qry);


        if ($news_res) {
            unlink('../news/images/news/'.$news_image_old);  //Delete the banner image


            //Query to delete the page view starts

            $page_view_qry = "DELETE FROM  " . TBL . "page_views where news_id='" . $news_id . "'";

            $page_view_res = mysqli_query($conn,$page_view_qry);

            //Query to delete the page view ends


            $_SESSION['status_msg'] = "News/Magazine has been Permanently Deleted!!!";
            header('Location: news-all.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: news-delete.php?code=' . $news_id);
        }

        //    News Trash Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: news-all.php');
}