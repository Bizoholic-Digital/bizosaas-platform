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

    $user_code = $razorpayOrder['receipt'];
    $amount_paid = $razorpayOrder['amount']/100;
    $item_currency      = $razorpayOrder['currency'];

    $plan_type_details = mysqli_query($conn,"SELECT * FROM  " . TBL . "plan_type where plan_type_price='" . $amount_paid . "'");
    $plan_type_details_row = mysqli_fetch_array($plan_type_details);

    $plan_type_id = $plan_type_details_row['plan_type_id'];  //Plan Type Id

    $user_details = mysqli_query($conn,"SELECT * FROM  " . TBL . "users where user_code='" . $user_code . "'");
    $user_details_row = mysqli_fetch_array($user_details);

    $user_id = $user_details_row['user_id'];  //User Id
    
    $transaction_mode = 'Razor Pay';


    $transaction_qry = "INSERT INTO " . TBL . "transactions 
					( user_code, plan_type_id , user_id, transaction_amount, transaction_mode, transaction_currency, transaction_cdt) 
					VALUES 
					('$user_code', '$plan_type_id', '$user_id', '$amount_paid', '$transaction_mode', '$item_currency', '$curDate')";

    $transaction_res = mysqli_query($conn,$transaction_qry);
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

    $traupqry = "UPDATE " . TBL . "transactions 
					  SET transaction_code = '$TransCode' 
					  WHERE transaction_id = $translastID";

    $traupres = mysqli_query($conn,$traupqry);

    if ($traupres) {

        $lisupqry = "UPDATE " . TBL . "users 
					  SET payment_status = 'Paid' 
					  WHERE user_id = $user_id";

        $lisupres = mysqli_query($conn,$lisupqry);

        unset($_SESSION['razor_pay_payment_user_country']);
        unset($_SESSION['razor_pay_payment_user_state']);
        unset($_SESSION['razor_pay_payment_user_city']);
        unset($_SESSION['razor_pay_payment_user_address']);
        unset($_SESSION['razor_pay_payment_user_zip_code']);
        unset($_SESSION['razor_pay_payment_user_contact_name']);
        unset($_SESSION['razor_pay_payment_user_contact_mobile']);
        unset($_SESSION['razor_pay_payment_user_contact_email']);

        $_SESSION['status_msg'] = $BIZBOOK['PAYMENT_SUCCESSFULL_USER_UPGRADE_SUCESS'];

        header('Location: db-payment');
        exit;
    }

//    $html = "<p>Your payment was successful</p>
//             <p>Payment ID: {$_POST['razorpay_payment_id']}</p>
//             <p>Viki : {$razorpayOrder['receipt']}</p>
//             <p>Order Id : {$_POST['razorpay_order_id']}</p>
//             <p>Session Id: {$_SESSION['razorpay_order_id']}</p>";

} else {

    unset($_SESSION['razor_pay_payment_user_country']);
    unset($_SESSION['razor_pay_payment_user_state']);
    unset($_SESSION['razor_pay_payment_user_city']);
    unset($_SESSION['razor_pay_payment_user_address']);
    unset($_SESSION['razor_pay_payment_user_zip_code']);
    unset($_SESSION['razor_pay_payment_user_contact_name']);
    unset($_SESSION['razor_pay_payment_user_contact_mobile']);
    unset($_SESSION['razor_pay_payment_user_contact_email']);

    $_SESSION['status_msg'] = $BIZBOOK['RAZOR_PAYMENT_FAILURE_MESSAGE'];
    header('Location: db-payment');
    exit;

//    $html = "<p>Your payment failed</p>
//             <p>{$error}</p>";
}

//echo $html;
