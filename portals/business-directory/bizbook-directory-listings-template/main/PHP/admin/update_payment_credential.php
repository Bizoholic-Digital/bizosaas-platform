<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['payment_credential_submit'])) {



        $admin_cod_status = $_POST['admin_cod_status'];

        $admin_paypal_id = $_POST['admin_paypal_id'];
        $admin_paypal_currency_code = $_POST['admin_paypal_currency_code'];
        $admin_paypal_status = $_POST['admin_paypal_status'];

        $admin_stripe_id = $_POST['admin_stripe_id'];
        $admin_stripe_secret_id = $_POST['admin_stripe_secret_id'];
        $admin_stripe_currency_code = $_POST['admin_stripe_currency_code'];
        $admin_stripe_status = $_POST['admin_stripe_status'];

        $admin_razor_pay_key_id = $_POST['admin_razor_pay_key_id'];
        $admin_razor_pay_key_id_secret = $_POST['admin_razor_pay_key_id_secret'];
        $admin_razor_pay_currency_code = $_POST['admin_razor_pay_currency_code'];
        $admin_razor_pay_status = $_POST['admin_razor_pay_status'];

        $admin_paytm_merchant_id = $_POST['admin_paytm_merchant_id'];
        $admin_paytm_merchant_key = $_POST['admin_paytm_merchant_key'];
        $admin_paytm_merchant_website = $_POST['admin_paytm_merchant_website'];
        $admin_paytm_status = $_POST['admin_paytm_status'];

        
        $footer_id = $_POST['footer_id'];


        if($_POST['footer_path'] == "cod"){

            $sql = mysqli_query($conn,"UPDATE  " . TBL . "footer SET  admin_cod_status='" . $admin_cod_status. "'  
        where footer_id='" . $footer_id . "'");

        }elseif($_POST['footer_path'] == "paypal"){

            $sql = mysqli_query($conn,"UPDATE  " . TBL . "footer SET admin_paypal_id='" . $admin_paypal_id. "'
        , admin_paypal_status='" . $admin_paypal_status. "' , admin_paypal_currency_code='" . $admin_paypal_currency_code. "' 
        where footer_id='" . $footer_id . "'");

        }elseif($_POST['footer_path'] == "stripe"){

            $sql = mysqli_query($conn,"UPDATE  " . TBL . "footer SET admin_stripe_id='" . $admin_stripe_id . "'
        , admin_stripe_status='" . $admin_stripe_status. "' , admin_stripe_secret_id='" . $admin_stripe_secret_id. "' 
        , admin_stripe_currency_code='" . $admin_stripe_currency_code. "'  
        where footer_id='" . $footer_id . "'");

        }elseif($_POST['footer_path'] == "razor_pay"){

            $sql = mysqli_query($conn,"UPDATE  " . TBL . "footer SET admin_razor_pay_key_id_secret='" . $admin_razor_pay_key_id_secret . "'
        , admin_razor_pay_status='" . $admin_razor_pay_status. "' , admin_razor_pay_key_id='" . $admin_razor_pay_key_id. "' 
        , admin_razor_pay_currency_code='" . $admin_razor_pay_currency_code. "'  
        where footer_id='" . $footer_id . "'");

        }elseif($_POST['footer_path'] == "paytm"){

            $sql = mysqli_query($conn,"UPDATE  " . TBL . "footer SET admin_paytm_merchant_id='" . $admin_paytm_merchant_id . "'
        , admin_paytm_merchant_key='" . $admin_paytm_merchant_key. "' , admin_paytm_merchant_website='" . $admin_paytm_merchant_website. "' 
        , admin_paytm_status='" . $admin_paytm_status. "'  
        where footer_id='" . $footer_id . "'");
        }

        if ($sql) {

            $_SESSION['status_msg'] = "Admin Payment Credential Data has been Updated Successfully!!!";


            header('Location: admin-payment-credentials.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-payment-credentials.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-payment-credentials.php');
    exit;
}
?>