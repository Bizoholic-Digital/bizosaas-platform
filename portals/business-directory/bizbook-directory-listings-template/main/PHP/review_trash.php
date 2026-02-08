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

if(isset($_GET['reviewreviewreviewreviewreviewreview'])){

    $review_id = $_GET['reviewreviewreviewreviewreviewreview'];


    $listing_qry =
        "DELETE  FROM " . TBL . "reviews  where review_id='" . $review_id . "'";

    $listing_res = mysqli_query($conn,$listing_qry);



    if ($listing_res) {

        $_SESSION['status_msg'] = $BIZBOOK['USER_REVIEW_DELETE_SUCCESSFUL_MESSAGE'];

        if(isset($_GET['way'])){
        header('Location: db-review');
        }else{
            header('Location: admin/admin-all-reviews.php');
        }
    } else {

        $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

        if(isset($_GET['way'])){
            header('Location: db-review');
        }else{
            header('Location: admin/admin-all-reviews.php');
        }
    }
    
}