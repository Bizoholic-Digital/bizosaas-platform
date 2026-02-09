<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD']=='POST') {
    if (isset($_POST['stripe_dash_form_submit'])) {

        $_SESSION['payment_user_id'] = $_POST["stripe_dash_user_id"];
        $_SESSION['stripe_payment_user_country'] = $_POST["user_country"];
        $_SESSION['stripe_payment_user_state'] = $_POST["user_state"];
        $_SESSION['stripe_payment_user_city'] = $_POST["user_city"];
        $_SESSION['stripe_payment_user_address'] = $_POST["user_address"];
        $_SESSION['stripe_payment_user_zip_code'] = $_POST["user_zip_code"];
        $_SESSION['stripe_payment_user_contact_name'] = $_POST["user_contact_name"];
        $_SESSION['stripe_payment_user_contact_mobile'] = $_POST["user_contact_mobile"];
        $_SESSION['stripe_payment_user_contact_email'] = $_POST["user_contact_email"];

        header('Location: stripe_payment?path=dbx');
        exit;

    }
    
}else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: db-payment');
    exit();
}