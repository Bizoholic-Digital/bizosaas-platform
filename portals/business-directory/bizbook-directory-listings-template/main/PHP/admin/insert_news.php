<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD']=='POST') {

    if (isset($_POST['news_submit'])) {

        $news_title = addslashes($_POST["news_title"]);
        $news_description = addslashes($_POST["news_description"]);
        $category_id = $_POST["category_id"];
        
        $seo_title = $_POST["seo_title"];
        $seo_description = $_POST["seo_description"];
        $seo_keywords = $_POST["seo_keywords"];

// News Status
        $news_status = "Active";


        if (!empty($_FILES['news_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['news_image']['name'];
            $file_loc = $_FILES['news_image']['tmp_name'];
            $file_size = $_FILES['news_image']['size'];
            $file_type = $_FILES['news_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if(in_array($file_type, $allowed)) {
                $folder = "../news/images/news/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $news_image_1 = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $news_image_1);
                $news_image = compressImage($news_image_1, $file_loc, $folder, $new_size);
            }else{
                $news_image = '';
            }
        }

        function checkNewsSlug($link, $counter=1){
            global $conn;
            $newLink = $link;
            do{
                $checkLink = mysqli_query($conn, "SELECT news_id FROM " . TBL . "news WHERE news_slug = '$newLink'");
                if(mysqli_num_rows($checkLink) > 0){
                    $newLink = $link.''.$counter;
                    $counter++;
                } else {
                    break;
                }
            } while(1);

            return $newLink;
        }


        $news_title1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $news_title));
        $news_slug = checkNewsSlug($news_title1);

//    news Insert Part Starts


        $news_qry = "INSERT INTO " . TBL . "news 
					(news_title, news_description, news_image, news_status,  category_id, news_slug, seo_title, seo_description, seo_keywords, news_cdt) 
					VALUES 
					('$news_title', '$news_description', '$news_image', '$news_status', '$category_id', '$news_slug', '$seo_title', '$seo_description', '$seo_keywords', '$curDate')";

        $news_res = mysqli_query($conn,$news_qry);


        //****************************    Admin Primary email fetch starts    *************************

        $admin_primary_email_fetch = mysqli_query($conn,"SELECT * FROM " . TBL . "footer  WHERE footer_id = '1' ");
        $admin_primary_email_fetchrow = mysqli_fetch_array($admin_primary_email_fetch);
        $admin_primary_email = $admin_primary_email_fetchrow['admin_primary_email'];
        $admin_footer_copyright = $admin_primary_email_fetchrow['footer_copyright'];
        $admin_site_name = $admin_primary_email_fetchrow['website_address'];
        $admin_address = $admin_primary_email_fetchrow['footer_address'];

        //****************************    Admin Primary email fetch ends    *************************


        if ($news_res) {

            $admin_email = $admin_primary_email; // Admin Email Id

            $webpage_full_link_with_login = $webpage_full_link. "login";  //URL Login Link

//****************************    Admin email starts    *************************

            $to = $admin_email;
            $subject = "$admin_site_name -New News has been created";

            $admin_sql_fetch = mysqli_query($conn,"SELECT * FROM " . TBL . "mail WHERE mail_id = 15 "); //admin mail template fetch
            $admin_sql_fetch_row = mysqli_fetch_array($admin_sql_fetch);

            $mail_template_admin = $admin_sql_fetch_row['mail_template'];

            $message1 =   stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \''
            ,'\' . $mobile_number . \'', '\' . $news_title . \'', '\' . $news_email . \'', '\' . $news_mobile . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'','\'.$webpage_full_link_with_login.\'','\'.$admin_primary_email.\''),
                array(''.$admin_site_name.'', '' . $first_name . '', '' . $email_id . '','' . $mobile_number . '', '' . $news_title . '', '' . $news_email . '', '' . $news_mobile . '', ''.$admin_footer_copyright.'', ''.$admin_address.'', ''.$webpage_full_link.'',''.$webpage_full_link_with_login.'',''.$admin_primary_email.''), $mail_template_admin));


            $headers = "From: " . "$email_id" . "\r\n";
            $headers .= "Reply-To: " . "$email_id" . "\r\n";
            $headers .= "MIME-Version: 1.0\r\n";
            $headers .= "Content-Type: text/html; charset=utf-8\r\n";


            mail($to, $subject, $message1, $headers); //admin email


//****************************    Admin email ends    *************************


                $_SESSION['status_msg'] = "New News has been created Successfully!!!";

                header('Location: news-all.php');

                exit();
            } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: news-add-new.php');
        }

        //    news Insert Part Ends

    }
}else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: news-all.php');
}