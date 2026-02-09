<?php

if (file_exists('config/info.php')) {
    include('config/info.php');
}

//if (file_exists('config/user_authentication.php')) {
//    include('config/user_authentication.php');
//}

$user_id = $_SESSION['payment_user_id'];

if (isset($_SESSION['payment_user_id'])) {

    $user_details_row = getUser($user_id); //Fetch Logged In user data
    $user_plan = $user_details_row['user_plan']; //Fetch of Logged In user Plan
    $user_code = $user_details_row['user_code']; //Fetch of Logged In user Plan

    $user_plan_type = getPlanType($user_plan); //Fetch Logged In User Plan details and data
} else {

    header('Location: index');
    exit;
}

$footer_row = getAllFooter(); //Fetch Footer Data

$paytm_merchant_key = $footer_row['admin_paytm_merchant_key'];   //Paytm Merchant Key
$paytm_merchant_id = $footer_row['admin_paytm_merchant_id'];      //Paytm Merchant Id
$paytm_merchant_website = $footer_row['admin_paytm_merchant_website']; //Paytm Merchant Website

define('PAYTM_MERCHANT_KEY', $paytm_merchant_key); //Change this constant's value with Merchant key downloaded from portal
define('PAYTM_MERCHANT_MID', $paytm_merchant_id); //Change this constant's value with MID (Merchant ID) received from Paytm
define('PAYTM_MERCHANT_WEBSITE', $paytm_merchant_website); //Change this constant's value with Website name received from Paytm


header("Pragma: no-cache");
header("Cache-Control: no-cache");
header("Expires: 0");

// following files need to be included
require_once("payments/paytm/lib/config_paytm.php");
require_once("payments/paytm/lib/encdec_paytm.php");

$paytmChecksum = "";
$paramList = array();
$isValidChecksum = "FALSE";

$paramList = $_POST;
$paytmChecksum = isset($_POST["CHECKSUMHASH"]) ? $_POST["CHECKSUMHASH"] : ""; //Sent by Paytm pg

//Verify all parameters received from Paytm pg to your application. Like MID received from paytm pg is same as your application�s MID, TXN_AMOUNT and ORDER_ID are same as what was sent by you to Paytm PG for initiating transaction etc.
$isValidChecksum = verifychecksum_e($paramList, PAYTM_MERCHANT_KEY, $paytmChecksum); //will return TRUE or FALSE string.


if($isValidChecksum == "TRUE") {
    echo "<b>Checksum matched and following are the transaction details:</b>" . "<br/>";
    if ($_POST["STATUS"] == "TXN_SUCCESS") {

        $point_enquiry_id = $_POST["orderId"];
        $amount_paid = $_POST["txnAmount"];
        $item_currency      = "INR";

        $all_points_enquiry = mysqli_query($conn, "SELECT * FROM  " . TBL . "all_points_enquiry where all_points_enquiry_id='" . $point_enquiry_id . "'");
        $all_points_enquiry_row = mysqli_fetch_array($all_points_enquiry);

        $user_id = $all_points_enquiry_row['user_id'];  //User Id

        $new_points = $all_points_enquiry_row['new_points'];  //New Points

        $user_details = mysqli_query($conn, "SELECT * FROM  " . TBL . "users where user_id='" . $user_id . "'");
        $user_details_row = mysqli_fetch_array($user_details);

        $user_code = $user_details_row['user_code'];  //User Code

        $existing_points = $user_details_row['user_points'];  //Existing Points

        $new_updated_points = $existing_points + $new_points; //New Total Points

        $transaction_mode = 'PayTm';


        $transaction_qry = "INSERT INTO " . TBL . "point_transactions 
					( user_code, point_enquiry_id , user_id, transaction_amount, transaction_mode, transaction_currency, transaction_cdt) 
					VALUES 
					('$user_code', '$point_enquiry_id', '$user_id', '$amount_paid', '$transaction_mode', '$item_currency', '$curDate')";

        $transaction_res = mysqli_query($conn, $transaction_qry);
        $TransactionID = mysqli_insert_id($conn);
        $translastID = $TransactionID;

        switch (strlen($TransactionID)) {
            case 1:
                $TransactionID = '00' . $TransactionID;
                break;
            case 2:
                $TransactionID = '0' . $TransactionID;
                break;
            default:
                $TransactionID = $TransactionID;
                break;
        }

        $TransCode = 'TRANS' . $TransactionID;

        $traupqry = "UPDATE " . TBL . "point_transactions 
					  SET transaction_code = '$TransCode' 
					  WHERE transaction_id = $translastID";

        $traupres = mysqli_query($conn, $traupqry);

        if ($traupres) {

            $lisupqry = "UPDATE " . TBL . "users 
					  SET user_points = $new_updated_points 
					  WHERE user_id = $user_id";

            $lisupres = mysqli_query($conn, $lisupqry);

            if ($lisupres) {

                $lisupqry23 = "UPDATE " . TBL . "all_points_enquiry 
					  SET all_points_status = 'Paid' 
					  WHERE all_points_enquiry_id = $point_enquiry_id";

                $lisupres23 = mysqli_query($conn, $lisupqry23);

                $_SESSION['status_msg'] = $BIZBOOK['PAYTM_PAY_SUCCESSFULL_USER_POINT_UPGRADE_SUCESS'];

                header('Location: db-point-history');

            }
        }

        // echo "<b>Transaction status is success</b>" . "<br/>";
        //Process your transaction here as success transaction.
        //Verify amount & order id received from Payment gateway with your application's order id and amount.
    }
    else {

        $_SESSION['status_msg'] = $BIZBOOK['PAYTM_POINT_PAYMENT_FAILURE_MESSAGE'];

        header('Location: buy-points');
        exit;
        //echo "<b>Transaction status is failure</b>" . "<br/>";
    }

    if (isset($_POST) && count($_POST)>0 )
    {
        foreach($_POST as $paramName => $paramValue) {
            echo "<br/>" . $paramName . " = " . $paramValue;
        }
    }


}
else {

    $_SESSION['status_msg'] = $BIZBOOK['PAYTM_POINT_PAYMENT_FAILURE_MESSAGE'];

    header('Location: buy-points');
    exit;

//    echo "<b>Checksum mismatched.</b>";
    //Process transaction as suspicious.
}


