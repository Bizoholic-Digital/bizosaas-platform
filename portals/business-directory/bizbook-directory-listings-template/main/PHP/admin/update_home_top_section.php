<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['top_section_submit'])) {

        $top_section_id = $_POST["top_section_id"];

        $top_section_image_old = $_POST["top_section_image_old"];


        $top_section_title = $_POST["top_section_title"];
        $top_section_description = $_POST["top_section_description"];
        $top_section_link_text = $_POST["top_section_link_text"];
        $top_section_link = $_POST["top_section_link"];


        if (!empty($_FILES['top_section_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['top_section_image']['name'];
            $file_loc = $_FILES['top_section_image']['tmp_name'];
            $file_size = $_FILES['top_section_image']['size'];
            $file_type = $_FILES['top_section_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/icon/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $top_section_image_old1 = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $top_section_image_old1);
                $top_section_image = compressImage($top_section_image_old1, $file_loc, $folder, $new_size);
            } else {
                $top_section_image = $top_section_image_old;
            }
        } else {
            $top_section_image = $top_section_image_old;
        }


        $event_qry =
            "UPDATE  " . TBL . "homepage_top_section  SET top_section_title='" . $top_section_title . "'
            , top_section_description='" . $top_section_description . "', top_section_link_text='" . $top_section_link_text . "'
            , top_section_link='" . $top_section_link . "', top_section_image='" . $top_section_image . "' 
            where top_section_id='" . $top_section_id . "'";


        $event_res = mysqli_query($conn, $event_qry);


        if ($event_res) {

            $_SESSION['status_msg'] = "Your Home Page Top Section has been Updated Successfully!!!";

            header('Location: admin-home-top-section.php');
            exit();

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header("Location: admin-home-top-section-edit.php?row=$top_section_id");
            exit();
        }

        //    Top Section Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-home-top-section.php');
    exit();
}