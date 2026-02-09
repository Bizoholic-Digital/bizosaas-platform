<?php

//To redirect the disabled Product modules to dashboard to avoid using this page

if($footer_row['admin_product_show'] != 1 || $user_details_row['setting_product_show'] != 1 ) {
    header("Location: ".$webpage_full_link."dashboard");
}

?>