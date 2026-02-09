<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";

if ($_SERVER['REQUEST_METHOD']=='POST') {

    if (isset($_POST['admin_submit'])) {
//Retrieving data from html form
        $admin_email = mysqli_real_escape_string($conn,$_POST['admin_email']);
        $admin_password = mysqli_real_escape_string($conn,$_POST['admin_password']);

        $src = $_POST["src"];


        $login = mysqli_query($conn,"SELECT * FROM " . TBL . "admin WHERE admin_email = '$admin_email'");
        //Check whether the query was successful or not
        $row = mysqli_fetch_array($login);

        if (mysqli_num_rows($login) > 0) {


            if (md5($admin_password) == $row['admin_password']) {

                $admin_id = $row['admin_id'];
                $_SESSION['admin_id'] = $admin_id;
                $update = mysqli_query($conn,"UPDATE " . TBL . "admin SET admin_login=now() where admin_id=" . $_SESSION['admin_id'] . "");
                
                
                if ($src == '' || empty($src)) {

                    header("location: profile.php");
                } else {

                    header("location: " . $src);
                }
            } else {
                $_SESSION['status_msg'] = "Your Email Id & Password Is Wrong!!!";
                $_SESSION['login_status_msg'] = 1;

                header("location: index.php");
            }
        } else {
            $_SESSION['status_msg'] = "Your Email Id & Password Is Wrong!!!";
            $_SESSION['login_status_msg'] = 1;

            header("location: index.php");
        }
    }
}else {
    $_SESSION['status_msg'] = "Your Email Id & Password Is Wrong!!!";
    $_SESSION['login_status_msg'] = 1;

    header("location: index.php");
}
?>