<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}
include "dashboard_left_pane.php";
?>
    <!--CENTER SECTION-->
    <div class="ud-main">
   <div class="ud-main-inn ud-no-rhs">
    <div class="ud-cen">
        <div class="log-bor">&nbsp;</div>
        <span class="udb-inst"><?php echo $BIZBOOK['PAYMENT']; ?></span>
        <?php include('config/user_activation_checker.php'); ?>
        <div class="ud-cen-s2">
            <h2><?php echo $BIZBOOK['DASH_RIGHT_PAYMENT_STATUS']; ?></h2>
            <?php include "page_level_message.php"; ?>
            <a href="db-plan-change" class="db-tit-btn"><?php echo $BIZBOOK['DASH_RIGHT_CHANGE_MY_PLAN']; ?></a>
            <div class="ud-payment">
                <div class="pay-lhs">
                    <img
                        src="images/user/<?php if (($user_details_row['profile_image'] == NULL) || empty($user_details_row['profile_image'])) {
                            echo $footer_row['user_default_image'];
                        } else {
                            echo $user_details_row['profile_image'];
                        } ?>" alt="">
                </div>
                <div class="pay-rhs">
                    <ul>
                        <li><b><?php echo $BIZBOOK['NAME'];  ?> : </b> <?php echo $user_details_row['first_name']; ?></li>
                        <li><b><?php echo $BIZBOOK['DASH_RIGHT_PLAN_NAME'];  ?> : </b> <?php echo $user_plan_type['plan_type_name']; ?></li>
                        <li><b><?php echo $BIZBOOK['DASH_RIGHT_START_DATE'];  ?> : </b> <?php echo dateFormatconverter($user_details_row['user_cdt']) ?></li>

                        <?php
                        //To calculate the expiry date from user created date starts

                        $start_date_timestamp = strtotime($user_details_row['user_cdt']);
                        $plan_type_duration = $user_plan_type['plan_type_duration'];

                        $expiry_date_timestamp = strtotime("+$plan_type_duration months", $start_date_timestamp);

                        $expiry_date = date("Y-m-d h:i:s", $expiry_date_timestamp);

                        //To calculate the expiry date from user created date ends
                        ?>

                        <li><b><?php echo $BIZBOOK['DASH_RIGHT_EXPIRY_DATE'];  ?> : </b> <?php echo dateFormatconverter($expiry_date) ?></li>
                        <li><b><?php echo $BIZBOOK['DURATION'];  ?> : </b> <?php if ($plan_type_duration >= 7) {
                                echo $plan_type_duration / 12 . ' ' . "year";
                            } else {
                                echo $plan_type_duration . ' ' . "month(s)";
                            } ?></li>

                        <?php
                        //To calculate the remaining days from expiry date to current date starts

                        $start = strtotime($curDate);
                        $end = strtotime($expiry_date);
                        $days_between = ceil(abs($end - $start) / 86400);

                        //To calculate the remaining days from expiry date to current date ends
                        ?>

                        <li><b><?php echo $BIZBOOK['DASH_RIGHT_REMAINING_DAYS'];  ?> : </b> <?php echo $days_between; ?></li>
                        <li><span
                                class="ud-stat-pay-btn"><?php echo $BIZBOOK['DASH_RIGHT_CHECKOUT_AMOUNT'];  ?>: <?php if ($user_plan_type['plan_type_price'] == 0) {
                                    echo "FREE";
                                } else {
                                    echo $footer_row['currency_symbol'] . '' . $user_plan_type['plan_type_price'];
                                } ?></span></li>
                        <li><span
                                class="ud-stat-pay-btn"><?php echo $BIZBOOK['DASH_RIGHT_PAYMENT_STATUS'];  ?>: <?php if ($user_details_row['payment_status'] == 'Paid') {
                                    echo "PAID";
                                } elseif ($user_details_row['payment_status'] == 'COD') {
                                    echo "COD Initiated / Pending";
                                } elseif ($user_plan_type['plan_type_price'] == 0) {
                                    echo "N/A";
                                } else {
                                    echo "PENDING";
                                } ?></span></li>
                    </ul>
                </div>
            </div>
            <?php if (empty($user_details_row['payment_status']) || ($user_details_row['payment_status'] == NULL)) { //To check the payment status  ?>
                <?php if ($user_plan_type['plan_type_price'] != 0) {  //To check the plan payment amount ?>
                    <div class="ud-pay-op">
                        <h4><?php echo $BIZBOOK['DB-PAYMENTS-HEADING']; ?></h4>
                        <ul>
                            <?php if ($footer_row['admin_cod_status'] == "Active") { ?>
                                <li>
                                    <div class="pay-full">
                                        <div class="rbbox">
                                            <input type="radio" id="paymentcash" name="payment" checked="">
                                            <label for="paymentcash"><?php echo $BIZBOOK['CASH_ON_DELIVERY'];  ?></label>
                                            <div class="pay-note">
                                                <span><i
                                                        class="material-icons">star</i><?php echo $BIZBOOK['DB-PAYMENTS-HEADING-P-1'];  ?></span>
                                                <span><i class="material-icons">star</i>  <?php echo $BIZBOOK['DB-PAYMENTS-HEADING-P-2'];  ?></span>
                                        <span><i
                                                class="material-icons">star</i> <?php echo $BIZBOOK['DB-PAYMENTS-HEADING-P-3'];  ?></span>
                                                <form name="cod_form" id="cod_form" method="post"
                                                      action="payment_cod_submit.php">
                                                    <h4><?php echo $BIZBOOK['DB-PAYMENTS-BILLING-DETAILS'];  ?></h4>
                                                    <ul>
                                                        <li>
                                                            <!--FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               readonly="readonly"
                                                                               value="<?php echo $user_details_row['first_name']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['FULL_NAME'];  ?> *" required>
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_country"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_country']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['COUNTRY'];  ?>">
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--FILED END-->
                                                            <!--FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_state"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_state']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['STATE'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_city"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_city']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CITY'];  ?> *"
                                                                               required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--FILED END-->
                                                            <!--FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-12">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_address"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_address']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['VILLAGE_STREET_NAME'];  ?>">
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--FILED END-->
                                                            <!--FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_zip_code"
                                                                               onkeypress="return isNumber(event)"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_zip_code']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['POSTCODE_ZIP'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_name"
                                                                               value="<?php echo $user_details_row['user_contact_name']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_PERSON'];  ?> *" required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--FILED END-->
                                                            <!--FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_mobile"
                                                                               onkeypress="return isNumber(event)"
                                                                               value="<?php echo $user_details_row['user_contact_mobile']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_PHONE_NUMBER'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_email"
                                                                               value="<?php echo $user_details_row['user_contact_email']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_EMAIL_ID'];  ?>" required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--FILED END-->
                                                        </li>
                                                    </ul>
                                                    <button type="submit" name="payment_submit" class="db-pro-bot-btn">
                                                        <?php echo $BIZBOOK['DB-PAYMENTS-SUBMIT-COD']; ?>
                                                    </button>
                                                </form>

                                            </div>
                                        </div>
                                    </div>
                                </li>

                            <?php }
                            if ($footer_row['admin_paypal_status'] == "Active") { ?>
                                <li>
                                    <div class="pay-full">
                                        <div class="rbbox">
                                            <input type="radio" id="paymentpaypal"
                                                   name="payment" <?php if ($footer_row['admin_cod_status'] != "Active") {
                                                echo "checked='checked'";
                                            } ?>>
                                            <label for="paymentpaypal"><?php echo $BIZBOOK['DB-PAYMENTS-PAYPAL-PAYMENT-GATEWAY']; ?></label>
                                            <div class="pay-note">
                                                <span><i class="material-icons">star</i> <?php echo $BIZBOOK['DB-PAYMENTS-PAYPAL-PAYMENT-GATEWAY-P-1']; ?></span>
                                                <span><i class="material-icons">star</i><?php echo $BIZBOOK['DB-PAYMENTS-WHAT-IS-PAYPAL'];?></span>
                                                <form name="paypal_form" id="paypal_form" method="post"
                                                      action="payment_paypal_submit.php">
                                                    <h4><?php echo $BIZBOOK['DB-PAYMENTS-BILLING-DETAILS'];  ?></h4>
                                                    <ul>
                                                        <li>
                                                            <!--FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" readonly="readonly"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['first_name']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['FULL_NAME'];  ?> *" required>
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_country"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_country']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['COUNTRY'];  ?>">
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--FILED END-->
                                                            <!--FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_state"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_state']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['STATE'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_city"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_city']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CITY'];  ?> *"
                                                                               required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--FILED END-->
                                                            <!--FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-12">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_address"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_address']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['VILLAGE_STREET_NAME'];  ?>">
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--FILED END-->
                                                            <!--FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_zip_code"
                                                                               onkeypress="return isNumber(event)"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_zip_code']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['POSTCODE_ZIP'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_name"
                                                                               value="<?php echo $user_details_row['user_contact_name']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_PERSON'];  ?> *" required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--FILED END-->
                                                            <!--FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_mobile"
                                                                               onkeypress="return isNumber(event)"
                                                                               value="<?php echo $user_details_row['user_contact_mobile']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_PHONE_NUMBER'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_email"
                                                                               value="<?php echo $user_details_row['user_contact_email']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_EMAIL_ID'];  ?>" required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--FILED END-->
                                                        </li>
                                                    </ul>
                                                    <button type="submit" name="payment_submit" class="db-pro-bot-btn">
                                                        <?php echo $BIZBOOK['DB-PAYMENTS-START-PAYMENT']; ?>
                                                    </button>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            <?php }
                            if ($footer_row['admin_stripe_status'] == "Active") { ?>
                                <li>
                                    <div class="pay-full">
                                        <div class="rbbox">
                                            <input type="radio" id="paymentstripe"
                                                   name="payment" <?php if ($footer_row['admin_cod_status'] != "Active" && $footer_row['admin_paypal_status'] != "Active") {
                                                echo "checked='checked'";
                                            } ?>>
                                            <label for="paymentstripe"><?php echo $BIZBOOK['DB-PAYMENTS-STRIPE-PAYMENT-GATEWAY']; ?></label>
                                            <div class="pay-note">
                                                <span><i class="material-icons">star</i> <?php echo $BIZBOOK['DB-PAYMENTS-STRIPE-PAYMENT-GATEWAY-P-1']; ?></span>
                                                <span><i class="material-icons">star</i><?php echo $BIZBOOK['DB-PAYMENTS-WHAT-IS-STRIPE']; ?></span>
                                                <form name="stripe_dash_form" id="stripe_dash_form" method="post"
                                                      action="stripe_bypass_submit.php">
                                                    <input type="hidden" readonly="readonly"
                                                           class="form-control" name="stripe_dash_user_id"
                                                           value="<?php echo $_SESSION['user_id']; ?>"
                                                           placeholder="<?php echo $BIZBOOK['FULL_NAME'];  ?> *" required>

                                                    <h4><?php echo $BIZBOOK['DB-PAYMENTS-BILLING-DETAILS'];  ?></h4>
                                                    <ul>
                                                        <li>
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" readonly="readonly"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['first_name']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['FULL_NAME'];  ?> *" required>
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_country"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_country']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['COUNTRY'];  ?>">
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_state"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_state']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['STATE'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_city"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_city']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CITY'];  ?> *"
                                                                               required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-12">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_address"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_address']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['VILLAGE_STREET_NAME'];  ?>">
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_zip_code"
                                                                               onkeypress="return isNumber(event)"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_zip_code']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['POSTCODE_ZIP'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_name"
                                                                               value="<?php echo $user_details_row['user_contact_name']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_PERSON'];  ?> *" required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_mobile"
                                                                               onkeypress="return isNumber(event)"
                                                                               value="<?php echo $user_details_row['user_contact_mobile']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_PHONE_NUMBER'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_email"
                                                                               value="<?php echo $user_details_row['user_contact_email']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_EMAIL_ID'];  ?>" required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                        </li>
                                                    </ul>
                                                    <button type="submit" name="stripe_dash_form_submit"
                                                            class="db-pro-bot-btn">
                                                        <?php echo $BIZBOOK['DB-PAYMENTS-START-PAYMENT']; ?>
                                                    </button>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            <?php } ?>
                            <?php if ($footer_row['admin_razor_pay_status'] == "Active") { ?>
                                <li>
                                    <div class="pay-full">
                                        <div class="rbbox">
                                            <input type="radio" id="payment_razor_pay"
                                                   name="payment" <?php if ($footer_row['admin_cod_status'] != "Active" && $footer_row['admin_paypal_status'] != "Active" && $footer_row['admin_stripe_status'] != "Active") {
                                                echo "checked='checked'";
                                            } ?>>
                                            <label for="payment_razor_pay"><?php echo $BIZBOOK['DB-PAYMENTS-RAZOR-PAYMENT-GATEWAY']; ?></label>
                                            <div class="pay-note">
                                                <span><i class="material-icons">star</i> <?php echo $BIZBOOK['DB-PAYMENTS-RAZOR-PAYMENT-GATEWAY-P-1']; ?></span>
                                                <span><i class="material-icons">star</i><?php echo $BIZBOOK['DB-PAYMENTS-WHAT-IS-RAZOR']; ?></span>
                                                <form name="razor_pay_dash_form" id="razor_pay_dash_form" method="post"
                                                      action="razor_pay_bypass_submit.php">
                                                    <input type="hidden" readonly="readonly"
                                                           class="form-control" name="razor_pay_dash_user_id"
                                                           value="<?php echo $_SESSION['user_id']; ?>"
                                                           placeholder="<?php echo $BIZBOOK['FULL_NAME'];  ?> *" required>

                                                    <h4><?php echo $BIZBOOK['DB-PAYMENTS-BILLING-DETAILS'];  ?></h4>
                                                    <ul>
                                                        <li>
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" readonly="readonly"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['first_name']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['FULL_NAME'];  ?> *" required>
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_country"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_country']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['COUNTRY'];  ?>">
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_state"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_state']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['STATE'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_city"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_city']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CITY'];  ?> *"
                                                                               required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-12">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_address"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_address']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['VILLAGE_STREET_NAME'];  ?>">
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_zip_code"
                                                                               onkeypress="return isNumber(event)"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_zip_code']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['POSTCODE_ZIP'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_name"
                                                                               value="<?php echo $user_details_row['user_contact_name']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_PERSON'];  ?> *" required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_mobile"
                                                                               onkeypress="return isNumber(event)"
                                                                               value="<?php echo $user_details_row['user_contact_mobile']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_PHONE_NUMBER'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_email"
                                                                               value="<?php echo $user_details_row['user_contact_email']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_EMAIL_ID'];  ?>" required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                        </li>
                                                    </ul>
                                                    <button type="submit" name="razor_pay_dash_form_submit"
                                                            class="db-pro-bot-btn">
                                                        <?php echo $BIZBOOK['DB-PAYMENTS-START-PAYMENT']; ?>
                                                    </button>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            <?php } ?>
                            <?php if ($footer_row['admin_paytm_status'] == "Active") { ?>
                                <li>
                                    <div class="pay-full">
                                        <div class="rbbox">
                                            <input type="radio" id="payment_paytm"
                                                   name="payment" <?php if ($footer_row['admin_cod_status'] != "Active" && $footer_row['admin_paypal_status'] != "Active" && $footer_row['admin_stripe_status'] != "Active" && $footer_row['admin_razor_pay_status'] != "Active") {
                                                echo "checked='checked'";
                                            } ?>>
                                            <label for="payment_paytm"><?php echo $BIZBOOK['DB-PAYMENTS-PAYTM-PAYMENT-GATEWAY']; ?></label>
                                            <div class="pay-note">
                                                <span><i class="material-icons">star</i> <?php echo $BIZBOOK['DB-PAYMENTS-PAYTM-PAYMENT-GATEWAY-P-1']; ?></span>
                                                <span><i class="material-icons">star</i><?php echo $BIZBOOK['DB-PAYMENTS-PAYTM-IS-RAZOR']; ?></span>
                                                <form name="paytm_dash_form" id="paytm_dash_form" method="post"
                                                      action="paytm_bypass_submit.php">
                                                    <input type="hidden" readonly="readonly"
                                                           class="form-control" name="paytm_dash_user_id"
                                                           value="<?php echo $_SESSION['user_id']; ?>"
                                                           placeholder="<?php echo $BIZBOOK['FULL_NAME'];  ?> *" required>

                                                    <h4><?php echo $BIZBOOK['DB-PAYMENTS-BILLING-DETAILS'];  ?></h4>
                                                    <ul>
                                                        <li>
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" readonly="readonly"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['first_name']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['FULL_NAME'];  ?> *" required>
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_country"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_country']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['COUNTRY'];  ?>">
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_state"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_state']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['STATE'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_city"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_city']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CITY'];  ?> *"
                                                                               required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-12">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_address"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_address']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['VILLAGE_STREET_NAME'];  ?>">
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" name="user_zip_code"
                                                                               onkeypress="return isNumber(event)"
                                                                               class="form-control"
                                                                               value="<?php echo $user_details_row['user_zip_code']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['POSTCODE_ZIP'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_name"
                                                                               value="<?php echo $user_details_row['user_contact_name']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_PERSON'];  ?> *" required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                            <!--                                                    FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_mobile"
                                                                               onkeypress="return isNumber(event)"
                                                                               value="<?php echo $user_details_row['user_contact_mobile']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_PHONE_NUMBER'];  ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-6">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               name="user_contact_email"
                                                                               value="<?php echo $user_details_row['user_contact_email']; ?>"
                                                                               placeholder="<?php echo $BIZBOOK['CONTACT_EMAIL_ID'];  ?>" required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!--                                                    FILED END-->
                                                        </li>
                                                    </ul>
                                                    <button type="submit" name="paytm_dash_form_submit"
                                                            class="db-pro-bot-btn">
                                                        <?php echo $BIZBOOK['DB-PAYMENTS-START-PAYMENT']; ?>
                                                    </button>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            <?php } ?>
                        </ul>
                    </div>
                <?php }
            } ?>
            <div class="ud-notes">
                <p><b><?php echo $BIZBOOK['DB-PAYMENTS-FOOTER-NOTES'];?>:</b> <?php echo $BIZBOOK['DB-PAYMENTS-FOOTER-NOTES-MESSAGE'];?></p>
            </div>
        </div>
    </div>
<?php
include "dashboard_right_pane.php";
?>