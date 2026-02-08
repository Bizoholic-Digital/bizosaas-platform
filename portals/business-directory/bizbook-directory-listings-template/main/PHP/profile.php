<?php
include "header.php";

if (isset($_SESSION['user_id'])) {
    $session_user_id = $_SESSION['user_id'];
}

$user_details_row = getUser($session_user_id);

$redirect_url = $webpage_full_link . 'dashboard';  //Redirect Url

if ($_GET['code'] == NULL && empty($_GET['code'])) {

    header("Location: $redirect_url");  //Redirect When code parameter is empty
}

//$user_codea = $_GET['code'];
$user_codea1 = str_replace('-', ' ', $_GET['code']);
$user_codea = str_replace('.php', '', $user_codea1);

$usersqlrow = getActiveUser($user_codea); // To Fetch particular User Data

if ($usersqlrow['user_id'] == NULL && empty($usersqlrow['user_id'])) {

    header("Location: $redirect_url");  //Redirect When No User Found in Table
}

$setting_user_status = $usersqlrow['setting_user_status'];

if ($setting_user_status == 1) {

    header("Location: $redirect_url");  //To Check whether listing owner made profile account Inactive
}

$profile_user_id = $usersqlrow['user_id'];

?>

<!-- START -->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?>">
    <div class="job-prof-pg defa-prof-pg">
        <div class="container">
            <div class="row">
                <div class="lhs">
                    <!--START-->
                    <div class="profile">
                        <div class="jpro-ban-bg-img">
                            <span><b><?php echo getCountUserFollowing($profile_user_id); ?></b> <?php echo $BIZBOOK['FOLLOWINGS']; ?></span>
                            <p><?php echo $BIZBOOK['JOIN_ON']; ?>:
                                <b><?php echo dateFormatconverter($usersqlrow['user_cdt']) ?></b></p>
                            <img src="<?php echo $slash; if (($usersqlrow['cover_image'] == NULL) || empty($usersqlrow['cover_image'])) {
                                echo "images/home4.jpg";
                            } else { ?>images/user/<?php echo $usersqlrow['cover_image'];  } ?>" alt="">
                        </div>
                        <div class="jpro-ban-tit">
                            <div class="s1">
                                <img
                                    src="<?php echo $slash; ?>images/user/<?php if (($usersqlrow['profile_image'] == NULL) || empty($usersqlrow['profile_image'])) {
                                        echo $footer_row['user_default_image'];
                                    } else {
                                        echo $usersqlrow['profile_image'];
                                    } ?>" class="pro" alt="">
                            </div>
                            <div class="s2">
                                <h1><?php echo $usersqlrow['first_name']; ?></h1>
                                <span class="loc"><b><?php echo $BIZBOOK['CITY']; ?>
                                        :</b> <?php echo $usersqlrow['user_city']; ?></span>
                                <p><?php echo getCountUserListing($profile_user_id); ?> <?php echo $BIZBOOK['LISTINGS']; ?>
                                    | <?php echo getCountUserBlog($profile_user_id); ?> <?php echo $BIZBOOK['BLOGS']; ?>
                                    | <?php echo getCountUserEvent($profile_user_id); ?> <?php echo $BIZBOOK['EVENTS']; ?></p>
                            </div>
                            <div class="s3">
                                <a href="mailto:<?php echo $usersqlrow['email_id']; ?>" class="cta fol" target="_blank">Message</a>
                                <span <?php
                                if ($session_user_id == NULL || empty($session_user_id)) {
                                    echo "disabled";
                                }
                                ?>
                                      class="cta userfollow follow-content<?php echo $profile_user_id ?>"
                                      data-item="<?php echo $profile_user_id; ?>"
                                      data-num="<?php echo $session_user_id; ?>">
                            <?php if (getCountUserProfileFollowing($session_user_id, $profile_user_id) == 0) {
                                echo $BIZBOOK['FOLLOW'];
                            } else {
                                echo $BIZBOOK['UN_FOLLOW'];
                            } ?></span>
                            </div>
                        </div>
                    </div>
                    <!--END-->
                    <!--START-->
                    <?php
                    if ($usersqlrow['user_facebook'] != NULL || $usersqlrow['user_twitter'] != NULL
                    || $usersqlrow['user_youtube'] != NULL || $usersqlrow['user_website'] != NULL) {
                        ?>
                        <div class="jb-pro-bio">
                            <h4><?php echo $BIZBOOK['FOOTER-SOCIAL-MEDIA']; ?></h4>
                            <ul class="pro-soci">
                                <?php
                                if ($usersqlrow['user_facebook'] != NULL) {
                                    ?>
                                    <li>
                                        <a target="_blank" href="<?php echo $usersqlrow['user_facebook']; ?>"><img
                                                src="<?php echo $slash; ?>images/social/3.png" alt=""></a>
                                    </li>
                                    <?php
                                }
                                if ($usersqlrow['user_twitter'] != NULL) {
                                    ?>
                                    <li>
                                        <a target="_blank" href="<?php echo $usersqlrow['user_twitter']; ?>"><img
                                                src="<?php echo $slash; ?>images/social/2.png" alt=""></a>
                                    </li>
                                    <?php
                                }
                                if ($usersqlrow['user_youtube'] != NULL) {
                                    ?>
                                    <li>
                                        <a target="_blank" href="<?php echo $usersqlrow['user_youtube']; ?>"><img
                                                src="<?php echo $slash; ?>images/social/5.png" alt=""></a>
                                    </li>
                                    <?php
                                }
                                if ($usersqlrow['user_website'] != NULL) {
                                    ?>
                                    <li>
                                        <a target="_blank" href="<?php echo $usersqlrow['user_website']; ?>"><img
                                                src="<?php echo $slash; ?>images/social/1.png" alt=""></a>
                                    </li>
                                    <?php
                                }
                                ?>
                            </ul>
                        </div>
                        <?php
                    }
                    ?>
                    <!--END-->
                    <!--START-->
                    <div class="jpro-bd">
                        <?php
                        if ($usersqlrow['user_type'] == "Service provider") {  //To Check User type is Service provider
                            ?>
                            <div class="jpro-bd-com">
                                <h4><?php echo $BIZBOOK['ALL_LISTING']; ?></h4>
                                <ul>
                                    <?php
                                    if (getCountUserListing($profile_user_id) == 0) {
                                        ?>
                                        <div class="log"><p><?php echo $BIZBOOK['NO_LISTINGS_TO_SHOW']; ?></p></div>
                                    <?php } else {

                                        foreach (getAllListingUser($profile_user_id) as $listrow) {

                                            $listing_id = $listrow['listing_id'];

                                            //  List Rating. for Rating of Star starts
                                            foreach (getListingReview($listing_id) as $Star_rateRow) {

                                                if ($Star_rateRow["rate_cnt"] > 0) {
                                                    $Star_rate_times = $Star_rateRow["rate_cnt"];
                                                    $Star_sum_rates = $Star_rateRow["total_rate"];
                                                    $star_rate_one = $Star_sum_rates / $Star_rate_times;
                                                    $star_rate_two = number_format($star_rate_one, 1);
                                                    $star_rate = floatval($star_rate_two);

                                                } else {
                                                    $rate_times = 0;
                                                    $rate_value = 0;
                                                    $star_rate = 0;
                                                }
                                            }
                                            //  List Rating. for Rating of Star Ends

                                            ?>
                                            <li>
                                                <div class="pro-listing-box">
                                                    <div>
                                                        <img
                                                            src="<?php if ($listrow['profile_image'] != NULL || !empty($listrow['profile_image'])) {
                                                                echo $slash . "images/listings/" . $listrow['profile_image'];
                                                            } else {
                                                                echo $slash . "images/listings/hot4.jpg";
                                                            } ?>">
                                                        <h2><?php echo $listrow['listing_name']; ?> </h2>
                                                        <?php
                                                        if ($star_rate != 0) {
                                                            ?>
                                                            <label class="rat">
                                                                <?php
                                                                for ($i = 1; $i <= ceil($star_rate); $i++) {
                                                                    ?>
                                                                    <i class="material-icons">star</i>
                                                                    <?php
                                                                }
                                                                $bal_star_rate = abs(ceil($star_rate) - 5);

                                                                for ($i = 1; $i <= $bal_star_rate; $i++) {
                                                                    ?>
                                                                    <i class="material-icons ratstar">star</i>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </label>
                                                            <?php
                                                        }
                                                        ?>
                                                        <p><?php echo $listrow['listing_address']; ?></p>
                                                        <a href="<?php echo $LISTING_URL . urlModifier($listrow['listing_slug']); ?>"
                                                           class="fclick">&nbsp;</a>
                                                    </div>
                                                    <div>
                                                    <span data-toggle="modal"
                                                          data-target="#quote"><?php echo $BIZBOOK['LEAD-GET-QUOTE']; ?></span>
                                                    </div>
                                                </div>
                                            </li>

                                            <div class="pop-ups pop-quo">
                                                <!-- The Modal -->
                                                <div class="modal fade" id="quote">
                                                    <div class="modal-dialog">
                                                        <div class="modal-content">
                                                            <button type="button" class="close"
                                                                    data-dismiss="modal">&times;</button>
                                                            <!-- Modal Header -->
                                                            <div class="quote-pop">
                                                                <h4><?php echo $BIZBOOK['LEAD-GET-QUOTE']; ?></h4>
                                                                <div id="profile_enq_success" class="log new-tnk-msg"
                                                                     style="display: none;">
                                                                    <p><?php echo $BIZBOOK['ENQUIRY_SUCCESSFUL_MESSAGE']; ?></p>
                                                                </div>
                                                                <div id="profile_enq_same" class="log"
                                                                     style="display: none;">
                                                                    <p><?php echo $BIZBOOK['ENQUIRY_OWN_LISTING_MESSAGE']; ?></p>
                                                                </div>
                                                                <div id="profile_enq_fail" class="log"
                                                                     style="display: none;">
                                                                    <p><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></p>
                                                                </div>
                                                                <form method="post" name="profile_enquiry_form"
                                                                      id="profile_enquiry_form">
                                                                    <input type="hidden" class="form-control"
                                                                           name="listing_id"
                                                                           value="<?php echo $listing_id ?>"
                                                                           placeholder=""
                                                                           required>
                                                                    <input type="hidden" class="form-control"
                                                                           name="listing_user_id"
                                                                           value="<?php echo $profile_user_id; ?>"
                                                                           placeholder="" required>
                                                                    <input type="hidden" class="form-control"
                                                                           name="enquiry_sender_id"
                                                                           value="<?php echo $session_user_id; ?>"
                                                                           placeholder="" required>
                                                                    <div class="form-group">
                                                                        <input type="text" readonly name="enquiry_name"
                                                                               value="<?php echo $user_details_row['first_name'] ?>"
                                                                               required="required" class="form-control"
                                                                               placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>">
                                                                    </div>
                                                                    <div class="form-group">
                                                                        <input type="email" class="form-control"
                                                                               placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>"
                                                                               readonly="readonly"
                                                                               value="<?php echo $user_details_row['email_id'] ?>"
                                                                               name="enquiry_email"
                                                                               pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                                                               title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>"
                                                                               required>
                                                                    </div>
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               readonly="readonly"
                                                                               value="<?php echo $user_details_row['mobile_number'] ?>"
                                                                               name="enquiry_mobile"
                                                                               placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>"
                                                                               pattern="[7-9]{1}[0-9]{9}"
                                                                               title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>"
                                                                               required>
                                                                    </div>
                                                                    <div class="form-group">
                                                                    <textarea class="form-control" rows="3"
                                                                              name="enquiry_message"
                                                                              placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                                                                    </div>
                                                                    <input type="hidden" id="source">
                                                                    <button type="submit" name="enquiry_submit"
                                                                            class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
                                                                </form>
                                                            </div>
                                                            <div class="log-bor">&nbsp;</div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>

                                            <?php
                                        }
                                    }
                                    ?>

                                </ul>

                            </div>
                            <div class="jpro-bd-com">
                                <h4><?php echo $BIZBOOK['BLOG_POSTS']; ?></h4>
                                <ul>
                                    <?php
                                    if (getCountUserBlog($profile_user_id) == 0) {
                                        ?>
                                        <div class="log"><p><?php echo $BIZBOOK['NO_BLOGS_TO_SHOW']; ?></p></div>
                                    <?php } else {
                                        foreach (getAllUserBlogs($profile_user_id) as $blogrow) { ?>
                                            <li>
                                                <div class="pro-eve-box">
                                                    <div>
                                                        <img
                                                            src="<?php echo $slash; ?>images/blogs/<?php echo $blogrow['blog_image']; ?>"
                                                            alt="">
                                                    </div>
                                                    <div>
                                                        <span><?php echo dateFormatconverter($blogrow['blog_cdt']); ?></span>
                                                        <h2><?php echo $blogrow['blog_name']; ?></h2>
                                                    </div>
                                                    <a href="<?php echo $BLOG_URL . urlModifier($blogrow['blog_slug']); ?>"
                                                       class="fclick">
                                                        &nbsp;</a>
                                                </div>
                                            </li>
                                        <?php }
                                    } ?>
                                </ul>

                            </div>
                            <div class="jpro-bd-com">
                                <h4><?php echo $BIZBOOK['EVENTS']; ?></h4>
                                <ul>
                                    <?php
                                    if (getCountUserEvent($profile_user_id) == 0) {
                                        ?>
                                        <div class="log"><p><?php echo $BIZBOOK['NO_EVENTS_TO_SHOW']; ?></p></div>
                                    <?php } else {

                                        foreach (getAllUserEvents($profile_user_id) as $eventrow) { ?>
                                            <li>
                                                <div class="pro-eve-box pro-eve-box1">
                                                    <div>
                                                        <img
                                                            src="<?php echo $slash; ?>images/events/<?php echo $eventrow['event_image']; ?>"
                                                            alt="">
                                                    </div>
                                                    <div>
                                                    <span><?php echo dateDayFormatconverter($eventrow['event_start_date']); ?>
                                                        <b><?php echo dateMonthFormatconverter($eventrow['event_start_date']); ?></b></span>
                                                        <h2><?php echo $eventrow['event_name']; ?></h2>
                                                        <p><?php echo $eventrow['event_address']; ?></p>
                                                    </div>
                                                    <a href="<?php echo $EVENT_URL . urlModifier($eventrow['event_slug']); ?>"
                                                       class="fclick">&nbsp;</a>
                                                </div>
                                            </li>
                                        <?php }
                                    } ?>
                                </ul>

                            </div>
                            <?php
                        }
                        ?>
                        <div class="jpro-bd-com">
                            <h4><?php echo $BIZBOOK['FOLLOWERS']; ?></h4>
                            <div class="ud-rhs-sec-2">
                                <ul>
                                    <?php
                                    if ($usersqlrow['user_followers'] == '') {
                                        ?>
                                        <div class="log"><p><?php echo $BIZBOOK['NO_FOLLOWERS_TO_SHOW']; ?></p></div>
                                    <?php } else {

                                        $user_followers_array = explode(",", $usersqlrow['user_followers']);
                                        foreach ($user_followers_array as $user_followers) {
                                            $user_followers_row = getUser($user_followers); // To Fetch particular User Data
                                            ?>
                                            <li>
                                                <div class="pro-sm-box">
                                                    <img
                                                        src="<?php echo $slash; ?>images/user/<?php if (($user_followers_row['profile_image'] == NULL) || empty($user_followers_row['profile_image'])) {
                                                            echo $footer_row['user_default_image'];
                                                        } else {
                                                            echo $user_followers_row['profile_image'];
                                                        } ?>" alt="">
                                                    <h5><?php echo $user_followers_row['first_name']; ?></h5>
                                                    <p><?php echo $BIZBOOK['CITY']; ?>: <b> <?php if ($user_followers_row['user_city'] == NULL) {
                                                                echo "N/A";
                                                            } else {
                                                                echo $user_followers_row['user_city'];
                                                            } ?></b></p>
                                                    <a href="<?php echo $PROFILE_URL . urlModifier($user_followers_row['user_slug']); ?>"></a>
                                                </div>
                                            </li>
                                            <?php
                                        }
                                    }
                                    ?>

                                </ul>

                            </div>
                        </div>
                        <div class="jpro-bd-com">
                            <h4><?php echo $BIZBOOK['SHARE_THIS_PROFILE']; ?></h4>
                            <div class="list-sh list-sh">
                                <span class="share-new" data-toggle="modal" data-target="#sharepop"><i class="material-icons">share</i> Share now</span>
                            </div>
                        </div>
                        <!--END-->
                    </div>
                </div>
                <div class="rhs">
                    <div class="ud-rhs-promo">
                        <h3><?php echo $BIZBOOK['PROFILE-PROMO-H3-TAG']; ?></h3>
                        <p><?php echo $BIZBOOK['PROFILE-PROMO-P-TAG']; ?></p>
                        <a href="<?php echo $slash; ?>login"><?php echo $BIZBOOK['JOB-PROFILE-A']; ?></a>
                    </div>
                    <div class="job-rel-pro">
                        <div class="hot-page2-hom-pre">
                            <h4><?php echo $BIZBOOK['JOB-RELATED-PROFILES']; ?></h4>
                            <ul>
                                <?php
                                foreach (getAllServiceUserExceptUserId($profile_user_id) as $related_user_details_row) {
                                    ?>
                                    <li>
                                        <div class="hot-page2-hom-pre-1">
                                            <img
                                                src="<?php echo $slash; ?>images/user/<?php if (($related_user_details_row['profile_image'] == NULL) || empty($related_user_details_row['profile_image'])) {
                                                    echo $footer_row['user_default_image'];
                                                } else {
                                                    echo $related_user_details_row['profile_image'];
                                                } ?>" alt="">
                                        </div>
                                        <div class="hot-page2-hom-pre-2">
                                            <h5><?php echo $related_user_details_row['first_name']; ?></h5>
                                            <span><?php echo $BIZBOOK['MEMBER_SINCE']; ?> <b><?php echo dateFormatconverter($related_user_details_row['user_cdt']) ?></b></span>
                                        </div>
                                        <a href="<?php echo $PROFILE_URL . urlModifier($related_user_details_row['user_slug']); ?>" class="fclick"></a>
                                    </li>
                                    <?php
                                }
                                ?>
                            </ul>
                        </div>
                    </div>
                    <div class="job-rel-pro">
                        <div class="hot-page2-hom-pre pmenu-spri">
                            <h4><?php echo $BIZBOOK['PROFILE-QUICK-ACCESS']; ?></h4>
                            <ul>
                                <li><a href="<?php echo $webpage_full_link; ?>all-category" class="act"><img
                                            src="<?php echo $slash; ?>images/icon/shop.png">
                                        <div class="qui-acc-short">
                                            <h5><?php echo $BIZBOOK['ALL_SERVICES']; ?></h5>
                                            <p><?php echo $BIZBOOK['PROFILE-QUICK-ACCESS-P-1']; ?></p>
                                            <span><?php echo $BIZBOOK['PROFILE-QUICK-ACCESS-SPAN-1']; ?></span>
                                        </div>

                                    </a></li>
                                <li><a href="<?php echo $webpage_full_link; ?>service-experts" class="act"><img
                                            src="<?php echo $slash; ?>images/icon/expert.png">
                                        <div class="qui-acc-short">
                                            <h5><?php echo $BIZBOOK['SERVICE-EXPERTS']; ?></h5>
                                            <p><?php echo $BIZBOOK['ALL-CATEGORY-MESSAGE']; ?></p>
                                            <span><?php echo $BIZBOOK['PROFILE-QUICK-ACCESS-SPAN-2']; ?></span>
                                        </div>

                                    </a></li>
                                <li><a href="<?php echo $webpage_full_link; ?>jobs" class="act"><img
                                            src="<?php echo $slash; ?>jobs/images/icon/employee.png">
                                        <div class="qui-acc-short">
                                            <h5> <?php echo $BIZBOOK['JOBS']; ?></h5>
                                            <p><?php echo $BIZBOOK['JOB-HEADER-H1']; ?></p>
                                            <span><?php echo $BIZBOOK['PROFILE-QUICK-ACCESS-SPAN-3']; ?></span>
                                        </div>
                                    </a></li>
                                <li><a href="<?php echo $webpage_full_link; ?>events"><img
                                            src="<?php echo $slash; ?>images/icon/calendar.png">
                                        <div class="qui-acc-short">
                                            <h5><?php echo $BIZBOOK['EVENTS']; ?></h5>
                                            <p><?php echo $BIZBOOK['PROFILE-QUICK-ACCESS-P-4']; ?></p>
                                            <span><?php echo $BIZBOOK['PROFILE-QUICK-ACCESS-SPAN-4']; ?></span>
                                        </div>
                                    </a></li>
                                <li><a href="<?php echo $webpage_full_link; ?>all-products"><img
                                            src="<?php echo $slash; ?>images/icon/cart.png">
                                        <div class="qui-acc-short">
                                            <h5><?php echo $BIZBOOK['PRODUCTS']; ?></h5>
                                            <p><?php echo $BIZBOOK['PROFILE-QUICK-ACCESS-P-5']; ?></p>
                                            <span><?php echo $BIZBOOK['PROFILE-QUICK-ACCESS-SPAN-5']; ?></span>
                                        </div>
                                    </a></li>
                                <li><a href="<?php echo $webpage_full_link; ?>coupons"><img
                                            src="<?php echo $slash; ?>images/icon/coupons.png">
                                        <div class="qui-acc-short">
                                            <h5><?php echo $BIZBOOK['COUPONS_AND_DEALS']; ?></h5>
                                            <p><?php echo $BIZBOOK['PROFILE-QUICK-ACCESS-P-6']; ?></p>
                                            <span><?php echo $BIZBOOK['PROFILE-QUICK-ACCESS-SPAN-6']; ?></span>
                                        </div>

                                    </a></li>
                                <li><a href="<?php echo $webpage_full_link; ?>blog-posts"><img
                                            src="<?php echo $slash; ?>images/icon/blog1.png">
                                        <div class="qui-acc-short">
                                            <h5> <?php echo $BIZBOOK['BLOGS']; ?></h5>
                                            <p><?php echo $BIZBOOK['PROFILE-QUICK-ACCESS-P-7']; ?></p>
                                            <span><?php echo $BIZBOOK['PROFILE-QUICK-ACCESS-SPAN-4']; ?></span>
                                        </div>

                                    </a></li>
                                <li><a href="<?php echo $webpage_full_link; ?>community"><img
                                            src="<?php echo $slash; ?>images/icon/11.png">
                                        <div class="qui-acc-short">
                                            <h5><?php echo $BIZBOOK['COMMUNITY']; ?></h5>
                                            <p><?php echo $BIZBOOK['COMMUNITY-PAGE-P-TAG']; ?></p>
                                            <span><?php echo $BIZBOOK['PROFILE-QUICK-ACCESS-SPAN-8']; ?></span>
                                        </div>

                                    </a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</section>
<!-- END -->


<!-- SHARE POPUP -->
<div class="modal fade sharepop" id="sharepop">
    <div class="modal-dialog modal-sm">
        <div class="modal-content">

            <!-- Modal Header -->
            <div class="modal-header">
                <h4 class="modal-title">Share now</h4>
                <button type="button" class="close" data-dismiss="modal">&times;</button>
            </div>

            <!-- Modal body -->
            <div class="modal-body">
                <input type="text" value="" id="shareurl">
                <div class="shareurltip">
                    <button onclick="shareurl()" onmouseout="shareurlout()">
                        <span class="shareurltxt" id="myTooltip">Copy to clipboard</span>
                        Copy text                    </button>
                </div>
            </div>

        </div>
    </div>
</div>

<?php
include "footer.php";
?>


<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>
<script>

    //
    <!-- Profile page Enquiry Form Ajax Call And Validation starts-->
    $(document).ready(function () {
        $("#profile_enquiry_form").validate({
            rules: {
                enquiry_name: {required: true},
                enquiry_email: {required: true, email: true},
                enquiry_mobile: {required: true}

            },
            messages: {

                enquiry_name: {required: "Name is Required"},
                enquiry_email: {required: "Email ID is Required"},
                enquiry_mobile: {required: "Mobile Number is Required"}
            },

            submitHandler: function (form) { // for demo
                //form.submit();
                $.ajax({
                    type: "POST",
                    data: $("#profile_enquiry_form").serialize(),
                    url: "<?php echo $slash; ?>enquiry_submit.php",
                    cache: true,
                    success: function (html) {
                        // alert(html);
                        if (html == 1) {
                            $("#profile_enq_success").show();
                            $("#profile_enquiry_form")[0].reset();
                        } else {
                            if (html == 3) {
                                $("#profile_enq_same").show();
                                $("#profile_enquiry_form")[0].reset();
                            } else {
                                $("#profile_enq_fail").show();
                                $("#profile_enquiry_form")[0].reset();
                            }
                        }

                    }

                })
            }
        });
    });
    <!--Profile page Enquiry Form Ajax Call And Validation ends-->

</script>

</body>

</html>