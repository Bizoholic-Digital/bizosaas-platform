<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

include "config/info.php";
if (isset($_POST['news_category_submit'])) {


        $category_name = $_POST['category_name'];

        $category_seo_title = $_POST['category_seo_title'];
        $category_seo_description = $_POST['category_seo_description'];
        $category_seo_keywords = $_POST['category_seo_keywords'];

        $category_status = "Active";

        $category_filter_pos_id = 1;


//************ Category Name Already Exist Check Starts ***************


        $category_name_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "news_categories  WHERE category_name='" . $category_name . "' ");

        if (mysqli_num_rows($category_name_exist_check) > 0) {


            $_SESSION['status_msg'] = "The Given Category name $category_name is Already Exist Try Other!!!";

            header('Location: news-add-new-category.php');
            exit;


        }

        $category_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $category_name));

        $counter = 1;
        $checkLink = mysqli_query($conn, "SELECT category_id FROM " . TBL . "news_categories WHERE category_slug = '$category_name1'");
        if (mysqli_num_rows($checkLink) > 0) {
            $category_slug = $category_name1 . '' . $counter;
        }else{
            $category_slug = $category_name1;
        }


        $sql = mysqli_query($conn, "INSERT INTO  " . TBL . "news_categories (category_name,category_status,category_image
        ,category_seo_title,category_seo_description,category_seo_keywords,category_filter_pos_id,category_slug,category_cdt)
VALUES ('$category_name','$category_status','$category_image'
        ,'$category_seo_title', '$category_seo_description', '$category_seo_keywords','$category_filter_pos_id', '$category_slug', '$curDate')");

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

        $CATID = 'CAT' . $LID;

        $upqry = mysqli_query($conn, "UPDATE " . TBL . "news_categories
					  SET category_code = '$CATID'
					  WHERE category_id = $lastID");



    if ($upqry) {

        $_SESSION['status_msg'] = "News Category has been Added Successfully!!!";


        header('Location: news-all-category.php');
        exit;

    } else {


        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: news-add-new-category.php');
        exit;
    }

}
?>