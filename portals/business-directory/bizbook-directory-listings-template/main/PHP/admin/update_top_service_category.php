<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['home_top_service_category_submit'])) {


        $top_service_provider_category_id = $_POST['category_id'];

        $category_id_old = $_POST['category_id_old'];

        $top_service_provider_id = $_POST['top_service_provider_id'];

//************ Listing Id Already Exist Check Starts ***************


        $sub_category_name_exist_check = mysqli_query($conn,"SELECT * FROM " . TBL . "top_service_providers  WHERE top_service_provider_category_id = '" .$top_service_provider_category_id . "' ");

        if (mysqli_num_rows($sub_category_name_exist_check) > 0) {


            $_SESSION['status_msg'] = "The Given Category name is Already Exist Try Other!!!";

            header('Location: admin-home-top-services-change.php?row=' . $category_id_old. '&&col=' . $top_service_provider_id);
            exit;


        }

//************ Listing Id Already Exist Check Ends ***************

// ************ Fetch 5 default listings under given category and insert in top services starts *****************

        $list_sql = "SELECT * FROM " . TBL . "listings  WHERE category_id= '$top_service_provider_category_id' AND listing_is_delete != '2' ORDER BY listing_id DESC LIMIT 5";
        $list_sql_rs = mysqli_query($conn, $list_sql);
         while ($listrow = mysqli_fetch_array($list_sql_rs)) {

             $listing_id123[] = $listrow["listing_id"];
         }

        $prefix1 = '';

        foreach ($listing_id123 as $fruit1)
        {
            $top_service_provider_listings .= $prefix1 .  $fruit1 ;
            $prefix1 = ',';
        }
        
// ************ Fetch 5 default listings under given category and insert in top services ends *****************

        $sql = mysqli_query($conn,"UPDATE  " . TBL . "top_service_providers SET top_service_provider_listings = '" . $top_service_provider_listings. "'
     ,top_service_provider_category_id='" . $top_service_provider_category_id . "' where top_service_provider_id='" . $top_service_provider_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Top Service Category has been Updated Successfully!!!";


            header('Location: admin-home-top-services.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-home-top-services-change.php?row=' . $category_id_old. '&&col=' . $top_service_provider_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-home-top-services-change.php?row=' . $category_id_old.'&&col=' . $top_service_provider_id);
    exit;
}
?>