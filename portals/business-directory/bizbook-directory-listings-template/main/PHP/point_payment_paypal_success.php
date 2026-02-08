<?php
if (file_exists('config/info.php')) {
    include('config/info.php');
}


$point_enquiry_id = $_REQUEST['item_number'];
$paypal_transaction_id = $_REQUEST['tx']; // PayPal transaction ID
$amount_paid = $_REQUEST['amt']; // PayPal received amount
$item_currency = $_REQUEST['cc']; // PayPal received currency type

$all_points_enquiry = mysqli_query($conn, "SELECT * FROM  " . TBL . "all_points_enquiry where all_points_enquiry_id='" . $point_enquiry_id . "'");
$all_points_enquiry_row = mysqli_fetch_array($all_points_enquiry);

$user_id = $all_points_enquiry_row['user_id'];  //User Id

$new_points = $all_points_enquiry_row['new_points'];  //New Points

$user_details = mysqli_query($conn, "SELECT * FROM  " . TBL . "users where user_id='" . $user_id . "'");
$user_details_row = mysqli_fetch_array($user_details);

$user_code = $user_details_row['user_code'];  //User Code

$existing_points = $user_details_row['user_points'];  //Existing Points

$new_updated_points = $existing_points + $new_points; //New Total Points

$transaction_mode = 'PayPal';


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

        $_SESSION['status_msg'] = $BIZBOOK['PAYPAL_PAY_SUCCESSFULL_USER_POINT_UPGRADE_SUCESS'];

        header('Location: db-point-history');

    }


}

