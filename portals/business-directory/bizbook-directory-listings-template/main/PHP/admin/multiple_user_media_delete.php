<?php

if (file_exists('config/info.php')) {
    include('config/info.php');
}

$deleteids_arr = $_POST['deleteids_arr'];


foreach ($deleteids_arr as $deleteid) {

    $null = '';

    list($a, $b, $c) = explode('-^^-', $deleteid);

    //Delete the Listing profile image starts

    if ($a == "list_prof") {

        $listing_qry = "UPDATE  " . TBL . "listings SET profile_image='" . $null . "' where listing_id='" . $c . "'";

        $listing_res = mysqli_query($conn, $listing_qry);

        unlink('../images/listings/' . $b);  //Delete the profile image
    }

    //Delete the Listing profile image ends

    //Delete the Events image starts

    if ($a == "event") {

        $event_qry = "UPDATE  " . TBL . "events SET event_image='" . $null . "' where event_id='" . $c . "'";

        $event_res = mysqli_query($conn, $event_qry);

        unlink('../images/events/' . $b);  //Delete the Events image
    }

    //Delete the Events image ends

    //Delete the Products image starts

    if ($a == "product") {

        $product_qry = "UPDATE " . TBL . "products SET `gallery_image` = TRIM(BOTH ',' FROM REPLACE(CONCAT(',', `gallery_image`, ','), ',$b,', ','))
       WHERE FIND_IN_SET('$b', `gallery_image`) AND product_id ='" . $c . "'";

        $product_res = mysqli_query($conn, $product_qry);

        unlink('../images/products/' . $b);  //Delete the Products image
    }

    //Delete the Products image ends

    //Delete the Expert image starts

    if ($a == "expert") {

        $expert_qry = "UPDATE  " . TBL . "experts SET profile_image='" . $null . "' where expert_id='" . $c . "'";

        $expert_res = mysqli_query($conn, $expert_qry);

        unlink('../service-experts/images/services/' . $b);  //Delete the Experts image
    }

    //Delete the Expert image ends

    //Delete the Job image starts

    if ($a == "job") {

        $job_qry = "UPDATE  " . TBL . "jobs SET company_logo='" . $null . "' where job_id='" . $c . "'";

        $job_res = mysqli_query($conn, $job_qry);

        unlink('../jobs/images/jobs/' . $b);  //Delete the Jobs image
    }

    //Delete the Job image ends

    //Delete the Coupon image starts

    if ($a == "coupon") {

        $coupon_qry = "UPDATE  " . TBL . "coupons SET coupon_photo='" . $null . "' where coupon_id='" . $c . "'";

        $coupon_res = mysqli_query($conn, $coupon_qry);

        unlink('../images/user/' . $b);  //Delete the coupons image
    }

    //Delete the Coupon image ends

    //Delete the Ads image starts

    if ($a == "ads") {

        $ads_qry = "UPDATE  " . TBL . "all_ads_enquiry SET ad_enquiry_photo='" . $null . "' where all_ads_enquiry_id='" . $c . "'";

        $ads_res = mysqli_query($conn, $ads_qry);

        unlink('../images/ads/' . $b);  //Delete the Ads image
    }

    //Delete the Ads image ends

    //Delete the Blog image starts

    if ($a == "blog") {

        $blog_qry = "UPDATE  " . TBL . "blogs SET blog_image='" . $null . "' where blog_id='" . $c . "'";

        $blog_res = mysqli_query($conn, $blog_qry);

        unlink('../images/blogs/' . $b);  //Delete the Blog image
    }

    //Delete the Blog image ends

    //Delete the User Profile image starts

    if ($a == "user_profile") {

        $user_profile_qry = "UPDATE  " . TBL . "users SET profile_image='" . $null . "' where user_id='" . $c . "'";

        $user_profile_res = mysqli_query($conn, $user_profile_qry);

        unlink('../images/blogs/' . $b);  //Delete the User profile image
    }

    //Delete the User profile image ends

    //Delete the Listing Service image starts

    if ($a == "listing_service") {

        $listing_service_qry = "UPDATE " . TBL . "listings SET `service_image` = TRIM(BOTH ',' FROM REPLACE(CONCAT(',', `service_image`, ','), ',$b,', ','))
       WHERE FIND_IN_SET('$b', `service_image`) AND listing_id ='" . $c . "'";

        $listing_service_res = mysqli_query($conn, $listing_service_qry);

        unlink('../images/services/' . $b);  //Delete the Listing Service image
    }

    //Delete the Listing Service image ends

    //Delete the Listing Gallery image starts

    if ($a == "listing_gallery") {

        $listing_gallery_qry = "UPDATE " . TBL . "listings SET `gallery_image` = TRIM(BOTH ',' FROM REPLACE(CONCAT(',', `gallery_image`, ','), ',$b,', ','))
       WHERE FIND_IN_SET('$b', `gallery_image`) AND listing_id ='" . $c . "'";

        $listing_gallery_res = mysqli_query($conn, $listing_gallery_qry);

        unlink('../images/listings/' . $b);  //Delete the Listing Gallery image
    }

    //Delete the Listing Gallery image ends


}

echo 1;
exit;