<?php

//To redirect the general type or Job Seeker user to dashboard to avoid using this page

if($user_details_row['user_type'] == "General" || $user_details_row['user_type'] == "Job seeker") {
    header("Location: ".$webpage_full_link."dashboard");
}

?>