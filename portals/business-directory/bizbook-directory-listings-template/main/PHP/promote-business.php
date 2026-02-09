<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

$actual_link = "http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";

$user_details_row = getUser($_SESSION['user_id']);

if ($user_details_row['user_points'] <= 0) {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_DONT_HAVE_ENOUGH_POINTS_BUY_SOME_POINTS'];

    header('Location: db-all-listing');
    exit;
}

?>
<!-- START -->
<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg">
    <div class="container">
        <div class="row">
            <div class="login-main add-list">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['PROMOTE-BUSINESS-START-PROMOTIONS']; ?></span>
                <div class="log">
                    <div class="login">
                        <h4><?php echo $BIZBOOK['PROMOTE-BUSINESS-START-PROMOTIONS']; ?></h4>
                        <?php include "page_level_message.php"; ?>
                        <form name="create_promote_form" id="create_promote_form" method="post"
                              action="new_promote_insert.php" enctype="multipart/form-data">
                            <input type="hidden" value="" name="ad_total_days" id="ad_total_days" class="validate">
                            <input type="hidden" value="" name="ad_cost_per_day" id="ad_cost_per_day" class="validate">
                            <input type="hidden" value="" name="ad_total_cost" id="ad_total_cost" class="validate">
                            <input type="hidden" value="1" name="adposi" id="adposi" class="validate">
                            <input type="hidden" value="<?php echo $actual_link; ?>" name="url" id="url"
                                   class="validate">
                            <input type="hidden" value="1" name="type_value" id="type_value" class="validate">
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <select name="type_id" required="required"
                                                id="type_id" class=" form-control">
                                            <option value=""><?php echo $BIZBOOK['PROMOTE-BUSINESS-CHOOSE-LISTING'];?></option>
                                            <?php
                                            foreach (getAllListingUser($_SESSION['user_id']) as $listing_row) {
                                                ?>
                                                <option <?php if ($_SESSION['listing_id'] == $listing_row['listing_id']) {
                                                    echo "selected";
                                                } ?>
                                                    value="<?php echo $listing_row['listing_id']; ?>">
                                                    <?php echo $listing_row['listing_name']; ?></option>
                                                <?php
                                            }
                                            ?>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label><?php echo $BIZBOOK['COUPON-START-DATE-PLACEHOLDER']; ?></label>
                                        <input id="start-date" name="ad_start_date" required="required" type="date"
                                               class="form-control">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label><?php echo $BIZBOOK['COUPON-END-DATE-PLACEHOLDER']; ?></label>
                                        <input id="end-date" name="ad_end_date" type="date" required="required"
                                               class="form-control">
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div style="display:block" class="ad-pri-cal">
                                        <ul>
                                            <li>
                                                <div>
                                                    <span><?php echo $BIZBOOK['PROMOTE-BUSINESS-TOTAL-DAYS']; ?></span>
                                                    <h5 class="ad-tdays">0</h5>
                                                </div>
                                            </li>
                                            <li>
                                                <div>
                                                    <span><?php echo $BIZBOOK['PROMOTE-BUSINESS-COST-PER-DAY']; ?></span>
                                                    <h5><b class="ad-pocost">1</b></h5>
                                                </div>
                                            </li>
                                            <li>
                                                <div>
                                                    <span><?php echo $BIZBOOK['PROMOTE-BUSINESS-TOTAL-POINTS']; ?></span>
                                                    <h5><b class="ad-tcost">0</b></h5>
                                                </div>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->

                            <button type="submit" name="create_promote_submit"
                                    class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!--END PRICING DETAILS-->
<?php
include "footer.php";
?>


<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script src="js/select-opt.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>

</body>

</html>