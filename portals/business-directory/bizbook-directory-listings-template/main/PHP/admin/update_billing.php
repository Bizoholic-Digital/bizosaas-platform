<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['billing_submit'])) {


        $user_id = $_POST['user_id'];


// Update Billing details of user starts

        $user_country = $_POST["user_country"];
        $user_state = $_POST["user_state"];
        $user_city = $_POST["user_city"];
        $user_address = $_POST["user_address"];
        $user_zip_code = $_POST["user_zip_code"];
        $user_contact_name = $_POST["user_contact_name"];
        $user_contact_mobile = $_POST["user_contact_mobile"];
        $user_contact_email = $_POST["user_contact_email"];

        $upqry = "UPDATE " . TBL . "users  SET user_country = '$user_country'
        , user_state = '$user_state', user_city = '$user_city', user_address = '$user_address'
        , user_zip_code = '$user_zip_code', user_contact_name = '$user_contact_name'
        , user_contact_mobile = '$user_contact_mobile', user_contact_email = '$user_contact_email' WHERE user_id = $user_id";

        $upres = mysqli_query($conn,$upqry);

        if ($upres) {

            $_SESSION['status_msg'] = "User Billing Details has been Updated Successfully!!!";


            header('Location: admin-user-billing-details.php?row=' . $user_id);
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-user-billing-details.php?row=' . $user_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-user-billing-details.php?row=' . $user_id);
    exit;
}
?>