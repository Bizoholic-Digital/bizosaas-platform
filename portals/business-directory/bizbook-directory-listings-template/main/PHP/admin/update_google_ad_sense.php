<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['google_ad_sense_submit'])) {


        $admin_google_ad_sense = addslashes($_POST["admin_google_ad_sense"]);


        $sql = mysqli_query($conn, "UPDATE  " . TBL . "footer SET  admin_google_ad_sense='" . $admin_google_ad_sense . "'
     where footer_id= 1");

        if ($sql) {

            $_SESSION['status_msg'] = "Google Ad Sense has been Updated Successfully!!!";


            header('Location: seo-google-adsense.php');
            exit;


        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: seo-google-ad-sense.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: seo-google-ad_sense-code.php');
    exit;
}
?>