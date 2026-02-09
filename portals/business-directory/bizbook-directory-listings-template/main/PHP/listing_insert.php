<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD']=='POST') {
    if (isset($_POST['listing_submit'])) {

        $_SESSION['listing_info_question'] = $_POST["listing_info_question"];
        $_SESSION['listing_info_answer'] = $_POST["listing_info_answer"];

// Basic Personal Details
        $first_name = $_SESSION["first_name"];
        $last_name = $_SESSION["last_name"];
        $mobile_number = $_SESSION["mobile_number"];
        $email_id = $_SESSION["email_id"];

        $register_mode = "Direct";
        
// Common Listing Details
        $listing_name = $_SESSION["listing_name"];
        $listing_mobile = $_SESSION["listing_mobile"];
        $listing_email = $_SESSION["listing_email"];
        $listing_website = $_SESSION["listing_website"];
        $listing_whatsapp = $_SESSION["listing_whatsapp"];
        $listing_address = $_SESSION["listing_address"];
        $listing_lat = $_SESSION["listing_lat"];
        $listing_lng = $_SESSION["listing_lng"];
        $listing_description = addslashes($_SESSION["listing_description"]);
        if(isset($_SESSION['listing_type_id']) && !empty($_SESSION['listing_type_id'])) {
            $listing_type_id = $_SESSION["listing_type_id"];
        }else{
            $listing_type_id = 1;
        }
        $country_id = $_SESSION["country_id"];
        $service_locations = $_SESSION["service_locations"];

        $state_id = "1";

        $city_id1 = $_SESSION["city_id"];

        $prefix = $fruitList = '';
        foreach ($city_id1 as $fruit)
        {
            $city_id .= $prefix .  $fruit ;
            $prefix = ',';
        }

        $category_id = $_SESSION["category_id"];

        $sub_category_id123 = $_SESSION["sub_category_id"];

        $prefix = $fruitList = '';
        foreach ($sub_category_id123 as $fruit)
        {
            $sub_category_id .= $prefix .  $fruit ;
            $prefix = ',';
        }

        $service_id123 = $_SESSION["service_id"];

        $prefix1 = $fruitList = '';
        foreach ($service_id123 as $fruit1)
        {
            $service_id .= $prefix1 .  $fruit1 ;
            $prefix1 = ',';
        }


// Listing Timing Details
        $opening_days = $_SESSION["opening_days"];
        $opening_time = $_SESSION["opening_time"];
        $closing_time = $_SESSION["closing_time"];

// Listing Social Link Details
        $fb_link = $_SESSION["fb_link"];
        $gplus_link = $_SESSION["gplus_link"];
        $twitter_link = $_SESSION["twitter_link"];

// Listing Location Details
        $google_map = $_SESSION["google_map"];
        $threesixty_view = $_SESSION["360_view"];

        // Listing Video
        $listing_video123 = $_SESSION['listing_video'];

        $prefix6 = $fruitList = '';
        foreach ($listing_video123 as $fruit6)
        {
            $listing_video1 = $prefix6 .  $fruit6 ;
            $listing_video .= addslashes($listing_video1);
            $prefix6 = '|';
        }


// Listing Service Names Details

        $service_1_name123 = $_SESSION["service_1_name"];
        
        $service_1_name = implode("|",$service_1_name123);

// Listing Offer Prices Details
        $service_1_price123 = $_SESSION["service_1_price"];

        $prefix1 = $fruitList = '';
        foreach ($service_1_price123 as $fruit1)
        {
            $service_1_price .= $prefix1 .  $fruit1 ;
            $prefix1 = ',';
        }
        $service_2_price = 0;
        $service_3_price = 0;
        $service_4_price = 0;
        $service_5_price = 0;
        $service_6_price = 0;

// Listing Offer Details
        $service_1_detail123 = $_SESSION["service_1_detail"];

        $service_1_detail1 = implode("|",$service_1_detail123);
        $service_1_detail = addslashes($service_1_detail1);

// Listing Offer View more link
        $service_1_view_more123 = $_SESSION["service_1_view_more"];
        $prefix1 = $fruitList = '';
        foreach ($service_1_view_more123 as $fruit1)
        {
            $service_1_view_more .= $prefix1 .  $fruit1 ;
            $prefix1 = ',';
        }
        

//Listing Other Informations
        $listing_info_question123 = $_SESSION["listing_info_question"];
        $prefix1 = $fruitList = '';
        foreach ($listing_info_question123 as $fruit1)
        {
            $listing_info_question .= $prefix1 .  $fruit1 ;
            $prefix1 = ',';
        }

        $listing_info_answer123 = $_SESSION["listing_info_answer"];
        $prefix1 = $fruitList = '';
        foreach ($listing_info_answer123 as $fruit1)
        {
            $listing_info_answer .= $prefix1 .  $fruit1 ;
            $prefix1 = ',';
        }

        // $listing_status = "Pending";
        $payment_status = "Pending";

        function checkListingSlug($link, $counter=1){
            global $conn;
            $newLink = $link;
            do{
                $checkLink = mysqli_query($conn, "SELECT listing_id FROM " . TBL . "listings WHERE listing_slug = '$newLink'");
                if(mysqli_num_rows($checkLink) > 0){
                    $newLink = $link.''.$counter;
                    $counter++;
                } else {
                    break;
                }
            } while(1);

            return $newLink;
        }


        $listing_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $listing_name));
        $listing_slug = checkListingSlug($listing_name1);

//    Condition to get User Id starts

        if (isset($_SESSION['user_code']) && !empty($_SESSION['user_code'])) {
            $user_code = $_SESSION['user_code'];
            $user_details = mysqli_query($conn,"SELECT * FROM  " . TBL . "users where user_code='" . $user_code . "'");
            $user_details_row = mysqli_fetch_array($user_details);

            $user_id = $user_details_row['user_id'];  //User Id

            if($user_details_row['user_status'] == 'Active'){
                // Listing Status
                $listing_status = "Active";
            }else{
                // Listing Status
                $listing_status = "Inactive";
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
            
            $upres = mysqli_query($conn,$upqry);

            $user_id = $lastID; //User Id
            
            // Listing Status
            $listing_status = "Inactive";

        }
//    Condition to get User Id Ends

//************************  Profile Image Upload starts  **************************

        $profile_image = $_SESSION['profile_image'];
//************************  Profile Image Upload Ends  **************************

//************************  Cover Image Upload starts  **************************

        $cover_image = $_SESSION['cover_image'];

//************************  Cover Image Upload ends  **************************

// ************************  Gallery Image Upload starts  **************************

        $gallery_image = $_SESSION['gallery_image'];

// ************************  Gallery Image Upload ends  **************************   

// ************************  Service Image Upload starts  ************************** 

        $service_image = $_SESSION['service_image'];

// ************************  Service Image Upload ends  **************************

// ************************  Offer Image Upload Starts  **************************

        $service_1_image = $_SESSION['service_1_image'];

// ************************  Offer Image Upload ends  **************************

//    Listing Insert Part Starts

        $listing_qry = "INSERT INTO " . TBL . "listings 
					(user_id, category_id, sub_category_id, service_id, service_image, listing_type_id, listing_name, listing_mobile, listing_email
					, listing_website, listing_whatsapp, listing_description, listing_address, listing_lat, listing_lng, service_locations, country_id, state_id, city_id, profile_image, cover_image
					, gallery_image, opening_days, opening_time, closing_time, fb_link, twitter_link, gplus_link, google_map
					, 360_view, listing_video, service_1_name, service_1_price, service_1_detail, service_1_image, service_1_view_more, service_2_name,service_2_price, service_2_image, service_3_name,service_3_price, service_3_image
					, service_4_name,service_4_price,service_4_image,service_5_name,service_5_price, service_5_image, service_6_name,service_6_price, service_6_image, listing_status
					, listing_info_question , listing_info_answer, payment_status, listing_slug, listing_cdt) 
					VALUES 
					('$user_id', '$category_id', '$sub_category_id', '$service_id', '$service_image', '$listing_type_id', '$listing_name', '$listing_mobile', '$listing_email', '$listing_website', '$listing_whatsapp', '$listing_description', '$listing_address'
					, '$listing_lat', '$listing_lng', '$service_locations', '$country_id', $state_id, '$city_id', '$profile_image', '$cover_image'
					,'$gallery_image', '$opening_days', '$opening_time', '$closing_time', '$fb_link', '$twitter_link', '$gplus_link', '$google_map'
					,'$threesixty_view', '$listing_video', '$service_1_name', '$service_1_price', '$service_1_detail', '$service_1_image', '$service_1_view_more', '$service_2_name', '$service_2_price', '$service_2_image', '$service_3_name', '$service_3_price', '$service_3_image'
					, '$service_4_name', '$service_4_price', '$service_4_image', '$service_5_name', '$service_5_price', '$service_5_image', '$service_6_name', '$service_6_price', '$service_6_image', '$listing_status'
					, '$listing_info_question', '$listing_info_answer', '$payment_status', '$listing_slug', '$curDate')";

        $listing_res = mysqli_query($conn,$listing_qry);
        $ListingID = mysqli_insert_id($conn);
        $listlastID = $ListingID;
      
        switch (strlen($ListingID)) {
            case 1:
                $ListingID = '00' . $ListingID;
                break;
            case 2:
                $ListingID = '0' . $ListingID;
                break;
            default:
                $ListingID = $ListingID;
                break;
        }

        $ListCode = 'LIST' . $ListingID;

        $lisupqry = "UPDATE " . TBL . "listings 
					  SET listing_code = '$ListCode' 
					  WHERE listing_id = $listlastID";

        $lisupres = mysqli_query($conn,$lisupqry);

        //****************************    Top Service Providers listing count check and addition starts    *************************


        //**  To check the given category id is available on top_service_provider_table    ***

        $top_service_sql = "SELECT * FROM  " . TBL . "top_service_providers where top_service_provider_category_id='".$category_id."'";
        $top_service_sql_rs = mysqli_query($conn, $top_service_sql);
        $top_service_sql_count = mysqli_num_rows($top_service_sql_rs);

        if($top_service_sql_count > 0){  //if category ID available in top service provider

            $top_service_sql_row = mysqli_fetch_array($top_service_sql_rs);

            $top_service_provider_listings = $top_service_sql_row['top_service_provider_listings'];
            $top_service_provider_category_id = $top_service_sql_row['top_service_provider_category_id'];

            $top_service_provider_listings_array = explode(",", $top_service_provider_listings);

            $top_service_provider_listings_array_count = count($top_service_provider_listings_array);

            if($top_service_provider_listings_array_count <= 4){   //if Listings less than or equal to 4 means update top service provider

                $parts = $top_service_provider_listings_array;
                $parts[] = $ListingID;                                  //updating existing listings array with new listing ID

                $top_service_provider_listings_new = implode(',', $parts);

                $top_service_provider_sql = mysqli_query($conn,"UPDATE  " . TBL . "top_service_providers SET top_service_provider_listings = '$top_service_provider_listings_new'
     where top_service_provider_category_id='" . $top_service_provider_category_id . "'");

            }
        }

        //****************************    Top Service Providers listing count check and addition ends    *************************

        //****************************    Admin Primary email fetch starts    *************************

        $admin_primary_email_fetch = mysqli_query($conn,"SELECT * FROM " . TBL . "footer  WHERE footer_id = '1' ");
        $admin_primary_email_fetchrow = mysqli_fetch_array($admin_primary_email_fetch);
        $admin_primary_email = $admin_primary_email_fetchrow['admin_primary_email'];
        $admin_footer_copyright = $admin_primary_email_fetchrow['footer_copyright'];
        $admin_site_name = $admin_primary_email_fetchrow['website_address'];
        $admin_address = $admin_primary_email_fetchrow['footer_address'];

        //****************************    Admin Primary email fetch ends    *************************


        if ($lisupres) {

            $admin_email = $admin_primary_email; // Admin Email Id

            $webpage_full_link_with_login = $webpage_full_link. "login";  //URL Login Link

//****************************    Admin email starts    *************************

            $to = $admin_email;
            $LISTING_INSERT_ADMIN_SUBJECT =  $BIZBOOK['LISTING_INSERT_ADMIN_SUBJECT'];
            $subject = "$admin_site_name $LISTING_INSERT_ADMIN_SUBJECT";
            

            $admin_sql_fetch = mysqli_query($conn,"SELECT * FROM " . TBL . "mail  WHERE mail_id = 7 "); //User mail template fetch
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
            $LISTING_INSERT_CLIENT_SUBJECT =  $BIZBOOK['LISTING_INSERT_CLIENT_SUBJECT'];
            $subject1 = "$admin_site_name $LISTING_INSERT_CLIENT_SUBJECT";

            $client_sql_fetch = mysqli_query($conn,"SELECT * FROM " . TBL . "mail  WHERE mail_id = 6 "); //User mail template fetch
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
            unset($_SESSION['listing_whatsapp']);
            unset($_SESSION['listing_address']);
            unset($_SESSION['listing_lat']);
            unset($_SESSION['listing_lng']);
            unset($_SESSION['listing_description']);
            unset($_SESSION['category_id']);
            unset($_SESSION['sub_category_id']);

            unset($_SESSION['country_id']);
            unset($_SESSION['service_locations']);
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
            unset($_SESSION['listing_video']);
            unset($_SESSION['gallery_image']);
            
            unset($_SESSION['listing_info_question']);
            unset($_SESSION['listing_info_answer']);
           

            header('Location: add-listing-step-6?code='.$ListCode);
        } else {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: add-listing-step-1');
        }

        //    Listing Insert Part Ends

    }
}else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: add-listing-step-1');
}