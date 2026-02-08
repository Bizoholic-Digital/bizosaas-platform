<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['install_submit'])) {


        $website_name = $_POST["website_name"];
        $website_url123 = $_POST["website_url"];
        $admin_user_name = $_POST["admin_user_name"];
        $admin_user_email_id = $_POST["admin_user_email_id"];
        $admin_user_password = md5($_POST["admin_user_password"]);
        $admin_currency = $_POST["admin_currency"];
        $footer_id = 1;
        $admin_install_flag = 1;


//************ Email Already Exist Check Starts ***************


        $email_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "admin WHERE admin_email = '$admin_user_name' ");


        if (mysqli_num_rows($email_exist_check) > 0) {

            $qry23 = mysqli_query($conn, "UPDATE  " . TBL . "admin SET  admin_password='" . $admin_user_password . "'
     where admin_email='" . $admin_user_name . "'");


        } else {

            $qry23 = mysqli_query($conn, "UPDATE  " . TBL . "admin SET  admin_password='" . $admin_user_password . "'
     ,admin_email='" . $admin_user_name . "' where admin_id='" . $footer_id . "'");

        }

//************ Email Already Exist Check Ends ***************


        $qry = mysqli_query($conn, "UPDATE  " . TBL . "footer SET  website_complete_url='" . $website_url123 . "'
        , website_address='" . $website_name . "', admin_primary_email='" . $admin_user_email_id . "'
        , currency_symbol='" . $admin_currency . "', admin_install_flag='" . $admin_install_flag . "'
     where footer_id='" . $footer_id . "'");


        if ($qry) {
            $_SESSION['admin_user_name'] = $admin_user_name;
            header('Location: install2');
            exit();


        } else {


            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: install1');
            exit();

        }

    }
} else {


    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: install1');
    exit();

}