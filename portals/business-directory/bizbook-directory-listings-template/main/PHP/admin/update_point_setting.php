<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['cost_per_point_submit'])) {


        $cost_per_point = $_POST['cost_per_point'];
        
        $footer_id = 1;

        $sql = mysqli_query($conn,"UPDATE  " . TBL . "footer SET  cost_per_point='" . $cost_per_point . "' where footer_id='" . $footer_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Point Setting Data has been Updated Successfully!!!";


            header('Location: admin-point-setting.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-point-setting.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-point-setting.php');
    exit;
}
?>