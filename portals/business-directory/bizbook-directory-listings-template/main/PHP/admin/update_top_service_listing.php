<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['home_top_service_listing_submit'])) {


        $top_service_provider_category_id = $_POST['category_id'];
        $top_service_provider_listings = $_POST['listing_id'];
        $all_top_service_listings = $_POST['all_top_service_listings'];

        $listing_id_old = $_POST['listing_id_old'];

//************ Listing Id Already Exist Check Starts ***************


        $sub_category_name_exist_check = mysqli_query($conn,"SELECT * FROM " . TBL . "top_service_providers  WHERE FIND_IN_SET('" .$top_service_provider_listings . "',top_service_provider_listings) AND top_service_provider_category_id = '$top_service_provider_category_id' ");

        if (mysqli_num_rows($sub_category_name_exist_check) > 0) {


            $_SESSION['status_msg'] = "The Given Listing name is Already Exist Try Other!!!";

            header('Location: admin-home-top-services-edit.php?row=' . $listing_id_old.'&&cat=' . $top_service_provider_category_id);
            exit;


        }

//************ Listing Id Already Exist Check Ends ***************

//*************** Convert String to array then replacing the updated listing id starts *************

        $myarray = explode(',', $all_top_service_listings);

        foreach($myarray as $key => $val)
        {
            if ($val == $listing_id_old) {
                $myarray[$key] = $top_service_provider_listings;
            }

        }


//*************** Convert String to array then replacing the updated listing id ends *************

        // ************** Convert Array To String Starts ********************
        $prefix1 = $fruitList = '';
        foreach ($myarray as $fruit1)
        {
            $top_service_provider_listings1 .= $prefix1 .  $fruit1 ;
            $prefix1 = ',';
        }


 // ************** Convert Array To String ends ********************

        $sql = mysqli_query($conn,"UPDATE  " . TBL . "top_service_providers SET top_service_provider_listings = '$top_service_provider_listings1'
     where top_service_provider_category_id='" . $top_service_provider_category_id . "'");
        
        if ($sql) {

            $_SESSION['status_msg'] = "Top Service Listing has been Updated Successfully!!!";


            header('Location: admin-home-top-services.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-home-top-services-edit.php?row=' . $listing_id_old. '&&cat=' . $top_service_provider_category_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-home-top-services-edit.php?row=' . $listing_id_old.'&&cat=' . $top_service_provider_category_id);
    exit;
}
?>