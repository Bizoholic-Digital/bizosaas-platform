<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

if (file_exists('config/general_user_authentication.php')) {
    include('config/general_user_authentication.php');
}

if (file_exists('config/coupon_page_authentication.php')) {
    include('config/coupon_page_authentication.php');
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
                <span class="steps"><?php echo $BIZBOOK['EDIT_THIS_COUPON']; ?></span>
                <div class="log">
                    <div class="login">
                        <h4><?php echo $BIZBOOK['EDIT_THIS_COUPON']; ?></h4>
                        <?php include "page_level_message.php"; ?>
                        <?php
                        $coupon_row_code = $_GET['FMFJGVPWERFGVPWOVGYMFMFJ188WOVGYMFUKEX8'];
                        $coupon_row = getCoupon($coupon_row_code);
                        ?>
                        <form name="coupon_form" id="edit_coupon_form" enctype="multipart/form-data" method="post"
                              action="coupon_update.php" class="listing_form_1">
                            <input type="hidden" id="coupon_id" value="<?php echo $coupon_row['coupon_id']; ?>"
                                   name="coupon_id" class="validate">
                            <input type="hidden" id="coupon_photo_old"
                                   value="<?php echo $coupon_row['coupon_photo']; ?>" name="coupon_photo_old"
                                   class="validate">
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <input type="text" class="form-control" name="coupon_name"
                                               value="<?php echo $coupon_row['coupon_name']; ?>"
                                               placeholder="<?php echo $BIZBOOK['COUPON-COUPON-NAME-PLACEHOLDER']; ?>" required>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <input type="text" class="form-control" name="coupon_code"
                                               value="<?php echo $coupon_row['coupon_code']; ?>"
                                               placeholder="<?php echo $BIZBOOK['COUPON-OFFER-CODE-PLACEHOLDER']; ?>" required>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <input type="text" class="form-control" name="coupon_link"
                                               value="<?php echo $coupon_row['coupon_link']; ?>"
                                               placeholder="<?php echo $BIZBOOK['COUPON-WEBSITE-LINK-PLACEHOLDER']; ?>">
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <label><?php echo $BIZBOOK['COUPON-BRAND-LOGO-PLACEHOLDER']; ?></label>
                                        <div class="fil-img-uplo">
                                            <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                            <input type="file" name="coupon_photo" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                        </div> 
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label><?php echo $BIZBOOK['COUPON-START-DATE-PLACEHOLDER']; ?></label>
                                        <input type="text" class="form-control"
                                               value="<?php echo date ('m/d/Y', strtotime($coupon_row['coupon_start_date'])); ?>"
                                               name="coupon_start_date" id="stdate" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label><?php echo $BIZBOOK['COUPON-END-DATE-PLACEHOLDER']; ?></label>
                                        <input type="text" class="form-control"
                                               value="<?php  echo date ('m/d/Y', strtotime($coupon_row['coupon_end_date'])); ?>"
                                               name="coupon_end_date" id="endate" required>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->

                            <button type="submit" name="coupon_submit" class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
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