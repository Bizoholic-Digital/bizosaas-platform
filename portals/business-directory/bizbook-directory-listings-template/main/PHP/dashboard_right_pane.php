<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */
$session_user_id = $_SESSION['user_id'];


?>
<!--RIGHT SECTION-->
<div class="ud-rhs">
    <?php
    if ($user_details_row['user_type'] == 'Service provider') {
        ?>
        <div class="ud-rhs-promo">
            <h3><?php echo $BIZBOOK['PROMOTE_MY_BUSINESS']; ?></h3>
            <p><?php echo $BIZBOOK['PROMOTE_MY_BUSINESS_P_TAG']; ?></p>
            <a href="<?php echo $webpage_full_link; ?>promote-business"><?php echo $BIZBOOK['PROMOTE_MY_BUSINESS_START_NOW']; ?></a>
        </div>
        <!--    //Total Point Section Starts-->
        <div class="ud-rhs-poin">
            <div class="ud-rhs-poin1">
                <h4><?php echo $BIZBOOK['YOUR_POINTS']; ?></h4>
                <span class="count1"><?php echo $user_details_row['user_points']; ?></span>
            </div>
            <div class="ud-rhs-poin2">
                <h3><?php echo $BIZBOOK['EARN_MORE_CREDIT_POINTS']; ?></h3>
                <p><?php echo $BIZBOOK['EARN_MORE_CREDIT_POINTS_P_TAG']; ?> <a
                        href="#"><?php echo $BIZBOOK['PROMOTE_MY_BUSINESS_CLICK_HERE']; ?></a> <?php echo $BIZBOOK['PROMOTE_MY_BUSINESS_FOR_DEMO']; ?>
                </p>
                <a href="<?php echo $webpage_full_link; ?>buy-points" class="cta"><?php echo $BIZBOOK['BUY_POINTS']; ?></a>
            </div>
        </div>
        <!--    //Total Point Section Ends-->

        <div class="ud-rhs-pay">
            <div class="ud-rhs-pay-inn">
                <h3><?php echo $BIZBOOK['PAYMENT_INFORMATION']; ?></h3>
                <ul>
                    <li><b><?php echo $BIZBOOK['DASH_RIGHT_PLAN_NAME']; ?>
                            : </b> <?php if ($user_details_row['user_type'] == "Service provider") {
                            echo $user_plan_type['plan_type_name'];
                        } else {
                            echo "General User";
                        } ?></li>
                    <li><b><?php echo $BIZBOOK['DASH_RIGHT_START_DATE']; ?>
                            : </b> <?php if ($user_details_row['user_cdt'] == '0000-00-00 00:00:00') {
                            echo 'N/A';
                        } else {
                            echo dateFormatconverter($user_details_row['user_cdt']);
                        } ?></li>

                    <?php
                    //To calculate the expiry date from user created date starts

                    $start_date_timestamp = strtotime($user_details_row['user_cdt']);
                    $plan_type_duration = $user_plan_type['plan_type_duration'];

                    $expiry_date_timestamp = strtotime("+$plan_type_duration months", $start_date_timestamp);

                    $expiry_date = date("Y-m-d h:i:s", $expiry_date_timestamp);

                    //To calculate the expiry date from user created date ends
                    ?>

                    <li><b><?php echo $BIZBOOK['DASH_RIGHT_EXPIRY_DATE']; ?>
                            : </b> <?php if ($user_details_row['user_type'] == "Service provider") {
                            if ($user_details_row['user_cdt'] == '0000-00-00 00:00:00') {
                                echo 'N/A';
                            } else {
                                echo dateFormatconverter($expiry_date);
                            }
                        } else {
                            echo "Unlimited";
                        } ?></li>
                    <li><b><?php echo $BIZBOOK['DURATION']; ?> : </b> <?php
                        if ($user_details_row['user_type'] == "Service provider") {
                            if ($plan_type_duration >= 7) {
                                echo $plan_type_duration / 12 . ' ' . "year";
                            } else {
                                echo $plan_type_duration . ' ' . "month";
                            }
                        } else {
                            echo "Unlimited";
                        } ?></li>
                    <?php
                    //To calculate the remaining days from expiry date to current date starts

                    $start = strtotime($curDate);
                    $end = strtotime($expiry_date);
                    $days_between = ceil(abs($end - $start) / 86400);

                    //To calculate the remaining days from expiry date to current date ends
                    ?>

                    <li><b><?php echo $BIZBOOK['DASH_RIGHT_REMAINING_DAYS']; ?>: </b> <?php
                        if ($user_details_row['user_type'] == "Service provider") {
                            if ($user_details_row['payment_cdt'] == '0000-00-00 00:00:00') {
                                echo 'N/A';
                            } else {
                                echo $days_between;
                            }
                        } else {
                            echo "Unlimited";
                        } ?></li>
                    <li><span
                            class="ud-stat-pay-btn"><b><?php echo $BIZBOOK['DASH_RIGHT_CHECKOUT_COST']; ?>
                                :</b> <?php if ($user_plan_type['plan_type_price'] == 0) {
                                echo "FREE";
                            } else {
                                echo $footer_row['currency_symbol'] . '' . $user_plan_type['plan_type_price'];
                            } ?></span></li>
                    <li><span
                            class="ud-stat-pay-btn"><b><?php echo $BIZBOOK['DASH_RIGHT_PAYMENT_STATUS']; ?>:</b> <?php
                            if ($user_details_row['user_type'] == "Service provider") {
                                if ($user_details_row['payment_status'] == 'Paid') {
                                    echo "PAID";
                                } elseif ($user_details_row['payment_status'] == 'COD') {
                                    echo "Bank payment Initiated / Pending";
                                } elseif ($user_plan_type['plan_type_price'] == 0) {
                                    echo "N/A";
                                } else {
                                    echo "PENDING";
                                }
                            } else {
                                echo "NIL";
                            } ?></span></li>


                </ul>

                <?php
                if ($user_details_row['user_type'] == "Service provider") {
                    if ($user_plan_type['plan_type_id'] != 4) { ?>
                        <a href="<?php echo $webpage_full_link; ?>pricing-details"
                           class="btn btn1"><?php echo $BIZBOOK['DASH_RIGHT_CHANGE_MY_PLAN']; ?></a>
                        <?php
                    }
                    if ($user_details_row['payment_status'] != 'Paid' && $user_plan_type['plan_type_id'] != 1) { ?>
                        <a href="<?php echo $webpage_full_link; ?>db-payment" class="btn btn2"><?php echo $BIZBOOK['PAY_NOW']; ?></a>
                        <?php
                    }
                } else { ?> <a href="<?php echo $webpage_full_link; ?>pricing-details"
                               class="btn btn1"><?php echo $BIZBOOK['DASH_RIGHT_CHANGE_MY_PLAN']; ?></a> <?php }
                ?>
            </div>
        </div>
        <?php
    }
    ?>
    <?php
    if (getCountUserListing($_SESSION['user_id']) > 0) {
        ?>
    <?php if ($footer_row['admin_listing_show'] == 1 && $user_details_row['setting_listing_show'] == 1) { ?>
            <div class="ud-rhs-pay ud-rhs-status">
                <div class="ud-rhs-pay-inn">
                    <h3><?php echo $BIZBOOK['LISTING_OPEN_CLOSE_TITLE']; ?></h3>
                    <ul>
                        <?php
                        foreach (getAllListingUser($_SESSION['user_id']) as $list_switch_row) {
                            ?>
                            <li>
                                <span><?php echo $list_switch_row['listing_name']; ?></span>
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="listing_open_close_switch custom-control-input"
                                           id="<?php echo $list_switch_row['listing_id']; ?>" <?php if ($list_switch_row['listing_open'] == 1) {
                                        echo "checked";
                                    } ?>>
                                    <label class="custom-control-label"
                                           for="<?php echo $list_switch_row['listing_id']; ?>"
                                           data-toggle="tooltip"
                                           title="<?php echo $BIZBOOK['LISTING_OPEN_CLOSE_TITLE_POPUP']; ?>">
                                        &nbsp;</label>
                                </div>
                            </li>
                            <?php
                        }
                        ?>
                    </ul>
                </div>
            </div>
            <?php
        }
    }
    ?>
    <?php
    if ($user_details_row['user_type'] == 'Service provider') {
        ?>
        <div class="ud-rhs-pay ud-rhs-repo">
            <div class="ud-rhs-pay-inn">
                <h3><?php echo $BIZBOOK['LAST_WEEK_REPORT']; ?></h3>
                <ul>
                    <li>
                        <span class="view"><?php echo $BIZBOOK['ENQUIRY']; ?></span>
                    <span
                        class="cout"><?php echo AddingZero_BeforeNumber(getLastWeekCountUserEnquiries($_SESSION['user_id'])); ?></span>
                        <span class="name"><?php echo $BIZBOOK['LEADS']; ?></span>
                    </li>
                    <li>
                        <span class="view"><?php echo $BIZBOOK['VIEWS']; ?></span>
                    <span
                        class="cout"><?php echo AddingZero_BeforeNumber(last_week_all_listing_pageview_count($_SESSION['user_id'])); ?></span>
                        <span class="name"><?php echo $BIZBOOK['LISTING']; ?></span>
                    </li>
                    <li>
                        <span class="view"><?php echo $BIZBOOK['VIEWS']; ?></span>
                    <span
                        class="cout"><?php echo AddingZero_BeforeNumber(last_week_all_event_pageview_count($_SESSION['user_id'])); ?></span>
                        <span class="name"><?php echo $BIZBOOK['EVENTS']; ?></span>
                    </li>
                    <li>
                        <span class="view"><?php echo $BIZBOOK['VIEWS']; ?></span>
                    <span
                        class="cout"><?php echo AddingZero_BeforeNumber(last_week_all_blog_pageview_count($_SESSION['user_id'])); ?></span>
                        <span class="name"><?php echo $BIZBOOK['BLOGS']; ?></span>
                    </li>
                    <li>
                        <span class="view"><?php echo $BIZBOOK['VIEWS']; ?></span>
                    <span
                        class="cout"><?php echo AddingZero_BeforeNumber(last_week_all_product_pageview_count($_SESSION['user_id'])); ?></span>
                        <span class="name"><?php echo $BIZBOOK['PRODUCTS']; ?></span>
                    </li>
                    <li>
                    <span
                        class="cout"><?php echo AddingZero_BeforeNumber(last_week_all_messages_count($_SESSION['user_id'])); ?></span>
                        <span class="name"><?php echo $BIZBOOK['MESSAGES']; ?></span>
                    </li>
                </ul>
            </div>
        </div>
        <?php
    }
    ?>
    <div class="ud-rhs-sec-1">
        <h4><?php echo $BIZBOOK['ADMIN_NOTIFICATION']; ?></h4>
        <ul>
            <?php
            if ($user_details_row['user_type'] == 'Service provider') {
                $user_type_id = 101;
            } else {
                $user_type_id = 102;
            }
            if ($user_plan_type['plan_type_id'] != NULL || !empty($user_plan_type['plan_type_id'])) {
                $plan_type_id = $user_plan_type['plan_type_id'];
            } else {
                $plan_type_id = 0;
            }

            foreach (getAllUserNotification($user_type_id, $plan_type_id) as $notificationrow) {
                ?>
                <li>
                    <a target="_blank" href="<?php echo $notificationrow['notification_link']; ?>">
                        <h5><?php echo $notificationrow['notification_title']; ?></h5>
                        <p><?php echo $notificationrow['notification_message']; ?></p>
                    </a>
                </li>
                <?php
            }
            ?>
        </ul>
    </div>
    <div class="ud-rhs-promo ud-rhs-promo-1">
        <h3><?php echo $BIZBOOK['COMMUNITY_MEMBERS']; ?></h3>
        <p><?php echo $BIZBOOK['COMMUNITY_MEMBERS_TITLE']; ?></p>
        <a href="<?php echo $webpage_full_link; ?>community"><?php echo $BIZBOOK['COMMUNITY']; ?></a>
    </div>
    <div class="ud-rhs-sec-3">
        <div class="list-mig-like">
            <div class="list-ri-peo-like">
                <h3><?php echo $BIZBOOK['WHO_ALL_FOLLOW_YOU']; ?></h3>
                <ul>
                    <?php
                    $user_followers_array = explode(",", $user_details_row['user_followers']);
                    foreach ($user_followers_array as $user_followers) {
                        $user_followers_row = getUser($user_followers); // To Fetch particular User Data
                        ?>
                        <li>
                            <a href="<?php echo $PROFILE_URL . urlModifier($user_followers_row['user_slug']); ?>"
                               target="_blank">
                                <img
                                    src="<?php echo $slash; ?>images/user/<?php if (($user_followers_row['profile_image'] == NULL) || empty($user_followers_row['profile_image'])) {
                                        echo $footer_row['user_default_image'];
                                    } else {
                                        echo $user_followers_row['profile_image'];
                                    } ?>" alt="">
                            </a>
                        </li>
                        <?php
                    }
                    ?>
                </ul>
            </div>
        </div>
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
<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script src="<?php echo $slash; ?>js/select-opt.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>
<script>
    $('.listing_open_close_switch').click(function () {
        var idd = $(this).attr('id');  //-->this will alert id of checked checkbox.
        if (this.checked) {
            var new1 = 1;
        } else {
            var new1 = 0;
        }
        $.ajax({
            type: "POST",
            url: '<?php echo $slash; ?>update_listing_open.php',
            data: {idd: idd, value1: new1}, //--> send data of checked checkbox on other page
            success: function (data) {
                //alert(data);
            },
            error: function () {
                alert('it broke');
            }
        });


    });
</script>
</body>

</html>