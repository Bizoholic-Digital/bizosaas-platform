<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('job-config-info.php')) {
    include "job-config-info.php";
}


if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['job_submit'])) {


// Basic Personal Details
        $first_name = $_SESSION["first_name"];
        $last_name = $_SESSION["last_name"];
        $mobile_number = $_SESSION["mobile_number"];
        $email_id = $_SESSION["email_id"];

        $register_mode = "Direct";


// Common product Details
        $job_title = $_POST["job_title"];
        $job_salary = $_POST["job_salary"];
        $no_of_openings = $_POST["no_of_openings"];
        $job_type = $_POST["job_type"];

        $job_interview_date_1 = $_POST["job_interview_date"];
        $job_interview_date = date ('Y-m-d', strtotime($job_interview_date_1));

        $job_interview_time = $_POST["job_interview_time"];

        $years_of_experience = $_POST["years_of_experience"];
        $job_role = $_POST["job_role"];
        $educational_qualification = $_POST["educational_qualification"];
        $job_small_description = addslashes($_POST["job_small_description"]);
        $job_location = $_POST["job_location"];
        $job_company_name = $_POST["job_company_name"];

        $contact_person = $_POST["contact_person"];
        $contact_email_id = $_POST["contact_email_id"];
        $contact_number = $_POST["contact_number"];
        $contact_website = $_POST["contact_website"];
        $interview_location = $_POST["interview_location"];

        $job_description = addslashes($_POST["job_description"]);

        $category_id = $_POST["category_id"];

        $sub_category_id = $_POST["sub_category_id"];

        $skill_set123 = $_POST["skill_set"];

        $prefix = $fruitList = '';
        foreach ($skill_set123 as $fruit) {
            $skill_set .= $prefix . $fruit;
            $prefix = ',';
        }

//product Specifications

        //$job_status = "Active";

//    Condition to get User Id starts

        if (isset($_SESSION['user_code']) && !empty($_SESSION['user_code'])) {
            $user_code = $_SESSION['user_code'];
            $user_details = mysqli_query($conn, "SELECT * FROM  " . TBL . "users where user_code='" . $user_code . "'");
            $user_details_row = mysqli_fetch_array($user_details);

            $user_id = $user_details_row['user_id'];  //User Id

            if ($user_details_row['user_status'] == 'Active') {
                // product Status
                $job_status = "Active";
            } else {
                // product Status
                $job_status = "Inactive";
            }


        } else {
            $user_status = "Inactive";

            $qry = "INSERT INTO " . TBL . "users 
					(first_name, last_name, email_id, mobile_number, register_mode, user_status, user_cdt) 
					VALUES ('$first_name', '$last_name', '$email_id', '$mobile_number','$register_mode', '$user_status', '$curDate')";

            $res = mysqli_query($conn, $qry);
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

            $userID = 'USER' . $LID;

            $upqry = "UPDATE " . TBL . "users 
					  SET user_code = '$userID' 
					  WHERE user_id = $lastID";

            //echo $upqry; die();
            $upres = mysqli_query($conn, $upqry);

            $user_id = $lastID; //User Id

            // product Status
            $job_status = "Inactive";

        }
//    Condition to get User Id Ends


// ************************  Gallery Image Upload starts  **************************

        $all_company_logo = $_FILES['company_logo'];

        if (!empty($all_company_logo['name'])) {
            $file1 = rand(1000, 100000) . $all_company_logo['name'];
            $file_loc1 = $all_company_logo['tmp_name'];
            $file_size1 = $all_company_logo['size'];
            $file_type1 = $all_company_logo['type'];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if (in_array($file_type1, $allowed)) {
                $folder1 = "images/jobs/";
                $new_size = $file_size1 / 1024;
                $new_file_name1 = strtolower($file1);
                $event_image1 = str_replace(' ', '-', $new_file_name1);
                //move_uploaded_file($file_loc1, $folder1 . $event_image1);
                $company_logo1 = compressImage($event_image1, $file_loc1, $folder1, $new_size);
            } else {
                $company_logo1 = '';
            }
        }
        $company_logo = $company_logo1;


// ************************  Gallery Image Upload ends  **************************   

        function checkJobSlug($link, $counter = 1)
        {
            global $conn;
            $newLink = $link;
            do {
                $checkLink = mysqli_query($conn, "SELECT job_id FROM " . TBL . "jobs WHERE job_slug = '$newLink'");
                if (mysqli_num_rows($checkLink) > 0) {
                    $newLink = $link . '' . $counter;
                    $counter++;
                } else {
                    break;
                }
            } while (1);

            return $newLink;
        }

        $job_title1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $job_title));
        $job_slug = checkJobSlug($job_title1);

//    Job Insert Part Starts

        $job_qry = "INSERT INTO " . TBL . "jobs 
					(user_id, category_id, sub_category_id, job_title, job_description
					, job_salary, no_of_openings, job_type, job_interview_date
					, years_of_experience, job_interview_time, job_role, educational_qualification
					, job_small_description, job_location, company_logo, contact_person
					, contact_email_id, contact_number, contact_website, interview_location
					, skill_set ,job_status, job_company_name
					, job_udt, job_slug, job_cdt) 
					VALUES 
					('$user_id', '$category_id', '$sub_category_id','$job_title','$job_description'
					, '$job_salary','$no_of_openings','$job_type','$job_interview_date'
					, '$years_of_experience','$job_interview_time','$job_role','$educational_qualification'
					, '$job_small_description','$job_location','$company_logo','$contact_person'
					, '$contact_email_id','$contact_number','$contact_website','$interview_location'
					, '$skill_set', '$job_status', '$job_company_name'
					, '$curDate', '$job_slug', '$curDate')";


        $job_res = mysqli_query($conn, $job_qry);
        $jobID = mysqli_insert_id($conn);
        $listlastID = $jobID;

        switch (strlen($jobID)) {
            case 1:
                $jobID = '00' . $jobID;
                break;
            case 2:
                $jobID = '0' . $jobID;
                break;
            default:
                $jobID = $jobID;
                break;
        }

        $ProdCode = 'JOB' . $jobID;

        $jobupqry = "UPDATE " . TBL . "jobs 
					  SET job_code = '$ProdCode' 
					  WHERE job_id = $listlastID";

        $jobupres = mysqli_query($conn, $jobupqry);


        //****************************    Admin Primary email fetch starts    *************************

        $admin_primary_email_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "footer  WHERE footer_id = '1' ");
        $admin_primary_email_fetchrow = mysqli_fetch_array($admin_primary_email_fetch);
        $admin_primary_email = $admin_primary_email_fetchrow['admin_primary_email'];
        $admin_footer_copyright = $admin_primary_email_fetchrow['footer_copyright'];
        $admin_site_name = $admin_primary_email_fetchrow['website_address'];
        $admin_address = $admin_primary_email_fetchrow['footer_address'];

        //****************************    Admin Primary email fetch ends    *************************


        if ($jobupres) {

            $admin_email = $admin_primary_email; // Admin Email Id

            $webpage_full_link_with_login = $webpage_full_link . "login";  //URL Login Link

//****************************    Admin email starts    *************************

            $to = $admin_email;
            $JOB_INSERT_ADMIN_SUBJECT = $BIZBOOK['JOB_INSERT_ADMIN_SUBJECT'];
            $subject = "$admin_site_name $JOB_INSERT_ADMIN_SUBJECT";

            $admin_sql_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "mail  WHERE mail_id = 19 "); //User mail template fetch
            $admin_sql_fetch_row = mysqli_fetch_array($admin_sql_fetch);

            $mail_template_admin = $admin_sql_fetch_row['mail_template'];

            $message1 = stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \''
            , '\' . $mobile_number . \'', '\' . $listing_name . \'', '\' . $listing_email . \'', '\' . $listing_mobile . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'', '\'.$webpage_full_link_with_login.\'', '\'.$admin_primary_email.\''),
                array('' . $admin_site_name . '', '' . $first_name . '', '' . $email_id . '', '' . $mobile_number . '', '' . $listing_name . '', '' . $listing_email . '', '' . $listing_mobile . '', '' . $admin_footer_copyright . '', '' . $admin_address . '', '' . $webpage_full_link . '', '' . $webpage_full_link_with_login . '', '' . $admin_primary_email . ''), $mail_template_admin));

            $headers = "From: " . "$email_id" . "\r\n";
            $headers .= "Reply-To: " . "$email_id" . "\r\n";
            $headers .= "MIME-Version: 1.0\r\n";
            $headers .= "Content-Type: text/html; charset=utf-8\r\n";


            mail($to, $subject, $message1, $headers); //admin email


//****************************    Admin email ends    *************************

//****************************    Client email starts    *************************

            $to1 = $email_id;
            $JOB_INSERT_CLIENT_SUBJECT = $BIZBOOK['JOB_INSERT_CLIENT_SUBJECT'];
            $subject1 = "$admin_site_name $JOB_INSERT_CLIENT_SUBJECT";

            $client_sql_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "mail  WHERE mail_id = 18 "); //User mail template fetch
            $client_sql_fetch_row = mysqli_fetch_array($client_sql_fetch);

            $mail_template_client = $client_sql_fetch_row['mail_template'];

            $message2 = stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \''
            , '\' . $mobile_number . \'', '\' . $listing_name . \'', '\' . $listing_email . \'', '\' . $listing_mobile . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\'', '\'.$webpage_full_link_with_login.\'', '\'.$admin_primary_email.\''),
                array('' . $admin_site_name . '', '' . $first_name . '', '' . $email_id . '', '' . $mobile_number . '', '' . $listing_name . '', '' . $listing_email . '', '' . $listing_mobile . '', '' . $admin_footer_copyright . '', '' . $admin_address . '', '' . $webpage_full_link . '', '' . $webpage_full_link_with_login . '', '' . $admin_primary_email . ''), $mail_template_client));


            $headers1 = "From: " . "$admin_email" . "\r\n";
            $headers1 .= "Reply-To: " . "$admin_email" . "\r\n";
            $headers1 .= "MIME-Version: 1.0\r\n";
            $headers1 .= "Content-Type: text/html; charset=utf-8\r\n";


            mail($to1, $subject1, $message2, $headers1); //admin email

//****************************    client email ends    *************************


            $_SESSION['status_msg'] = $BIZBOOK['JOB_INSERT_SUCCESS_MESSAGE'];


            header('Location: db-jobs');
        } else {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: create-job');
        }

        //    Job Insert Part Ends

    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: create-job');
}