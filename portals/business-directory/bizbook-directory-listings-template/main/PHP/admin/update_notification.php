<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['notification_submit'])) {


        $notification_id = $_POST['notification_id'];

        $notification_title = $_POST["notification_title"];
        $notification_message = $_POST["notification_message"];
        $notification_link = $_POST["notification_link"];
        $notification_cdt = $_POST["notification_cdt"];
        $notification_user = $_POST["notification_user"];



        $sql = mysqli_query($conn,"UPDATE  " . TBL . "notifications SET notification_title='" . $notification_title . "',notification_message='" . $notification_message . "', notification_user='" . $notification_user. "'
        ,notification_link='" . $notification_link . "', notification_cdt='" . $curDate. "'
     where notification_id='" . $notification_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "User Notification has been Updated Successfully!!!";


            header('Location: admin-notification-all.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-edit-notification.php?id=' . $notification_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-notification-all.php');
    exit;
}
?>