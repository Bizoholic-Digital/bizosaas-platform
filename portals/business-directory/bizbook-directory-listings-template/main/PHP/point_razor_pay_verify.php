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


$razor_key_id = $footer_row['admin_razor_pay_key_id'];      //Razor pay key Id
$razor_secret_key = $footer_row['admin_razor_pay_key_id_secret'];   //Razor pay secret key
$razor_pay_currency_code = $footer_row['admin_razor_pay_currency_code']; //Razor pay currency code


require('payments/razorpay/razorpay-src/Razorpay.php');
use Razorpay\Api\Api;
use Razorpay\Api\Errors\SignatureVerificationError;

$success = true;

$error = "Payment Failed";

if (empty($_POST['razorpay_payment_id']) === false) {
    $api = new Api($razor_key_id, $razor_secret_key);

    try {
        // Please note that the razorpay order ID must
        // come from a trusted source (session here, but
        // could be database or something else)
        $attributes = array(
            'razorpay_order_id' => $_SESSION['razorpay_order_id'],
            'razorpay_payment_id' => $_POST['razorpay_payment_id'],
            'razorpay_signature' => $_POST['razorpay_signature']
        );

        $api->utility->verifyPaymentSignature($attributes);
    } catch (SignatureVerificationError $e) {
        $success = false;
        $error = 'Razorpay Error : ' . $e->getMessage();
    }
}

if ($success === true) {

    $razorpay_order_id = $_POST['razorpay_order_id'];
    $razorpayOrder = $api->order->fetch($razorpay_order_id);

    $point_enquiry_id = $razorpayOrder['receipt'];
    $amount_paid = $razorpayOrder['amount']/100;
    $item_currency      = $razorpayOrder['currency'];

    $all_points_enquiry = mysqli_query($conn, "SELECT * FROM  " . TBL . "all_points_enquiry where all_points_enquiry_id='" . $point_enquiry_id . "'");
    $all_points_enquiry_row = mysqli_fetch_array($all_points_enquiry);

    $user_id = $all_points_enquiry_row['user_id'];  //User Id

    $new_points = $all_points_enquiry_row['new_points'];  //New Points

    $user_details = mysqli_query($conn, "SELECT * FROM  " . TBL . "users where user_id='" . $user_id . "'");
    $user_details_row = mysqli_fetch_array($user_details);

    $user_code = $user_details_row['user_code'];  //User Code

    $existing_points = $user_details_row['user_points'];  //Existing Points

    $new_updated_points = $existing_points + $new_points; //New Total Points

    $transaction_mode = 'Razor Pay';


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

            $_SESSION['status_msg'] = $BIZBOOK['RAZOR_PAY_SUCCESSFULL_USER_POINT_UPGRADE_SUCESS'];

            header('Location: db-point-history');

        }
        exit;
    }

//    $html = "<p>Your payment was successful</p>
//             <p>Payment ID: {$_POST['razorpay_payment_id']}</p>
//             <p>Viki : {$razorpayOrder['receipt']}</p>
//             <p>Order Id : {$_POST['razorpay_order_id']}</p>
//             <p>Session Id: {$_SESSION['razorpay_order_id']}</p>";

} else {

    $_SESSION['status_msg'] = $BIZBOOK['RAZOR_POINT_PAYMENT_FAILURE_MESSAGE'];

    header('Location: buy-points');
    exit;

//    $html = "<p>Your payment failed</p>
//             <p>{$error}</p>";
}

//echo $html;
