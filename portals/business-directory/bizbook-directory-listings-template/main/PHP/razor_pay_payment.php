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


$razor_key_id = $footer_row['admin_razor_pay_key_id'];      //Razor pay key Id
$razor_secret_key = $footer_row['admin_razor_pay_key_id_secret'];   //Razor pay secret key
$razor_pay_currency_code = $footer_row['admin_razor_pay_currency_code']; //Razor pay currency code


require('payments/razorpay/razorpay-src/Razorpay.php');


// Create the Razorpay Order

use Razorpay\Api\Api;

$api = new Api($razor_key_id, $razor_secret_key);

$name = $_SESSION['razor_pay_payment_user_contact_name'];
$mobile_number = $_SESSION['razor_pay_payment_user_contact_mobile'];
$email_id_new = $_SESSION['razor_pay_payment_user_contact_email'];
$address = $_SESSION['razor_pay_payment_user_address'];
$city = $_SESSION['razor_pay_payment_user_city'];
$state = $_SESSION['razor_pay_payment_user_state'];
$country = $_SESSION['razor_pay_payment_user_country'];
$zipCode = $_SESSION['razor_pay_payment_user_zip_code'];

$company_name = $footer_row['admin_seo_title'];
$logo = $slash . "images/home/" . $footer_row['header_logo'];

// item details for which payment made
$itemName = $user_plan_type['plan_type_name'] . " Plan from " . $footer_row['website_address'];
$itemNumber = $user_code;
$itemPrice = $user_plan_type['plan_type_price'];

$orderID = $user_code;


//
// We create an razorpay order using orders api
// Docs: https://docs.razorpay.com/docs/orders
//
$orderData = [
    'receipt' => $itemNumber,
    'amount' => $itemPrice * 100, // 2000 rupees in paise
    'currency' => $razor_pay_currency_code,
    'payment_capture' => 1 // auto capture
];

$razorpayOrder = $api->order->create($orderData);

$razorpayOrderId = $razorpayOrder['id'];

$_SESSION['razorpay_order_id'] = $razorpayOrderId;

$displayAmount = $amount = $orderData['amount'];

if ($razor_pay_currency_code !== 'INR') {
    $url = "https://api.fixer.io/latest?symbols=$razor_pay_currency_code&base=INR";
    $exchange = json_decode(file_get_contents($url), true);

    $displayAmount = $exchange['rates'][$razor_pay_currency_code] * $amount / 100;
}

$checkout = 'automatic';

if (isset($_GET['checkout']) and in_array($_GET['checkout'], ['automatic', 'manual'], true)) {
    $checkout = $_GET['checkout'];
}

$data = [
    "key" => $razor_key_id,
    "amount" => $amount,
    "name" => $company_name,
    "description" => $itemName,
    "image" => $logo,
    "prefill" => [
        "name" => $name,
        "email" => $email_id_new,
        "contact" => $mobile_number,
    ],
    "notes" => [
        "address" => $address,
        "merchant_order_id" => "12312321",
    ],
    "theme" => [
        "color" => "#F37254"
    ],
    "order_id" => $razorpayOrderId,
];

if ($razor_pay_currency_code !== 'INR') {
    $data['display_currency'] = $razor_pay_currency_code;
    $data['display_amount'] = $displayAmount;
}

$json = json_encode($data);

?>
<body>
<style>
    .razorpay-payment-button {
        display: none !important;
    }
</style>
<?php echo $BIZBOOK['REDIRECTING_TO_RAZOR_PAY']; ?>
<form name="frmRazorPay1" id="frmRazorPay1" action="razor_pay_verify.php" method="POST">
    <script
        src="https://checkout.razorpay.com/v1/checkout.js"
        data-key="<?php echo $data['key'] ?>"
        data-amount="<?php echo $data['amount'] ?>"
        data-currency="<?php echo $razor_pay_currency_code; ?>"
        data-name="<?php echo $data['name'] ?>"
        data-image="<?php echo $data['image'] ?>"
        data-description="<?php echo $data['description'] ?>"
        data-prefill.name="<?php echo $data['prefill']['name'] ?>"
        data-prefill.email="<?php echo $data['prefill']['email'] ?>"
        data-prefill.contact="<?php echo $data['prefill']['contact'] ?>"
        data-notes.shopping_order_id="3456"
        data-order_id="<?php echo $data['order_id']; ?>"
        <?php if ($razor_pay_currency_code !== 'INR') { ?> data-display_amount="<?php echo $data['display_amount'] ?>" <?php } ?>
        <?php if ($razor_pay_currency_code !== 'INR') { ?> data-display_currency="<?php echo $data['display_currency'] ?>" <?php } ?>
    >
    </script>
    <!-- Any extra fields to be submitted with the form but not sent to Razorpay -->
    <input type="hidden" name="shopping_order_id" value="3456">
</form>
</body>

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<script>
    $(window).on('load', function () {
        jQuery('.razorpay-payment-button').click();
    });
</script>
<script>
    $(".modal").on("hidden.bs.modal", function () {
        window.location = "db-payment";
    });
</script>