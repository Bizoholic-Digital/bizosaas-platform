<?php
include "header.php";
?>

<?php if ($footer_row['admin_expert_show'] != 1 || $admin_row['admin_service_expert_options'] != 1) {
    header("Location: profile.php");
} ?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Service Expert Admin Info</span>
                <div class="ud-cen-s2 ud-pro-edit">
                    <h2>Service Expert - Admin details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <form name="service_expert_admin_setting_form" id="service_expert_admin_setting_form" method="post" enctype="multipart/form-data" action="update_service_expert_admin_setting.php">

                        <table class="responsive-table bordered">
                            <?php
                            $admin_sql_row = getAllFooter();
                            ?>
                            <input type="hidden" autocomplete="off" name="footer_id"
                                   value="<?php echo $admin_sql_row['footer_id']; ?>" id="footer_id" class="validate">
                            <tbody>
                            <tr>
                                <td>Service Expert Email :</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" name="admin_service_expert_email" required="required" class="form-control" placeholder="Email"
                                               value="<?php echo $admin_sql_row['admin_service_expert_email']; ?>">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Service Expert Mobile</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" name="admin_service_expert_mobile" required="required" value="<?php echo $admin_sql_row['admin_service_expert_mobile']; ?>"
                                               placeholder="i.e 9874561230">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Service Expert Whatsapp</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" name="admin_service_expert_whatsapp" required="required" value="<?php echo $admin_sql_row['admin_service_expert_whatsapp']; ?>"
                                               placeholder="i.e +19874512630">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <button type="submit" name="service_expert_admin_setting_submit" class="db-pro-bot-btn">Submit Changes</button>
                                </td>
                                <td></td>
                            </tr>
                            </tbody>

                        </table>
                    </form>
                </div>
            </div>

        </div>
    </div>
</section>
<!-- END -->

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="../js/jquery.min.js"></script>
<script src="../js/popper.min.js"></script>
<script src="../js/bootstrap.min.js"></script>
<script src="../js/jquery-ui.js"></script>
<script src="../js/select-opt.js"></script>
<script src="js/admin-custom.js"></script>

</body>

</html>