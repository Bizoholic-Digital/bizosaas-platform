<?php

//To redirect the Job Seeker user to dashboard to avoid using this page

if($user_details_row['user_type'] == "Job seeker") {
    header("Location: ".$webpage_full_link."dashboard");
}

?>