<?php

//To redirect the disabled job modules to dashboard to avoid using this page

if($footer_row['admin_job_show'] != 1 || $user_details_row['setting_job_show'] != 1 ) {
    header("Location: ".$webpage_full_link."dashboard");
}

?>