<?php

//To redirect the disabled expert modules to dashboard to avoid using this page

if($footer_row['admin_expert_show'] != 1 || $user_details_row['setting_expert_show'] != 1 ) {
    header("Location: ".$webpage_full_link."dashboard");
}

?>