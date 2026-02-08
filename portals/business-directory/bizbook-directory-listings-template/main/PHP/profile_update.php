<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['profile_update_submit'])) {


        $user_code = $_SESSION['user_code']; //Session User Code

        // $first_name = $_POST["first_name"];
        $last_name = $_POST["last_name"];
        $mobile_number = $_POST["mobile_number"];
        $email_id = $_POST["email_id"];
        $date_of_birth = $_POST["date_of_birth"];
        $user_city = $_POST["user_city"];

        $password_old = $_POST["password_old"];

        if ($_POST["password"] != NULL) {

            $password = md5($_POST["password"]);
        } else {
            $password = $password_old;
        }

        $user_facebook = $_POST["user_facebook"];
        $user_twitter = $_POST["user_twitter"];
        $user_youtube = $_POST["user_youtube"];
        $user_website = $_POST["user_website"];

        $profile_image_old = $_POST["profile_image_old"];
        $cover_image_old = $_POST["cover_image_old"];
        $profile_id_proof_old = $_POST["profile_id_proof_old"];


        $_FILES['profile_image']['name'];

        if (!empty($_FILES['profile_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['profile_image']['name'];
            $file_loc = $_FILES['profile_image']['tmp_name'];
            $file_size = $_FILES['profile_image']['size'];
            $file_type = $_FILES['profile_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "images/user/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $profile_image = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $profile_image = $profile_image_old;
            }
        } else {
            $profile_image = $profile_image_old;
        }

        $_FILES['cover_image']['name'];

        if (!empty($_FILES['cover_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['cover_image']['name'];
            $file_loc = $_FILES['cover_image']['tmp_name'];
            $file_size = $_FILES['cover_image']['size'];
            $file_type = $_FILES['cover_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "images/user/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $cover_image = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $cover_image = $cover_image_old;
            }
        } else {
            $cover_image = $cover_image_old;
        }

        $_FILES['profile_id_proof']['name'];

        if (!empty($_FILES['profile_id_proof']['name'])) {
            $file = rand(1000, 100000) . $_FILES['profile_id_proof']['name'];
            $file_loc = $_FILES['profile_id_proof']['tmp_name'];
            $file_size = $_FILES['profile_id_proof']['size'];
            $file_type = $_FILES['profile_id_proof']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "images/user/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $profile_id_proof = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $profile_id_proof = $profile_id_proof_old;
            }
        } else {
            $profile_id_proof = $profile_id_proof_old;
        }


        $sql = mysqli_query($conn, "UPDATE  " . TBL . "users SET  last_name ='" . $last_name . "'
     ,date_of_birth ='" . $date_of_birth . "', user_city ='" . $user_city . "', profile_image ='" . $profile_image . "'
     ,password ='" . $password . "', user_facebook ='" . $user_facebook . "', user_twitter ='" . $user_twitter . "'
     ,user_youtube ='" . $user_youtube . "', user_website ='" . $user_website . "'
     ,cover_image ='" . $cover_image . "', profile_id_proof ='" . $profile_id_proof . "'
     ,mobile_number='" . $mobile_number . "'
     where user_code='" . $user_code . "'");

        if ($sql) {

            $_SESSION['status_msg'] = $BIZBOOK['USER_PROFILE_UPDATE_SUCCESS_MESSAGE'];


            header('Location: db-my-profile');
            exit;

        } else {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: db-my-profile-edit');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: db-my-profile');
    exit;
}
?>