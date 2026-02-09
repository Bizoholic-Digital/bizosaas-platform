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
                            <span class="udb-inst">Delete This Coupon</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Delete Coupon</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $coupon_row_code = $_GET['row'];
                                    $coupon_row = getCoupon($coupon_row_code);

                                    ?>
                                    <form name="coupon_form" id="coupon_form" method="post" enctype="multipart/form-data"
                                          action="trash_coupon.php"  class="cre-dup-form cre-dup-form-show">
                                        <input type="hidden" id="coupon_id" value="<?php echo $coupon_row['coupon_id']; ?>"
                                               name="coupon_id" class="validate">
                                        <input type="hidden" id="coupon_photo_old"
                                               value="<?php echo $coupon_row['coupon_photo']; ?>" name="coupon_photo_old"
                                               class="validate">
                                        <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select name="coupon_user_id" required="required" disabled="disabled"
                                                                    class="form-control" id="coupon_user_id">
                                                                <option value="">Choose a user *</option>
                                                                <?php
                                                                foreach (getAllUser() as $row) {

                                                                    ?>
                                                                    <option <?php if($coupon_row['coupon_user_id']== $row['user_id']){ echo "selected"; } ?>
                                                                        value="<?php echo $row['user_id']; ?>"><?php echo $row['first_name']; ?></option>
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
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" class="form-control" name="coupon_name" readonly
                                                                   value="<?php echo $coupon_row['coupon_name']; ?>" placeholder="Coupon name" required>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" class="form-control" name="coupon_code" readonly
                                                                   value="<?php echo $coupon_row['coupon_code']; ?>" placeholder="Offer code" required>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" class="form-control" name="coupon_link" readonly
                                                                   value="<?php echo $coupon_row['coupon_link']; ?>" placeholder="Website link(if online offer)">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                               
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <label>Start date</label>
                                                            <input type="date" class="form-control" readonly
                                                                   value="<?php echo $coupon_row['coupon_start_date']; ?>" name="coupon_start_date" required>
                                                        </div>
                                                    </div>
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <label>End date</label>
                                                            <input type="date" class="form-control" readonly
                                                                   value="<?php echo $coupon_row['coupon_end_date']; ?>" name="coupon_end_date" required>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                            </li>
                                        </ul>
                                        <button type="submit" name="coupon_submit" class="btn btn-primary">Delete
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