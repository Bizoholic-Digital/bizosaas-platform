<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['home_featured_listing_submit'])) {

        $listing_id_old = $_POST['listing_id_old'];
        $listing_id = $_POST['listing_id'];
        $featured_listing_id = $_POST['featured_listing_id'];



//************ Listing Name Already Exist Check Starts ***************

        if($listing_id_old != $listing_id) {
            $listing_name_exist_check = mysqli_query($conn,"SELECT * FROM " . TBL . "featured_listings  WHERE listing_id='" . $listing_id . "' ");


            if (mysqli_num_rows($listing_name_exist_check) > 0) {


                $_SESSION['status_msg'] = "The Given Home Popular Business Listing is Already Exist Try Other!!!";

                header('Location: admin-home-popular-business-edit.php?row=' . $listing_id_old);
                exit;


            }
        }

//************ Listing Name Already Exist Check Ends ***************


        $sql = mysqli_query($conn,"UPDATE  " . TBL . "featured_listings SET listing_id ='" . $listing_id . "'
     where featured_listing_id='" . $featured_listing_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Home page Popular Business Listing has been Updated Successfully!!!";


            header('Location: admin-home-popular-business.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-home-popular-business-edit.php?row=' . $listing_id_old);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-home-popular-business.php');
    exit;
}
?>