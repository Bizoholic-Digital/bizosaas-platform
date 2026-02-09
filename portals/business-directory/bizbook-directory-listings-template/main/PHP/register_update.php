<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['register_submit'])) {


        $trap_box = $_POST["trap_box"];

        $mode_path = $_POST["mode_path"];

        if (!empty($trap_box) || $trap_box != NULL) {

            if ($mode_path == "XeBaCk_MoDeX_PATHXHU") {

                $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

                header('Location: admin/admin-add-new-user.php');
                exit();
            } else {
                $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];
                $_SESSION['register_status_msg'] = 1;

                header('Location: login?login=register');
                exit();
            }
        }


        $first_name = $_POST["first_name"];
        $last_name = $_POST["last_name"];
        $mobile_number = $_POST["mobile_number"];
        $email_id = $_POST["email_id"];
        $password = $_POST["password"];
        $password_hash = md5($_POST["password"]);
        $user_type = $_POST["user_type"];

        $star_password = "*********";

        if ($user_type == "General") {

            $user_plan = '';

            $user_points = 0;

        } elseif ($user_type == "job seeker") {

            $user_plan = '';

            $user_points = 0;

        } elseif ($user_type == "Service provider") {

            $user_plan = $_POST["user_plan"];

            $plan_type = "SELECT * FROM " . TBL . "plan_type WHERE plan_type_status='Active' AND plan_type_id = '$user_plan'";

            $rs_plan_type = mysqli_query($conn, $plan_type);
            $plan_type_row = mysqli_fetch_array($rs_plan_type);

            $user_points = $plan_type_row['plan_type_points'];

        }
        $register_mode = "Direct";
        $user_status = "Inactive";

        $user_address = $_POST["user_address"];
        $user_facebook = $_POST["user_facebook"];
        $user_twitter = $_POST["user_twitter"];
        $user_youtube = $_POST["user_youtube"];
        $user_website = $_POST["user_website"];

        $_FILES['profile_image']['name'];

        if (!empty($_FILES['profile_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['profile_image']['name'];
            $file_loc = $_FILES['profile_image']['tmp_name'];
            $file_size = $_FILES['profile_image']['size'];
            $file_type = $_FILES['profile_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "images/profile/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $profile_image = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $profile_image = '';
            }
        }


        function checkUserSlug($link, $counter = 1)
        {
            global $conn;
            $newLink = $link;
            do {
                $checkLink = mysqli_query($conn, "SELECT user_id FROM " . TBL . "users WHERE user_slug = '$newLink'");
                if (mysqli_num_rows($checkLink) > 0) {
                    $newLink = $link . '' . $counter;
                    $counter++;
                } else {
                    break;
                }
            } while (1);

            return $newLink;
        }

        $first_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $first_name));
        $user_slug = checkUserSlug($first_name1);

        // Email Verification Code Starts

        $verification_code = generateNumberOnlyRandomString(5);

        function checkUniqueVerificationLink($link, $counter = 1)
        {
            global $conn;
            $newLink = $link;
            do {
                $checkLink = mysqli_query($conn, "SELECT verification_link FROM " . TBL . "users WHERE verification_link = '$newLink'");
                if (mysqli_num_rows($checkLink) > 0) {
                    $newLink = $link . '' . $counter;
                    $counter++;
                } else {
                    break;
                }
            } while (1);

            return $newLink;
        }

        $verification_link = checkUniqueVerificationLink(generateAlphabetsOnlyRandomString(112));

        $webpage_full_link_with_verification_link = $webpage_full_link . "activate?q=" . $verification_link;

        $verification_status = 1; //**** If 0 means Activated 1 Means Not activated **//


//************ Email Already Exist Check Starts ***************


        $email_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "users WHERE email_id = '$email_id' ");


        if (mysqli_num_rows($email_exist_check) > 0) {


            if ($mode_path == "XeBaCk_MoDeX_PATHXHU") {

                $_SESSION['status_msg'] = $BIZBOOK['GIVEN_EMAIL_ID_ALREADY_EXISTS_MESSAGE'];

                header('Location: admin/admin-add-new-user.php');
                exit();
            } else {

                $_SESSION['status_msg'] = $BIZBOOK['GIVEN_EMAIL_ID_ALREADY_EXISTS_MESSAGE'];
                $_SESSION['register_status_msg'] = 1;

                header('Location: login?login=register');
                exit();
            }

        }

//************ Email Already Exist Check Ends ***************

//************ Mobile Number Already Exist Check Starts ***************


        $mobile_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "users  WHERE mobile_number = '$mobile_number' ");

        if (mysqli_num_rows($mobile_exist_check) > 0) {


            if ($mode_path == "XeBaCk_MoDeX_PATHXHU") {

                $_SESSION['status_msg'] = $BIZBOOK['GIVEN_MOBILE_NUMBER_ALREADY_EXISTS_MESSAGE'];

                header('Location: admin/admin-add-new-user.php');
                exit();
            } else {

                $_SESSION['status_msg'] = $BIZBOOK['GIVEN_MOBILE_NUMBER_ALREADY_EXISTS_MESSAGE'];
                $_SESSION['register_status_msg'] = 1;

                header('Location: login?login=register');
                exit();
            }

        }

//************ Mobile Number Already Exist Check Ends ***************

        $qry = "INSERT INTO " . TBL . "users 
					(first_name, last_name, email_id, mobile_number, password, user_type, user_plan, register_mode, user_address, profile_image
					, user_points, user_facebook, user_twitter, user_youtube, user_website, user_slug, verification_code, verification_link,verification_status, user_status, user_clear_notification_cdt, user_cdt)
					VALUES ('$first_name', '$last_name', '$email_id', '$mobile_number', '$password_hash', '$user_type', '$user_plan', '$register_mode',
					 '$user_address', '$profile_image', '$user_points', '$user_facebook','$user_twitter', '$user_youtube', '$user_website',
					 '$user_slug','$verification_code','$verification_link','$verification_status','$user_status', '$curDate', '$curDate')";


        $res = mysqli_query($conn, $qry);
        $LID = mysqli_insert_id($conn);
        $lastID = $LID;

        switch (strlen($LID)) {
            case 1:
                $LID = '00' . $LID;
                break;
            case 2:
                $LID = '0' . $LID;
                break;
            default:
                $LID = $LID;
                break;
        }

        $userID = 'USER' . $LID;

        $upqry = "UPDATE " . TBL . "users 
					  SET user_code = '$userID' 
					  WHERE user_id = $lastID";

        $upres = mysqli_query($conn, $upqry);

        //****************************    Admin Primary email fetch starts    *************************

        $admin_primary_email_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "footer  WHERE footer_id = '1' ");
        $admin_primary_email_fetchrow = mysqli_fetch_array($admin_primary_email_fetch);
        $admin_primary_email = $admin_primary_email_fetchrow['admin_primary_email'];
        $admin_footer_copyright = $admin_primary_email_fetchrow['footer_copyright'];
        $admin_site_name = $admin_primary_email_fetchrow['website_address'];
        $admin_address = $admin_primary_email_fetchrow['footer_address'];

        //****************************    Admin Primary email fetch ends    *************************

        if ($upres) {

            $admin_email = $admin_primary_email; // Admin Email Id

            $webpage_full_link_with_login = $webpage_full_link . "login";  //URL Login Link

            $USER_INSERT_ADMIN_SUBJECT = $BIZBOOK['USER_INSERT_ADMIN_SUBJECT'];

//****************************    Admin email starts    *************************

            $to = $admin_email;
            $subject = "$admin_site_name $USER_INSERT_ADMIN_SUBJECT";

            $admin_sql_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "mail WHERE mail_id = 2 "); //Admin mail template fetch
            $admin_sql_fetch_row = mysqli_fetch_array($admin_sql_fetch);

            $mail_template_admin = $admin_sql_fetch_row['mail_template'];

            $message1 = stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \'', '\' . $password . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'', '\'.$webpage_full_link_with_login.\'', '\'.$admin_primary_email.\''),
                array('' . $admin_site_name . '', '' . $first_name . '', '' . $email_id . '', '' . $star_password . '', '' . $admin_footer_copyright . '', '' . $admin_address . '', '' . $webpage_full_link . '', '' . $webpage_full_link_with_login . '', '' . $admin_primary_email . ''), $mail_template_admin));

            $headers = "From: " . "$email_id" . "\r\n";
            $headers .= "Reply-To: " . "$email_id" . "\r\n";
            $headers .= "MIME-Version: 1.0\r\n";
            $headers .= "Content-Type: text/html; charset=utf-8\r\n";


            mail($to, $subject, $message1, $headers); //admin email


//****************************    Admin email ends    *************************

//****************************    Client email starts    *************************

            $to1 = $email_id;
            $USER_INSERT_CLIENT_SUBJECT = $BIZBOOK['USER_INSERT_CLIENT_SUBJECT'];
            $subject1 = "$admin_site_name $USER_INSERT_CLIENT_SUBJECT";

            $client_sql_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "mail WHERE mail_id = 1 "); //User mail template fetch
            $client_sql_fetch_row = mysqli_fetch_array($client_sql_fetch);

            $mail_template_client = $client_sql_fetch_row['mail_template'];

            $message2 = stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \'', '\' . $password . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'', '\'.$webpage_full_link_with_login.\'', '\'.$verify_code.\'', '\'.$webpage_full_link_with_verification_link.\'', '\'.$admin_primary_email.\''),
                array('' . $admin_site_name . '', '' . $first_name . '', '' . $email_id . '', '' . $star_password . '', '' . $admin_footer_copyright . '', '' . $admin_address . '', '' . $webpage_full_link . '', '' . $webpage_full_link_with_login . '', '' . $verification_code . '', '' . $webpage_full_link_with_verification_link . '', '' . $admin_primary_email . ''), $mail_template_client));

            $headers1 = "From: " . "$admin_email" . "\r\n";
            $headers1 .= "Reply-To: " . "$admin_email" . "\r\n";
            $headers1 .= "MIME-Version: 1.0\r\n";
            $headers1 .= "Content-Type: text/html; charset=utf-8\r\n";


            mail($to1, $subject1, $message2, $headers1); //admin email

//****************************    client email ends    *************************


            if ($mode_path == "XeBaCk_MoDeX_PATHXHU") {
                $_SESSION['status_msg'] = $BIZBOOK['USER_INSERT_SUCCESS_MESSAGE'];  // Success Message in session

                header('Location: admin/admin-new-user-requests.php');
                exit();
            } else {

                $_SESSION['status_msg'] = $BIZBOOK['USER_INSERT_SUCCESS_MESSAGE'];  // Success Message in session
                $_SESSION['register_status_msg'] = 1;

                header('Location: login?login=register');
                exit();
            }

        } else {


            if ($mode_path == "XeBaCk_MoDeX_PATHXHU") {
                $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

                header('Location: admin/admin-add-new-user.php');
                exit();
            } else {
                $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];
                $_SESSION['register_status_msg'] = 1;

                header('Location: login?login=register');
                exit();
            }
        }

    }
} else {


    if ($mode_path == "XeBaCk_MoDeX_PATHXHU") {
        $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

        header('Location: admin/admin-add-new-user.php');
        exit();
    } else {
        $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];
        $_SESSION['register_status_msg'] = 1;

        header('Location: login?login=register');
        exit();
    }
}