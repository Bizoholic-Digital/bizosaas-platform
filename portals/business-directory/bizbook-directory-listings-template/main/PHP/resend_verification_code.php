<?php

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if (isset($_GET['q']) && isset($_GET['resend'])) {

    $verification_link_user = $_GET['q'];

} else {

    $redirect_url = $webpage_full_link . 'login';  //Redirect Url

    header("Location: $redirect_url");  //Redirect When No Verification on URL
    exit();
}


$activation = mysqli_query($conn, "SELECT * FROM " . TBL . "users  WHERE verification_link = '$verification_link_user'");

if (mysqli_num_rows($activation) > 0) {

    $activation_row = mysqli_fetch_array($activation);

    if ($verification_link_user == $activation_row['verification_link']) {

        $first_name = $activation_row['first_name'];

        $email_id = $activation_row['email_id'];

        $verification_link = $activation_row['verification_link'];

        $verification_code = $activation_row['verification_code'];

        $webpage_full_link_with_verification_link = $webpage_full_link . "activate?q=" . $verification_link;


        //****************************    Admin Primary email fetch starts    *************************

        $admin_primary_email_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "footer  WHERE footer_id = '1' ");
        $admin_primary_email_fetchrow = mysqli_fetch_array($admin_primary_email_fetch);
        $admin_primary_email = $admin_primary_email_fetchrow['admin_primary_email'];
        $admin_footer_copyright = $admin_primary_email_fetchrow['footer_copyright'];
        $admin_site_name = $admin_primary_email_fetchrow['website_address'];
        $admin_address = $admin_primary_email_fetchrow['footer_address'];

        //****************************    Admin Primary email fetch ends    *************************

        $admin_email = $admin_primary_email; // Admin Email Id

        $webpage_full_link_with_login = $webpage_full_link . "login";  //URL Login Link

//****************************    Client email starts    *************************

        $to1 = $email_id;
        $USER_INSERT_CLIENT_SUBJECT = $BIZBOOK['USER_VERIFICATION_RESENT_CLIENT_SUBJECT'];
        $subject1 = "$admin_site_name $USER_INSERT_CLIENT_SUBJECT";

        $client_sql_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "mail WHERE mail_id = 22 "); //User mail template fetch
        $client_sql_fetch_row = mysqli_fetch_array($client_sql_fetch);

        $mail_template_client = $client_sql_fetch_row['mail_template'];

        $message2 = stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \'', '\' . $password . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'', '\'.$webpage_full_link_with_login.\'', '\'.$verify_code.\'', '\'.$webpage_full_link_with_verification_link.\'', '\'.$admin_primary_email.\''),
            array('' . $admin_site_name . '', '' . $first_name . '', '' . $email_id . '', '' . $password . '', '' . $admin_footer_copyright . '', '' . $admin_address . '', '' . $webpage_full_link . '', '' . $webpage_full_link_with_login . '', '' . $verification_code . '', '' . $webpage_full_link_with_verification_link . '', '' . $admin_primary_email . ''), $mail_template_client));

        $headers1 = "From: " . "$admin_email" . "\r\n";
        $headers1 .= "Reply-To: " . "$admin_email" . "\r\n";
        $headers1 .= "MIME-Version: 1.0\r\n";
        $headers1 .= "Content-Type: text/html; charset=utf-8\r\n";


        $mail_success = mail($to1, $subject1, $message2, $headers1); //admin email

//****************************    client email ends    *************************
        if ($mail_success){

            $_SESSION['status_msg'] = $BIZBOOK['USER_RESEND_VERIFICATION_SUCCESS_MESSAGE'];  // Success Message in session

            header('Location: activate?q=' . $verification_link);
            exit();
            
        } else {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: activate?q=' . $verification_link);
            exit();
        }

    } else {

        $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];
        $_SESSION['login_status_msg'] = 1;

        header('Location: login');
        exit();
    }

} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];
    $_SESSION['login_status_msg'] = 1;

    header('Location: login');
    exit();
}
