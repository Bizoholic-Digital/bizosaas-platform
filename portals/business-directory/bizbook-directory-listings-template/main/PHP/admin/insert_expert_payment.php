<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";
if (isset($_POST['payment_submit'])) {

    $cnt = count($_POST['payment_name']);

// *********** if Count of payment name is zero means redirect starts ********

    if($cnt == 0){
        header('Location: expert-add-new-payment.php');
        exit;
    }

// *********** if Count of payment name is zero means redirect ends ********

    for ($i = 0; $i < $cnt; $i++) {

        $payment_name = $_POST['payment_name'][$i];

        $payment_status = "Active";

        $payment_filter_pos_id = 1;


//************ Category Name Already Exist Check Starts ***************


        $payment_name_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "expert_payments  WHERE payment_name='" . $payment_name . "' ");

        if (mysqli_num_rows($payment_name_exist_check) > 0) {


            $_SESSION['status_msg'] = "The Given Payment name $payment_name is Already Exist Try Other!!!";

            header('Location: expert-add-new-payment.php');
            exit;


        }


        $sql = mysqli_query($conn, "INSERT INTO  " . TBL . "expert_payments (payment_name,payment_status,payment_cdt)
VALUES ('$payment_name','$payment_status','$curDate')");

    }

    if ($sql) {

        $_SESSION['status_msg'] = "Expert Payment(s) has been Added Successfully!!!";


        header('Location: expert-payment-accept.php');
        exit;

    } else {


        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: expert-add-new-payment.php');
        exit;
    }

}
?>