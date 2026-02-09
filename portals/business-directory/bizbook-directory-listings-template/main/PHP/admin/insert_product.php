<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}


if ($_SERVER['REQUEST_METHOD']=='POST') {
    if (isset($_POST['product_submit'])) {


// Basic Personal Details
        $first_name = $_SESSION["first_name"];
        $last_name = $_SESSION["last_name"];
        $mobile_number = $_SESSION["mobile_number"];
        $email_id = $_SESSION["email_id"];

        $register_mode = "Direct";


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
        foreach ($sub_category_id123 as $fruit)
        {
            $sub_category_id .= $prefix .  $fruit ;
            $prefix = ',';
        }

//product highlights

        $product_highlights123 = $_POST["product_highlights"];
        $prefix1 = $fruitList = '';
        foreach ($product_highlights123 as $fruit1)
        {
            $product_highlights .= $prefix1 .  $fruit1 ;
            $prefix1 = '|';
        }

//product Specifications
        $product_info_question123 = $_POST["product_info_question"];
        $prefix1 = $fruitList = '';
        foreach ($product_info_question123 as $fruit1)
        {
            $product_info_question .= $prefix1 .  $fruit1 ;
            $prefix1 = ',';
        }

        $product_info_answer123 = $_POST["product_info_answer"];
        $prefix1 = $fruitList = '';
        foreach ($product_info_answer123 as $fruit1)
        {
            $product_info_answer .= $prefix1 .  $fruit1 ;
            $prefix1 = ',';
        }

        // $product_status = "Pending";
        $payment_status = "Pending";

//    Condition to get User Id starts

        if (isset($_POST['user_code']) && !empty($_POST['user_code'])) {
            $user_code = $_POST['user_code'];
            $user_details = mysqli_query($conn,"SELECT * FROM  " . TBL . "users where user_code='" . $user_code . "'");
            $user_details_row = mysqli_fetch_array($user_details);

            $user_id = $user_details_row['user_id'];  //User Id

            if($user_details_row['user_status'] == 'Active'){
                // product Status
                $product_status = "Active";
            }else{
                // product Status
                $product_status = "Inactive";
            }


        } else {
            $user_status = "Inactive";

            $qry = "INSERT INTO " . TBL . "users 
					(first_name, last_name, email_id, mobile_number, register_mode, user_status, user_cdt) 
					VALUES ('$first_name', '$last_name', '$email_id', '$mobile_number','$register_mode', '$user_status', '$curDate')";

            $res = mysqli_query($conn,$qry);
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
            $upres = mysqli_query($conn,$upqry);

            $user_id = $lastID; //User Id

            // product Status
            $product_status = "Inactive";

        }
//    Condition to get User Id Ends



// ************************  Gallery Image Upload starts  **************************

        $all_gallery_image = $_FILES['gallery_image'];

        for ($k = 0; $k < count($all_gallery_image); $k++) {


            if (!empty($all_gallery_image['name'][$k])) {
                $file1 = rand(1000, 100000) . $all_gallery_image['name'][$k];
                $file_loc1 = $all_gallery_image['tmp_name'][$k];
                $file_size1 = $all_gallery_image['size'][$k];
                $file_type1 = $all_gallery_image['type'][$k];
                $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
                if(in_array($file_type1, $allowed)) {
                $folder1 = "../images/products/";
                $new_size = $file_size1 / 1024;
                $new_file_name1 = strtolower($file1);
                $event_image1 = str_replace(' ', '-', $new_file_name1);
                //move_uploaded_file($file_loc1, $folder1 . $event_image1);
                $gallery_image1[] = compressImage($event_image1,$file_loc1,$folder1,$new_size);
                } else {
                    $gallery_image1[] = '';
                }
            }
            $gallery_image = implode(",", $gallery_image1);
        }



// ************************  Gallery Image Upload ends  **************************
        
        function checkProductSlug($link, $counter=1){
            global $conn;
            $newLink = $link;
            do{
                $checkLink = mysqli_query($conn, "SELECT product_id FROM " . TBL . "products WHERE product_slug = '$newLink'");
                if(mysqli_num_rows($checkLink) > 0){
                    $newLink = $link.''.$counter;
                    $counter++;
                } else {
                    break;
                }
            } while(1);

            return $newLink;
        }


        $product_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $product_name));
        $product_slug = checkProductSlug($product_name1);

//    Product Insert Part Starts

        $product_qry = "INSERT INTO " . TBL . "products 
					(user_id, category_id, sub_category_id, product_name, product_description
					, gallery_image, product_price, product_price_offer, product_payment_link, product_tags, product_highlights, product_status
					, product_info_question , product_info_answer, payment_status, product_slug, product_cdt) 
					VALUES 
					('$user_id', '$category_id', '$sub_category_id','$product_name','$product_description'
					,'$gallery_image', '$product_price', '$product_price_offer', '$product_payment_link', '$product_tags', '$product_highlights', '$product_status'
					, '$product_info_question', '$product_info_answer', '$payment_status', '$product_slug', '$curDate')";


        $product_res = mysqli_query($conn,$product_qry);
        $productID = mysqli_insert_id($conn);
        $listlastID = $productID;

        switch (strlen($productID)) {
            case 1:
                $productID = '00' . $productID;
                break;
            case 2:
                $productID = '0' . $productID;
                break;
            default:
                $productID = $productID;
                break;
        }

        $ProdCode = 'PROD' . $productID;

        $produpqry = "UPDATE " . TBL . "products 
					  SET product_code = '$ProdCode' 
					  WHERE product_id = $listlastID";

        $produpres = mysqli_query($conn,$produpqry);


        //****************************    Admin Primary email fetch starts    *************************

        $admin_primary_email_fetch = mysqli_query($conn,"SELECT * FROM " . TBL . "footer  WHERE footer_id = '1' ");
        $admin_primary_email_fetchrow = mysqli_fetch_array($admin_primary_email_fetch);
        $admin_primary_email = $admin_primary_email_fetchrow['admin_primary_email'];
        $admin_footer_copyright = $admin_primary_email_fetchrow['footer_copyright'];
        $admin_site_name = $admin_primary_email_fetchrow['website_address'];
        $admin_address = $admin_primary_email_fetchrow['footer_address'];

        //****************************    Admin Primary email fetch ends    *************************


        if ($produpres) {

            $admin_email = $admin_primary_email; // Admin Email Id

            $webpage_full_link_with_login = $webpage_full_link. "login";  //URL Login Link

//****************************    Admin email starts    *************************

            $to = $admin_email;
            $subject = "$admin_site_name -New Product has been created";

            $to1 = $email_id;
            $subject1 = "$admin_site_name Product Creation Successful";

            $admin_sql_fetch = mysqli_query($conn,"SELECT * FROM " . TBL . "mail  WHERE mail_id = 19 "); //User mail template fetch
            $admin_sql_fetch_row = mysqli_fetch_array($admin_sql_fetch);

            $mail_template_admin = $admin_sql_fetch_row['mail_template'];

            $message1 =   stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \''
            ,'\' . $mobile_number . \'', '\' . $listing_name . \'', '\' . $listing_email . \'', '\' . $listing_mobile . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'','\'.$webpage_full_link_with_login.\'','\'.$admin_primary_email.\''),
                array(''.$admin_site_name.'', '' . $first_name . '', '' . $email_id . '','' . $mobile_number . '', '' . $listing_name . '', '' . $listing_email . '', '' . $listing_mobile . '', ''.$admin_footer_copyright.'', ''.$admin_address.'', ''.$webpage_full_link.'',''.$webpage_full_link_with_login.'',''.$admin_primary_email.''), $mail_template_admin));


            $headers = "From: " . "$email_id" . "\r\n";
            $headers .= "Reply-To: " . "$email_id" . "\r\n";
            $headers .= "MIME-Version: 1.0\r\n";
            $headers .= "Content-Type: text/html; charset=utf-8\r\n";


            mail($to, $subject, $message1, $headers); //admin email


//****************************    Admin email ends    *************************

//****************************    Client email starts    *************************

            $to1 = $email_id;
            $subject1 = "$admin_site_name Product Creation Successful";

            $client_sql_fetch = mysqli_query($conn,"SELECT * FROM " . TBL . "mail  WHERE mail_id = 18 "); //User mail template fetch
            $client_sql_fetch_row = mysqli_fetch_array($client_sql_fetch);

            $mail_template_client = $client_sql_fetch_row['mail_template'];

            $message2 =   stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \''
            ,'\' . $mobile_number . \'', '\' . $listing_name . \'', '\' . $listing_email . \'', '\' . $listing_mobile . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'','\'.$webpage_full_link_with_login.\'','\'.$admin_primary_email.\''),
                array(''.$admin_site_name.'', '' . $first_name . '', '' . $email_id . '','' . $mobile_number . '', '' . $listing_name . '', '' . $listing_email . '', '' . $listing_mobile . '', ''.$admin_footer_copyright.'', ''.$admin_address.'', ''.$webpage_full_link.'',''.$webpage_full_link_with_login.'',''.$admin_primary_email.''), $mail_template_client));
            

            $headers1 = "From: " . "$admin_email" . "\r\n";
            $headers1 .= "Reply-To: " . "$admin_email" . "\r\n";
            $headers1 .= "MIME-Version: 1.0\r\n";
            $headers1 .= "Content-Type: text/html; charset=utf-8\r\n";


            mail($to1, $subject1, $message2, $headers1); //admin email

//****************************    client email ends    *************************


            $_SESSION['status_msg'] = "New Product has been created Successfully!!!";


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


            header('Location: admin-all-products.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-add-new-product.php');
        }

        //    Listing Insert Part Ends

    }
}else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-add-new-product.php');
}