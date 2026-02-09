<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['coupon_submit'])) {

// Coupon Details
        $coupon_user_id = $_SESSION['user_id'];
        $coupon_name = $_POST["coupon_name"];
        $coupon_code = $_POST["coupon_code"];
        $coupon_link = $_POST["coupon_link"];

        $coupon_start_date_1 = $_POST["coupon_start_date"];
        $coupon_start_date = date ('Y-m-d', strtotime($coupon_start_date_1));

        $coupon_end_date_1 = $_POST["coupon_end_date"];
        $coupon_end_date = date ('Y-m-d', strtotime($coupon_end_date_1));

        $coupon_status = "Active";

        if (!empty($_FILES['coupon_photo']['name'])) {
            $file = rand(1000, 100000) . $_FILES['coupon_photo']['name'];
            $file_loc = $_FILES['coupon_photo']['tmp_name'];
            $file_size = $_FILES['coupon_photo']['size'];
            $file_type = $_FILES['coupon_photo']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "images/user/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $coupon_photo_1 = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $coupon_photo_1);
                $coupon_photo = compressImage($coupon_photo_1, $file_loc, $folder, $new_size);
            } else {
                $coupon_photo = '';
            }

        }

// Coupon Insert Part Starts


        $coupon_qry = "INSERT INTO " . TBL . "coupons 
					(coupon_user_id, coupon_name, coupon_code,coupon_link,coupon_photo,coupon_start_date,coupon_end_date
					,coupon_status, coupon_cdt) 
					VALUES 
					('$coupon_user_id', '$coupon_name', '$coupon_code', '$coupon_link', '$coupon_photo', '$coupon_start_date'
					, '$coupon_end_date', '$coupon_status', '$curDate')";

        $coupon_res = mysqli_query($conn, $coupon_qry);


        if ($coupon_res) {

            $_SESSION['status_msg'] = $BIZBOOK['COUPON_INSERT_SUCCESS_MESSAGE'];

            header('Location: db-coupons');
            exit;

        } else {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: add-coupons');
        }

        //    Coupon Insert Part Ends

    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: db-coupons');
}