<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['plan_type_submit'])) {

        $user_plan = $_POST["user_plan"];
        $user_type = "Service provider";
        $user_status = "Inactive";
        $payment_status = "";

        $listing_user_id = $_SESSION['user_id'];
        $user_row = getUser($listing_user_id);

        $user_email_id = $user_row['email_id'];
        $first_name = $user_row['first_name'];

        $upqry = "UPDATE " . TBL . "users 
					  SET user_plan = '$user_plan',user_type = '$user_type', user_status = '$user_status', payment_status = '$payment_status', user_cdt = '$curDate'
					  WHERE user_id = $listing_user_id";

        //echo $upqry; die();
        $upres = mysqli_query($conn, $upqry);

        if ($upres) {

            //****************************    Admin Primary email fetch starts    *************************

            $admin_primary_email_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "footer  WHERE footer_id = '1' ");
            $admin_primary_email_fetchrow = mysqli_fetch_array($admin_primary_email_fetch);
            $admin_primary_email = $admin_primary_email_fetchrow['admin_primary_email'];
            $admin_footer_copyright = $admin_primary_email_fetchrow['footer_copyright'];
            $admin_site_name = $admin_primary_email_fetchrow['website_address'];
            $admin_address = $admin_primary_email_fetchrow['footer_address'];

            //****************************    Admin Primary email fetch ends    *************************

            $admin_email = $admin_primary_email; // Admin Email Id


//****************************    Client email starts    *************************

            $to1 = $user_email_id;
            $PLAN_CHANGE_CLIENT_SUBJECT = $BIZBOOK['PLAN_CHANGE_CLIENT_SUBJECT'];
            $subject1 = "'.$admin_site_name $PLAN_CHANGE_CLIENT_SUBJECT";
            

            $message1 = '<!DOCTYPE html>
<html lang="en">

<head>
	<meta http-equiv="Content-Type" content="text/html" charset="utf-8">
	<title>' . $admin_site_name . '</title>
</head>

<body id="page-top" class="index">
    <table border="0" cellspacing="0" cellpadding="0" style="width:100%;font-size:14px;font-family:Quicksand, Calibri, Arial, Verdana, sans-serif;background: #f5f6fa;color:#738196;line-height: 21px;padding: 30px;">
        <tbody>
            <tr>
                <td>
                    <table style="background: #fff;width:500px;padding: 20px;margin: 0 auto;box-shadow: 0px 1px 10px 13px #2d313703;border-radius: 8px;font-weight: 500;">
                        <tbody>
                        <tr>
                            <td style="font-size: 24px;color:#000;font-weight: bold;line-height: 30px;">'.$BIZBOOK['PLAN_CHANGE_REQUEST_GREETINGS'].' <span contenteditable="false">'.$admin_site_name.'</span></td>
                        </tr>
                        <tr>
                            <td>' .$BIZBOOK['HI']. ', <b>' .$first_name. '</b></td>
                        </tr>
                        <tr>
                            <td>&nbsp;</td>
                        </tr>
                        <tr>
                            <td style="font-size: 18px;color:#000;font-weight: bold;line-height: 26px;">'.$BIZBOOK['PLAN_CHANGE_REQUEST_RECEIVED'].'</td>
                        </tr>
                        <tr>
                            <td style="height: 5px;line-height: 2px;">&nbsp;</td>
                        </tr>
                        <tr>
                            <td>'.$BIZBOOK['PLAN_CHANGE_REQUEST_PLEASE_WAIT'].'</td>
                        </tr>
                        <tr>
                            <td>&nbsp;</td>
                        </tr>
                        <tr>
                            <td>'.$BIZBOOK['PLAN_CHANGE_REQUEST_THANKS'].', <br><span contenteditable="false">'.$admin_site_name.'</span></td>
                        </tr>
                    </tbody></table>
                </td>
            </tr>

        </tbody>
    </table>
</body>

</html>';


            $headers1 = "From: " . "$admin_email" . "\r\n";
            $headers1 .= "Reply-To: " . "$admin_email" . "\r\n";
            $headers1 .= "MIME-Version: 1.0\r\n";
            $headers1 .= "Content-Type: text/html; charset=utf-8\r\n";


            mail($to1, $subject1, $message1, $headers1); //Client email


            $_SESSION['status_msg'] = $BIZBOOK['PLAN_CHANGE_REQUEST_SUCCESS_MESSAGE'];  // Success Message in session

            header('Location: db-payment');
            exit;
        }else{
            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: db-plan-change');
            exit;
        }

    }else{
        $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

        header('Location: db-plan-change');
        exit;
    }
}else{
    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: db-plan-change');
    exit;
}