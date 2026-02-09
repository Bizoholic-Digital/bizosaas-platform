<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('job-config-info.php')) {
    include "job-config-info.php";
}


if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['job_profile_submit'])) {

// Common Job Profile Details

        $profile_name = addslashes($_POST["profile_name"]);
        $current_company = $_POST["current_company"];
        $notice_period = $_POST["notice_period"];
        $educational_qualification = $_POST["educational_qualification"];
        $sub_category_id = $_POST["sub_category_id"];
        $years_of_experience = $_POST["years_of_experience"];
        $available_time_start = $_POST["available_time_start"];

        $experience_1 = addslashes($_POST["experience_1"]);
        $experience_2 = addslashes($_POST["experience_2"]);
        $experience_3 = addslashes($_POST["experience_3"]);
        $experience_4 = addslashes($_POST["experience_4"]);

        $education_1 = addslashes($_POST["education_1"]);
        $education_2 = addslashes($_POST["education_2"]);
        $education_3 = addslashes($_POST["education_3"]);
        $education_4 = addslashes($_POST["education_4"]);

        $additional_info_1 = addslashes($_POST["additional_info_1"]);
        $additional_info_2 = addslashes($_POST["additional_info_2"]);
        $additional_info_3 = addslashes($_POST["additional_info_3"]);
        $additional_info_4 = addslashes($_POST["additional_info_4"]);

        $job_profile_image_old = $_POST["job_profile_image_old"];
        $cover_image_old = $_POST["cover_image_old"];
        $job_profile_resume_old = $_POST["job_profile_resume_old"];

        $root_path = $_POST["root_path"];

        $skill_set123 = $_POST["skill_set"];

        $prefix = $fruitList = '';
        foreach ($skill_set123 as $fruit) {
            $skill_set .= $prefix . $fruit;
            $prefix = ',';
        }

        $sub_category_sql = "SELECT * FROM  " . TBL . "job_sub_categories where sub_category_id='" . $sub_category_id . "'";
        $sub_category_rs = mysqli_query($conn, $sub_category_sql);
        $sub_category_row = mysqli_fetch_array($sub_category_rs);

        $category_id = $sub_category_row["category_id"];

        $job_profile_status = "Active";


        //************************  Job Profile Image Upload starts  **************************

        if (!empty($_FILES['job_profile_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['job_profile_image']['name'];
            $file_loc = $_FILES['job_profile_image']['tmp_name'];
            $file_size = $_FILES['job_profile_image']['size'];
            $file_type = $_FILES['job_profile_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "images/jobs/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $job_profile_image = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $job_profile_image = $job_profile_image_old;
            }
        } else {
            $job_profile_image = $job_profile_image_old;
        }

//************************  Job Profile Image Upload Ends  **************************

        //************************  Cover Image Upload starts  **************************

        if (!empty($_FILES['cover_image']['name'])) {
            $file = rand(1000, 100000) . $_FILES['cover_image']['name'];
            $file_loc = $_FILES['cover_image']['tmp_name'];
            $file_size = $_FILES['cover_image']['size'];
            $file_type = $_FILES['cover_image']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "images/jobs/";
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

//************************  Job Resume Upload starts  **************************

        if (!empty($_FILES['job_profile_resume']['name'])) {
            $file = rand(1000, 100000) . $_FILES['job_profile_resume']['name'];
            $file_loc = $_FILES['job_profile_resume']['tmp_name'];
            $file_size = $_FILES['job_profile_resume']['size'];
            $file_type = $_FILES['job_profile_resume']['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type, $allowed)) {
                $folder = "images/jobs/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $job_profile_resume = compressImage($event_image, $file_loc, $folder, $new_size);
            } else {
                $job_profile_resume = $job_profile_resume_old;
            }
        } else {
            $job_profile_resume = $job_profile_resume_old;
        }

//************************  Job Resume Upload Ends  **************************


//************ User Company Already Exist Check Starts ***************

        $user_id = $_SESSION['user_id'];

        $job_profile_exist_check = mysqli_query($conn, "SELECT * FROM " . TBL . "job_profile WHERE user_id='" . $user_id . "' ");

        if (mysqli_num_rows($job_profile_exist_check) > 0) {

            $job_profile_fetchrow = mysqli_fetch_array($job_profile_exist_check);

            $job_profile_id = $job_profile_fetchrow['job_profile_id'];


            //User job profile URL slug for update starts

            function checkUserJobProfileUpdateSlug($link,$job_profile_id, $counter=1){
                global $conn;
                $newLink = $link;
                do{
                    $checkLink = mysqli_query($conn, "SELECT job_profile_id FROM " . TBL . "job_profile WHERE job_profile_slug = '$newLink' AND job_profile_id != '$job_profile_id'");
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
            $job_profile_slug = checkUserJobProfileUpdateSlug($profile_name1,$job_profile_id);

            //User job profile URL slug for update ends


            $job_profile_profile_res = mysqli_query($conn, "UPDATE  " . TBL . "job_profile SET profile_name='" . $profile_name . "'
     , current_company='" . $current_company . "', years_of_experience='" . $years_of_experience . "', notice_period='" . $notice_period . "'
     , available_time_start='" . $available_time_start . "', educational_qualification='" . $educational_qualification . "', job_profile_image='" . $job_profile_image . "'
     , cover_image='" . $cover_image . "', job_profile_resume='" . $job_profile_resume . "', skill_set='" . $skill_set . "'
     , experience_1='" . $experience_1 . "', experience_2 ='" . $experience_2 . "', experience_3='" . $experience_3 . "', experience_4 ='" . $experience_4 . "'
     , education_1='" . $education_1 . "', education_2 ='" . $education_2 . "', education_3 ='" . $education_3 . "', education_4 ='" . $education_4 . "'
     , additional_info_1='" . $additional_info_1 . "', additional_info_2 ='" . $additional_info_2 . "', additional_info_3='" . $additional_info_3 . "', additional_info_4 ='" . $additional_info_4 . "'
     , category_id='" . $category_id . "', sub_category_id='" . $sub_category_id . "', job_profile_udt ='" . $curDate . "', job_profile_status='" . $job_profile_status . "', job_profile_slug ='" . $job_profile_slug . "'
       where job_profile_id ='" . $job_profile_id . "'");

        } else {

            //User job profile URL slug for insert starts

            function checkUserJobProfileSlug($link, $counter=1){
                global $conn;
                $newLink = $link;
                do{
                    $checkLink = mysqli_query($conn, "SELECT job_profile_id FROM " . TBL . "job_profile WHERE job_profile_slug = '$newLink'");
                    if(mysqli_num_rows($checkLink) > 0){
                        $newLink = $link.''.$counter;
                        $counter++;
                    } else {
                        break;
                    }
                } while(1);

                return $newLink;
            }

            //User job profile URL slug for insert ends

            $profile_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $profile_name));

            $job_profile_slug = checkUserJobProfileSlug($profile_name1);

            $job_profile_profile_qry = "INSERT INTO " . TBL . "job_profile 
					(user_id, profile_name, current_company, years_of_experience, notice_period, available_time_start, educational_qualification, cover_image, job_profile_image, job_profile_resume, skill_set
					, experience_1, experience_2, experience_3, experience_4
					, education_1, education_2, education_3, education_4
					, additional_info_1, additional_info_2, additional_info_3, additional_info_4
					, category_id, sub_category_id
					, job_profile_udt, job_profile_status, job_profile_slug, job_profile_cdt)
					VALUES 
					('$user_id', '$profile_name', '$current_company', '$years_of_experience', '$notice_period', '$available_time_start', '$educational_qualification', '$cover_image', '$job_profile_image', '$job_profile_resume', '$skill_set'
					, '$experience_1', '$experience_2', '$experience_3', '$experience_4'
					, '$education_1', '$education_2', '$education_3', '$education_4'
					, '$additional_info_1', '$additional_info_2', '$additional_info_3', '$additional_info_4'
					, '$category_id', '$sub_category_id',
					 '$curDate', '$job_profile_status', '$job_profile_slug', '$curDate')";

            $job_profile_profile_res = mysqli_query($conn, $job_profile_profile_qry);

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

            $profileID = 'JOB-PROFILE' . $LID;

            $upqry = "UPDATE " . TBL . "job_profile 
					  SET job_profile_code = '$profileID' 
					  WHERE job_profile_id = $lastID";

            $upres = mysqli_query($conn, $upqry);
        }

//************ /// ***************


        if ($job_profile_profile_res) {

            $_POST['status_msg'] = $BIZBOOK['JOB_PROFILE_SUCCESS_MESSAGE'];
            header('Location: ' . $root_path . 'dashboard');
        } else {

            $_POST['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: ' . $root_path . 'dashboard');
        }

        //    Job Profile Insert Part Ends

    }
} else {

    $_POST['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: ' . $root_path . 'dashboard');
}