<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['listing_submit'])) {

        $src_path = $_POST["src_path"];

        $listing_code = $_POST["listing_code"];

//    Condition to get User Id starts

        if (isset($_SESSION['user_code']) && !empty($_SESSION['user_code'])) {
            $user_code = $_SESSION['user_code'];
            $user_details = mysqli_query($conn, "SELECT * FROM  " . TBL . "users where user_code='" . $user_code . "'");
            $user_details_row = mysqli_fetch_array($user_details);

            $user_id = $user_details_row['user_id'];  //User Id

            if ($user_details_row['user_status'] == 'Active') {
                // Listing Status
                $listing_status = "Active";
            } else {
                // Listing Status
                $listing_status = "Inactive";
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

            $upres = mysqli_query($conn, $upqry);

            $user_id = $lastID; //User Id

            // Listing Status
            $listing_status = "Inactive";

        }
//    Condition to get User Id Ends

        //On Update data from edit listing step -1 starts
        if ($src_path == "edit-1") {

            $listing_id = $_POST["listing_id"];
            $profile_image_old = $_POST["profile_image_old"];
            $cover_image_old = $_POST["cover_image_old"];

            // Basic Personal Details
            $first_name = $_POST["first_name"];
            $last_name = $_POST["last_name"];
            $mobile_number = $_POST["mobile_number"];
            $email_id = $_POST["email_id"];

            $register_mode = "Direct";

// Common Listing Details
            $listing_name = $_POST["listing_name"];
            $listing_mobile = $_POST["listing_mobile"];
            $listing_email = $_POST["listing_email"];
            $listing_website = $_POST["listing_website"];
            $listing_whatsapp = $_POST["listing_whatsapp"];
            $listing_address = $_POST["listing_address"];
            $listing_lat = $_POST["listing_lat"];
            $listing_lng = $_POST["listing_lng"];
            $listing_description = addslashes($_POST["listing_description"]);
            $listing_type_id = 1;

            $country_id = $_POST["country_id"];
            $service_locations = $_POST["service_locations"];
            $state_id = "1";

            $city_id1 = $_POST["city_id"];
            $prefix = $fruitList = '';
            foreach ($city_id1 as $fruit) {
                $city_id .= $prefix . $fruit;
                $prefix = ',';
            }

            $category_id = $_POST["category_id"];

            $sub_category_id123 = $_POST["sub_category_id"];
            $prefix = $fruitList = '';
            foreach ($sub_category_id123 as $fruit) {
                $sub_category_id .= $prefix . $fruit;
                $prefix = ',';
            }

            function checkListingSlug($link, $listing_id, $counter = 1)
            {
                global $conn;
                $newLink = $link;
                do {
                    $checkLink = mysqli_query($conn, "SELECT listing_id FROM " . TBL . "listings WHERE listing_slug = '$newLink' AND listing_id != '$listing_id'");
                    if (mysqli_num_rows($checkLink) > 0) {
                        $newLink = $link . '' . $counter;
                        $counter++;
                    } else {
                        break;
                    }
                } while (1);

                return $newLink;
            }


            $listing_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $listing_name));
            $listing_slug = checkListingSlug($listing_name1, $listing_id);


//************************  Profile Image Upload starts  **************************

            if (!empty($_FILES['profile_image']['name'])) {
                $file = rand(1000, 100000) . $_FILES['profile_image']['name'];
                $file_loc = $_FILES['profile_image']['tmp_name'];
                $file_size = $_FILES['profile_image']['size'];
                $file_type = $_FILES['profile_image']['type'];
                $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
                if (in_array($file_type, $allowed)) {
                    $folder = "images/listings/";
                    $new_size = $file_size / 1024;
                    $new_file_name = strtolower($file);
                    $event_image = str_replace(' ', '-', $new_file_name);
                    //move_uploaded_file($file_loc, $folder . $event_image);
                    $profile_image1 = compressImage($event_image, $file_loc, $folder, $new_size);
                    $profile_image = $profile_image1;
                } else {
                    $profile_image = $profile_image_old;
                }
            } else {
                $profile_image = $profile_image_old;
            }
//************************  Profile Image Upload Ends  **************************

//************************  Cover Image Upload starts  **************************

            if (!empty($_FILES['cover_image']['name'])) {
                $file = rand(1000, 100000) . $_FILES['cover_image']['name'];
                $file_loc = $_FILES['cover_image']['tmp_name'];
                $file_size = $_FILES['cover_image']['size'];
                $file_type = $_FILES['cover_image']['type'];
                $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
                if (in_array($file_type, $allowed)) {
                    $folder = "images/listing-ban/";
                    $new_size = $file_size / 1024;
                    $new_file_name = strtolower($file);
                    $event_image = str_replace(' ', '-', $new_file_name);
                    //move_uploaded_file($file_loc, $folder . $event_image);
                    $cover_image1 = compressImage($event_image, $file_loc, $folder, $new_size);
                    $cover_image = $cover_image1;
                } else {
                    $cover_image = $cover_image_old;
                }
            } else {
                $cover_image = $cover_image_old;
            }
//************************  Cover Image Upload ends  **************************

            $listing_qry =
                "UPDATE  " . TBL . "listings  SET user_id='" . $user_id . "', category_id='" . $category_id . "', sub_category_id='" . $sub_category_id . "',
                 listing_type_id='" . $listing_type_id . "', listing_mobile='" . $listing_mobile . "', listing_email='" . $listing_email . "', service_locations='" . $service_locations . "' 
    , listing_website='" . $listing_website . "', listing_whatsapp='" . $listing_whatsapp . "', listing_name='" . $listing_name . "',listing_description='" . $listing_description . "', listing_address='" . $listing_address . "'
    , listing_lat='" . $listing_lat . "', listing_lng='" . $listing_lng . "', listing_slug ='" . $listing_slug . "'
    ,country_id='" . $country_id . "',state_id='" . $state_id . "',city_id='" . $city_id . "',profile_image='" . $profile_image . "', cover_image='" . $cover_image . "' 
    where listing_id='" . $listing_id . "'";

        }

        //On Update data from edit listing step -1 ends

//===========================================================================================

        //On Update data from edit listing step -2 starts
        if ($src_path == "edit-2") {

            $listing_id = $_POST["listing_id"];

            $service_id123 = $_POST["service_id"];

            $prefix1 = $fruitList = '';
            foreach ($service_id123 as $fruit1) {
                $service_id .= $prefix1 . $fruit1;
                $prefix1 = ',';
            }

            $service_image_old = $_POST["service_image_old"];


// ************************  Service Image Upload starts  **************************

            $all_service_image = $_FILES['service_image'];
            $all_service_image23 = $_FILES['service_image']['name'];

            if (count(array_filter($_FILES['service_image']['name'])) <= 0) {
                $service_image = $service_image_old;
            } else {

                for ($k = 0; $k < count($all_service_image23); $k++) {

                    if (!empty($_FILES['service_image']['name'][$k])) {
                        $file = rand(1000, 100000) . $_FILES['service_image']['name'][$k];
                        $file_loc = $_FILES['service_image']['tmp_name'][$k];
                        $file_size = $_FILES['service_image']['size'][$k];
                        $file_type = $_FILES['service_image']['type'][$k];
                        $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
                        if (in_array($file_type, $allowed)) {
                            $folder = "images/services/";
                            $new_size = $file_size / 1024;
                            $new_file_name = strtolower($file);
                            $event_image = str_replace(' ', '-', $new_file_name);
                            //move_uploaded_file($file_loc, $folder . $event_image);
                            $service_image1[] = compressImage($event_image, $file_loc, $folder, $new_size);
                        } else {
                            $service_image1 = '';
                        }
                    }

                }
                $service_image = implode(",", $service_image1);
            }

// ************************  Service Image Upload ends  **************************

            $listing_qry =
                "UPDATE  " . TBL . "listings  SET user_id='" . $user_id . "', service_id='" . $service_id . "'
            , service_image='" . $service_image . "' where listing_id='" . $listing_id . "'";

        }

        //On Update data from edit listing step -2 ends

//===========================================================================================

        //On Update data from edit listing step -3 starts
        if ($src_path == "edit-3") {

            $listing_id = $_POST["listing_id"];

            $service_1_image_old = $_POST["service_1_image_old"];

// Listing Service Names Details

            $service_1_name123 = $_POST["service_1_name"];

            $service_1_name = implode("|", $service_1_name123);


// Listing Offer Prices Details
            $service_1_price123 = $_POST["service_1_price"];

            $prefix1 = $fruitList = '';
            foreach ($service_1_price123 as $fruit1) {
                $service_1_price .= $prefix1 . $fruit1;
                $prefix1 = ',';
            }


// Listing Offer Details
            $service_1_detail123 = $_POST["service_1_detail"];
            $service_1_detail1 = implode("|", $service_1_detail123);
            $service_1_detail = addslashes($service_1_detail1);

// Listing Offer View More
            $service_1_view_more123 = $_POST["service_1_view_more"];
            $prefix1 = $fruitList = '';
            foreach ($service_1_view_more123 as $fruit1) {
                $service_1_view_more .= $prefix1 . $fruit1;
                $prefix1 = ',';
            }


// ************************  Offer Image Upload Starts  **************************

            $all_service_1_image = $_FILES['service_1_image'];
            $all_service_1_image2 = $_FILES['service_1_image']['name'];

            if (count(array_filter($_FILES['service_1_image']['name'])) <= 0) {
                $service_1_image = $service_1_image_old;
            } else {
                for ($k = 0; $k < count($all_service_1_image2); $k++) {

                    if (!empty($_FILES['service_1_image']['name'][$k])) {
                        $file = rand(1000, 100000) . $_FILES['service_1_image']['name'][$k];
                        $file_loc = $_FILES['service_1_image']['tmp_name'][$k];
                        $file_size = $_FILES['service_1_image']['size'][$k];
                        $file_type = $_FILES['service_1_image']['type'][$k];
                        $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
                        if (in_array($file_type, $allowed)) {
                            $folder = "images/services/";
                            $new_size = $file_size / 1024;
                            $new_file_name = strtolower($file);
                            $event_image = str_replace(' ', '-', $new_file_name);
                            //move_uploaded_file($file_loc, $folder . $event_image);
                            $service_1_image1[] = compressImage($event_image, $file_loc, $folder, $new_size);
                        } else {
                            $service_1_image1 = '';
                        }
                    }

                }
                $service_1_image = implode(",", $service_1_image1);
            }
// ************************  Offer Image Upload ends  **************************

            $listing_qry =
                "UPDATE  " . TBL . "listings  SET user_id='" . $user_id . "'
    ,service_1_name='" . $service_1_name . "',service_1_price='" . $service_1_price . "', service_1_detail='" . $service_1_detail . "'
    ,service_1_image='" . $service_1_image . "' , service_1_view_more='" . $service_1_view_more . "' where listing_id='" . $listing_id . "'";


        }

        //On Update data from edit listing step -3 ends

//===========================================================================================

        //On Update data from edit listing step -4 starts
        if ($src_path == "edit-4") {

            $listing_id = $_POST["listing_id"];

            // Listing Location Details
            $google_map = $_POST["google_map"];
            $threesixty_view = $_POST["360_view"];

            $listing_video123 = $_POST["listing_video"];

            // Listing Video

            $prefix6 = $fruitList = '';
            foreach ($listing_video123 as $fruit6) {
                $listing_video1 = $prefix6 . $fruit6;
                $listing_video .= addslashes($listing_video1);
                $prefix6 = '|';
            }

            $gallery_image_old = $_POST["gallery_image_old"];

            // ************************  Gallery Image Upload starts  **************************

            $all_gallery_image = $_FILES['gallery_image'];
            $all_gallery_image23 = $_FILES['gallery_image']['name'];

            if (count(array_filter($_FILES['gallery_image']['name'])) <= 0) {
                $gallery_image = $gallery_image_old;
            } else {


                for ($k = 0; $k < count($all_gallery_image23); $k++) {


                    if (!empty($all_gallery_image['name'][$k])) {
                        $file1 = rand(1000, 100000) . $all_gallery_image['name'][$k];
                        $file_loc1 = $all_gallery_image['tmp_name'][$k];
                        $file_size1 = $all_gallery_image['size'][$k];
                        $file_type1 = $all_gallery_image['type'][$k];
                        $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
                        if (in_array($file_type1, $allowed)) {
                            $folder1 = "images/listings/";
                            $new_size1 = $file_size1 / 1024;
                            $new_file_name1 = strtolower($file1);
                            $event_image1 = str_replace(' ', '-', $new_file_name1);
                            //move_uploaded_file($file_loc1, $folder1 . $event_image1);
                            $gallery_image1[] = compressImage($event_image1, $file_loc1, $folder1, $new_size1);
                        } else {
                            $gallery_image1[] = '';
                        }

                    }


                }
                $gallery_image = implode(",", $gallery_image1);
            }

            // ************************  Gallery Image Upload ends  **************************

            $listing_qry =
                "UPDATE  " . TBL . "listings  SET user_id='" . $user_id . "'
    ,gallery_image='" . $gallery_image . "', google_map='" . $google_map . "',360_view ='" . $threesixty_view . "'
    ,listing_video ='" . $listing_video . "'
     where listing_id='" . $listing_id . "'";

        }

        //On Update data from edit listing step -4 ends


//===========================================================================================

        //On Update data from edit listing step -5 starts

        if ($src_path == "edit-5") {

            $listing_id = $_POST["listing_id"];


//Listing Other Informations
            $listing_info_question123 = $_POST["listing_info_question"];
            $prefix1 = $fruitList = '';
            foreach ($listing_info_question123 as $fruit1) {
                $listing_info_question .= $prefix1 . $fruit1;
                $prefix1 = ',';
            }

            $listing_info_answer123 = $_POST["listing_info_answer"];
            $prefix1 = $fruitList = '';
            foreach ($listing_info_answer123 as $fruit1) {
                $listing_info_answer .= $prefix1 . $fruit1;
                $prefix1 = ',';
            }

            $listing_qry = "UPDATE  " . TBL . "listings  SET user_id='" . $user_id . "', listing_info_question ='" . $listing_info_question . "'
    , listing_info_answer ='" . $listing_info_answer . "'  where listing_id='" . $listing_id . "'";


        }

        //On Update data from edit listing step -5 ends

        //===========================================================================================


//   ***************************** Listing Update Part Starts *****************************

        $listing_res = mysqli_query($conn, $listing_qry);


        //****************************    Admin Primary email fetch starts    *************************

        $admin_primary_email_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "footer  WHERE footer_id = '1' ");
        $admin_primary_email_fetchrow = mysqli_fetch_array($admin_primary_email_fetch);
        $admin_primary_email = $admin_primary_email_fetchrow['admin_primary_email'];
        $admin_footer_copyright = $admin_primary_email_fetchrow['footer_copyright'];
        $admin_site_name = $admin_primary_email_fetchrow['website_address'];
        $admin_address = $admin_primary_email_fetchrow['footer_address'];

        //****************************    Admin Primary email fetch ends    *************************

        if ($listing_res) {

            $admin_email = $admin_primary_email; // Admin Email Id

            $webpage_full_link_with_login = $webpage_full_link . "login";  //URL Login Link

//****************************    Admin email starts    *************************

            $to = $admin_email;
            $LISTING_UPDATE_ADMIN_SUBJECT = $BIZBOOK['LISTING_UPDATE_ADMIN_SUBJECT'];
            $subject = "$admin_site_name $LISTING_UPDATE_ADMIN_SUBJECT";

            $admin_sql_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "mail  WHERE mail_id = 9 "); //admin mail template fetch
            $admin_sql_fetch_row = mysqli_fetch_array($admin_sql_fetch);

            $mail_template_admin = $admin_sql_fetch_row['mail_template'];

            $message1 = stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \''
            , '\' . $mobile_number . \'', '\' . $listing_name . \'', '\' . $listing_email . \'', '\' . $listing_mobile . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'', '\'.$webpage_full_link_with_login.\'', '\'.$admin_primary_email.\''),
                array('' . $admin_site_name . '', '' . $first_name . '', '' . $email_id . '', '' . $mobile_number . '', '' . $listing_name . '', '' . $listing_email . '', '' . $listing_mobile . '', '' . $admin_footer_copyright . '', '' . $admin_address . '', '' . $webpage_full_link . '', '' . $webpage_full_link_with_login . '', '' . $admin_primary_email . ''), $mail_template_admin));


            $headers = "From: " . "$email_id" . "\r\n";
            $headers .= "Reply-To: " . "$email_id" . "\r\n";
            $headers .= "MIME-Version: 1.0\r\n";
            $headers .= "Content-Type: text/html; charset=utf-8\r\n";


            mail($to, $subject, $message1, $headers); //admin email


//****************************    Admin email ends    *************************

//****************************    Client email starts    *************************

            $to1 = $email_id;
            $LISTING_UPDATE_CLIENT_SUBJECT = $BIZBOOK['LISTING_UPDATE_CLIENT_SUBJECT'];
            $subject1 = "$admin_site_name $LISTING_UPDATE_CLIENT_SUBJECT";

            $client_sql_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "mail  WHERE mail_id = 8 "); //User mail template fetch
            $client_sql_fetch_row = mysqli_fetch_array($client_sql_fetch);

            $mail_template_client = $client_sql_fetch_row['mail_template'];

            $message2 = stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \''
            , '\' . $mobile_number . \'', '\' . $listing_name . \'', '\' . $listing_email . \'', '\' . $listing_mobile . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'', '\'.$webpage_full_link_with_login.\'', '\'.$admin_primary_email.\''),
                array('' . $admin_site_name . '', '' . $first_name . '', '' . $email_id . '', '' . $mobile_number . '', '' . $listing_name . '', '' . $listing_email . '', '' . $listing_mobile . '', '' . $admin_footer_copyright . '', '' . $admin_address . '', '' . $webpage_full_link . '', '' . $webpage_full_link_with_login . '', '' . $admin_primary_email . ''), $mail_template_client));


            $headers1 = "From: " . "$admin_email" . "\r\n";
            $headers1 .= "Reply-To: " . "$admin_email" . "\r\n";
            $headers1 .= "MIME-Version: 1.0\r\n";
            $headers1 .= "Content-Type: text/html; charset=utf-8\r\n";


            mail($to1, $subject1, $message2, $headers1); //admin email

//****************************    client email ends    *************************

            if ($listing_type_id == 1) {


// Basic Personal Details
                unset($_SESSION['first_name']);
                unset($_SESSION['last_name']);
                unset($_SESSION['mobile_number']);
                unset($_SESSION['email_id']);

                unset($_SESSION['register_mode']);
                unset($_SESSION['user_status']);

// Common Listing Details
                unset($_SESSION['listing_name']);
                unset($_SESSION['listing_mobile']);
                unset($_SESSION['listing_email']);
                unset($_SESSION['listing_website']);
                unset($_SESSION['listing_address']);
                unset($_SESSION['listing_description']);
                unset($_SESSION['category_id']);
                unset($_SESSION['sub_category_id']);

                unset($_SESSION['country_id']);
                unset($_SESSION['state_id']);
                unset($_SESSION['city_id']);
                unset($_SESSION['profile_image']);
                unset($_SESSION['cover_image']);

                unset($_SESSION['service_id']);
                unset($_SESSION['service_image']);

                unset($_SESSION['service_1_name']);
                unset($_SESSION['service_1_price']);
                unset($_SESSION['service_1_detail']);
                unset($_SESSION['service_1_image']);

                unset($_SESSION['google_map']);
                unset($_SESSION['360_view']);
                unset($_SESSION['gallery_image']);

                unset($_SESSION['listing_info_question']);
                unset($_SESSION['listing_info_answer']);


                header('Location: edit-listing-step-6?code=' . $listing_code);
                exit;
            } else {


// Basic Personal Details
                unset($_SESSION['first_name']);
                unset($_SESSION['last_name']);
                unset($_SESSION['mobile_number']);
                unset($_SESSION['email_id']);

                unset($_SESSION['register_mode']);
                unset($_SESSION['user_status']);

// Common Listing Details
                unset($_SESSION['listing_name']);
                unset($_SESSION['listing_mobile']);
                unset($_SESSION['listing_email']);
                unset($_SESSION['listing_website']);
                unset($_SESSION['listing_address']);
                unset($_SESSION['listing_description']);
                unset($_SESSION['category_id']);
                unset($_SESSION['sub_category_id']);

                unset($_SESSION['country_id']);
                unset($_SESSION['state_id']);
                unset($_SESSION['city_id']);
                unset($_SESSION['profile_image']);
                unset($_SESSION['cover_image']);

                unset($_SESSION['service_id']);
                unset($_SESSION['service_image']);

                unset($_SESSION['service_1_name']);
                unset($_SESSION['service_1_price']);
                unset($_SESSION['service_1_detail']);
                unset($_SESSION['service_1_image']);

                unset($_SESSION['google_map']);
                unset($_SESSION['360_view']);
                unset($_SESSION['gallery_image']);

                unset($_SESSION['listing_info_question']);
                unset($_SESSION['listing_info_answer']);

                header('Location: edit-listing-step-6?code=' . $listing_code);
                exit;
            }

        } else {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: edit-listing-step-1?row=' . $listing_code);
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: edit-listing-step-1?row=' . $listing_code);
}