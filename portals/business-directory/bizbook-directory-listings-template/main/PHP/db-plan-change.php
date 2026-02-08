<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

?>
<!-- START -->
<!--PRICING DETAILS-->
<section class="login-reg">
    <div class="container">
        <div class="row">
            <div class="login-main add-list posr">
                <div class="log-bor">&nbsp;</div>
                <div class="log log-1">
                    <div class="login login-new">
                        <h4><?php echo $BIZBOOK['DASH_RIGHT_CHANGE_MY_PLAN']; ?></h4>
                        <?php include "page_level_message.php"; ?>
                        <?php
                        //To calculate the expiry date from user created date starts

                        $start_date_timestamp = strtotime($user_details_row['user_cdt']);
                        $plan_type_duration = $user_plan_type['plan_type_duration'];

                        $expiry_date_timestamp = strtotime("+$plan_type_duration months", $start_date_timestamp);

                        $expiry_date = date("Y-m-d h:i:s", $expiry_date_timestamp);

                        //To calculate the expiry date from user created date ends
                        ?>
                        <p><?php echo $BIZBOOK['HI']; ?> <?php echo $user_details_row['first_name']; ?>, </br><?php echo $BIZBOOK['DASH_RIGHT_YOUR_CURRENT_PLAN']; ?>
                            <b><?php if ($user_details_row['user_type'] == "Service provider") {
                                    echo $user_plan_type['plan_type_name'];
                                } else {
                                    echo "General User";
                                } ?></b></br> <?php echo $BIZBOOK['DASH_RIGHT_EXPIRATION_DATE']; ?> <?php if ($user_details_row['user_type'] == "Service provider") {
                                echo dateFormatconverter($expiry_date);
                            } else {
                                echo "Unlimited";
                            } ?></p>
                        <form name="plan_change_form" id="plan_change_form" method="post" enctype="multipart/form-data"
                              action="plan_change_submit.php">
                            <div class="form-group">
                                <div class="form-group">
                                    <select name="user_plan" required="required" id="user_plan" class="form-control">
                                        <option value=""
                                                selected="selected"><?php echo $BIZBOOK['CHOOSE_YOUR_PLAN']; ?></option>
                                        <?php
                                        if ($user_details_row['user_type'] == "Service provider") {
                                            $plan_type_id = $user_plan_type['plan_type_id'];
                                        } else {
                                            $plan_type_id = 1;
                                        }
                                        $plan_type = "SELECT *
										FROM " . TBL . "plan_type WHERE plan_type_status='Active' AND plan_type_id >= $plan_type_id

										ORDER BY plan_type_id ASC";


                                        $rs_plan_type = mysqli_query($conn, $plan_type);

                                        $si = 1;
                                        while ($plan_type_row = mysqli_fetch_array($rs_plan_type)) {

                                            if ($plan_type_row['plan_type_duration'] >= 7) {
                                                $date_text = "/year";
                                            } else {
                                                $date_text = "/month";
                                            }
                                            ?>
                                            <option
                                                value="<?php echo $plan_type_row['plan_type_id']; ?>"><?php echo $plan_type_row['plan_type_name'];
                                                if ($plan_type_row['plan_type_price'] != 0) {
                                                    echo ' - ' . $footer_row['currency_symbol'] . '' . $plan_type_row['plan_type_price'] . $date_text;
                                                } ?></option>
                                            <?php
                                        }
                                        ?>
                                    </select>
                                    <a href="pricing-details" class="frmtip" target="_blank"><?php echo $BIZBOOK['PLAN_DETAILS'];?></a>
                                </div>
                            </div>
                            <button type="submit" name="plan_type_submit" class="btn btn-primary"><?php echo $BIZBOOK['CHANGE'];?></button>
                        </form>
                        <div class="col-md-12">
                            <a href="dashboard" class="skip"><?php echo $BIZBOOK['GO_TO_USER_DASHBOARD']; ?> &gt;&gt;</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!--END PRICING DETAILS-->


<section>
    <div class="pop-ups pop-quo">
        <!-- The Modal -->
        <div class="modal fade" id="quote">
            <div class="modal-dialog">
                <div class="modal-content">
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                    <!-- Modal Header -->
                    <div class="quote-pop">
                        <h4><?php echo $BIZBOOK['LEAD-GET-QUOTE']; ?></h4>
                        <form>
                            <div class="form-group">
                                <input type="text" class="form-control" placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>" required>
                            </div>
                            <div class="form-group">
                                <input type="email" class="form-control" placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>"
                                       pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>" required>
                            </div>
                            <div class="form-group">
                                <input type="text" class="form-control" placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>"
                                       pattern="[7-9]{1}[0-9]{9}"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>" required>
                            </div>
                            <div class="form-group">
                                <textarea class="form-control" rows="3"
                                          placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
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