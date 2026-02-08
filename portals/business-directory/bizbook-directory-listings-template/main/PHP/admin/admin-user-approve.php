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


        $sql = mysqli_query($conn,"UPDATE  " . TBL . "users SET user_status = 'Active'
     where user_id='" . $user_id . "'");

        if ($sql) {

            $status = "Active";

            //Update listings status
            $listing_qry =
                "UPDATE  " . TBL . "listings SET listing_status ='" . $status . "' where user_id='" . $user_id . "'";

            $listing_res = mysqli_query($conn,$listing_qry);

            //Update Event status
            $event_qry =
                "UPDATE  " . TBL . "events SET event_status ='" . $status . "' where user_id='" . $user_id . "'";

            $event_res = mysqli_query($conn,$event_qry);

            //Update Blog status
            $blog_qry =
                "UPDATE  " . TBL . "blogs SET blog_status ='" . $status . "' where user_id='" . $user_id . "'";

            $blog_res = mysqli_query($conn,$blog_qry);

            //Update Product status
            $product_qry =
                "UPDATE  " . TBL . "products SET product_status ='" . $status . "' where user_id='" . $user_id . "'";

            $product_res = mysqli_query($conn,$product_qry);

            $user_details = mysqli_query($conn,"SELECT * FROM  " . TBL . "users where user_id='" . $user_id . "'");
            $user_details_row = mysqli_fetch_array($user_details);

            $first_name = $user_details_row['first_name'];
            $email_id = $user_details_row['email_id'];
            $password = $user_details_row["password"];

            //****************************    Admin Primary email fetch starts    *************************

            $admin_primary_email_fetch = mysqli_query($conn,"SELECT * FROM " . TBL . "footer  WHERE footer_id = '1' ");
            $admin_primary_email_fetchrow = mysqli_fetch_array($admin_primary_email_fetch);
            $admin_primary_email = $admin_primary_email_fetchrow['admin_primary_email'];
            $admin_footer_copyright = $admin_primary_email_fetchrow['footer_copyright'];
            $admin_site_name = $admin_primary_email_fetchrow['website_address'];
            $admin_address = $admin_primary_email_fetchrow['footer_address'];

            //****************************    Admin Primary email fetch ends    *************************


                $admin_email = $admin_primary_email; // Admin Email Id

                $webpage_full_link_with_login = $webpage_full_link. "login";  //URL Login Link

//****************************    Admin email starts    *************************

                $to = $admin_email;
                $subject = "$admin_site_name -User Registration Approval";

            $admin_sql_fetch = mysqli_query($conn,"SELECT * FROM " . TBL . "mail WHERE mail_id = 4 "); //Admin mail template fetch
            $admin_sql_fetch_row = mysqli_fetch_array($admin_sql_fetch);

            $mail_template_admin = $admin_sql_fetch_row['mail_template'];

            $message1 =   stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'','\'.$webpage_full_link_with_login.\'','\'.$admin_primary_email.\''),
                array(''.$admin_site_name.'', '' . $first_name . '', '' . $email_id . '', ''.$admin_footer_copyright.'', ''.$admin_address.'', ''.$webpage_full_link.'',''.$webpage_full_link_with_login.'',''.$admin_primary_email.''), $mail_template_admin));

                $headers = "From: " . "$email_id" . "\r\n";
                $headers .= "Reply-To: " . "$email_id" . "\r\n";
                $headers .= "MIME-Version: 1.0\r\n";
                $headers .= "Content-Type: text/html; charset=utf-8\r\n";


                mail($to, $subject, $message1, $headers); //admin email


//****************************    Admin email ends    *************************

//****************************    Client email starts    *************************

                $to1 = $email_id;
                $subject1 = "$admin_site_name User Registration Approval Successful";

            $client_sql_fetch = mysqli_query($conn,"SELECT * FROM " . TBL . "mail WHERE mail_id = 3 "); //User mail template fetch
            $client_sql_fetch_row = mysqli_fetch_array($client_sql_fetch);

            $mail_template_client = $client_sql_fetch_row['mail_template'];

            $message2 =   stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'','\'.$webpage_full_link_with_login.\'','\'.$admin_primary_email.\''),
                array(''.$admin_site_name.'', '' . $first_name . '', '' . $email_id . '', ''.$admin_footer_copyright.'', ''.$admin_address.'', ''.$webpage_full_link.'',''.$webpage_full_link_with_login.'',''.$admin_primary_email.''), $mail_template_client));
            

                $headers1 = "From: " . "$admin_email" . "\r\n";
                $headers1 .= "Reply-To: " . "$admin_email" . "\r\n";
                $headers1 .= "MIME-Version: 1.0\r\n";
                $headers1 .= "Content-Type: text/html; charset=utf-8\r\n";


                mail($to1, $subject1, $message2, $headers1); //admin email

//****************************    client email ends    *************************

            $_SESSION['status_msg'] = "User has been Approved Successfully!!!";


            header('Location: admin-new-user-requests.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-new-user-requests.php');
            exit;
        }

    }else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-new-user-requests.php');
    exit;
}

?>