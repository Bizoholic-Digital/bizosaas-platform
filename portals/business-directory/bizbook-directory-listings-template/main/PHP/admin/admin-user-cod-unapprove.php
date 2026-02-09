<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}



if(isset($_GET['userstatususerstatususerstatususerstatususerstatus'])){

    $user_id = $_GET['userstatususerstatususerstatususerstatususerstatus'];


    $sql = mysqli_query($conn,"UPDATE  " . TBL . "users SET payment_status = ''
     where user_id='" . $user_id . "'");

    if ($sql) {

        $_SESSION['status_msg'] = "User COD has been Rejected Successfully!!!";


        header('Location: admin-new-cod-requests.php');
        exit;

    } else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: admin-new-cod-requests.php');
        exit;
    }

}else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-new-user-requests.php');
    exit;
}

?>