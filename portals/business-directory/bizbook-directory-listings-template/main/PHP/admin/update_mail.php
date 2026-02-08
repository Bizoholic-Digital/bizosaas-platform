<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['mail_template_submit'])) {


       $sql_fetch = mysqli_query($conn,"SELECT * FROM " . TBL . "footer  WHERE footer_id = '1' ");
        $row_f = mysqli_fetch_array($sql_fetch);

        $website_name = $row_f['website_address'];
        $footer_copyright = $row_f['footer_copyright'];
        $admin_primary_email = $row_f['admin_primary_email'];
        $footer_address = $row_f['footer_address'];

        $mail_template_data1 = $_POST['mail_template_data'];
        $mail_template_data = addslashes(
            str_replace(array($website_name, 'Johxx', 'axx@gmxx.com', 'casxxz', $footer_copyright, $footer_address
            , $webpage_full_link,'axx@gmxx.com', 'DirectoryZZ', '987654xxxx', 'axx@gmxx.com','987654xxxx'
            ,'Eventzz', '987654xxxx', 'axx@gmxx.com', 'Blogzz', '987654xxxx', 'axx@gmxx.com'),
                array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \''
                , '\' . $password . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\''
                ,'\'.$rec_email_id.\'','\' . $listing_name . \'','\' . $listing_mobile . \'','\' . $listing_email . \''
                ,'\' . $mobile_number . \'','\' . $event_name . \'','\' . $event_mobile . \'','\' . $event_email . \''
                ,'\' . $blog_name . \'','\' . $blog_mobile . \'','\' . $blog_email . \''),
                $mail_template_data1));


        $mail_id = $_POST['mail_id'];

        $footer_id = 1;

        $sql = mysqli_query($conn,"UPDATE  " . TBL . "mail SET mail_template ='" . $mail_template_data. "' where mail_id='" . $mail_id . "'");

       
        if ($sql) {

            $_SESSION['status_msg'] = "Mail Template has been Updated Successfully!!!";


            header('Location: admin-all-mail.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-all-mail.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-all-mail.php');
    exit;
}
?>