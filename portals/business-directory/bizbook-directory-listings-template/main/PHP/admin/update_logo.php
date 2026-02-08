<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['logo_form_submit'])) {

        $footer_id = $_POST['footer_id'];
        $header_logo_old = $_POST['header_logo_old'];

        $header_logo_width = $_POST['header_logo_width'];
        $header_logo_height = $_POST['header_logo_height'];

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


        $sql = mysqli_query($conn, "UPDATE  " . TBL . "footer SET  header_logo_width = '" . $header_logo_width . "'
        ,header_logo_height = '" . $header_logo_height . "', header_logo = '" . $header_logo . "'
        where footer_id = '" . $footer_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Logo has been Updated Successfully!!!";

            header('Location: admin-logo.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-logo.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-setting.php');
    exit;
}
?>