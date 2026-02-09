<?php
include "header.php";

?>
<!-- START -->
<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg">
    <div class="container">
        <div class="row">
                <div class="login-main add-list">
                    <?php
                    if(!isset($_SESSION['user_code']) && empty($_SESSION['user_code'])) {
                        ?>
                        <div class="coup-sec-log">
                            <h4><?php echo $BIZBOOK['AD-DETAILS-SIGN-IN-POST-YOUR-ADS']; ?></h4>
                            <p><?php echo $BIZBOOK['AD-DETAILS-SIGN-IN-POST-YOUR-ADS-P-TAG']; ?></p>
                            <a href="<?php echo $LOGIN_URL; ?>"><?php echo $BIZBOOK['COUPON-NO-LOGIN-SIGN-IN-NOW']; ?></a>
                        </div>
                        <?php
                    }else {
                    ?>
                    <div class="log-bor">&nbsp;</div>
                    <span class="steps"><?php echo $BIZBOOK['AD-DETAILS-CREATE-NEW-ADS']; ?></span>
                    <div class="log">
                        <div class="login">

                            <h4><?php echo $BIZBOOK['AD-DETAILS-SUBMIT-YOUR-ADS']; ?></h4>
                            <form name="create_ads_form" id="create_ads_form" method="post" action="new_ads_insert.php"
                                  enctype="multipart/form-data">
                                <input type="hidden" value="" name="ad_total_days" id="ad_total_days" class="validate">
                                <input type="hidden" value="" name="ad_cost_per_day" id="ad_cost_per_day"
                                       class="validate">
                                <input type="hidden" value="" name="ad_total_cost" id="ad_total_cost" class="validate">
                                <ul>
                                    <li>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group ca-sh-user">
                                                    <select name="all_ads_price_id" required="required"
                                                            class="form-control"
                                                            id="adposi">
                                                        <option value=""><?php echo $BIZBOOK['AD-DETAILS-CHOOSE-ADS-POSITION']; ?></option>
                                                        <?php
                                                        foreach (getAllActiveAdsPrice() as $row) {
                                                            ?>
                                                            <option myTag="<?php echo $row['ad_price_cost']; ?>"
                                                                    value="<?php echo $row['all_ads_price_id']; ?>"><?php echo $row['ad_price_name']; ?>
                                                                (<?php echo $row['ad_price_cost']; ?><?php echo $footer_row['currency_symbol']; ?>
                                                                /per day)
                                                            </option>
                                                            <?php
                                                        }
                                                        ?>
                                                    </select>
                                                    <a href="ad-details" class="frmtip" target="_blank"><?php echo $BIZBOOK['AD-DETAILS-PRICING-DETAILS']; ?></a>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <input type="date" autocomplete="off" name="ad_start_date"
                                                           class="form-control" placeholder="<?php echo $BIZBOOK['AD-DETAILS-AD-START-DATE']; ?>"
                                                           required>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <input type="date" autocomplete="off" name="ad_end_date"
                                                           class="form-control" placeholder="<?php echo $BIZBOOK['AD-DETAILS-AD-END-DATE']; ?>"
                                                           required>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <label><?php echo $BIZBOOK['AD-DETAILS-CHOOSE-AD-IMAGE']; ?></label>
                                                    <input type="file" name="ad_enquiry_photo" class="form-control"
                                                           required>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                <textarea id="ad_link" name="ad_link" class="form-control"
                                                          placeholder="<?php echo $BIZBOOK['AD-DETAILS-ADVERTISEMENT-EXTERNAL-LINK']; ?>" required></textarea>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="ad-pri-cal">
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
                                                                <h5><?php echo $footer_row['currency_symbol']; ?><b
                                                                        class="ad-pocost">0</b></h5>
                                                            </div>
                                                        </li>
                                                        <li>
                                                            <div>
                                                                <span><?php echo $BIZBOOK['TAX']; ?></span>
                                                                <h5><?php echo $footer_row['currency_symbol']; ?>4</h5>
                                                            </div>
                                                        </li>
                                                        <li>
                                                            <div>
                                                                <span><?php echo $BIZBOOK['PROMOTE-BUSINESS-TOTAL-COST']; ?></span>
                                                                <h5><?php echo $footer_row['currency_symbol']; ?><b
                                                                        class="ad-tcost">0</b></h5>
                                                            </div>
                                                        </li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                    </li>
                                </ul>
                                <!--FILED START-->
                                <div class="row">
                                    <div class="col-md-12">
                                        <button type="submit" name="create_ad_submit" class="btn btn-primary"><?php echo $BIZBOOK['AD-DETAILS-PUBLISH-THIS-AD'];?></button>
                                    </div>
                                    <div class="col-md-12">
                                        <a href="dashboard" class="skip"><?php echo $BIZBOOK['GO_TO_USER_DASHBOARD']; ?> >></a>
                                    </div>
                                </div>
                                <!--FILED END-->
                            </form>
                            <div class="ud-notes">
                                <p><b><?php echo $BIZBOOK['DB-PAYMENTS-FOOTER-NOTES']; ?>:</b> <?php echo $BIZBOOK['AD-DETAILS-NOTES-MESSAGE']; ?></p>
                            </div>
                        </div>
                    </div>
                        <?php
                    }
                    ?>
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
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>
</body>

</html>