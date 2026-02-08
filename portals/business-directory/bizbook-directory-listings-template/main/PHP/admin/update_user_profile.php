<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['register_submit'])) {


        $path_id = $_POST['path_id'];
        $user_id = $_POST['user_id']; //Session User Code

        $first_name = $_POST["first_name"];
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


        $_FILES['profile_image']['name'];

        if (!empty($_FILES['profile_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['profile_image']['name'];
            $file_loc = $_FILES['profile_image']['tmp_name'];
            $file_size = $_FILES['profile_image']['size'];
            $file_type = $_FILES['profile_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/user/";
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

        function checkUserSlug($link, $user_id, $counter = 1)
        {
            global $conn;
            $newLink = $link;
            do {
                $checkLink = mysqli_query($conn, "SELECT user_id FROM " . TBL . "users WHERE user_slug = '$newLink' AND user_id != '$user_id'");
                if (mysqli_num_rows($checkLink) > 0) {
                    $newLink = $link . '' . $counter;
                    $counter++;
                } else {
                    break;
                }
            } while (1);

            return $newLink;
        }

        $first_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $first_name));
        $user_slug = checkUserSlug($first_name1, $user_id);


        $sql = mysqli_query($conn, "UPDATE  " . TBL . "users SET first_name='" . $first_name . "', last_name='" . $last_name . "'
     ,date_of_birth='" . $date_of_birth . "', user_city='" . $user_city . "', profile_image='" . $profile_image . "'
     ,password='" . $password . "', user_facebook='" . $user_facebook . "', user_twitter='" . $user_twitter . "'
     ,user_youtube='" . $user_youtube . "', user_website='" . $user_website . "', mobile_number='" . $mobile_number . "'
     , user_slug ='" . $user_slug . "' where user_id='" . $user_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "User Profile has been Updated Successfully!!!";

            if ($path_id == 1) {
                header('Location: admin-new-user-requests.php');
                exit;
            } elseif ($path_id == 2) {
                header('Location: admin-all-users.php');
                exit;
            } elseif ($path_id == 3) {
                header('Location: admin-all-users-general.php');
                exit;
            } elseif ($path_id == 4) {
                header('Location: admin-all-users-service-provider.php');
                exit;
            } elseif ($path_id == 5) {
                header('Location: admin-free-users.php');
                exit;
            } elseif ($path_id == 6) {
                header('Location: admin-standard-users.php');
                exit;
            } elseif ($path_id == 7) {
                header('Location: admin-premium-users.php');
                exit;
            } elseif ($path_id == 8) {
                header('Location: admin-premium-plus-users.php');
                exit;
            } else {
                header('Location: admin-all-users.php');
                exit;
            }


        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            if ($path_id == 1) {
                header('Location: admin-new-user-requests.php');
                exit;
            } elseif ($path_id == 2) {
                header('Location: admin-all-users.php');
                exit;
            } elseif ($path_id == 3) {
                header('Location: admin-all-users-general.php');
                exit;
            } elseif ($path_id == 4) {
                header('Location: admin-all-users-service-provider.php');
                exit;
            } elseif ($path_id == 5) {
                header('Location: admin-free-users.php');
                exit;
            } elseif ($path_id == 6) {
                header('Location: admin-standard-users.php');
                exit;
            } elseif ($path_id == 7) {
                header('Location: admin-premium-users.php');
                exit;
            } elseif ($path_id == 8) {
                header('Location: admin-premium-plus-users.php');
                exit;
            } else {
                header('Location: admin-all-users.php');
                exit;
            }
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    if ($path_id == 1) {
        header('Location: admin-new-user-requests.php');
        exit;
    } elseif ($path_id == 2) {
        header('Location: admin-all-users.php');
        exit;
    } elseif ($path_id == 3) {
        header('Location: admin-all-users-general.php');
        exit;
    } elseif ($path_id == 4) {
        header('Location: admin-all-users-service-provider.php');
        exit;
    } elseif ($path_id == 5) {
        header('Location: admin-free-users.php');
        exit;
    } elseif ($path_id == 6) {
        header('Location: admin-standard-users.php');
        exit;
    } elseif ($path_id == 7) {
        header('Location: admin-premium-users.php');
        exit;
    } elseif ($path_id == 8) {
        header('Location: admin-premium-plus-users.php');
        exit;
    } else {
        header('Location: admin-all-users.php');
        exit;
    }
}
?>