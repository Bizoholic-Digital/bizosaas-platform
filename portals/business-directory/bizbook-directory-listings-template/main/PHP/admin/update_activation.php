<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['code_activation_submit'])) {


        $purchase_code = $_POST['purchase_code'];


// Surrounding whitespace can cause a 404 error, so trim it first
        $purchase_code = trim($purchase_code);

// Make sure the purchase code looks valid before sending it to RN53

        $data_array['website_purchase_code'] = $purchase_code;
        $data_array['website_complete_url'] = 'http://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];

// Build the request & Send the request with warnings supressed

        $ch = curl_init();
        curl_setopt_array($ch, array(
            CURLOPT_URL => "http://directoryfinder.net/sales-verification/updation_wizard.php",
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 20,
            CURLOPT_POST => count($data_array),
            CURLOPT_POSTFIELDS => $data_array
        ));

// Send the request with warnings supressed
        $response = @curl_exec($ch);
// Handle connection errors (such as an API outage)

// HTTP 405 indicates that the purchase code doesn't exist
        if ($response == 405) {
            $_SESSION['status_msg'] = "Error connecting to API !! Try Later!!!";

            header('Location: activate.php');
            exit;
        }

// HTTP 404 indicates that the purchase code doesn't exist
        if ($response == 404) {
            $_SESSION['status_msg'] = "The Entered purchase code was invalid!!!";

            header('Location: activate.php');
            exit;
        }

// HTTP 202 indicates that the purchase code doesn't exist
        if ($response == 202) {
            $_SESSION['status_msg'] = "Failed to validate code due to an error !! Try Later!!!";

            header('Location: activate.php');
            exit;
        }

// HTTP 200 indicates that the purchase code valid
        if ($response == 200) {

            $sql = mysqli_query($conn, "UPDATE  " . TBL . "admin SET activation_date = '" . $curDate . "', expiry_date='" . $activation_expiry_date . "'
        , activation_status ='" . $activation_status_activated . "', activation_code ='" . $purchase_code . "'  where admin_type = 'Super Admin'");
            
            $_SESSION['status_msg'] = "Activation code has been Updated Successfully!!!";

            header('Location: activate.php');
            exit;
        } else {

            //$_SESSION['status_msg'] = $response;
            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: activate.php');
            exit;
        }

    } else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: activate.php');
        exit;
    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: activate.php');
    exit;
}
?>