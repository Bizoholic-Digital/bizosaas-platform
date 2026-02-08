<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['coupon_submit'])) {

        $coupon_id = $_POST["coupon_id"];

        $coupon_qry = "DELETE FROM  " . TBL . "coupons  where coupon_id='" . $coupon_id . "'";


        $coupon_res = mysqli_query($conn,$coupon_qry);


        if ($coupon_res) {

           //Query to delete the page view starts

            $page_view_qry = "DELETE FROM  " . TBL . "page_views where coupon_id='" . $coupon_id . "'";

            $page_view_res = mysqli_query($conn,$page_view_qry);

            //Query to delete the page view ends

            $_SESSION['status_msg'] = "Coupon has been Deleted Successfully!!!";

            header('Location: admin-coupons.php');

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-coupons.php');
        }


    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-coupons.php');
}