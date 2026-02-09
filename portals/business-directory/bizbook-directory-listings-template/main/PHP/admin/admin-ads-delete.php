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
                            <span class="udb-inst">Delete ads</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Delete this Ad</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $path = $_GET['path'];
                                    $all_ads_enquiry_id = $_GET['row'];
                                    $row = getAdsEnquiry($all_ads_enquiry_id);
                                    ?>
                                    <form name="delete_ads_form" id="delete_ads_form" method="post" action="trash_ads.php" enctype="multipart/form-data">
                                        <input type="hidden" class="validate" id="all_ads_enquiry_id" name="all_ads_enquiry_id" value="<?php echo $row['all_ads_enquiry_id']; ?>" required="required">
                                        <input type="hidden" class="validate" id="ad_enquiry_photo_old" name="ad_enquiry_photo_old" value="<?php echo $row['ad_enquiry_photo']; ?>" required="required">
                                        <input type="hidden" value="<?php echo $row['ad_total_days']; ?>" name="ad_total_days" id="ad_total_days" class="validate">
                                        <input type="hidden" value="<?php echo $row['ad_cost_per_day']; ?>" name="ad_cost_per_day" id="ad_cost_per_day" class="validate">
                                        <input type="hidden" value="<?php echo $row['ad_total_cost']; ?>" name="ad_total_cost" id="ad_total_cost" class="validate">
                                        <input type="hidden" value="<?php echo $path; ?>" name="path" id="path" class="validate">
                                        <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select name="user_id" disabled="disabled" required="required" class="form-control" id="user_id">
                                                                <option value="">Choose a user *</option>
                                                                <?php
                                                                foreach (getAllUser() as $user_row) {

                                                                    ?>
                                                                    <option <?php if ($user_row['user_id'] == $row['user_id']) {
                                                                        echo "selected";
                                                                    } ?>
                                                                        value="<?php echo $user_row['user_id']; ?>"><?php echo $user_row['first_name']; ?></option>
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
                                                        <div class="form-group ca-sh-user">
                                                            <select disabled="disabled" name="all_ads_price_id" required="required" class="form-control" id="adposi">
                                                                <option value="">Choose Ads Position *</option>
                                                                <?php
                                                                foreach (getAllActiveAdsPrice() as $ad_row) {
                                                                    ?>
                                                                    <option <?php if ($ad_row['all_ads_price_id'] == $row['all_ads_price_id']) {
                                                                        echo "selected";
                                                                    } ?> myTag = "<?php echo $ad_row['ad_price_cost']; ?>"
                                                                         value="<?php echo $ad_row['all_ads_price_id']; ?>"><?php echo $ad_row['ad_price_name']; ?> (<?php echo $ad_row['ad_price_cost']; ?><?php echo $footer_row['currency_symbol']; ?>/per day)</option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                            <a href="../ad-details.php" class="frmtip" target="_blank">Pricing details</a>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input disabled="disabled"  type="text" id="stdate" name="ad_start_date" value="<?php echo $row['ad_start_date']; ?>" class="form-control" placeholder="Ad start date (MM/DD/YYYY)" required>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input disabled="disabled"  type="text" id="endate" name="ad_end_date" value="<?php echo $row['ad_end_date']; ?>" class="form-control" placeholder="Ad end date (MM/DD/YYYY)" required>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->

                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <textarea readonly="readonly"  id="ad_link"  name="ad_link" class="form-control" placeholder="Advertisement External link" required><?php echo $row['ad_link']; ?></textarea>
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
                                                                        <span>Total days</span>
                                                                        <h5 class="ad-tdays">0</h5>
                                                                    </div>
                                                                </li>
                                                                <li>
                                                                    <div>
                                                                        <span>Cost Per Day</span>
                                                                        <h5><?php echo $footer_row['currency_symbol']; ?><b class="ad-pocost"><?php echo $row['ad_total_days']; ?></b></h5>
                                                                    </div>
                                                                </li>
                                                                <li>
                                                                    <div>
                                                                        <span>Tax</span>
                                                                        <h5><?php echo $footer_row['currency_symbol']; ?>4</h5>
                                                                    </div>
                                                                </li>
                                                                <li>
                                                                    <div>
                                                                        <span>Total Cost</span>
                                                                        <h5><?php echo $footer_row['currency_symbol']; ?><b class="ad-tcost"><?php echo $row['ad_total_cost']; ?></b></h5>
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
                                                <button type="submit" name="delete_ad_submit" class="btn btn-primary">Delete this Ad</button>
                                            </div>
                                            <div class="col-md-12">
                                                <a href="profile.php" class="skip">Go to User Dashboard >></a>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                    </form>
                                    <div class="ud-notes">
                                        <p><b>Notes:</b> Hi, Before submit your <b>Ads</b> please check the <b>available date</b> because previous Ads running in same date. Kindly check this manually</p>
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
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>