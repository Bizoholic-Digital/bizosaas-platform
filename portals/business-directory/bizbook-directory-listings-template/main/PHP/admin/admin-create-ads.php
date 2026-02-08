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
                    <span class="udb-inst">Create ads</span>
                    <div class="log log-1">
                        <div class="login">
                            <h4>Create new Ads</h4>
                            <?php include "../page_level_message.php"; ?>
                            <form name="create_ads_form" id="create_ads_form" method="post" action="insert_new_ads.php" enctype="multipart/form-data">
                                <input type="hidden" value="" name="ad_total_days" id="ad_total_days" class="validate">
                                <input type="hidden" value="" name="ad_cost_per_day" id="ad_cost_per_day" class="validate">
                                <input type="hidden" value="" name="ad_total_cost" id="ad_total_cost" class="validate">
                                <ul>
										<li>
                                   <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <select name="user_id" required="required" class="form-control" id="user_id">
                                                    <option value="">Choose a user *</option>
                                                    <?php
                                                    foreach (getAllUser() as $row) {

                                                        ?>
                                                        <option value="<?php echo $row['user_id']; ?>"><?php echo $row['first_name']; ?></option>
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
                                                <select name="all_ads_price_id" required="required" class="form-control" id="adposi">
                                                    <option value="">Choose Ads Position *</option>
                                                    <?php
                                                    foreach (getAllActiveAdsPrice() as $row) {
                                                        ?>
                                                        <option myTag = "<?php echo $row['ad_price_cost']; ?>"
                                                                value="<?php echo $row['all_ads_price_id']; ?>"><?php echo $row['ad_price_name']; ?> (<?php echo $row['ad_price_cost']; ?><?php echo $footer_row['currency_symbol']; ?>/per day)</option>
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
                                             <input type="text" id="stdate" autocomplete="off" name="ad_start_date" class="form-control" placeholder="Ad start date (MM/DD/YYYY)" required>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                   <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                             <input type="text" id="endate" autocomplete="off" name="ad_end_date" class="form-control" placeholder="Ad end date (MM/DD/YYYY)" required>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <label>Choose Ad image</label>
                                              <input type="file" name="ad_enquiry_photo" class="form-control" required>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                            <!--FILED START-->
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <textarea  id="ad_link"  name="ad_link" class="form-control" placeholder="Advertisement External link" required></textarea>
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
                                                            <h5><?php echo $footer_row['currency_symbol']; ?><b class="ad-pocost">0</b></h5>
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
                                                            <h5><?php echo $footer_row['currency_symbol']; ?><b class="ad-tcost">0</b></h5>
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
                                            <button type="submit" name="create_ad_submit" class="btn btn-primary">Publish this Ad</button>
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