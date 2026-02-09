<?php
include "header.php";
?>
<?php if ($admin_row['admin_seo_setting_options'] != 1) {
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <section class="login-reg">
                <div class="container">
                    <div class="row">
                        <div class="login-main add-list add-ncate">
                            <div class="log-bor">&nbsp;</div>
                            <span class="udb-inst">Add Google Analytics Code</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Google Analytics</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $row_f = getAllFooter();
                                    ?>
                                    <form name="google_analytics_form" action="update_google_analytics.php" id="country_form" method="post"
                                          class="cre-dup-form cre-dup-form-show">
                                        <ul>
                                            <li>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                    <textarea name="admin_google_analytics" id="admin_google_analytics" class="form-control"
                                                              placeholder="Google analytics code *" required><?php echo stripslashes($row_f['admin_google_analytics']); ?></textarea>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        </ul>
                                        <button type="submit" name="google_analytics_submit" class="btn btn-primary">Submit
                                        </button>
                                    </form>

                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

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
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
</body>

</html>