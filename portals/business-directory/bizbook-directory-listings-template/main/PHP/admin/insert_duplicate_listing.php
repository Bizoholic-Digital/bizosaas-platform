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

        $listing_code = $_POST["listing_id"];
        $user_code = $_POST["user_code"];

        $listing_name = $_POST["listing_name"];

        $user_details = mysqli_query($conn,"SELECT * FROM  " . TBL . "users where user_code='" . $user_code . "'");
        $user_details_row = mysqli_fetch_array($user_details);

        $user_id = $user_details_row['user_id'];  //User Id
        
        $listings_a = mysqli_query($conn,"SELECT * FROM  " . TBL . "listings where listing_code='" . $listing_code . "'");
        $listings_a_row = mysqli_fetch_array($listings_a);

// Basic Personal Details
        $first_name = $listings_a_row["first_name"];
        $last_name = $listings_a_row["last_name"];
        $mobile_number = $user_details_row["mobile_number"]; //User Mobile Number
        $email_id = $user_details_row["email_id"]; //User Email Id
        

        $register_mode = "Direct";
        $user_status = "Inactive";

// Common Listing Details

        $listing_mobile = $listings_a_row["listing_mobile"];
        $listing_email = $listings_a_row["listing_email"];
        $listing_website = $listings_a_row["listing_website"];
        $listing_whatsapp = $listings_a_row["listing_whatsapp"];
        $listing_address = $listings_a_row["listing_address"];
        $listing_description = addslashes($listings_a_row["listing_description"]);
        $listing_type_id = $listings_a_row["listing_type_id"];

        $country_id = $listings_a_row["country_id"];
        
        $state_id = "1";

        $city_id = $listings_a_row["city_id"];
        
        $profile_image = $listings_a_row["profile_image"];
        $gallery_image = $listings_a_row["gallery_image"];
        $cover_image = $listings_a_row["cover_image"];

        $category_id = $listings_a_row["category_id"];

        $sub_category_id = $listings_a_row["sub_category_id"];

        $service_id = $listings_a_row["service_id"];
        $service_image = $listings_a_row["service_image"];

// Listing Timing Details
        $opening_days = $listings_a_row["opening_days"];
        $opening_time = $listings_a_row["opening_time"];
        $closing_time = $listings_a_row["closing_time"];

// Listing Social Link Details
        $fb_link = $listings_a_row["fb_link"];
        $gplus_link = $listings_a_row["gplus_link"];
        $twitter_link = $listings_a_row["twitter_link"];

// Listing Location Details
        $google_map = $listings_a_row["google_map"];
        $threesixty_view = $listings_a_row["360_view"];
        
// Listing Video
        $listing_video = $listings_a_row["listing_video"];

// Listing Service Names Details

        $service_1_name = $listings_a_row["service_1_name"];

// Listing Offer Prices Details
        $service_1_price = $listings_a_row["service_1_price"];

// Listing Offer Details
        $service_1_detail = addslashes($listings_a_row["service_1_detail"]);

// Listing Offer image
        $service_1_image = $listings_a_row["service_1_image"];
        
// Listing Offer view more        
        $service_1_view_more = $listings_a_row["service_1_view_more"];

//Listing Other Informations
        
        $listing_info_question = $listings_a_row["listing_info_question"];
        $listing_info_answer = $listings_a_row["listing_info_answer"];
        
// Listing Status
        $listing_status = "Active";
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

//    Listing Insert Part Starts

        $listing_qry = "INSERT INTO " . TBL . "listings 
					(user_id, category_id, sub_category_id, service_id, service_image, listing_type_id, listing_name, listing_mobile, listing_email
					, listing_website, listing_whatsapp, listing_description, listing_address, country_id, state_id, city_id, profile_image, cover_image
					, gallery_image, opening_days, opening_time, closing_time, fb_link, twitter_link, gplus_link, google_map
					, 360_view, listing_video, service_1_name, service_1_price, service_1_detail, service_1_image, service_1_view_more, service_2_name,service_2_price, service_2_image, service_3_name,service_3_price, service_3_image
					, service_4_name,service_4_price,service_4_image,service_5_name,service_5_price, service_5_image, service_6_name,service_6_price, service_6_image, listing_status
					, listing_info_question , listing_info_answer, payment_status, listing_slug, listing_cdt) 
					VALUES 
					('$user_id', '$category_id', '$sub_category_id', '$service_id', '$service_image', '$listing_type_id', '$listing_name', '$listing_mobile', '$listing_email', '$listing_website', '$listing_whatsapp', '$listing_description', '$listing_address', '$country_id'
					, '$state_id', '$city_id', '$profile_image', '$cover_image'
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

//****************************    Admin email starts    *************************

            $to = $admin_email;
            $LISTING_INSERT_ADMIN_SUBJECT = "-New Listing has been created";
            $subject = "$admin_site_name $LISTING_INSERT_ADMIN_SUBJECT";

            $admin_sql_fetch = mysqli_query($conn,"SELECT * FROM " . TBL . "mail  WHERE mail_id = 7 "); //admin mail template fetch
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
            $LISTING_INSERT_CLIENT_SUBJECT = "- Listing Creation Successful";
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


            $_SESSION['status_msg'] = "New Duplicate Listing has been created Successfully!!!";

            header('Location: admin-all-listings.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: create-duplicate-listing.php');
        }

        //    Listing Insert Part Ends

    }
}else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: create-duplicate-listing.php');
}