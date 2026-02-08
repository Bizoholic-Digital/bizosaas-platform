<?php

//To redirect the disabled News modules to dashboard to avoid using this page

if($footer_row['admin_news_show'] != 1) {
    header("Location: ".$webpage_full_link."dashboard");
}

?>