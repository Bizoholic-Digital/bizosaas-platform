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


        $payment_qry =
            " DELETE FROM  " . TBL . "expert_payments WHERE payment_id='" . $payment_id . "'";


        $payment_res = mysqli_query($conn,$payment_qry);


        if ($payment_res) {

            $_SESSION['status_msg'] = "Expert Payment has been Permanently Deleted!!!";


            header('Location: expert-payment-accept.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: expert-delete-payment.php?row=' . $payment_id);
        }

        //    expert Trash Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: expert-payment-accept.php');
}