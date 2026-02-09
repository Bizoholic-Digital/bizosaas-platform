<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

# ADMIN FOLDER NAME #
define('ADMIN_FOLDER_NAME', 'admin');

# IMAGE DIMENSION #
define('THUMB_WIDTH', '72'); // Thum image.
define('THUMB_HEIGHT', '72');

define('LIST_WIDTH', '321'); // Listing image.
define('LIST_HEIGHT', '187');

define('GAL_SLIDER_WIDTH', '800'); // Gallery slider image.
define('GAL_SLIDER_HEIGHT', '356');

define('GAL_WIDTH', '285'); // Gallery image.
define('GAL_HEIGHT', '190');

define('BAN_WIDTH', '1200'); // Banner image.
define('BAN_HEIGHT', '90');

define('TEST_WIDTH', '540'); // Testimonials image.
define('TEST_HEIGHT', '340');

define('CAT_WIDTH', '32'); // Category Icon image.
define('CAT_HEIGHT', '32');

# IMAGE FOLDER NAME #

# User Starts. #
define('USER_IMG_ORGINAL_DIR', 'user_uploads/orginal/'); // User image, For Back End.
define('USER_IMG_RESIZE_DIR', 'user_uploads/resize/');
define('USER_IMG_RESIZE_THUMB_DIR', 'user_uploads/thumb/');

define('USER_IMG_ORGINAL_ADMIN_DIR', ADMIN_FOLDER_NAME . '/user_uploads/orginal/'); // User Image, For Front End.
define('USER_IMG_RESIZE_ADMIN_DIR', ADMIN_FOLDER_NAME . '/user_uploads/resize/');
define('USER_IMG_RESIZE_ADMIN_THUMB_DIR', ADMIN_FOLDER_NAME . '/user_uploads/thumb/');
# User Ends. #

# Listing Starts. #
define('LIST_IMG_ORGINAL_DIR', 'list_uploads/orginal/'); // Listing image, For Back End.
define('LIST_IMG_RESIZE_DIR', 'list_uploads/321x187/');
define('LIST_IMG_RESIZE_THUMB_DIR', 'list_uploads/thumb/');

define('LIST_IMG_ORGINAL_ADMIN_DIR', ADMIN_FOLDER_NAME . '/list_uploads/orginal/'); // Listing image, For Front End.
define('LIST_IMG_RESIZE_ADMIN_DIR', ADMIN_FOLDER_NAME . '/list_uploads/321x187/');
define('LIST_IMG_RESIZE_ADMIN_THUMB_DIR', ADMIN_FOLDER_NAME . '/list_uploads/thumb/');
# Listing Ends. #

# Gallery Starts. #
define('GAL_IMG_ORGINAL_DIR', 'gallery_uploads/orginal/'); // Gallery image, For Back End.
define('GAL_IMG_SLIDER_RESIZE_DIR', 'gallery_uploads/800x356/');
define('GAL_IMG_RESIZE_DIR', 'gallery_uploads/285x190/');
define('GAL_IMG_RESIZE_THUMB_DIR', 'gallery_uploads/thumb/');

define('GAL_IMG_ORGINAL_ADMIN_DIR', ADMIN_FOLDER_NAME . '/gallery_uploads/orginal/'); // Gallery image, For Front End.
define('GAL_IMG_SLIDER_RESIZE_ADMIN_DIR', ADMIN_FOLDER_NAME . '/gallery_uploads/800x356/');
define('GAL_IMG_RESIZE_ADMIN_DIR', ADMIN_FOLDER_NAME . '/gallery_uploads/285x190/');
define('GAL_IMG_RESIZE_ADMIN_THUMB_DIR', ADMIN_FOLDER_NAME . '/gallery_uploads/thumb/');
# Gallery Ends. #


# Banner Starts. #
define('BAN_IMG_ORGINAL_DIR', 'banner_uploads/orginal/'); // Banner image, For Back End.
define('BAN_IMG_RESIZE_DIR', 'banner_uploads/1200x90/');
define('BAN_IMG_RESIZE_THUMB_DIR', 'banner_uploads/thumb/');

define('BAN_IMG_ORGINAL_ADMIN_DIR', ADMIN_FOLDER_NAME . '/banner_uploads/orginal/'); // Banner image, For Front End.
define('BAN_IMG_RESIZE_ADMIN_DIR', ADMIN_FOLDER_NAME . '/banner_uploads/1200x90/');
define('BAN_IMG_RESIZE_ADMIN_THUMB_DIR', ADMIN_FOLDER_NAME . '/banner_uploads/thumb/');
# Banner Ends. #


# Testimonials Starts. #
define('TEST_IMG_ORGINAL_DIR', 'test_uploads/orginal/'); // Testimonials image, For Back End.
define('TEST_IMG_RESIZE_DIR', 'test_uploads/540x340/');
define('TEST_IMG_RESIZE_THUMB_DIR', 'test_uploads/thumb/');

define('TEST_IMG_ORGINAL_ADMIN_DIR', ADMIN_FOLDER_NAME . '/test_uploads/orginal/'); // Testimonials image, For Front End.
define('TEST_IMG_RESIZE_ADMIN_DIR', ADMIN_FOLDER_NAME . '/test_uploads/540x340/');
define('TEST_IMG_RESIZE_ADMIN_THUMB_DIR', ADMIN_FOLDER_NAME . '/test_uploads/thumb/');
# Testimonials Starts. #

# Category Icon Starts. #
define('CAT_IMG_ORGINAL_DIR', 'category_uploads/orginal/'); // Category Icon image, For Back End.
define('CAT_IMG_RESIZE_DIR', 'category_uploads/32x32/');

define('CAT_IMG_ORGINAL_ADMIN_DIR', ADMIN_FOLDER_NAME . '/category_uploads/orginal/'); // Category Icon image, For Front End.
define('CAT_IMG_RESIZE_ADMIN_DIR', ADMIN_FOLDER_NAME . '/category_uploads/32x32/');
# Category Icon Starts. #


# MESSAGES #
define('MSG_A', ' added successfully.');
define('MSG_U', ' updated successfully.');
define('MSG_D', ' deleted successfully.');

define('MSG_A_APRO', ' added successfully. It&#8217;s now awaiting approval.');
define('MSG_U_APRO', ' updated successfully. It&#8217;s now awaiting approval.');

define('ERR_ADD', 'Error in adding');
define('ERR_UP', 'Error in updating');
define('ERR_DEL', 'Error in deleting');
define('ERR_IMG', 'Upload the correct file format (gif, jpeg, jpg, png).');

define('MAIL_YES', 'Mail sent successfully !.');
define('MAIL_NO', 'Mail fail to sent !.');

define('MAIL_YES1', ' mail sent successfully !.');
define('MAIL_NO1', ' mail fail to sent !.');

define('EMAIL_EX', 'E-mail Id already exists !.');
define('USER_EX', 'User Name (Log in ID) already exists !.');

define('EMAIL_EX_NO', 'Email Id, does not exists !.');
define('USER_EX_NO', 'User Name (Log in ID), does not exists !.');

define('VAILD_EMAIL_NO', 'Enter a valid email address !.');
define('VAILD_URL_NO', 'Slash not allowed at the end of site URL !.');


define('PASS_OK', 'Your password has been reset successfully, Your new password has been sent to your primary email address.!');
define('REG_OK', 'Thank you for signing up, please check your email to activate your subscription.');
define('EXISTS', ' already exists !.');
define('ERR_CAPCODE', 'The Security code does not match, please enter the correct security code !.');
define('IN_ACT_CODE', 'In - Active Code, Please Contact The Admin.');
define('IN_ACT_CODE_OR_UNAME_PASS', 'In - Active Code Or User Name Or Password, please try again ! ! !.');
define('WRONG_ACT_CODE', 'Wrong - Activation, Please Contact The Admin.');
define('ACT_YES', 'Login already activated !.');
define('ERR_OLDPASS', 'Old Password does not match, Try again.');

# CURRENT FILE NAME #
$cFileName = basename($_SERVER["SCRIPT_FILENAME"], '.php');
define('FILE_NAME', $cFileName);

# MISCELLANEOUS #
define('ADMIN_IMG_FOLDER', '/' . ADMIN_FOLDER_NAME . '/image/'); # ADMIN FOLDER IMAGE
define('PERPAGE_NO', 2); # Paging number of count

# SMS GATE WAY. #
define('SMS_UNAME', 'directory_finder'); # SMS USER NAME.
define('SMS_PWORD', '123'); # SMS PASSWORD.
define('SENDER_ID', 'BIZGO'); # SMS PASSWORD.

# Data Array
$data_array = array();

$data_array['website_url'] = $webpage_full_link;

##### Page Redirect URl's

$ALL_LISTING_URL = $webpage_full_link.'all-listing/';

$ALL_PRODUCTS_URL = $webpage_full_link.'all-products/';

$ALL_JOBS_URL = $webpage_full_link.'all-jobs/';

$ALL_EXPERTS_URL = $webpage_full_link.'all-service-experts/';

$ALL_NEWS_URL = $webpage_full_link.'news-all/';

$PROFILE_URL = $webpage_full_link.'profile/';

$LISTING_URL = $webpage_full_link.'listing/';

$JOB_URL = $webpage_full_link.'job/';

$SERVICE_EXPERT_URL = $webpage_full_link.'service-expert/';

$NEWS_DETAIL_URL = $webpage_full_link.'news-detail/';

$PLACE_DETAIL_URL = $webpage_full_link.'place/';

$JOB_PROFILE_URL = $webpage_full_link.'job-profile/';

$JOB_PROFILE_CREATION_URL = $webpage_full_link.'jobs/create-job-seeker-profile';

$EVENT_URL = $webpage_full_link.'event/';

$BLOG_URL = $webpage_full_link.'blog/';

$PRODUCT_URL = $webpage_full_link.'product/';

$COMPANY_URL = $webpage_full_link.'company/';

$TARGET_LISTING_URL = $webpage_full_link.'listings/';

$EBOOK_URL = $webpage_full_link.'ebook/';

$GENERAL_PROMOTION_URL = $webpage_full_link.'promotion/';

$SHYIRAMO = 'install1';

//Login URL redirect with current page URL 

$protocol = ((!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] != 'off') || $_SERVER['SERVER_PORT'] == 443) ? "https://" : "http://";
$CurPageURL = $protocol . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI']; 

$LOGIN_URL = $webpage_full_link.'login?src='.$CurPageURL;

//if($footer_row['admin_install_flag'] == 0) { kwohereza($SHYIRAMO); }

# Time Array. #

$timeArr = array("12:00AM", "12:00AM", "1:00AM", "1:30AM", "2:00AM", "2:30AM", "3:00AM", "3:30AM", "4:00AM", "4:30AM", "5:00AM", "5:30AM", "6:00AM", "6:30AM", "7:00AM", "7:30AM", "8:00AM", "8:30AM", "9:00AM", "9:30AM", "10:00AM", "10:30AM", "11:00AM", "11:30AM", "12:00PM", "12:30PM", "1:00PM", "1:30PM", "2:00PM", "2:30PM", "3:00PM", "3:30PM", "4:00PM", "4:30PM", "5:00PM", "5:30PM", "6:00PM", "6:30PM", "7:00PM", "7:30PM", "8:00PM", "8:30PM", "9:00PM", "9:30PM", "10:00PM", "10:30PM", "11:00PM", "11:30PM");

define('TIME_LIST', json_encode($timeArr)); # Time List.


//***************** Important Part Do Not Delete **************************

# Auto Update Of Listing Status when it has expiry dates starts

$exp_listsql = "SELECT * FROM " . TBL . "listings  WHERE listing_status= 'Active' AND listing_is_delete != '2' ORDER BY listing_id ASC";

$exp_listrs = mysqli_query($conn,$exp_listsql);

while ($exp_listrow = mysqli_fetch_array($exp_listrs)) {

    $exp_user_id = $exp_listrow['user_id'];
    $exp_listing_id = $exp_listrow['listing_id'];

    $exp_users = "SELECT * FROM " . TBL . "users WHERE user_id= '$exp_user_id'";
    $exp_users_rs = mysqli_query($conn,$exp_users);

    $exp_users_row = mysqli_fetch_array($exp_users_rs);
    $exp_user_plan = $exp_users_row['user_plan'];

    $exp_users_plan_type = "SELECT * FROM " . TBL . "plan_type  WHERE plan_type_id= '$exp_user_plan'";
    $exp_users_plan_type_rs = mysqli_query($conn,$exp_users_plan_type);

    $exp_users_plan_type_row = mysqli_fetch_array($exp_users_plan_type_rs);

    $exp_plan_type_duration = $exp_users_plan_type_row['plan_type_duration'];


    $listing_inactive_status = "Inactive";

    $exp_update_sql = "UPDATE  " . TBL . "listings SET listing_status='$listing_inactive_status'
    where listing_id='$exp_listing_id'
AND listing_cdt < DATE_SUB(NOW(), INTERVAL $exp_plan_type_duration MONTH)";

    $exp_update_rs = mysqli_query($conn,$exp_update_sql);

}


# Auto Update Of Listing Status when it has expiry dates ends

//***************** Important Part Do Not Delete **************************


# Compress Image while uploading

function compressImage($imagename,$source,$path,$new_size){

    $target = $path.$imagename;

    move_uploaded_file($source, $target);

    $imagepath = $imagename;
    $save = $path . $imagepath; //This is the new file you saving
    $file = $path . $imagepath; //This is the original file

    list($width, $height) = getimagesize($file);

    $tn = imagecreatetruecolor($width, $height);

    $image = imagecreatefromjpeg($file);
    $info = getimagesize($target);
    if ($info['mime'] == 'image/jpeg') {
        $image = imagecreatefromjpeg($file);
    } elseif ($info['mime'] == 'image/gif') {
        $image = imagecreatefromgif($file);
    } elseif ($info['mime'] == 'image/png') {
        $image = imagecreatefrompng($file);
        $bck   = imagecolorallocate( $image , 0, 0, 0, 127 );
        imagecolortransparent( $image, $bck );
        imagealphablending( $image, false );
        imagesavealpha( $image, true );
    }

    if ($info['mime'] != 'image/png') {
        imagecopyresampled($tn, $image, 0, 0, 0, 0, $width, $height, $width, $height);
        if ($new_size <= 100) {
            imagejpeg($tn, $save, 95);
        } elseif ($new_size > 100 && $new_size <= 200) {
            imagejpeg($tn, $save, 80);
        } elseif ($new_size > 200 && $new_size <= 500) {
            imagejpeg($tn, $save, 70);
        } elseif ($new_size > 500) {
            imagejpeg($tn, $save, 40);
        }
    }

    return $imagepath;
}
# Redirect URL function starts

function kwohereza($url)
{
    if(headers_sent())
    {
        echo "<script>document.location.href='".$url."'</script>";
    }
    else
    {
        header("location: ".$url);
    }
}

# Redirect URL function ends

$activation_status_activated = 1;

$activation_status_not_activated = 0;

$activation_expiry_date = date('Y-m-d',strtotime(date("Y-m-d", time()) . " + 365 day"));

# Auto Update Of Buy Points starts
function delBuyPoints()
{
    global $conn;
    
    $exp_tlistsql1 = "SELECT * FROM " . TBL . "all_points_enquiry ORDER BY all_points_enquiry_id ASC";

    $exp_tlistrs1 = mysqli_query($conn, $exp_tlistsql1);

    while ($exp_tlistrow1 = mysqli_fetch_array($exp_tlistrs1)) {
        
        $exp_tlisting_id = $exp_tlistrow1['all_points_enquiry_id'];


        $exp_tupdate_sql = "DELETE FROM  " . TBL . "all_points_enquiry where all_points_enquiry_id ='$exp_tlisting_id' AND all_points_status != 'Paid'";


        $exp_tupdate_rs = mysqli_query($conn, $exp_tupdate_sql);

        $exp_tupdate_row = mysqli_fetch_array($exp_tupdate_rs);

    }
    return true;
}

# Auto Update Of Buy Points ends