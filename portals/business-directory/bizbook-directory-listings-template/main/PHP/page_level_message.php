<?php
if (isset($_SESSION['status_msg'])) {
    ?>
    <div class="log-suc"><p><?php echo $_SESSION['status_msg']; ?></p></div>
    <?php
    unset($_SESSION['status_msg']);
}
?>