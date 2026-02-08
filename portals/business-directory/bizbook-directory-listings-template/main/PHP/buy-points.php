<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

$user_details_row = getUser($_SESSION['user_id']);

delBuyPoints();

?>

<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg">
    <div class="container">
        <div class="row">
            <div class="login-main add-list  buy-poin">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['BUY_POINTS']; ?></span>
                <div class="log">
                    <div class="login">
                        <h4>Hi, <?php echo $user_details_row['first_name']; ?>!!!</h4>
                        <?php include "page_level_message.php"; ?>
                        <form name="buy_points_form" id="buy_points_form" method="post"
                              action="new_buy_points_insert.php" enctype="multipart/form-data">
                            <input id="all_cost" name="all_cost" type="hidden" class="form-control">
                            <input id="cost_per_point" name="cost_per_point" value="<?php echo $footer_row['cost_per_point']; ?>" type="hidden" class="form-control">
                            <input id="cost_symbol" name="cost_symbol" value="<?php echo $footer_row['currency_symbol']; ?>" type="hidden" class="form-control">
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <p class="notes"><?php echo $BIZBOOK['BUY-POINTS-EXISTING-POINTS-LABEL']; ?> <?php echo $user_details_row['user_points']; ?> | <?php echo $BIZBOOK['BUY-POINTS-COST-1-POINT']; ?> <?php echo $footer_row['currency_symbol'].$footer_row['cost_per_point']; ?></p>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->

                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <label><?php echo $BIZBOOK['BUY-POINTS-PLEASE-ENTER-POINT']; ?></label>
                                        <input id="new_points" name="new_points" autocomplete="off" required="required" min="1" type="text" onkeypress="return isNumber(event)" class="form-control">
                                    </div>
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-12">

                                    <div class="form-group">
                                        <h5><?php echo $BIZBOOK['BUY-POINTS-PAYMENT-MODE']; ?></h5>
                                        <?php
                                        if ($footer_row['admin_paypal_status'] == "Active") {
                                            ?>
                                            <div class="radi-v4">
                                                <input type="radio" id="paymentpaypal" value="1"
                                                       name="payment" checked='checked'>
                                                <label for="paymentpaypal"><?php echo $BIZBOOK['PAYPAL']; ?></label>
                                            </div>
                                            <?php
                                        }
                                        ?>
                                        <?php
                                        if ($footer_row['admin_stripe_status'] == "Active") {
                                            ?>
                                            <div class="radi-v4">
                                                <input type="radio" id="paymentstripe" value="2"
                                                       name="payment" >
                                                <label for="paymentstripe"><?php echo $BIZBOOK['STRIPE']; ?></label>
                                            </div>
                                            <?php
                                        }
                                        ?>
                                        <?php
                                        if ($footer_row['admin_razor_pay_status'] == "Active") {
                                            ?>
                                            <div class="radi-v4">
                                                <input type="radio" id="payment_razor_pay" value="3"
                                                       name="payment" >
                                                <label for="payment_razor_pay"><?php echo $BIZBOOK['RAZOR_PAY']; ?></label>
                                            </div>
                                            <?php
                                        }
                                        ?>
                                        <?php
                                        if ($footer_row['admin_paytm_status'] == "Active") {
                                            ?>
                                            <div class="radi-v4">
                                                <input type="radio" id="payment_paytm" value="4"
                                                       name="payment" >
                                                <label for="payment_paytm"><?php echo $BIZBOOK['PAYTM']; ?></label>
                                            </div>
                                            <?php
                                        }
                                        ?>

                                    </div>
                                </div>

                            </div>

                            <button type="submit" id="buy_points_submit" name="buy_points_submit" class="btn btn-primary"><?php echo $BIZBOOK['PAY_NOW']; ?></button>
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