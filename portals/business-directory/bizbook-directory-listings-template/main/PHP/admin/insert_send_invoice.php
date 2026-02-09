<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['invoice_submit'])) {

// Basic Details
        $user_code = $_POST["user_code"];
        $transaction_amount = $_POST["transaction_amount"];
        $plan_type_id = $_POST["plan_type_id"];
        $item_currency = "USD";

        $user_details = mysqli_query($conn, "SELECT * FROM  " . TBL . "users where user_code='" . $user_code . "'");
        $user_details_row = mysqli_fetch_array($user_details);

        $user_id = $user_details_row['user_id'];  //User Id

//************************  Invoice PDF Upload starts  **************************

        if (!empty($_FILES['invoice_name']['name'])) {
            $file = rand(1000, 100000) . $_FILES['invoice_name']['name'];
            $file_loc = $_FILES['invoice_name']['tmp_name'];
            $file_size = $_FILES['invoice_name']['size'];
            $file_type = $_FILES['invoice_name']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/invoices/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $transaction_invoice = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $transaction_invoice = '';
            }
        }
//************************  Invoice PDF Upload Ends  **************************


        $transaction_qry = "INSERT INTO " . TBL . "transactions
					( user_code, plan_type_id , user_id, transaction_amount, transaction_invoice, transaction_currency, transaction_cdt) 
					VALUES 
					('$user_code', '$plan_type_id', '$user_id', '$transaction_amount', '$transaction_invoice', '$item_currency', '$curDate')";

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


        if ($traupres) {


            $_SESSION['status_msg'] = "Invoice Sent Successfully!!! ";

            header('Location: admin-invoice-shared.php');

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-send-invoice.php');

            exit;
        }

    } else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: admin-send-invoice.php');
    }


} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-send-invoice.php');
}