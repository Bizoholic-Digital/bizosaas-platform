<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['product_submit'])) {

        $product_id = $_POST["product_id"];

        $product_code = $_POST["product_code"];

        $gallery_image_old = $_POST["gallery_image_old"];


// Basic Personal Details
        $first_name = $_POST["first_name"];
        $last_name = $_POST["last_name"];
        $mobile_number = $_POST["mobile_number"];
        $email_id = $_POST["email_id"];

        $register_mode = "Direct";
//        $user_status = "Inactive";

// Common product Details
        $product_name = $_POST["product_name"];
        $product_price = $_POST["product_price"];
        $product_price_offer = $_POST["product_price_offer"];
        $product_payment_link = $_POST["product_payment_link"];
        $product_tags = $_POST["product_tags"];
        $product_description = addslashes($_POST["product_description"]);


        $category_id = $_POST["category_id"];

        $sub_category_id123 = $_POST["sub_category_id"];

        $prefix = $fruitList = '';
        foreach ($sub_category_id123 as $fruit) {
            $sub_category_id .= $prefix . $fruit;
            $prefix = ',';
        }


//product highlights

        $product_highlights123 = $_POST["product_highlights"];
        $prefix1 = $fruitList = '';
        foreach ($product_highlights123 as $fruit1) {
            $product_highlights .= $prefix1 . $fruit1;
            $prefix1 = '|';
        }

//product Specifications
        $product_info_question123 = $_POST["product_info_question"];
        $prefix1 = $fruitList = '';
        foreach ($product_info_question123 as $fruit1) {
            $product_info_question .= $prefix1 . $fruit1;
            $prefix1 = ',';
        }

        $product_info_answer123 = $_POST["product_info_answer"];
        $prefix1 = $fruitList = '';
        foreach ($product_info_answer123 as $fruit1) {
            $product_info_answer .= $prefix1 . $fruit1;
            $prefix1 = ',';
        }

        // $product_status = "Pending";
        $payment_status = "Pending";

        $product_type_id = 1;


//    Condition to get User Id starts

        if (isset($_POST['user_code']) && !empty($_POST['user_code'])) {
            $user_code = $_POST['user_code'];
            $user_details = mysqli_query($conn, "SELECT * FROM  " . TBL . "users where user_code='" . $user_code . "'");
            $user_details_row = mysqli_fetch_array($user_details);

            $user_id = $user_details_row['user_id'];  //User Id

            if ($user_details_row['user_status'] == 'Active') {
                // product Status
                $product_status = "Active";
            } else {
                // product Status
                $product_status = "Inactive";
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
// product Status
            $product_status = "Inactive";

        }
//    Condition to get User Id Ends


// ************************  Gallery Image Upload starts  **************************

        $all_gallery_image = $_FILES['gallery_image'];

        if (count(array_filter($_FILES['gallery_image']['name'])) <= 0) {
            $gallery_image = $gallery_image_old;
        } else {


            for ($k = 0; $k < count($all_gallery_image); $k++) {


                if (!empty($all_gallery_image['name'][$k])) {
                    $file1 = rand(1000, 100000) . $all_gallery_image['name'][$k];
                    $file_loc1 = $all_gallery_image['tmp_name'][$k];
                    $file_size1 = $all_gallery_image['size'][$k];
                    $file_type1 = $all_gallery_image['type'][$k];
                    $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
                    if (in_array($file_type1, $allowed)) {
                        $folder1 = "../images/products/";
                        $new_size1 = $file_size1 / 1024;
                        $new_file_name1 = strtolower($file1);
                        $event_image1 = str_replace(' ', '-', $new_file_name1);
                        //move_uploaded_file($file_loc1, $folder1 . $event_image1);
                        $gallery_image1[] = compressImage($event_image1, $file_loc1, $folder1, $new_size1);
                    } else {
                        $gallery_image1[] = '';
                    }

                }
                $gallery_image = implode(",", $gallery_image1);

            }
        }

        // ************************  Gallery Image Upload ends  **************************


        function checkProductSlug($link, $product_id, $counter = 1)
        {
            global $conn;
            $newLink = $link;
            do {
                $checkLink = mysqli_query($conn, "SELECT product_id FROM " . TBL . "products WHERE product_slug = '$newLink' AND product_id != '$product_id'");
                if (mysqli_num_rows($checkLink) > 0) {
                    $newLink = $link . '' . $counter;
                    $counter++;
                } else {
                    break;
                }
            } while (1);

            return $newLink;
        }


        $product_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $product_name));
        $product_slug = checkProductSlug($product_name1, $product_id);


        $product_qry =
            "UPDATE  " . TBL . "products  SET user_id='" . $user_id . "', product_name='" . $product_name . "'
            ,product_description='" . $product_description . "', product_price='" . $product_price . "'
            ,category_id='" . $category_id . "', sub_category_id='" . $sub_category_id . "'
            , product_price_offer='" . $product_price_offer . "',product_payment_link='" . $product_payment_link . "'
            , product_tags='" . $product_tags . "'
            ,product_highlights='" . $product_highlights . "' ,product_info_question ='" . $product_info_question . "' 
        ,product_info_answer='" . $product_info_answer . "' ,gallery_image='" . $gallery_image . "'
        , product_status='" . $product_status . "', product_slug='" . $product_slug . "' where product_id='" . $product_id . "'";


        $product_res = mysqli_query($conn, $product_qry);

        //****************************    Admin Primary email fetch starts    *************************

        $admin_primary_email_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "footer  WHERE footer_id = '1' ");
        $admin_primary_email_fetchrow = mysqli_fetch_array($admin_primary_email_fetch);
        $admin_primary_email = $admin_primary_email_fetchrow['admin_primary_email'];
        $admin_footer_copyright = $admin_primary_email_fetchrow['footer_copyright'];
        $admin_site_name = $admin_primary_email_fetchrow['website_address'];
        $admin_address = $admin_primary_email_fetchrow['footer_address'];

        //****************************    Admin Primary email fetch ends    *************************

        if ($product_res) {

            $admin_email = $admin_primary_email; // Admin Email Id

            $webpage_full_link_with_login = $webpage_full_link . "login";  //URL Login Link

//****************************    Admin email starts    *************************

            $to = $admin_email;
            $subject = "$admin_site_name - product has been updated";

            $admin_sql_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "mail  WHERE mail_id = 21 "); //admin mail template fetch
            $admin_sql_fetch_row = mysqli_fetch_array($admin_sql_fetch);

            $mail_template_admin = $admin_sql_fetch_row['mail_template'];

            $message1 = stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \''
            , '\' . $mobile_number . \'', '\' . $product_name . \'', '\' . $product_email . \'', '\' . $product_mobile . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'', '\'.$webpage_full_link_with_login.\'', '\'.$admin_primary_email.\''),
                array('' . $admin_site_name . '', '' . $first_name . '', '' . $email_id . '', '' . $mobile_number . '', '' . $product_name . '', '' . $product_email . '', '' . $product_mobile . '', '' . $admin_footer_copyright . '', '' . $admin_address . '', '' . $webpage_full_link . '', '' . $webpage_full_link_with_login . '', '' . $admin_primary_email . ''), $mail_template_admin));

            $headers = "From: " . "$email_id" . "\r\n";
            $headers .= "Reply-To: " . "$email_id" . "\r\n";
            $headers .= "MIME-Version: 1.0\r\n";
            $headers .= "Content-Type: text/html; charset=utf-8\r\n";


            mail($to, $subject, $message1, $headers); //admin email


//****************************    Admin email ends    *************************

//****************************    Client email starts    *************************

            $to1 = $email_id;
            $subject1 = "$admin_site_name Product Update Successful";

            $client_sql_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "mail  WHERE mail_id = 20 "); //User mail template fetch
            $client_sql_fetch_row = mysqli_fetch_array($client_sql_fetch);

            $mail_template_client = $client_sql_fetch_row['mail_template'];

            $message2 = stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \''
            , '\' . $mobile_number . \'', '\' . $product_name . \'', '\' . $product_email . \'', '\' . $product_mobile . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'', '\'.$webpage_full_link_with_login.\'', '\'.$admin_primary_email.\''),
                array('' . $admin_site_name . '', '' . $first_name . '', '' . $email_id . '', '' . $mobile_number . '', '' . $product_name . '', '' . $product_email . '', '' . $product_mobile . '', '' . $admin_footer_copyright . '', '' . $admin_address . '', '' . $webpage_full_link . '', '' . $webpage_full_link_with_login . '', '' . $admin_primary_email . ''), $mail_template_client));


            $headers1 = "From: " . "$admin_email" . "\r\n";
            $headers1 .= "Reply-To: " . "$admin_email" . "\r\n";
            $headers1 .= "MIME-Version: 1.0\r\n";
            $headers1 .= "Content-Type: text/html; charset=utf-8\r\n";


            mail($to1, $subject1, $message2, $headers1); //admin email

//****************************    client email ends    *************************

            if ($product_type_id == 1) {

                $_SESSION['status_msg'] = "Your Product has been Updated Successfully!!!";

                header('Location: admin-all-products.php');
                exit;
            } else {

                header("Location: paypal_pay?map_id=$product_id&type_id=$product_type_id");

                $_SESSION['status_msg'] = "Your product has been Updated Successfully!!!";

                exit;
            }

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header("Location: admin-edit-product.php?code=$product_code");
        }

        //    product Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: profile.php');
}