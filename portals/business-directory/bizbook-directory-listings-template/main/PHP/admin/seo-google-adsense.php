<?php
include "header.php";
?>
<?php if ($admin_row['admin_country_options'] != 1) {
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
                            <span class="udb-inst">Add Google AdSense Code</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Google AdSense</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $row_f = getAllFooter();
                                    ?>
                                    <form name="google_ad_sense_form" action="update_google_ad_sense.php" id="country_form" method="post"
                                          class="cre-dup-form cre-dup-form-show">
                                        <ul>
                                            <li>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                    <textarea name="admin_google_ad_sense" id="admin_google_ad_sense" class="form-control"
                                                              placeholder="Google Ad sense code *" required><?php echo stripslashes($row_f['admin_google_ad_sense']); ?></textarea>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        </ul>
                                        <button type="submit" name="google_ad_sense_submit" class="btn btn-primary">Submit
                                        </button>
                                    </form>
                                    <div class="ud-notes">
                                        <p><b>Notes:</b> You can get <b>Google AdSense</b> code from <b>Google</b> and
                                            paste above the box. Once you update the Google Ads means Ads start showing
                                            all Ads positions. If you updated any <b>custom banner Ads</b> in any other
                                            position means <b>Google Ads can't showing the particular positions</b>.</p>
                                    </div>
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