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


        $notification_id = $_POST['notification_id']; //Session User Code

        $sql =
            " DELETE FROM  " . TBL . "notifications  WHERE notification_id='" . $notification_id . "'";


        $sql_res = mysqli_query($conn,$sql);


        if ($sql_res) {

            $_SESSION['status_msg'] = "User Notifications has been Permenantly Deleted!!!";


            header('Location: admin-notification-all.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-notification-delete.php?row=' . $notification_id);
            exit;
        }

    }
    else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: admin-notification-all.php');
        exit;
    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-notification-all.php');
    exit;
}
?>