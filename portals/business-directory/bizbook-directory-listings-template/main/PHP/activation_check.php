<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['verification_submit'])) {


        $verification_link = $_POST["verification_link"];
        $verification_code = $_POST["verification_code"];


        $activate = mysqli_query($conn,"SELECT * FROM " . TBL . "users  WHERE verification_link = '$verification_link'");

        if (mysqli_num_rows($activate) > 0) {
            $activate_row = mysqli_fetch_array($activate);

                if ($verification_code == $activate_row['verification_code']) {

                    $user_id = $activate_row['user_id'];

                    $upqry = "UPDATE " . TBL . "users 
					  SET verification_code = '', verification_link = '',verification_status = 0
					  WHERE user_id = $user_id";

                    $upres = mysqli_query($conn,$upqry);

                    $_SESSION['status_msg'] = $BIZBOOK['ACTIVATION_EMAIL_VERIFICATION_SUCCESS_MESSAGE'];

                    $_SESSION['login_status_msg'] = 1;

                    header('Location: login');
                    exit();

                } else {

                    $_SESSION['status_msg'] = $BIZBOOK['ACTIVATION_EMAIL_VERIFICATION_FAILURE_MESSAGE'];

                    header('Location: activate?q='.$verification_link);
                    exit();
                }
            }

    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];
    $_SESSION['login_status_msg'] = 1;

    header('Location: login');
}