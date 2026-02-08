<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}


if(isset($_GET['adsstatusadsstatusadsstatusadsstatusadsstatus'])){

    $all_ads_enquiry_id = $_GET['adsstatusadsstatusadsstatusadsstatusadsstatus'];


    $sql = mysqli_query($conn,"UPDATE  " . TBL . "all_ads_enquiry SET ad_enquiry_status = 'Active'
     where all_ads_enquiry_id='" . $all_ads_enquiry_id . "'");

    if ($sql) {

        $_SESSION['status_msg'] = "Ads has been Approved Successfully!!!";


        header('Location: admin-current-ads.php');
        exit;

    } else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: admin-ads-request.php');
        exit;
    }

}else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-new-user-requests.php');
    exit;
}

?>