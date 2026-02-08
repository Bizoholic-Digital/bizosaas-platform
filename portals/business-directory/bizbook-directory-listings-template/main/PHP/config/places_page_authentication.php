<?php

//To redirect the disabled Places modules to dashboard to avoid using this page

if($footer_row['admin_place_show'] != 1) {
    header("Location: ".$webpage_full_link."dashboard");
}

?>