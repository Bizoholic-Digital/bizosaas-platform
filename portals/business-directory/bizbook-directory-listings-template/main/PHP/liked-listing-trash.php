<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if(file_exists('config/user_authentication.php'))
{
    include('config/user_authentication.php');
}

if(file_exists('config/info.php'))
{
    include('config/info.php');
}

if(isset($_GET['likedlistinglikedlistinglikedlistinglikedlistinglikedlisting'])){

    $review_id = $_GET['likedlistinglikedlistinglikedlistinglikedlistinglikedlisting'];


    $listing_qry =
        "DELETE  FROM " . TBL . "listing_likes  where listing_likes_id='" . $review_id . "'";

    $listing_res = mysqli_query($conn,$listing_qry);



    if ($listing_res) {

        $_SESSION['status_msg'] = $BIZBOOK['LIKED_LISTING_DELETED_SUCCESS_MESSAGE'];


            header('Location: db-like-listings');

    } else {

        $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];


            header('Location:db-liked-listings');

    }


}