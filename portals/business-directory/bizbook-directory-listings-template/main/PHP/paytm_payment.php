<?php
if (file_exists('config/info.php')) {
    include('config/info.php');
}


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


header("Pragma: no-cache");
header("Cache-Control: no-cache");
header("Expires: 0");
// following files need to be included
require_once("payments/paytm/lib/config_paytm.php");
require_once("payments/paytm/lib/encdec_paytm.php");

$checkSum = "";
$paramList = array();


$contact_name = $_SESSION['paytm_payment_user_contact_name'];
$mobile_number = $_SESSION['paytm_payment_user_contact_mobile'];
$email_id_new = $_SESSION['paytm_payment_user_contact_email'];
$address = $_SESSION['paytm_payment_user_address'];
$city = $_SESSION['paytm_payment_user_city'];
$state = $_SESSION['paytm_payment_user_state'];
$country = $_SESSION['paytm_payment_user_country'];
$zipCode = $_SESSION['paytm_payment_user_zip_code'];

$company_name = $footer_row['admin_seo_title'];
$logo = $slash . "images/home/" . $footer_row['header_logo'];

$paytm_merchant_key = $footer_row['admin_paytm_merchant_key'];   //Paytm Merchant Key
$paytm_merchant_id = $footer_row['admin_paytm_merchant_id'];      //Paytm Merchant Id
$paytm_merchant_website = $footer_row['admin_paytm_merchant_website']; //Paytm Merchant Website

define('PAYTM_MERCHANT_KEY', $paytm_merchant_key); //Change this constant's value with Merchant key downloaded from portal
define('PAYTM_MERCHANT_MID', $paytm_merchant_id); //Change this constant's value with MID (Merchant ID) received from Paytm
define('PAYTM_MERCHANT_WEBSITE', $paytm_merchant_website); //Change this constant's value with Website name received from Paytm

// item details for which payment made
$itemName = $user_plan_type['plan_type_name'] . " Plan from " . $footer_row['website_address'];
$itemNumber = $user_code;
$itemPrice = $user_plan_type['plan_type_price'];

$orderID = $user_code;

$ORDER_ID = $itemNumber;
$CUST_ID = $itemNumber.'1';
$INDUSTRY_TYPE_ID = "Retail";
$CHANNEL_ID = "WEB";
$TXN_AMOUNT = $itemPrice;
$CALLBACK_URL = $webpage_full_link.'paytm_response';

// Create an array having all required parameters for creating checksum.
$paramList["MID"] = PAYTM_MERCHANT_MID;
$paramList["ORDER_ID"] = $ORDER_ID;
$paramList["CUST_ID"] = $CUST_ID;
$paramList["INDUSTRY_TYPE_ID"] = $INDUSTRY_TYPE_ID;
$paramList["CHANNEL_ID"] = $CHANNEL_ID;
$paramList["TXN_AMOUNT"] = $TXN_AMOUNT;
$paramList["WEBSITE"] = PAYTM_MERCHANT_WEBSITE;

$paramList["CALLBACK_URL"] = $CALLBACK_URL;
$paramList["MSISDN"] = $mobile_number; //Mobile number of customer
$paramList["EMAIL"] = $email_id_new; //Email ID of customer
$paramList["VERIFIED_BY"] = "EMAIL"; //
$paramList["IS_USER_VERIFIED"] = "YES"; //
//Here checksum string will return by getChecksumFromArray() function.
$checkSum = getChecksumFromArray($paramList,PAYTM_MERCHANT_KEY);

?>
<html>
<head>
    <title>Merchant Check Out Page</title>
</head>
<body>
<center><h1>Please do not refresh this page...</h1></center>
<form method="post" action="<?php echo PAYTM_TXN_URL ?>" name="f1">
    <table border="1">
        <tbody>
        <?php
        foreach($paramList as $name => $value) {
            echo '<input type="text" name="' . $name .'" value="' . $value . '">';
        }
        ?>
        <input type="hidden" name="CHECKSUMHASH" value="<?php echo $checkSum ?>">
        </tbody>
    </table>
    <script type="text/javascript">
        document.f1.submit();
    </script>
</form>
</body>
</html>