<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['event_submit'])) {

// Basic Personal Details
        $first_name = $_POST["first_name"];
        $last_name = $_POST["last_name"];
        $mobile_number = $_POST["mobile_number"];
        $email_id = $_POST["email_id"];

        $register_mode = "Direct";
//        $user_status = "Inactive";

// Common Event Details
        $event_name = $_POST["event_name"];
        $event_address = $_POST["event_address"];
        $event_map = $_POST["event_map"];
        $event_contact_name = $_POST["event_contact_name"];
        $event_website = $_POST["event_website"];
        $event_mobile = $_POST["event_mobile"];
        $event_email = $_POST["event_email"];
        $event_description = addslashes($_POST["event_description"]);

        $event_start_date_old = $_POST["event_start_date"];
        $timestamp = strtotime($event_start_date_old);
        $event_start_date = date('Y-m-d H:i:s', $timestamp);

        $event_end_date = $_POST["event_end_date"];
        $event_time = $_POST["event_time"];
        $isenquiry_old = $_POST["isenquiry"];

        if ($isenquiry_old == "on") {
            $isenquiry = 1;
        } else {
            $isenquiry = 0;
        }

        $event_type = "All";


// Event Status
//        $event_status = "Active";
        // $event_status = "Pending";
        $payment_status = "Pending";
        $event_type_id = 1;

//    Condition to get User Id starts


        if (isset($_SESSION['user_code']) && !empty($_SESSION['user_code'])) {
            $user_code = $_SESSION['user_code'];
            $user_details = mysqli_query($conn, "SELECT * FROM  " . TBL . "users where user_code='" . $user_code . "'");
            $user_details_row = mysqli_fetch_array($user_details);

            $user_id = $user_details_row['user_id'];  //User Id

            if ($user_details_row['user_status'] == 'Active') {
                // Event Status
                $event_status = "Active";
            } else {
                // Event Status
                $event_status = "Inactive";
            }

        } else {
            $user_status = "Inactive";

            $qry = "INSERT INTO " . TBL . "users 
					(first_name, last_name, email_id, mobile_number, register_mode, user_status, user_cdt) 
					VALUES ('$first_name', '$last_name', '$email_id', '$mobile_number','$register_mode', '$user_status', '$curDate')";

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

            //echo $upqry; die();
            $upres = mysqli_query($conn, $upqry);

            $user_id = $lastID; //User Id

// Event Status
            $event_status = "Inactive";
        }
//    Condition to get User Id Ends


        if (!empty($_FILES['event_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['event_image']['name'];
            $file_loc = $_FILES['event_image']['tmp_name'];
            $file_size = $_FILES['event_image']['size'];
            $file_type = $_FILES['event_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "images/events/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image_1 = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image_1);
                $event_image = compressImage($event_image_1, $file_loc, $folder, $new_size);
            } else {
                $event_image = '';
            }
        }

        function checkEventSlug($link, $counter = 1)
        {
            global $conn;
            $newLink = $link;
            do {
                $checkLink = mysqli_query($conn, "SELECT event_id FROM " . TBL . "events WHERE event_slug = '$newLink'");
                if (mysqli_num_rows($checkLink) > 0) {
                    $newLink = $link . '' . $counter;
                    $counter++;
                } else {
                    break;
                }
            } while (1);

            return $newLink;
        }


        $event_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $event_name));
        $event_slug = checkEventSlug($event_name1);


//    Event Insert Part Starts


        $event_qry = "INSERT INTO " . TBL . "events
					(user_id, event_name, event_description,event_email,event_mobile,event_website, event_address
					,event_contact_name, event_map, event_start_date, event_time, event_image, event_status, event_type, isenquiry, event_slug, event_cdt)
					VALUES
					('$user_id', '$event_name', '$event_description', '$event_email', '$event_mobile', '$event_website'
					, '$event_address', '$event_contact_name', '$event_map', '$event_start_date',  '$event_time', '$event_image', '$event_status', '$event_type', '$isenquiry', '$event_slug', '$curDate')";

        $event_res = mysqli_query($conn, $event_qry);


        //****************************    Admin Primary email fetch starts    *************************

        $admin_primary_email_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "footer  WHERE footer_id = '1' ");
        $admin_primary_email_fetchrow = mysqli_fetch_array($admin_primary_email_fetch);
        $admin_primary_email = $admin_primary_email_fetchrow['admin_primary_email'];
        $admin_footer_copyright = $admin_primary_email_fetchrow['footer_copyright'];
        $admin_site_name = $admin_primary_email_fetchrow['website_address'];
        $admin_address = $admin_primary_email_fetchrow['footer_address'];

        //****************************    Admin Primary email fetch ends    *************************


        if ($event_res) {

            $admin_email = $admin_primary_email; // Admin Email Id

            $webpage_full_link_with_login = $webpage_full_link . "login";  //URL Login Link

//****************************    Admin email starts    *************************

            $to = $admin_email;
            $EVENT_INSERT_ADMIN_SUBJECT = $BIZBOOK['EVENT_INSERT_ADMIN_SUBJECT'];
            $subject = "$admin_site_name $EVENT_INSERT_ADMIN_SUBJECT";

            $admin_sql_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "mail  WHERE mail_id = 11 "); //admin mail template fetch
            $admin_sql_fetch_row = mysqli_fetch_array($admin_sql_fetch);

            $mail_template_admin = $admin_sql_fetch_row['mail_template'];

            $message1 = stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \''
            , '\' . $mobile_number . \'', '\' . $event_name . \'', '\' . $event_start_date . \'', '\' . $event_time . \'', '\' . $event_contact_name . \'', '\' . $event_address . \'', '\' . $event_email . \'', '\' . $event_mobile . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'', '\'.$webpage_full_link_with_login.\'', '\'.$admin_primary_email.\''),
                array('' . $admin_site_name . '', '' . $first_name . '', '' . $email_id . '', '' . $mobile_number . '', '' . $event_name . '', '' . $event_start_date_old . '', '' . $event_time . '', '' . $event_contact_name . '', '' . $event_address . '', '' . $event_email . '', '' . $event_mobile . '', '' . $admin_footer_copyright . '', '' . $admin_address . '', '' . $webpage_full_link . '', '' . $webpage_full_link_with_login . '', '' . $admin_primary_email . ''), $mail_template_admin));


            $headers = "From: " . "$email_id" . "\r\n";
            $headers .= "Reply-To: " . "$email_id" . "\r\n";
            $headers .= "MIME-Version: 1.0\r\n";
            $headers .= "Content-Type: text/html; charset=utf-8\r\n";


         //   mail($to, $subject, $message1, $headers); //admin email


//****************************    Admin email ends    *************************

//****************************    Client email starts    *************************

            $to1 = $email_id;
            $EVENT_INSERT_CLIENT_SUBJECT = $BIZBOOK['EVENT_INSERT_CLIENT_SUBJECT'];
            $subject1 = "$admin_site_name $EVENT_INSERT_CLIENT_SUBJECT";

            $client_sql_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "mail  WHERE mail_id = 10 "); //User mail template fetch
            $client_sql_fetch_row = mysqli_fetch_array($client_sql_fetch);

            $mail_template_client = $client_sql_fetch_row['mail_template'];

            $message2 = stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \''
            , '\' . $mobile_number . \'', '\' . $event_name . \'', '\' . $event_start_date . \'', '\' . $event_time . \'', '\' . $event_contact_name . \'', '\' . $event_address . \'', '\' . $event_email . \'', '\' . $event_mobile . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'', '\'.$webpage_full_link_with_login.\'', '\'.$admin_primary_email.\''),
                array('' . $admin_site_name . '', '' . $first_name . '', '' . $email_id . '', '' . $mobile_number . '', '' . $event_name . '', '' . $event_start_date_old . '', '' . $event_time . '', '' . $event_contact_name . '', '' . $event_address . '', '' . $event_email . '', '' . $event_mobile . '', '' . $admin_footer_copyright . '', '' . $admin_address . '', '' . $webpage_full_link . '', '' . $webpage_full_link_with_login . '', '' . $admin_primary_email . ''), $mail_template_client));


            $headers1 = "From: " . "$admin_email" . "\r\n";
            $headers1 .= "Reply-To: " . "$admin_email" . "\r\n";
            $headers1 .= "MIME-Version: 1.0\r\n";
            $headers1 .= "Content-Type: text/html; charset=utf-8\r\n";


            mail($to1, $subject1, $message2, $headers1); //admin email

//****************************    client email ends    *************************

            if ($event_type_id == 1) {

                $_SESSION['status_msg'] = $BIZBOOK['EVENT_INSERT_SUCCESS_MESSAGE'];

                header('Location: db-events');

            } else {

                header("Location: paypal_pay?map_id=$listlastID&type_id=$event_type_id");

                $_SESSION['status_msg'] = $BIZBOOK['EVENT_INSERT_SUCCESS_MESSAGE'];

                //           header('Location: db-payment');

                exit;
            }

        } else {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: create-new-event');
        }

        //    Event Insert Part Ends

    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: dashboard');
}