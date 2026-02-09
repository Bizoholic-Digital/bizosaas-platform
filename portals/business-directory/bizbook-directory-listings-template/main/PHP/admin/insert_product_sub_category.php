<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";
if (isset($_POST['sub_category_submit'])) {

    $cnt = count($_POST['sub_category_name']);
    $category_id = $_POST['category_id'];


// *********** if Count of sub category name is zero means redirect starts ********

    if ($cnt == 0) {
        header('Location: admin-add-new-product-sub-category.php');
        exit;
    }

// *********** if Count of sub category name is zero means redirect ends ********

    for ($i = 0; $i < $cnt; $i++) {

        $sub_category_name = $_POST['sub_category_name'][$i];

        $sub_category_status = "Active";


//************ sub_category Name Already Exist Check Starts ***************


        $sub_category_name_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "product_sub_categories  WHERE sub_category_name='" . $sub_category_name . "' ");

        if (mysqli_num_rows($sub_category_name_exist_check) > 0) {


            $_SESSION['status_msg'] = "The Given sub category name $sub_category_name is Already Exist Try Other!!!";

            header('Location: admin-add-new-product-sub-category.php');
            exit;


        }

//************ sub_category Name Already Exist Check Ends ***************


        $_FILES['sub_category_image']['name'][$i];

        if (!empty($_FILES['sub_category_image']['name'][$i])) {
            $file = rand(1000, 100000) . $_FILES['sub_category_image']['name'][$i];
            $file_loc = $_FILES['sub_category_image']['tmp_name'][$i];
            $file_size = $_FILES['sub_category_image']['size'][$i];
            $file_type = $_FILES['sub_category_image']['type'][$i];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/services/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $sub_category_image = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $sub_category_image = '';
            }
        }

//        function checkProductSubCategorySlug($link, $counter = 1)
//        {
//            global $conn;
//            $newLink = $link;
//            do {
//                $checkLink = mysqli_query($conn, "SELECT sub_category_id FROM " . TBL . "product_sub_categories WHERE sub_category_slug = '$newLink'");
//                if (mysqli_num_rows($checkLink) > 0) {
//                    $newLink = $link . '' . $counter;
//                    $counter++;
//                } else {
//                    break;
//                }
//            } while (1);
//
//            return $newLink;
//        }


        $sub_category_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $sub_category_name));
        //$sub_category_slug = checkProductSubCategorySlug($sub_category_name1);

        $counter = 1;
        $checkLink = mysqli_query($conn, "SELECT sub_category_id FROM " . TBL . "product_sub_categories WHERE sub_category_slug = '$sub_category_name1'");
        if (mysqli_num_rows($checkLink) > 0) {
            $sub_category_slug = $sub_category_name1 . '' . $counter;
        }else{
            $sub_category_slug = $sub_category_name1;
        }

        $sql = mysqli_query($conn, "INSERT INTO  " . TBL . "product_sub_categories (sub_category_name,sub_category_status, sub_category_slug,category_id,sub_category_cdt)
VALUES ('$sub_category_name','$sub_category_status', '$sub_category_slug','$category_id','$curDate')");

        $LID = mysqli_insert_id($conn);
        $lastID = $LID;

        switch (strlen($LID)) {
            case 1:
                $LID = '00' . $LID;
                break;
            case 2:
                $LID = '0' . $LID;
                break;
            default:
                $LID = $LID;
                break;
        }

        $CATID = 'SUB_CAT' . $LID;

        $upqry = mysqli_query($conn, "UPDATE " . TBL . "product_sub_categories 
					  SET sub_category_code = '$CATID' 
					  WHERE sub_category_id = $lastID");

    }


    if ($upqry) {

        $_SESSION['status_msg'] = "Sub category(s) has been Added Successfully!!!";


        header('Location: admin-all-product-sub-category.php');
        exit;

    } else {


        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: admin-add-new-product-sub-category.php');
        exit;
    }

}
?>