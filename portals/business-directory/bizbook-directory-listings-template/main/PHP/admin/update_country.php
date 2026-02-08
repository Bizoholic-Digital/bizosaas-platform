<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['country_submit'])) {

        $country_id = $_POST['country_id'];
        $country_name = $_POST['country_name'];


//************ country Name Already Exist Check Starts ***************


        $country_name_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "countries  WHERE country_name='" . $country_name . "' AND country_id != $country_id ");

        if (mysqli_num_rows($country_name_exist_check) > 0) {


            $_SESSION['status_msg'] = "The Given country name is Already Exist Try Other!!!";

            header('Location: admin-country-edit.php?row=' . $country_id);
            exit;


        }

//************ country Name Already Exist Check Ends ***************


        $_FILES['country_image']['name'];

        if (!empty($_FILES['country_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['country_image']['name'];
            $file_loc = $_FILES['country_image']['tmp_name'];
            $file_size = $_FILES['country_image']['size'];
            $file_type = $_FILES['country_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/services/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $country_image = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $country_image = $country_image_old;
            }
        } else {
            $country_image = $country_image_old;
        }


        $sql = mysqli_query($conn, "UPDATE  " . TBL . "countries SET country_name='" . $country_name . "'
     where country_id='" . $country_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Country has been Updated Successfully!!!";


            header('Location: admin-all-country.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-country-edit.php?row=' . $country_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-all-country.php');
    exit;
}
?>