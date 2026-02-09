<?php
include "header.php";
if (!isset($_SESSION['payment_user_id']) && empty($_SESSION['payment_user_id'])) {
    header("Location: buy-points");
    exit();
}
?>

<!-- START -->
<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg">
    <div class="container">
        <div class="row">
            <div class="login-main">
                <div class="log-bor">&nbsp;</div>

                <div class="log ">
                    <div class="login">
                        <?php
                        if (isset($_SESSION['register_status_msg'])) {
                            include "page_level_message.php";
                            unset($_SESSION['register_status_msg']);
                        }
                        ?>
                        <?php
                        if (isset($_SESSION['status_msg'])) {
                            include "page_level_message.php";
                            unset($_SESSION['status_msg']);
                        }
                        ?>
                        <h4><?php echo $BIZBOOK['DB-PAYMENTS-STRIPE-PAYMENT']; ?></h4>
                        <p><?php echo $BIZBOOK['DB-PAYMENTS-STRIPE-PAYMENT-SIMPLE-WAY-MESSAGE']; ?></p>
                        <?php
                        $user_details_row = getUser($_SESSION['payment_user_id']);

                        if (isset($_SESSION['new_plan_id'])) {

                            $user_plan_type = getPlanType($_SESSION['new_plan_id']); //Fetch Logged In User Plan details and data

                        } else {

                            $user_plan = $user_details_row['user_plan']; //Fetch of Logged In user Plan

                            $user_plan_type = getPlanType($user_plan); //Fetch Logged In User Plan details and data
                        }


                        ?>
                        <span class="paymentErrors alert-danger"></span>
                        <div><?php echo $BIZBOOK['HI']; ?> <?php echo $user_details_row['first_name']; ?>,</br> <?php echo $BIZBOOK['DB-PAYMENTS-STRIPE-PAYMENT-YOUR-FINAL-AMOUNT']; ?> :
                            <b><?php echo $footer_row['currency_symbol']; ?><?php echo $_SESSION['point_total_cost']; ?></b>
                        </div>
                        <form name="payment_stripe_form" id="payment_stripe_form" method="post"
                              action="point_payment_stripe_submit.php">

                            <input type="hidden" autocomplete="off" value="1" name="path" id="path" class="validate">
                            <input type="hidden" autocomplete="off" name="trap_box" id="trap_box" class="validate">

                            <input type="hidden" autocomplete="off" name="mode_path" value="XeFrOnT_MoDeX_PATHXHU"
                                   id="mode_path" class="validate">

                            <div class="form-group">
                                <input type="text" autocomplete="off" name="first_name" id="first_name"
                                       required="required"
                                       class="form-control" placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>">
                            </div>
                            <div class="form-group">
                                <input type="email" autocomplete="off" name="email_id" id="email_id"
                                       class="form-control" placeholder="<?php echo $BIZBOOK['LEAD-EMAIL-PLACEHOLDER']; ?>" required>
                            </div>
                            <div class="form-group">
                                <input type="text" onkeypress="return isNumber(event)" autocomplete="off"
                                       name="card_number" id="card_number"
                                       class="form-control" placeholder="<?php echo $BIZBOOK['LEAD-CARD-NUMBER-PLACEHOLDER'];?>" required>
                            </div>

                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <input type="text" name="cardExpMonth" required
                                               onkeypress="return isNumber(event)" maxlength="2" placeholder="<?php echo $BIZBOOK['LEAD-CARD-NUMBER-MM-PLACEHOLDER']; ?>"
                                               size="2" id="cardExpMonth" class="form-control">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <input type="text" name="cardExpYear" required
                                               onkeypress="return isNumber(event)" maxlength="4" placeholder="<?php echo $BIZBOOK['LEAD-CARD-NUMBER-YYYY-PLACEHOLDER']; ?>"
                                               size="4" id="cardExpYear" class="form-control">
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <input type="text" onkeypress="return isNumber(event)" required name="cardCVC" size="4"
                                       maxlength="4" autocomplete="off" id="cardCVC" class="form-control"
                                       placeholder="<?php echo $BIZBOOK['LEAD-CARD-NUMBER-CVC-PLACEHOLDER']; ?>">
                            </div>

                            <button type="submit" name="stripe_payment_submit" id="stripe_payment_submit"
                                    class="btn btn-primary">
                                <?php echo $BIZBOOK['PAY']; ?> <?php echo $footer_row['currency_symbol']; ?><?php echo $user_plan_type['plan_type_price']; ?>
                                <?php echo $BIZBOOK['NOW']; ?>
                            </button>
                        </form>
                    </div>
                </div>

            </div>
        </div>
    </div>
</section>
<!--END PRICING DETAILS-->

<?php
$stripe_publishable_key = $footer_row['admin_stripe_id'];
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
<script type="text/javascript" src="https://js.stripe.com/v2/"></script>
<script>
    Stripe.setPublishableKey('<?php echo $stripe_publishable_key; ?>');  // set your stripe publishable key
    $(document).ready(function () {
        $("#payment_stripe_form").submit(function (event) {
            $('#stripe_payment_submit').attr("disabled", "disabled");
// create stripe token to make payment
            Stripe.createToken({
                number: $('#card_number').val(),
                cvc: $('#cardCVC').val(),
                exp_month: $('#cardExpMonth').val(),
                exp_year: $('#cardExpYear').val()
            }, handleStripeResponse);
            return false;
        });
    });
    // handle the response from stripe
    function handleStripeResponse(status, response) {
        console.log(JSON.stringify(response));
        if (response.error) {
            $('#stripe_payment_submit').removeAttr("disabled");
            $(".paymentErrors").html(response.error.message);
        } else {
            var payForm = $("#payment_stripe_form");
//get stripe token id from response
            var stripeToken = response['id'];
//set the token into the form hidden input to make payment
            payForm.append("<input type='hidden' name='stripeToken' value='" + stripeToken + "' />");
            payForm.get(0).submit();
        }
    }
</script>
</body>

</html>