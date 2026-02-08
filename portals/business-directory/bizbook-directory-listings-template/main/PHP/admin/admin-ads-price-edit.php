<?php
include "header.php";
?>
<?php if($admin_row['admin_ads_options'] != 1){
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
                        <div class="login-main add-list posr">
                            <div class="log-bor">&nbsp;</div>
                            <span class="udb-inst">Ad details</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Ad Pricing and other details</h4><?php include "../page_level_message.php"; ?>
                                    <?php
                                    $all_ads_price_id = $_GET['row'];
                                    $row = getAdsPrice($all_ads_price_id);
                                    ?>
                                    <form name="ads_price_form" id="ads_price_form" method="post" action="update_ads_price.php" enctype="multipart/form-data">
                                        <input type="hidden" class="validate" id="all_ads_price_id" name="all_ads_price_id" value="<?php echo $row['all_ads_price_id']; ?>" required="required">
                                        <input type="hidden" class="validate" id="ad_price_photo_old" name="ad_price_photo_old" value="<?php echo $row['ad_price_photo']; ?>" required="required">
                                        <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" class="form-control" name="ad_price_name"
                                                                   value="<?php echo $row['ad_price_name']; ?>" placeholder="Ad position name" required>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" class="form-control" name="ad_price_size"
                                                                   value="<?php echo $row['ad_price_size']; ?>"
                                                                   placeholder="Ad image size" required>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" class="form-control" name="ad_price_cost"
                                                                   value="<?php echo $row['ad_price_cost']; ?>"
                                                                   onkeypress="return isNumber(event)"
                                                                   placeholder="Ad cost" required>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label>Choose Ad preview image</label>
                                                            <input type="file" name="ad_price_photo" class="form-control">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select name="ad_price_status" class="form-control">
                                                                <option <?php if($row['ad_price_status']=="Active"){ echo "selected"; } ?>  value="Active">Active</option>
                                                                <option <?php if($row['ad_price_status']=="Inactive"){ echo "selected"; } ?> value="Inactive">InActive</option>
                                                            </select>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                            </li>
                                        </ul>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <button type="submit" name="ad_price_submit" class="btn btn-primary">update</button>
                                            </div>
                                            <div class="col-md-12">
                                                <a href="admin-current-ads.php" class="skip">Go to Current Ads >></a>
                                            </div>
                                        </div>
                                        <!--FILED END-->
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
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>