<?php
if (file_exists('config/info.php')) {
    include('config/info.php');
}

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

$user_id = $_SESSION['user_id'];

if (isset($user_id)) {

    $user_details_row = getUser($user_id); //Fetch Logged In user data
    $user_plan = $user_details_row['user_plan']; //Fetch of Logged In user Plan

    $user_plan_type = getPlanType($user_plan); //Fetch Logged In User Plan details and data
}else{

    header('Location: index');
    exit;
}

$footer_row = getAllFooter(); //Fetch Footer Data


$point_enquiry_id = $_SESSION['point_enquiry_id'];  //point enquiry id
$point_total_cost = $_SESSION['point_total_cost'];  //point enquiry id



//$paypal_url='https://www.sandbox.paypal.com/cgi-bin/webscr'; // Test Paypal API URL

$paypal_url='https://www.paypal.com/cgi-bin/webscr';  //Live Paypal API URL

$admin_paypal_id = $footer_row['admin_paypal_id']; // Admin Paypal email ID
$admin_paypal_currency_code = $footer_row['admin_paypal_currency_code']; // Admin Paypal Currency Code

$link_with_payment_failure = $webpage_full_link. "point_payment_paypal_failure";  //URL Payment Failure Link
$link_with_payment_success = $webpage_full_link. "point_payment_paypal_success";  //URL Payment Failure Link

?>

<body onload="document.getElementById('frmPayPal1').submit();">
<?php echo $BIZBOOK['REDIRECTING_TO_PAYPAL']; ?>
<form action="<?php echo $paypal_url; ?>" method="post" name="frmPayPal1" id="frmPayPal1">
    <input type="hidden" name="business" value="<?php echo $admin_paypal_id; ?>">
    <input type="hidden" name="cmd" value="_xclick">
    <input type="hidden" name="item_name" value="<?php echo $footer_row['website_address']; ?>">
    <input type="hidden" name="item_number" value="<?php echo $point_enquiry_id; ?>">
    <input type="hidden" name="credits" value="510">
    <input type="hidden" name="userid" value="1">
    <input type="hidden" name="amount" value="<?php echo $point_total_cost; ?>">
    <input type="hidden" name="no_shipping" value="0">
    <input type="hidden" name="currency_code" value="<?php echo $admin_paypal_currency_code; ?>">
    <input type="hidden" name="handling" value="0">
    <input type="hidden" name="cancel_return" value="<?php echo $link_with_payment_failure; ?>">
    <input type="hidden" name="return" value="<?php echo $link_with_payment_success; ?>">
</form>
</body>