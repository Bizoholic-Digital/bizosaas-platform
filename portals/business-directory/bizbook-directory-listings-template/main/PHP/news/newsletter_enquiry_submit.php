<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists("news-config-info.php")) {
    include("news-config-info.php");
}

if (file_exists('../config/news_page_authentication.php')) {
    include('../config/news_page_authentication.php');
}

if ($_SERVER['REQUEST_METHOD']=='POST') {

//    Newsletter Insert Part Starts

    $subscriber_email_id = $_POST["news_newsletter_subscribe_name"];


    $news_subscribers_qry = "INSERT INTO " . TBL . "news_subscribers
					(subscriber_email_id, news_subscribers_cdt)
					VALUES 
					('$subscriber_email_id', '$curDate')";

    $news_subscribers_res = mysqli_query($conn,$news_subscribers_qry);


    if ($news_subscribers_res) {

            echo '1';

    } else {
        echo '2';
    }
}else {

    header('Location: index');
    exit;
}

//    Newsletter Insert Part Ends

