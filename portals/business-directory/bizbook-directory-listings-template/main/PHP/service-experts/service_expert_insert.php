<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('expert-config-info.php')) {
    include "expert-config-info.php";
}


if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['service_expert_submit'])) {

// Common Job Profile Details

        $profile_name = addslashes($_POST["profile_name"]);
        $city_id = $_POST["city_id"];
        $base_fare = $_POST["base_fare"];
        $date_of_birth = $_POST["date_of_birth"];
        $category_id = $_POST["category_id"];

        $years_of_experience = $_POST["years_of_experience"];
        $available_time_start = $_POST["available_time_start"];
        $available_time_end = $_POST["available_time_end"];

        $experience_1 = $_POST["experience_1"];
        $experience_2 = $_POST["experience_2"];
        $experience_3 = $_POST["experience_3"];
        $experience_4 = $_POST["experience_4"];

        $education_1 = $_POST["education_1"];
        $education_2 = $_POST["education_2"];
        $education_3 = $_POST["education_3"];
        $education_4 = $_POST["education_4"];

        $additional_info_1 = $_POST["additional_info_1"];
        $additional_info_2 = $_POST["additional_info_2"];
        $additional_info_3 = $_POST["additional_info_3"];
        $additional_info_4 = $_POST["additional_info_4"];

        $cover_image_old = $_POST["cover_image_old"];
        $profile_image_old = $_POST["profile_image_old"];
        $id_proof_old = $_POST["id_proof_old"];

        $root_path = $_POST["root_path"];

        $area_id123 = $_POST["area_id"];

        $prefix = $fruitList = '';
        foreach ($area_id123 as $fruit) {
            $area_id .= $prefix . $fruit;
            $prefix = ',';
        }

        $sub_category_id123 = $_POST["sub_category_id"];

        $prefix1 = $fruitList1 = '';
        foreach ($sub_category_id123 as $fruit1) {
            $sub_category_id .= $prefix1 . $fruit1;
            $prefix1 = ',';
        }

        $payment_id123 = $_POST["payment_id"];

        $prefix2 = $fruitList2 = '';
        foreach ($payment_id123 as $fruit2) {
            $payment_id .= $prefix2 . $fruit2;
            $prefix2 = ',';
        }

        $expert_status = "Active";


        //************************  Cover Image Upload starts  **************************

        if (!empty($_FILES['cover_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['cover_image']['name'];
            $file_loc = $_FILES['cover_image']['tmp_name'];
            $file_size = $_FILES['cover_image']['size'];
            $file_type = $_FILES['cover_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "images/services/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $cover_image = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $cover_image = $cover_image_old;
            }
        } else {
            $cover_image = $cover_image_old;
        }

//************************  Cover Image Upload Ends  **************************

//************************  Profile Image Upload starts  **************************

        if (!empty($_FILES['profile_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['profile_image']['name'];
            $file_loc = $_FILES['profile_image']['tmp_name'];
            $file_size = $_FILES['profile_image']['size'];
            $file_type = $_FILES['profile_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "images/services/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $profile_image = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $profile_image = $profile_image_old;
            }
        } else {
            $profile_image = $profile_image_old;
        }

//************************  Profile Image Upload Ends  **************************

        //************************  Id Proof Image Upload starts  **************************

        if (!empty($_FILES['id_proof']['name'])) {
            $file = rand(1000, 100000) . $_FILES['id_proof']['name'];
            $file_loc = $_FILES['id_proof']['tmp_name'];
            $file_size = $_FILES['id_proof']['size'];
            $file_type = $_FILES['id_proof']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "images/services/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $id_proof = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $id_proof = $id_proof_old;
            }
        } else {
            $id_proof = $id_proof_old;
        }

//************************  Id Proof Image Upload Ends  **************************


//************ Service Expert Already Exist Check Starts ***************

        $user_id = $_SESSION['user_id'];

        $user_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "users  WHERE user_id='" . $user_id . "' ");
        $user_exist_fetchrow = mysqli_fetch_array($user_exist_check);

        $user_plan = $user_exist_fetchrow['user_plan'];


        $expert_profile_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "experts  WHERE user_id='" . $user_id . "' ");

        if (mysqli_num_rows($expert_profile_exist_check) > 0) {

            $expert_profile_fetchrow = mysqli_fetch_array($expert_profile_exist_check);

            $expert_id = $expert_profile_fetchrow['expert_id'];


            //Service Expert profile URL slug for update starts

            function checkUserServiceExpertUpdateSlug($link,$expert_id, $counter=1){
                global $conn;
                $newLink = $link;
                do{
                    $checkLink = mysqli_query($conn, "SELECT expert_id FROM " . TBL . "experts WHERE expert_slug = '$newLink' AND expert_id != '$expert_id'");
                    if(mysqli_num_rows($checkLink) > 0){
                        $newLink = $link.''.$counter;
                        $counter++;
                    } else {
                        break;
                    }
                } while(1);

                return $newLink;
            }

            $profile_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $profile_name));
            $expert_slug = checkUserServiceExpertUpdateSlug($profile_name1,$expert_id);

            //Service Expert profile URL slug for update ends


            $expert_profile_res = mysqli_query($conn, "UPDATE  " . TBL . "experts SET profile_name='" . $profile_name . "'
     , city_id='" . $city_id . "', years_of_experience='" . $years_of_experience . "', base_fare='" . $base_fare . "'
     , available_time_start='" . $available_time_start . "', available_time_end='" . $available_time_end . "'
     , profile_image='" . $profile_image . "', cover_image='" . $cover_image . "'
     , id_proof ='" . $id_proof . "', area_id='" . $area_id . "', user_plan='" . $user_plan . "'
     , experience_1='" . $experience_1 . "', experience_2 ='" . $experience_2 . "'
     , experience_3='" . $experience_3 . "', experience_4 ='" . $experience_4 . "'
     , education_1='" . $education_1 . "', education_2 ='" . $education_2 . "'
     , education_3 ='" . $education_3 . "', education_4 ='" . $education_4 . "'
     , additional_info_1='" . $additional_info_1 . "', additional_info_2 ='" . $additional_info_2 . "'
     , additional_info_3='" . $additional_info_3 . "', additional_info_4 ='" . $additional_info_4 . "'
     , category_id='" . $category_id . "', sub_category_id='" . $sub_category_id . "'
     , date_of_birth='" . $date_of_birth . "', payment_id='" . $payment_id . "'
     , expert_udt ='" . $curDate . "', expert_status='" . $expert_status . "', expert_slug='" . $expert_slug . "'
       where expert_id ='" . $expert_id . "'");

        } else {

            //Service Expert profile URL slug for insert starts

            function checkUserServiceExpertSlug($link, $counter=1){
                global $conn;
                $newLink = $link;
                do{
                    $checkLink = mysqli_query($conn, "SELECT expert_id FROM " . TBL . "experts WHERE expert_slug = '$newLink'");
                    if(mysqli_num_rows($checkLink) > 0){
                        $newLink = $link.''.$counter;
                        $counter++;
                    } else {
                        break;
                    }
                } while(1);

                return $newLink;
            }

            //Service Expert profile URL slug for insert ends

            $profile_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $profile_name));

            $expert_slug = checkUserServiceExpertSlug($profile_name1);

            $expert_profile_profile_qry = "INSERT INTO " . TBL . "experts
					(user_id, profile_name, city_id, years_of_experience, base_fare, available_time_start
					, available_time_end, profile_image, cover_image, id_proof, area_id, user_plan
					, experience_1, experience_2, experience_3, experience_4
					, education_1, education_2, education_3, education_4
					, additional_info_1, additional_info_2, additional_info_3, additional_info_4
					, category_id, sub_category_id, date_of_birth, payment_id
					, expert_udt, expert_status, expert_slug, expert_cdt)
					VALUES
					('$user_id', '$profile_name', '$city_id', '$years_of_experience', '$base_fare', '$available_time_start'
					, '$available_time_end', '$profile_image', '$cover_image', '$id_proof', '$area_id', '$user_plan'
					, '$experience_1', '$experience_2', '$experience_3', '$experience_4'
					, '$education_1', '$education_2', '$education_3', '$education_4'
					, '$additional_info_1', '$additional_info_2', '$additional_info_3', '$additional_info_4'
					, '$category_id', '$sub_category_id', '$date_of_birth', '$payment_id'
					, '$curDate', '$expert_status', '$expert_slug', '$curDate')";

            $expert_profile_res = mysqli_query($conn, $expert_profile_profile_qry);

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

            $profileID = 'EXPERT-SERVICE' . $LID;

            $upqry = "UPDATE " . TBL . "experts
					  SET expert_code = '$profileID'
					  WHERE expert_id = $lastID";

            $upres = mysqli_query($conn, $upqry);
        }

//************ /// ***************


        if ($expert_profile_res) {

            $_SESSION['status_msg'] = $BIZBOOK['EXPERT_PROFILE_SUCCESS_MESSAGE'];
            header('Location: ' . $root_path . 'dashboard');
        } else {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: ' . $root_path . 'dashboard');
        }

        //    Service Expert Insert Part Ends

    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: ' . $root_path . 'dashboard');
}