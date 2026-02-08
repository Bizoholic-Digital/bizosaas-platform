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


        $sub_category_name_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "job_sub_categories  WHERE sub_category_name='" . $sub_category_name . "' AND sub_category_id != $sub_category_id ");

        if (mysqli_num_rows($sub_category_name_exist_check) > 0) {


            $_SESSION['status_msg'] = "The Given Sub Category name is Already Exist Try Other!!!";

            header('Location: admin-job-sub-category-edit.php?row=' . $sub_category_id);
            exit;


        }

//************ Category Name Already Exist Check Ends ***************


        $_FILES['sub_category_image']['name'];

        if (!empty($_FILES['sub_category_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['sub_category_image']['name'];
            $file_loc = $_FILES['sub_category_image']['tmp_name'];
            $file_size = $_FILES['sub_category_image']['size'];
            $file_type = $_FILES['sub_category_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../images/services/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $sub_category_image = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $sub_category_image = $sub_category_image_old;
            }
        } else {
            $sub_category_image = $sub_category_image_old;
        }

        function checkJobbbSubCategorySlug($link, $sub_category_id, $counter = 1)
        {
            global $conn;
            $newLink = $link;
            do {
                $checkLink = mysqli_query($conn, "SELECT sub_category_id FROM " . TBL . "job_sub_categories WHERE sub_category_slug = '$newLink' AND sub_category_id != '$sub_category_id'");
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
        $sub_category_slug = checkJobbbSubCategorySlug($sub_category_slug1, $sub_category_id);


        $sql = mysqli_query($conn, "UPDATE  " . TBL . "job_sub_categories SET sub_category_name='" . $sub_category_name . "', sub_category_status='" . $sub_category_status . "'
     , category_id='" . $category_id . "', sub_category_slug='" . $sub_category_slug . "'
     where sub_category_id='" . $sub_category_id . "'");

        if ($sql) {

            $_SESSION['status_msg'] = "Sub Category has been Updated Successfully!!!";


            header('Location: admin-all-job-sub-category.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-job-sub-category-edit.php?row=' . $sub_category_id);
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-all-job-sub-category.php');
    exit;
}
?>