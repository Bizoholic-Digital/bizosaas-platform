<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['delete_ad_submit'])) {

        $path = $_POST['path'];
        $all_ads_enquiry_id = $_POST['all_ads_enquiry_id'];

        $ads_qry =
            "DELETE FROM  " . TBL . "all_ads_enquiry  where all_ads_enquiry_id='" . $all_ads_enquiry_id . "'";


        $ads_res = mysqli_query($conn,$ads_qry);


        if ($ads_res) {

            $_SESSION['status_msg'] = "Ad has been Deleted Successfully!!!";

            if($path == 1){

                header('Location: admin-current-ads.php');
                exit;

            }else{

                header('Location: admin-ads-request.php');
                exit;
            }

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-current-ads.php');
            exit;
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-current-ads.php');
}