<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['login_submit'])) {


        $email_id = mysqli_real_escape_string($conn, $_POST["email_id"]);
        $password = mysqli_real_escape_string($conn, $_POST["password"]);

        $src = $_POST["src"];

//        $login = mysqli_query($conn,"SELECT * FROM " . TBL . "users  WHERE email_id = '$email_id' AND user_status= 'Active'");
        $login = mysqli_query($conn, "SELECT * FROM " . TBL . "users  WHERE email_id = '$email_id'");

        if (mysqli_num_rows($login) > 0) {
            $login_row = mysqli_fetch_array($login);

            //To Check Email Veriication is Done or not starts

            if ($login_row['verification_status'] == 1) {   //**** If 0 means Activated 1 Means Not activated **//

                header('Location: activate?q=' . $login_row['verification_link']);
                exit();

                //To Check Email Veriication is Done or not ends
            } else {
                if (md5($password) == $login_row['password']) {
                    $user_code = $login_row['user_code'];
                    $user_name = $login_row['first_name'];
                    $user_id = $login_row['user_id'];
                    $_SESSION['user_code'] = $user_code;
                    $_SESSION['user_name'] = $user_name;
                    $_SESSION['user_id'] = $user_id;

                    if ($src == '' || empty($src)) {
                        
                        header("location: dashboard");
                    } else {
                        
                        header("location: " . $src);
                    }
                } else {

                    $_SESSION['status_msg'] = $BIZBOOK['YOUR_PASSWORD_IS_WRONG'];
                    $_SESSION['login_status_msg'] = 1;

                    header("location: login");
                }
            }
        } else {

            $_SESSION['status_msg'] = $BIZBOOK['YOUR_EMAIL_ID_IS_WRONG'];
            $_SESSION['login_status_msg'] = 1;

            header("location: login");
        }

    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];
    $_SESSION['login_status_msg'] = 1;

    header('Location: login');
}