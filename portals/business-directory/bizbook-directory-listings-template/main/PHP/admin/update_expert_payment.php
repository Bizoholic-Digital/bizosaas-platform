<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['payment_submit'])) {

        $payment_id = $_POST['payment_id'];
        $payment_name = $_POST['payment_name'];
        $payment_status = "Active";


//************ Category Name Already Exist Check Starts ***************


        $payment_name_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "expert_payments  WHERE payment_name='" . $payment_name . "' AND payment_id != $payment_id ");

        if (mysqli_num_rows($payment_name_exist_check) > 0) {


            $_SESSION['status_msg'] = "The Given Payment name is Already Exist Try Other!!!";

            header('Location: expert-edit-payment.php?row=' . $payment_id);
            exit;


        }

//************ Category Name Already Exist Check Ends ***************

        $sql = mysqli_query($conn, "UPDATE  " . TBL . "expert_payments SET payment_name='" . $payment_name . "'
        , payment_status='" . $payment_status . "' where payment_id='" . $payment_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Expert Payment has been Updated Successfully!!!";


            header('Location: expert-payment-accept.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: expert-edit-payment.php?row=' . $payment_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: expert-all-payment.php');
    exit;
}
?>