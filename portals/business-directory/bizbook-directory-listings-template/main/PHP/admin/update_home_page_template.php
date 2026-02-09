<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['home_page_template_submit'])) {


        $admin_home_page = $_POST['admin_home_page'];
        $footer_id = 1;


        $sql = mysqli_query($conn,"UPDATE  " . TBL . "footer SET  admin_home_page='" . $admin_home_page. "'  
        where footer_id='" . $footer_id . "'");


        if ($sql) {

            $_SESSION['status_msg'] = "Home Page Template has been Updated Successfully!!!";


            header('Location: home-page-template.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: home-page-template.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: home-page-template.php');
    exit;
}
?>