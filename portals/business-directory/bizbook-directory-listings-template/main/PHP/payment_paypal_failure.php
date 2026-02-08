<?php
if (file_exists('config/info.php')) {
    include('config/info.php');
}
$_SESSION['status_msg'] = $BIZBOOK['PAYPAL_PAYMENT_FAILURE_MESSAGE'];

header('Location: db-payment');
exit;
?>