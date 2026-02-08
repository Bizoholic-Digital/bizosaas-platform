<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['transaction_submit'])) {

        $transaction_id = $_POST["transaction_id"];

        $transaction_qry = "DELETE FROM  " . TBL . "transactions  where transaction_id='" . $transaction_id . "'";


        $transaction_res = mysqli_query($conn,$transaction_qry);


        if ($transaction_res) {


            $_SESSION['status_msg'] = "Payment has been Deleted Successfully!!!";

            header('Location: admin-all-payments.php');

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-all-payments.php');
        }


    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-all-payments.php');
}