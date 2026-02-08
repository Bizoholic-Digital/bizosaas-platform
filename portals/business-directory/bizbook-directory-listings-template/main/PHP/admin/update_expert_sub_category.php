<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['sub_category_submit'])) {


        $sub_category_id = $_POST['sub_category_id'];
        $sub_category_name = $_POST['sub_category_name'];
        $sub_category_image_old = $_POST['sub_category_image_old'];
        $category_id = $_POST['category_id'];
        $sub_category_status = "Active";


//************ Category Name Already Exist Check Starts ***************


        $sub_category_name_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "expert_sub_categories  WHERE sub_category_name='" . $sub_category_name . "' AND sub_category_id != $sub_category_id ");

        if (mysqli_num_rows($sub_category_name_exist_check) > 0) {


            $_SESSION['status_msg'] = "The Given Sub Category name is Already Exist Try Other!!!";

            header('Location: expert-sub-category-edit.php?row=' . $sub_category_id);
            exit;


        }

//************ Category Name Already Exist Check Ends ***************


        function checkListinggSubCategorySlug($link, $sub_category_id, $counter = 1)
        {
            global $conn;
            $newLink = $link;
            do {
                $checkLink = mysqli_query($conn, "SELECT sub_category_id FROM " . TBL . "expert_sub_categories WHERE sub_category_slug = '$newLink' AND sub_category_id != '$sub_category_id'");
                if (mysqli_num_rows($checkLink) > 0) {
                    $newLink = $link . '' . $counter;
                    $counter++;
                } else {
                    break;
                }
            } while (1);

            return $newLink;
        }


        $sub_category_slug1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $sub_category_name));
        $sub_category_slug = checkListinggSubCategorySlug($sub_category_slug1, $sub_category_id);


        $sql = mysqli_query($conn, "UPDATE  " . TBL . "expert_sub_categories SET sub_category_name='" . $sub_category_name . "', sub_category_status='" . $sub_category_status . "'
     , category_id='" . $category_id . "', sub_category_slug='" . $sub_category_slug . "'
     where sub_category_id='" . $sub_category_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Sub Category has been Updated Successfully!!!";


            header('Location: expert-all-sub-category.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: expert-sub-category-edit.php?row=' . $sub_category_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: expert-all-sub-category.php');
    exit;
}
?>