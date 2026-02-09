<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}


if ($_SERVER['REQUEST_METHOD']=='POST') {
    if (isset($_POST['company_profile_submit'])) {

// Common Company Profile Details
        
        $company_name= addslashes($_POST["company_name"]);
        $company_address = $_POST["company_address"];
        $company_mobile = $_POST["company_mobile"];
        $company_email_id = $_POST["company_email_id"];
        $company_website = $_POST["company_website"];

        $company_tax = $_POST["company_tax"];

        $company_facebook = $_POST["company_facebook"];
        $company_twitter = $_POST["company_twitter"];
        $company_linkedin = $_POST["company_linkedin"];
        $company_instagram = $_POST["company_instagram"];
        $company_youtube = $_POST["company_youtube"];
        $company_whatsapp = $_POST["company_whatsapp"];

        $company_profile_photo_old = $_POST["company_profile_photo_old"];
        $company_banner_photo_old = $_POST["company_banner_photo_old"];
        $company_header_photo_old = $_POST["company_header_photo_old"];

        $company_description = addslashes($_POST["company_description"]);

        $company_listings = '';
        
        $company_products123 = $_POST["company_products"];
        
        $prefix = '';
        foreach ($company_products123 as $fruit)
        {
            $company_products .= $prefix .  $fruit ;
            $prefix = ',';
        }
        
        $company_events123 = $_POST["company_events"];

        $prefix1 = '';
        foreach ($company_events123 as $fruit1)
        {
            $company_events .= $prefix1 .  $fruit1 ;
            $prefix1 = ',';
        }
        
        $company_blogs123 = $_POST["company_blogs"];
        
        $prefix2 = '';
        foreach ($company_blogs123 as $fruit2)
        {
            $company_blogs .= $prefix2 .  $fruit2 ;
            $prefix2 = ',';
        }

        $company_seo_description = $_POST["company_seo_description"];
        $company_seo_keywords = $_POST["company_seo_keywords"];

        $company_status = "Active";

        
        
        //************************  Header Logo Image Upload starts  **************************

        if (!empty($_FILES['comp-head-logo']['name'])) {
            $file = rand(1000, 100000) . $_FILES['comp-head-logo']['name'];
            $file_loc = $_FILES['comp-head-logo']['tmp_name'];
            $file_size = $_FILES['comp-head-logo']['size'];
            $file_type = $_FILES['comp-head-logo']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if(in_array($file_type, $allowed)) {
                $folder = "images/user/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $company_header_photo = compressImage($event_image, $file_loc, $folder, $new_size);
            }else{
                $company_header_photo = $company_header_photo_old;
            }
        }else {
            $company_header_photo = $company_header_photo_old;
        }

//************************  Header Logo Image Upload Ends  **************************

//************************  Profile Image Upload starts  **************************

        if (!empty($_FILES['comp-top-logo']['name'])) {
            $file = rand(1000, 100000) . $_FILES['comp-top-logo']['name'];
            $file_loc = $_FILES['comp-top-logo']['tmp_name'];
            $file_size = $_FILES['comp-top-logo']['size'];
            $file_type = $_FILES['comp-top-logo']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if(in_array($file_type, $allowed)) {
                $folder = "images/user/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $company_profile_photo = compressImage($event_image, $file_loc, $folder, $new_size);
            }else{
                $company_profile_photo = $company_profile_photo_old;
            }
        }else {
            $company_profile_photo = $company_profile_photo_old;
        }

//************************  Profile Image Upload Ends  **************************

//************************  Cover Image Upload starts  **************************

        if (!empty($_FILES['comp-bann-logo']['name'])) {
            $file = rand(1000, 100000) . $_FILES['comp-bann-logo']['name'];
            $file_loc = $_FILES['comp-bann-logo']['tmp_name'];
            $file_size = $_FILES['comp-bann-logo']['size'];
            $file_type = $_FILES['comp-bann-logo']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if(in_array($file_type, $allowed)) {
                $folder = "images/user/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $company_banner_photo = compressImage($event_image, $file_loc, $folder, $new_size);
            }else{
                $company_banner_photo = $company_banner_photo_old;
            }
        }else {
            $company_banner_photo = $company_banner_photo_old;
    }

//************************  Cover Image Upload ends  **************************


//************ User Company Already Exist Check Starts ***************

        $user_id = $_SESSION['user_id'];

        $user_company_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "user_company  WHERE user_id='" . $user_id . "' ");

        if (mysqli_num_rows($user_company_exist_check) > 0) {

            $user_company_fetchrow = mysqli_fetch_array($user_company_exist_check);

            $user_company_id = $user_company_fetchrow['user_company_id'];

            //User Company URL slug for update starts

            function checkUserCompanyUpdateSlug($link,$user_company_id, $counter=1){
                global $conn;
                $newLink = $link;
                do{
                    $checkLink = mysqli_query($conn, "SELECT user_company_id FROM " . TBL . "user_company WHERE company_slug = '$newLink' AND user_company_id != '$user_company_id'");
                    if(mysqli_num_rows($checkLink) > 0){
                        $newLink = $link.''.$counter;
                        $counter++;
                    } else {
                        break;
                    }
                } while(1);

                return $newLink;
            }

            $company_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $company_name));
            $company_slug = checkUserCompanyUpdateSlug($company_name1,$user_company_id);

            //User Company URL slug for update ends

            $company_profile_res = mysqli_query($conn,"UPDATE  " . TBL . "user_company SET  company_name='" . $company_name. "'
     ,company_email_id='" . $company_email_id . "', company_mobile='" . $company_mobile. "', company_address='" . $company_address . "'
     ,company_website='" . $company_website . "', company_tax='" . $company_tax . "', company_facebook='" . $company_facebook. "', company_twitter='" . $company_twitter . "'
     ,company_linkedin='" . $company_linkedin . "', company_instagram='" . $company_instagram. "', company_youtube='" . $company_youtube . "'
     ,company_whatsapp='" . $company_whatsapp . "', company_description='" . $company_description. "', company_profile_photo='" . $company_profile_photo . "'
     , company_header_photo='" . $company_header_photo . "'
     ,company_banner_photo='" . $company_banner_photo . "', company_listings='" . $company_listings. "', company_products='" . $company_products . "'
     ,company_blogs='" . $company_blogs . "', company_events ='" . $company_events. "', company_seo_description='" . $company_seo_description . "'
     ,company_seo_keywords='" . $company_seo_keywords . "', company_slug ='" . $company_slug. "', company_status='" . $company_status . "'
     where user_company_id ='" . $user_company_id . "'");

        }else{

            //User Company URL slug for insert starts

            function checkUserCompanySlug($link, $counter=1){
                global $conn;
                $newLink = $link;
                do{
                    $checkLink = mysqli_query($conn, "SELECT user_company_id FROM " . TBL . "user_company WHERE user_slug = '$newLink'");
                    if(mysqli_num_rows($checkLink) > 0){
                        $newLink = $link.''.$counter;
                        $counter++;
                    } else {
                        break;
                    }
                } while(1);

                return $newLink;
            }

            //User Company URL slug for insert ends

            $company_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $company_name));

            $company_slug = checkUserCompanySlug($company_name1);


            $company_profile_qry = "INSERT INTO " . TBL . "user_company 
					(user_id, company_name, company_email_id, company_mobile, company_address, company_website, company_tax, company_facebook, company_twitter, company_linkedin
					, company_instagram, company_youtube, company_whatsapp, company_description, company_profile_photo, company_header_photo, company_banner_photo, company_listings, company_products, company_blogs
					, company_events, company_seo_description, company_seo_keywords, company_slug, company_status, company_cdt) 
					VALUES 
					('$user_id', '$company_name', '$company_email_id', '$company_mobile', '$company_address', '$company_website', '$company_tax', '$company_facebook', '$company_twitter', '$company_linkedin'
					, '$company_instagram', '$company_youtube', '$company_whatsapp', '$company_description', '$company_profile_photo', '$company_header_photo', '$company_banner_photo', '$company_listings', '$company_products', '$company_blogs'
					, '$company_events', '$company_seo_description','$company_seo_keywords', '$company_slug', '$company_status',  '$curDate')";

            $company_profile_res = mysqli_query($conn,$company_profile_qry);
        }

//************ User Company Already Exist Check Ends ***************


        if ($company_profile_res) {

            $_POST['status_msg'] = $BIZBOOK['COMPANY_PROFILE_SUCCESS_MESSAGE'];
            header('Location: dashboard');
        } else {

            $_POST['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: dashboard');
        }

        //    Listing Insert Part Ends

    }
}else {

    $_POST['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: dashboard');
}