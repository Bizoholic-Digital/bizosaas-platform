<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}


if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['news_submit'])) {

// Common Service Expert Profile Details

        $news_title = addslashes($_POST["news_title"]);
        $news_description = addslashes($_POST["news_description"]);
        $category_id = $_POST["category_id"];

        $seo_title = $_POST["seo_title"];
        $seo_description = $_POST["seo_description"];
        $seo_keywords = $_POST["seo_keywords"];

// News Status
        $news_status = "Active";

        $news_image_old = $_POST["news_image_old"];
        $news_id = $_POST["news_id"];


        //************************  News Image Upload starts  **************************

        if (!empty($_FILES['news_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['news_image']['name'];
            $file_loc = $_FILES['news_image']['tmp_name'];
            $file_size = $_FILES['news_image']['size'];
            $file_type = $_FILES['news_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "../news/images/news/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $news_image = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $news_image = $news_image_old;
            }
        } else {
            $news_image = $news_image_old;
        }

//************************  News Image Upload Ends  **************************
        

        //News URL slug for update starts

        function checkNewsSlug($link, $news_id, $counter = 1)
        {
            global $conn;
            $newLink = $link;
            do {
                $checkLink = mysqli_query($conn, "SELECT news_id FROM " . TBL . "news WHERE news_slug = '$newLink' AND news_id != '$news_id'");
                if (mysqli_num_rows($checkLink) > 0) {
                    $newLink = $link . '' . $counter;
                    $counter++;
                } else {
                    break;
                }
            } while (1);

            return $newLink;
        }

        $news_title1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $news_title));
        $news_slug = checkNewsSlug($news_title1, $news_id);

        //News URL slug for update ends


        $news_res = mysqli_query($conn, "UPDATE  " . TBL . "news SET news_title='" . $news_title . "'
     , news_description='" . $news_description . "', news_image='" . $news_image . "', category_id='" . $category_id . "'
     , news_slug='" . $news_slug . "', seo_title='" . $seo_title . "'
     , seo_description='" . $seo_description . "', seo_keywords='" . $seo_keywords . "'
       where news_id ='" . $news_id . "'");


//************ /// ***************


        if ($news_res) {

            $_SESSION['status_msg'] = "News/Magazine Successfully Updated!!!";
            header('Location: news-all.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: news-edit.php?code= ' . $expert_id);
        }

        //  News Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: news-edit.php?code= ' . $expert_id);
}