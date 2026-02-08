<?php

//database configuration
if (file_exists('config/info.php')) {
    include('config/info.php');
}


if (isset($_SESSION['user_id'])) {

    $sql = mysqli_query($conn, "UPDATE  " . TBL . "users SET user_clear_notification_cdt = '" . $curDate . "'
     where user_id ='" . $_SESSION['user_id'] . "'");
    if ($sql) {
        echo 1;
    } else {
        echo 2;
    }
} else {
    echo 3;
}
?>