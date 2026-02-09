<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['footer_submit'])) {


        $footer_description = $_POST['footer_description'];
        $footer_address = $_POST['footer_address'];
        $footer_mobile = $_POST['footer_mobile'];
        $footer_fb = $_POST['footer_fb'];
        $footer_google_plus = $_POST['footer_google_plus'];
        $footer_twitter = $_POST['footer_twitter'];
        $footer_linked_in = $_POST['footer_linked_in'];
        $footer_youtube = $_POST['footer_youtube'];
        $footer_whatsapp = $_POST['footer_whatsapp'];
        $footer_copyright = $_POST['footer_copyright'];

        //Top category Data's
        $top_category_1 = $_POST['top_category_1'];
        $top_category_2 = $_POST['top_category_2'];
        $top_category_3 = $_POST['top_category_3'];
        $top_category_4 = $_POST['top_category_4'];
        $top_category_5 = $_POST['top_category_5'];
        $top_category_6 = $_POST['top_category_6'];
        $top_category_7 = $_POST['top_category_7'];
        $top_category_8 = $_POST['top_category_8'];

        //Trend category Data's
        $trend_category_1 = $_POST['trend_category_1'];
        $trend_category_2 = $_POST['trend_category_2'];
        $trend_category_3 = $_POST['trend_category_3'];
        $trend_category_4 = $_POST['trend_category_4'];
        $trend_category_5 = $_POST['trend_category_5'];
        $trend_category_6 = $_POST['trend_category_6'];
        $trend_category_7 = $_POST['trend_category_7'];
        $trend_category_8 = $_POST['trend_category_8'];

        $mobile_app_andriod = $_POST['mobile_app_andriod'];
        $mobile_app_ios = $_POST['mobile_app_ios'];


        //Footer Page name and url Data's
        $footer_page_name_1 = $_POST['footer_page_name_1'];
        $footer_page_url_1 = $_POST['footer_page_url_1'];
        $footer_page_name_2 = $_POST['footer_page_name_2'];
        $footer_page_url_2 = $_POST['footer_page_url_2'];
        $footer_page_name_3 = $_POST['footer_page_name_3'];
        $footer_page_url_3 = $_POST['footer_page_url_3'];
        $footer_page_name_4 = $_POST['footer_page_name_4'];
        $footer_page_url_4 = $_POST['footer_page_url_4'];

        //Footer Country name and url Data's
        $footer_country_name_1 = $_POST['footer_country_name_1'];
        $footer_country_url_1 = $_POST['footer_country_url_1'];
        $footer_country_name_2 = $_POST['footer_country_name_2'];
        $footer_country_url_2 = $_POST['footer_country_url_2'];
        $footer_country_name_3 = $_POST['footer_country_name_3'];
        $footer_country_url_3 = $_POST['footer_country_url_3'];
        $footer_country_name_4 = $_POST['footer_country_name_4'];
        $footer_country_url_4 = $_POST['footer_country_url_4'];
        $footer_country_name_5 = $_POST['footer_country_name_5'];
        $footer_country_url_5 = $_POST['footer_country_url_5'];
        $footer_country_name_6 = $_POST['footer_country_name_6'];
        $footer_country_url_6 = $_POST['footer_country_url_6'];
        $footer_country_name_7 = $_POST['footer_country_name_7'];
        $footer_country_url_7 = $_POST['footer_country_url_7'];

        $copyright_year = $_POST['copyright_year'];
        $copyright_website = $_POST['copyright_website'];
        $copyright_website_link = $_POST['copyright_website_link'];


        $footer_payment_option123 = $_POST["footer_payment_option"];

        $prefix = $fruitList = '';
        foreach ($footer_payment_option123 as $fruit) {
            $footer_payment_option .= $prefix . $fruit;
            $prefix = ', ';
        }

        $footer_id = $_POST['footer_id'];
        $header_logo_old = $_POST['header_logo_old'];
        $mobile_view_logo_old = $_POST['mobile_view_logo_old'];


        $_FILES['header_logo']['name'];

        if (!empty($_FILES['header_logo']['name'])) {
            $file = rand(1000, 100000) . $_FILES['header_logo']['name'];
            $file_loc = $_FILES['header_logo']['tmp_name'];
            $file_size = $_FILES['header_logo']['size'];
            $file_type = $_FILES['header_logo']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/home/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $header_logo = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $header_logo = $header_logo_old;
            }
        } else {
            $header_logo = $header_logo_old;
        }

        $_FILES['mobile_view_logo']['name'];

        if (!empty($_FILES['mobile_view_logo']['name'])) {
            $file = rand(1000, 100000) . $_FILES['mobile_view_logo']['name'];
            $file_loc = $_FILES['mobile_view_logo']['tmp_name'];
            $file_size = $_FILES['mobile_view_logo']['size'];
            $file_type = $_FILES['mobile_view_logo']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/home/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $mobile_view_logo = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $mobile_view_logo = $mobile_view_logo_old;
            }
        } else {
            $mobile_view_logo = $mobile_view_logo_old;
        }


        $sql = mysqli_query($conn, "UPDATE  " . TBL . "footer SET  footer_description='" . $footer_description . "', footer_address='" . $footer_address . "'
     , footer_mobile='" . $footer_mobile . "', footer_fb='" . $footer_fb . "', footer_google_plus='" . $footer_google_plus . "'
     , footer_twitter='" . $footer_twitter . "', footer_linked_in='" . $footer_linked_in . "', footer_youtube='" . $footer_youtube . "'
     , footer_whatsapp='" . $footer_whatsapp . "', footer_payment_option='" . $footer_payment_option . "', header_logo='" . $header_logo . "'
     , mobile_view_logo='" . $mobile_view_logo . "',footer_copyright='" . $footer_copyright . "'
     , top_category_1='" . $top_category_1 . "',top_category_2='" . $top_category_2 . "'
     , top_category_3='" . $top_category_3 . "',top_category_4='" . $top_category_4 . "'
     , top_category_5='" . $top_category_5 . "',top_category_6='" . $top_category_6 . "'
     , top_category_7='" . $top_category_7 . "',top_category_8='" . $top_category_8 . "'
     , trend_category_1='" . $trend_category_1 . "',trend_category_2='" . $trend_category_2 . "'
     , trend_category_3='" . $trend_category_3 . "',trend_category_4='" . $trend_category_4 . "'
     , trend_category_5='" . $trend_category_5 . "',trend_category_6='" . $trend_category_6 . "'
     , trend_category_7='" . $trend_category_7 . "',trend_category_8='" . $trend_category_8 . "'
     , mobile_app_andriod='" . $mobile_app_andriod . "',mobile_app_ios='" . $mobile_app_ios . "'
     , footer_page_name_1='" . $footer_page_name_1 . "',footer_page_url_1='" . $footer_page_url_1 . "'
     , footer_page_name_2='" . $footer_page_name_2 . "',footer_page_url_2='" . $footer_page_url_2 . "'
     , footer_page_name_3='" . $footer_page_name_3 . "',footer_page_url_3='" . $footer_page_url_3 . "'
     , footer_page_name_4='" . $footer_page_name_4 . "',footer_page_url_4='" . $footer_page_url_4 . "'
     , footer_country_name_1='" . $footer_country_name_1 . "',footer_country_url_1='" . $footer_country_url_1 . "'
     , footer_country_name_2='" . $footer_country_name_2 . "',footer_country_url_2='" . $footer_country_url_2 . "'
     , footer_country_name_3='" . $footer_country_name_3 . "',footer_country_url_3='" . $footer_country_url_3 . "'
     , footer_country_name_4='" . $footer_country_name_4 . "',footer_country_url_4='" . $footer_country_url_4 . "'
     , footer_country_name_5='" . $footer_country_name_5 . "',footer_country_url_5='" . $footer_country_url_5 . "'
     , footer_country_name_6='" . $footer_country_name_6 . "',footer_country_url_6='" . $footer_country_url_6 . "'
     , footer_country_name_7='" . $footer_country_name_7 . "',footer_country_url_7='" . $footer_country_url_7 . "'
     , copyright_year='" . $copyright_year . "',copyright_website='" . $copyright_website . "'
     , copyright_website_link='" . $copyright_website_link . "'
     
     where footer_id='" . $footer_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Footer Data has been Updated Successfully!!!";


            header('Location: admin-footer.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-footer.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-footer.php');
    exit;
}
?>