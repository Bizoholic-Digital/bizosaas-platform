<?php
include "header.php";
?>
<?php if ($footer_row['admin_coupon_show'] != 1){
    header("Location: profile.php");
}
?>
<?php if ($admin_row['admin_feedback_options'] != 1) {
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
                            <span class="udb-inst">Edit This Coupon</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Edit Coupon</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $coupon_row_code = $_GET['row'];
                                    $coupon_row = getCoupon($coupon_row_code);

                                    ?>
                                    <form name="coupon_form" id="coupon_form" method="post" enctype="multipart/form-data"
                                        action="update_coupon.php"  class="cre-dup-form cre-dup-form-show">
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
                                                            <select name="coupon_user_id" required="required"
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
                                                            <input type="text" class="form-control" name="coupon_name"
                                                                   value="<?php echo $coupon_row['coupon_name']; ?>" placeholder="Coupon name" required>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" class="form-control" name="coupon_code"
                                                                   value="<?php echo $coupon_row['coupon_code']; ?>" placeholder="Offer code" required>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" class="form-control" name="coupon_link"
                                                                   value="<?php echo $coupon_row['coupon_link']; ?>" placeholder="Website link(if online offer)">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label>Brand logo or Offer image(Recommended size 65 X
                                                                65)</label>
                                                            <input type="file" name="coupon_photo"
                                                                   class="form-control" placeholder="Offer image">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <label>Start date</label>
                                                            <input type="date" class="form-control"
                                                                   value="<?php echo $coupon_row['coupon_start_date']; ?>" name="coupon_start_date" required>
                                                        </div>
                                                    </div>
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <label>End date</label>
                                                            <input type="date" class="form-control"
                                                                   value="<?php echo $coupon_row['coupon_end_date']; ?>" name="coupon_end_date" required>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                            </li>
                                        </ul>
                                        <button type="submit" name="coupon_submit" class="btn btn-primary">Submit
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