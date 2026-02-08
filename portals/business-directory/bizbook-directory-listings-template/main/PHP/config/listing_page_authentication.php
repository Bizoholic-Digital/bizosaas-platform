<?php

//To redirect the disabled listing modules to dashboard to avoid using this page

if($footer_row['admin_listing_show'] != 1 || $user_details_row['setting_listing_show'] != 1 ) {
    header("Location: ".$webpage_full_link."dashboard");
}

?>