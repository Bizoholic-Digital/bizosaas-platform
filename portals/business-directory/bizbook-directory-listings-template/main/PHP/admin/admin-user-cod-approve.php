<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}



if(isset($_GET['userstatususerstatususerstatususerstatususerstatus'])){

    $user_id = $_GET['userstatususerstatususerstatususerstatususerstatus'];

//Update Transaction Table starts
    
    $amount_paid         = $_GET['amtranamttranamtranamttransamtranamttrans'];
    $item_currency      = "USD"; 

    $plan_type_details = mysqli_query($conn,"SELECT * FROM  " . TBL . "plan_type where plan_type_price='" . $amount_paid . "'");
    $plan_type_details_row = mysqli_fetch_array($plan_type_details);

    $plan_type_id = $plan_type_details_row['plan_type_id'];  //Plan Type Id

    $user_details = mysqli_query($conn,"SELECT * FROM  " . TBL . "users where user_id='" . $user_id . "'");
    $user_details_row = mysqli_fetch_array($user_details);

    $user_code = $user_details_row['user_code'];  //User Id


    $transaction_qry = "INSERT INTO " . TBL . "transactions 
					( user_code, plan_type_id , user_id, transaction_amount, transaction_currency, transaction_cdt) 
					VALUES 
					('$user_code', '$plan_type_id', '$user_id', '$amount_paid', '$item_currency', '$curDate')";

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

//Update Transaction Table ends
    echo 
    
    $sql = mysqli_query($conn,"UPDATE  " . TBL . "users SET payment_status = 'Paid'
     where user_id='" . $user_id . "'");

    if ($sql) {

        $_SESSION['status_msg'] = "User COD has been Upgraded To PAID Successfully!!!";


        header('Location: admin-new-cod-requests.php');
        exit;

    } else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: admin-new-cod-requests.php');
        exit;
    }

}else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-new-user-requests.php');
    exit;
}

?>