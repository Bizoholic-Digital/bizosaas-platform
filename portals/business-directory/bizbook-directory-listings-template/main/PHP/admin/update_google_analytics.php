<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['google_analytics_submit'])) {


        $admin_google_analytics = addslashes($_POST["admin_google_analytics"]);


        $sql = mysqli_query($conn, "UPDATE  " . TBL . "footer SET  admin_google_analytics='" . $admin_google_analytics . "'
     where footer_id= 1");

        if ($sql) {

            $_SESSION['status_msg'] = "Google Analytics has been Updated Successfully!!!";


            header('Location: seo-google-analytics-code.php');
            exit;


        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: seo-google-analytics-code.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: seo-google-analytics-code.php');
    exit;
}
?>