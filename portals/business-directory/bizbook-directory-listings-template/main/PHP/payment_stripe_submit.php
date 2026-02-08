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

//check if stripe token exist to proceed with payment

//if(!empty($_POST['stripeToken'])){

// get token and user details
// $stripeToken = $_POST['stripeToken'];
$custName = $_POST['first_name'];
$custEmail = $_POST['email_id'];
$cardNumber = $_POST['card_number'];
$cardCVC = $_POST['cardCVC'];
$cardExpMonth = $_POST['cardExpMonth'];
$cardExpYear = $_POST['cardExpYear'];
$path = $_POST['path'];

$address = $_SESSION['stripe_payment_user_address'];
$city = $_SESSION['stripe_payment_user_city'];
$state = $_SESSION['stripe_payment_user_state'];
$country = $_SESSION['stripe_payment_user_country'];
$zipCode = $_SESSION['stripe_payment_user_zip_code'];


$stripe_publishable_key = $footer_row['admin_stripe_id'];      //stripe publishable key
$stripe_secret_key = $footer_row['admin_stripe_secret_id'];   //stripe secret key
$admin_stripe_currency_code = $footer_row['admin_stripe_currency_code']; //stripe currency code


//include Stripe PHP library
require_once('payments/stripe/init.php');

//set stripe secret key and publishable key
$stripe = array(
    "secret_key" => $stripe_secret_key,
    "publishable_key" => $stripe_publishable_key
);

\Stripe\Stripe::setApiKey($stripe['secret_key']);

$stripeToken = \Stripe\Token::create([
    'card' => [
        'number' => $cardNumber,
        'exp_month' => $cardExpMonth,
        'exp_year' => $cardExpYear,
        'cvc' => $cardCVC,
    ],
]);


//add customer to stripe
$customer = \Stripe\Customer::create(array(
    'name' => $custName,
    'email' => $custEmail,
    'source' => $stripeToken['id'],
    "address" => ["city" => $city, "country" => $country, "line1" => $address, "line2" => "", "postal_code" => $zipCode, "state" => $state]
));

// item details for which payment made
$itemName = $user_plan_type['plan_type_name'] . " Plan from " . $footer_row['website_address'];
$itemNumber = $user_code;
$itemPrice = $user_plan_type['plan_type_price'];
$currency = $admin_stripe_currency_code;
$orderID = $user_code;

// details for which payment performed
try {
    $payDetails = \Stripe\Charge::create(array(
        'customer' => $customer['id'],
        'amount' => $itemPrice*100,
        'currency' => $currency,
        'description' => $itemName,
        'metadata' => ["order_id" => $user_code]
    ));
} catch (Stripe_CardError $e) {
    // Since it's a decline, Stripe_CardError will be caught
    $body = $e->getJsonBody();
    $err = $body['error'];

    echo 'Status is:' . $e->getHttpStatus() . "\n";
    echo 'Type is:' . $err['type'] . "\n";
    echo 'Code is:' . $err['code'] . "\n";
    // param is '' in this case
    echo 'Param is:' . $err['param'] . "\n";
    echo 'Message is:' . $err['message'] . "\n";
} catch (Exception $e) {
    echo $e->getMessage();
} catch (ErrorException $e) {
    echo $e->getMessage();
}


// get payment details
$paymenyResponse = $payDetails->jsonSerialize();

// check whether the payment is successful

if ($paymenyResponse['amount_refunded'] == 0 && empty($paymenyResponse['failure_code']) && $paymenyResponse['paid'] == 1 && $paymenyResponse['captured'] == 1) {

// transaction details
    $amountPaid1 = $paymenyResponse['amount'];

    $balanceTransaction = $paymenyResponse['balance_transaction'];

    $paidCurrency = $paymenyResponse['currency'];

    $paymentStatus = $paymenyResponse['status'];

    $user_code = $paymenyResponse['metadata']['order_id'];
    $amountPaid = $amountPaid1 / 100;

//insert transaction details into database

    $plan_type_details = mysqli_query($conn, "SELECT * FROM  " . TBL . "plan_type where plan_type_price='" . $amountPaid . "'");
    $plan_type_details_row = mysqli_fetch_array($plan_type_details);

    $plan_type_id = $plan_type_details_row['plan_type_id'];  //Plan Type Id

    $user_details = mysqli_query($conn, "SELECT * FROM  " . TBL . "users where user_code='" . $user_code . "'");
    $user_details_row = mysqli_fetch_array($user_details);

    $user_id = $user_details_row['user_id'];  //User Id
    
    $transaction_mode = 'Stripe';

    $transaction_qry = "INSERT INTO " . TBL . "transactions 
					( user_code, plan_type_id , user_id, transaction_amount, transaction_mode, transaction_currency, transaction_cdt) 
					VALUES 
					('$user_code', '$plan_type_id', '$user_id', '$amountPaid', '$transaction_mode', '$paidCurrency', '$curDate')";

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

    $traupqry = "UPDATE " . TBL . "transactions 
					  SET transaction_code = '$TransCode' 
					  WHERE transaction_id = $translastID";

    $traupres = mysqli_query($conn, $traupqry);

    if ($traupres && $paymentStatus == 'succeeded') {

        $lisupqry = "UPDATE " . TBL . "users 
					  SET payment_status = 'Paid' 
					  WHERE user_id = $user_id";

        $lisupres = mysqli_query($conn, $lisupqry);

        $_SESSION['register_status_msg'] = 1;

        $_SESSION['status_msg'] = $BIZBOOK['PAYMENT_SUCCESSFULL_USER_UPGRADE_SUCESS'];

        if ($path == 1) {

            unset($_SESSION['stripe_payment_user_country']);
            unset($_SESSION['stripe_payment_user_state']);
            unset($_SESSION['stripe_payment_user_city']);
            unset($_SESSION['stripe_payment_user_address']);
            unset($_SESSION['stripe_payment_user_zip_code']);
            unset($_SESSION['stripe_payment_user_contact_name']);
            unset($_SESSION['stripe_payment_user_contact_mobile']);
            unset($_SESSION['stripe_payment_user_contact_email']);

            header('Location: db-payment');
            exit;
        } else {
            header('Location: login?login=register');
            exit;
        }
    } //if order inserted successfully

    else {
        unset($_SESSION['stripe_payment_user_country']);
        unset($_SESSION['stripe_payment_user_state']);
        unset($_SESSION['stripe_payment_user_city']);
        unset($_SESSION['stripe_payment_user_address']);
        unset($_SESSION['stripe_payment_user_zip_code']);
        unset($_SESSION['stripe_payment_user_contact_name']);
        unset($_SESSION['stripe_payment_user_contact_mobile']);
        unset($_SESSION['stripe_payment_user_contact_email']);

        $_SESSION['status_msg'] = $BIZBOOK['STRIPE_PAYMENT_FAILURE_MESSAGE'];
        header('Location: stripe_payment');
        exit;
    }
} else {
    $_SESSION['status_msg'] = $BIZBOOK['STRIPE_PAYMENT_FAILURE_MESSAGE'];
    header('Location: stripe_payment');
    exit;
}
//}
// else{
//    $_SESSION['status_msg'] = "Token missing";
//    header('Location: stripe_payment');
//    exit;
//}