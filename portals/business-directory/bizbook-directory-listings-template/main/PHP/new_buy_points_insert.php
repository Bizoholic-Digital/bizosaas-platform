<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['buy_points_submit'])) {


        $user_id = $_SESSION['user_id']; //Session data

        $new_points = $_POST["new_points"];

        $total_cost = $_POST["all_cost"];

        $payment = $_POST["payment"];

        $all_points_status = "Not-Paid";

        if($new_points <= 0) {

        $_SESSION['status_msg'] = $BIZBOOK['PLEASE_ENTER_VALID_POINTS_TO_BUY'];
        header('Location: buy-points' );
        exit;
    }


        $qry = "INSERT INTO " . TBL . "all_points_enquiry 
					(user_id,new_points, total_cost, all_points_status, all_points_cdt) 
					VALUES ('$user_id', '$new_points', '$total_cost', '$all_points_status', '$curDate')";

        $res = mysqli_query($conn, $qry);
        $promote_id = mysqli_insert_id($conn);


        if ($res) {

            if ($payment == 1) {
                
                //if paypal means

                $_SESSION['point_enquiry_id'] = $promote_id;

                $_SESSION['point_total_cost'] = $total_cost;
                
                header('Location: points_payment_paypal_submit.php');
                exit;

            }elseif ($payment == 2) {

                //if Stripe means

                $_SESSION['payment_user_id'] = $user_id;

                $_SESSION['point_enquiry_id'] = $promote_id;

                $_SESSION['point_total_cost'] = $total_cost;

                header('Location: point_stripe_payment.php');
                exit;

            }elseif ($payment == 3) {

                //if Razorpay means

                $_SESSION['payment_user_id'] = $user_id;

                $_SESSION['point_enquiry_id'] = $promote_id;

                $_SESSION['point_total_cost'] = $total_cost;

                header('Location: point_razor_pay_payment.php');
                exit;

            }elseif ($payment == 4) {

                //if PayTm means

                $_SESSION['payment_user_id'] = $user_id;

                $_SESSION['point_enquiry_id'] = $promote_id;

                $_SESSION['point_total_cost'] = $total_cost;

                header('Location: point_paytm_payment.php');
                exit;

            }

            // $_SESSION['status_msg'] = "Your Listing has been promoted successfully!!!";

//            header('Location: buy-points');
//            exit;


        } else {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: buy-points');
            exit;
        }

    } else {

        $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

        header('Location: buy-points');
        exit;
    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: buy-points');
    exit;
}
?>