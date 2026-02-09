<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['service_expert_admin_setting_submit'])) {

        $admin_service_expert_email = $_POST['admin_service_expert_email'];
        $admin_service_expert_mobile = $_POST['admin_service_expert_mobile'];
        $admin_service_expert_whatsapp = $_POST['admin_service_expert_whatsapp'];

        $footer_id = $_POST['footer_id'];

        $sql1 = mysqli_query($conn, "UPDATE  " . TBL . "footer SET admin_service_expert_email='" . $admin_service_expert_email . "'
        , admin_service_expert_mobile='" . $admin_service_expert_mobile . "'
        , admin_service_expert_whatsapp='" . $admin_service_expert_whatsapp . "'
         where footer_id ='" . $footer_id . "'");

        if ($sql1) {

            $_SESSION['status_msg'] = "Service Expert Admin Setting Data has been Updated Successfully!!!";

            header('Location: expert-admin-info.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: expert-admin-info.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: expert-admin-info.php');
    exit;
}
?>