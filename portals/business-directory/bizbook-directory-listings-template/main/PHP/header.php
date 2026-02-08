<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if (file_exists('functions.php')) {
    include('functions.php');
}

$footer_row = getAllFooter(); //Fetch Footer Data

$admin_row = getAllSuperAdmin(); //Fetch Admin Data

$data_array['website_email_id'] = $footer_row['admin_primary_email'];
$data_array['admin_user_name'] = $admin_row['admin_email'];
$data_array['admin_user_password'] = $admin_row['admin_password'];

$all_texts_row = getAllTexts(); //Fetch All Text Data

if (isset($_SESSION['user_id'])) {

    $user_details_row = getUser($_SESSION['user_id']); //Fetch Logged In user data
    $user_plan = $user_details_row['user_plan']; //Fetch of Logged In user Plan

    $user_plan_type = getPlanType($user_plan); //Fetch Logged In User Plan details and data
    $session_user_id = $_SESSION['user_id'];
}

//Home page preview process
if (isset($_GET['preview']) && isset($_GET['q']) && isset($_GET['type']) && isset($_GET['query'])) {
    $current_home_page = $_GET['type']; //To set Homepage type.
} else {
    $current_home_page = $footer_row['admin_home_page']; //To set Homepage type.
}

?>
<!doctype html>
<html lang="en">

<head>
    <?php include('seo.php'); ?>
    <!--== FAV ICON(BROWSER TAB ICON) ==-->
    <link rel="shortcut icon" href="<?php echo $slash; ?>images/<?php echo $footer_row['home_page_fav_icon']; ?>"
          type="image/x-icon">
    <!--== GOOGLE FONTS ==-->
    <link href="https://fonts.googleapis.com/css?family=Oswald:700|Source+Sans+Pro:300,400,600,700&display=swap"
          rel="stylesheet">
    <!--== WEB ICON FONTS ==-->
    <link rel="preload" as="font" href="<?php echo $slash; ?>css/icon.woff2" type="font/woff2" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <!--== CSS FILES ==-->
    <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.0/themes/base/jquery-ui.css">
    <link rel="stylesheet" href="<?php echo $slash; ?>css/jquery-ui.css">
    <link rel="stylesheet" href="<?php echo $slash; ?>css/bootstrap.css">
    <link rel="stylesheet" type="text/css" href="<?php echo $slash; ?>css/theme-color.php">
    <link rel="stylesheet" type="text/css" href="<?php echo $slash; ?>css/style.css">
    <link rel="stylesheet" href="<?php echo $slash; ?>css/fonts.css">
    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
    <script src="<?php echo $slash; ?>js/html5shiv.js"></script>
    <script src="<?php echo $slash; ?>js/respond.min.js"></script>
    <![endif]-->

    <!--    Google Analytics Code Starts-->
    <?php echo stripslashes($footer_row['admin_google_analytics']); ?>
    <!--    Google Analytics Code Ends-->

</head>

<body>

<!--    Google Ad Sense Code Starts-->
<?php echo stripslashes($footer_row['admin_google_ad_sense']); ?>
<!--    Google Ad Sense Code Ends-->

<!-- Preloader -->
<div id="preloader">
    <div id="status">&nbsp;</div>
</div>

<!-- START -->
<section>
    <div class="str ind2-home">
        <?php if ($footer_row['admin_install_flag'] == 0) {
            kwohereza($SHYIRAMO);
        } ?>
        <div <?php if ($current_page == "index.php" || $current_page == "all-category.php") { ?> class="hom-head" style=" background-image: url(images/<?php echo $footer_row['home_page_banner']; ?>);" <?php } ?>>
            <div class="hom-top">
                <div class="container">
                    <div class="row">
                        <div class="hom-nav <?php if (!isset($_SESSION['user_name']) && empty($_SESSION['user_name'])) {
                        } else { ?> db-open <?php } ?>"><!--MOBILE MENU-->
                            <a href="<?php echo $webpage_full_link; ?>" class="top-log"><img
                                    src="<?php echo $slash; ?>images/home/<?php echo $footer_row['header_logo']; ?>"
                                    <?php if ($footer_row['header_logo_width'] != NULL || $footer_row['header_logo_height'] != NULL){ ?>style="<?php if ($footer_row['header_logo_width'] != NULL) { ?>width: <?php echo $footer_row['header_logo_width']; ?>; <?php }
                                    if ($footer_row['header_logo_height'] != NULL) { ?>height: <?php echo $footer_row['header_logo_height']; ?>;<?php } ?>"<?php } ?>
                                    alt="" class="ic-logo"></a>
                            <div class="menu">
                                <h4><?php echo $BIZBOOK['EXPLORE']; ?></h4>
                            </div>
                            <div class="pop-menu">
                                <div class="container">
                                    <div class="row">
                                        <i class="material-icons clopme">close</i>
                                        <div class="pmenu-spri">
                                            <ul>
                                                <?php if ($footer_row['admin_listing_show'] == 1) { ?>
                                                <li><a href="<?php echo $webpage_full_link; ?>all-category" class="act"><img
                                                            src="<?php echo $slash; ?>images/icon/shop.png"><?php echo $BIZBOOK['ALL_SERVICES']; ?>
                                                    </a></li>
                                                <?php }if ($footer_row['admin_expert_show'] == 1) { ?>
                                                <li><a href="<?php echo $webpage_full_link; ?>service-experts"
                                                       class="act"><img
                                                            src="<?php echo $slash; ?>images/icon/expert.png"><?php echo $BIZBOOK['SERVICE-EXPERTS']; ?>
                                                    </a></li>
                                                <?php }if ($footer_row['admin_job_show'] == 1) { ?>
                                                <li><a href="<?php echo $webpage_full_link; ?>jobs" class="act"><img
                                                            src="<?php echo $slash; ?>images/icon/employee.png"><?php echo $BIZBOOK['JOBS']; ?>
                                                    </a></li>
                                                <?php }if ($footer_row['admin_place_show'] == 1) { ?>
                                                <li><a href="<?php echo $webpage_full_link; ?>places" class="act"><img
                                                            src="<?php echo $slash; ?>images/places/icons/hot-air-balloon.png"><?php echo $BIZBOOK['PLACE-MENU']; ?>
                                                    </a></li>
                                                <?php }if ($footer_row['admin_news_show'] == 1) { ?>
                                                <li><a href="<?php echo $webpage_full_link; ?>news"><img
                                                            src="<?php echo $slash; ?>images/icon/news.png"><?php echo $BIZBOOK['NEWS-MAGA']; ?>
                                                    </a></li>
                                                <?php }if ($footer_row['admin_event_show'] == 1) { ?>
                                                <li><a href="<?php echo $webpage_full_link; ?>events"><img
                                                            src="<?php echo $slash; ?>images/icon/calendar.png"><?php echo $BIZBOOK['EVENTS']; ?>
                                                    </a></li>
                                                <?php }if ($footer_row['admin_product_show'] == 1) { ?>
                                                <li><a href="<?php echo $webpage_full_link; ?>all-products"><img
                                                            src="<?php echo $slash; ?>images/icon/cart.png"><?php echo $BIZBOOK['PRODUCTS']; ?>
                                                    </a></li>
                                                <?php }if ($footer_row['admin_coupon_show'] == 1) { ?>
                                                <li><a href="<?php echo $webpage_full_link; ?>coupons"><img
                                                            src="<?php echo $slash; ?>images/icon/coupons.png"><?php echo $BIZBOOK['COUPONS_AND_DEALS']; ?>
                                                    </a></li>
                                                <?php }if ($footer_row['admin_blog_show'] == 1) { ?>
                                                <li><a href="<?php echo $webpage_full_link; ?>blog-posts"><img
                                                            src="<?php echo $slash; ?>images/icon/blog1.png"><?php echo $BIZBOOK['BLOGS']; ?>
                                                    </a></li>
                                                <?php }?>
                                                <li><a href="<?php echo $webpage_full_link; ?>community"><img
                                                            src="<?php echo $slash; ?>images/icon/11.png"><?php echo $BIZBOOK['COMMUNITY']; ?>
                                                    </a></li>
                                            </ul>
                                        </div>
                                        <div class="pmenu-cat">
                                            <h4><?php echo $BIZBOOK['ALL_CATEGORIES']; ?></h4>
                                            <input type="text" id="pg-sear" placeholder="Search category">
                                            <ul id="pg-resu">
                                                <?php
                                                foreach (getAllCategoriesPos() as $category_row) {

                                                    ?>
                                                    <li>
                                                        <a href="<?php echo $ALL_LISTING_URL . urlModifier($category_row['category_slug']); ?>"><?php echo $category_row['category_name']; ?> -<span><?php echo AddingZero_BeforeNumber(getCountCategoryListing($category_row['category_id'])); ?></span></a>
                                                    </li>
                                                    <?php
                                                }
                                                ?>
                                            </ul>
                                        </div>
                                        <div class="dir-home-nav-bot">
                                            <ul>
                                                <li><?php echo $BIZBOOK['HOM-FEW-REASON-LOVE']; ?>
                                                    <span><?php echo $BIZBOOK['HOM-CALL-US-ON']; ?></span></li>
                                                <li><a href="<?php echo $webpage_full_link; ?>post-your-ads"
                                                       class="waves-effect waves-light btn-large"><i
                                                            class="material-icons">font_download</i> <?php echo $BIZBOOK['POST_ADS']; ?>
                                                    </a>
                                                </li>
                                                <li><a href="<?php echo $webpage_full_link; ?>pricing-details"
                                                       class="waves-effect waves-light btn-large"> <i
                                                            class="material-icons">store</i> <?php echo $BIZBOOK['HOM-HOW-P-TIT-2']; ?>
                                                    </a>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!--END MOBILE MENU-->

                            <div class="top-ser">
                                <form name="filter_form" id="filter_form" class="filter_form">
                                    <ul>
                                        <li class="sr-sea">
                                            <input type="text" autocomplete="off" id="top-select-search"
                                                   placeholder="<?php echo $BIZBOOK['SEARCHBOX_LABEL']; ?>">
                                            <ul id="tser-res1" class="tser-res tser-res2">
                                                <?php
                                                foreach (getAllSearch() as $search_row) {
                                                    ?>
                                                    <li>
                                                        <div>
                                                            <h4><?php echo $search_row['search_title']; ?></h4>
                                                            <span><?php echo $search_row['search_tag_line']; ?></span>
                                                            <a href="<?php echo $search_row['search_list_link']; ?>"></a>
                                                        </div>
                                                    </li>
                                                    <?php
                                                }
                                                ?>
                                            </ul>
                                        </li>

                                        <li class="sbtn">
                                            <button type="button" class="btn btn-success" id="top_filter_submit"><i
                                                    class="material-icons">&nbsp;</i></button>
                                        </li>
                                    </ul>
                                </form>
                            </div>
                            <?php
                            if (!isset($_SESSION['user_name']) && empty($_SESSION['user_name'])) {
                                ?>
                                <ul class="bl">
                                    <li>
                                        <a href="<?php echo $webpage_full_link; ?>pricing-details"><?php echo $BIZBOOK['ADD_BUSINESS']; ?></a>
                                    </li>
                                    <li>
                                        <a href="<?php echo $webpage_full_link; ?>login"><?php echo $BIZBOOK['SIGN_IN']; ?></a>
                                    </li>
                                    <li>
                                        <a href="<?php echo $webpage_full_link; ?>login?login=register"><?php echo $BIZBOOK['CREATE_AN_ACCOUNT']; ?></a>
                                    </li>
                                </ul>
                                <?php
                            } else {
                                include("top-notifications.php");
                                ?>
                                <div class="al">
                                    <div class="head-pro">
                                        <img
                                            src="<?php echo $slash; ?>images/user/<?php if (($user_details_row['profile_image'] == NULL) || empty($user_details_row['profile_image'])) {
                                                echo $footer_row['user_default_image'];
                                            } else {
                                                echo $user_details_row['profile_image'];
                                            } ?>" alt="User" title="Go to dashboard">
                                        <span class="fclick near-pro-cta"></span>
                                    </div>
                                    <div class="db-menu">
                                        <span class="material-icons db-menu-clo">close</span>
                                        <div class="ud-lhs-s1">
                                            <img
                                                src="<?php echo $slash; ?>images/user/<?php if (($user_details_row['profile_image'] == NULL) || empty($user_details_row['profile_image'])) {
                                                    echo $footer_row['user_default_image'];
                                                } else {
                                                    echo $user_details_row['profile_image'];
                                                } ?>" alt="">
                                            <div class="ud-lhs-pro-bio">    
                                            <h4><?php echo $user_details_row['first_name']; ?></h4>
                                            <b><?php echo $BIZBOOK['JOIN_ON']; ?><?php echo dateFormatconverter($user_details_row['user_cdt']) ?></b>
                                            <a class="ud-lhs-view-pro" target="_blank"
                                               href="<?php echo $PROFILE_URL . urlModifier($user_details_row['user_slug']); ?>"><?php echo $BIZBOOK['MY_PROFILE']; ?></a>
                                            </div>   
                                        </div>
                                        <ul>
                                            <li>
                                                <a href="<?php echo $slash; ?>dashboard"
                                                   class="<?php if ($current_page == "dashboard.php") {
                                                       echo "db-lact";
                                                   } ?>"><img src="<?php echo $slash; ?>images/icon/dbl1.png"
                                                              alt=""/> <?php echo $BIZBOOK['MY_DASHBOARD']; ?></a>
                                            </li>
                                            <?php
                                            if ($user_details_row['user_type'] == "Service provider") {  //To Check User type is Service provider
                                                ?>
                                                <?php if ($footer_row['admin_listing_show'] == 1 && $user_details_row['setting_listing_show'] == 1) { ?>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>db-all-listing"
                                                           class="<?php if ($current_page == "db-all-listing.php") {
                                                               echo "db-lact";
                                                           } ?>"><img src="<?php echo $slash; ?>images/icon/shop.png"
                                                                      alt=""/><?php echo $BIZBOOK['ALL_LISTING']; ?></a>
                                                    </li>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>add-listing-start"><img
                                                                src="<?php echo $slash; ?>images/icon/dbl3.png"
                                                                alt=""/><?php echo $BIZBOOK['ADD_NEW_LISTING']; ?>
                                                        </a>
                                                    </li>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>db-enquiry"
                                                           class="<?php if ($current_page == "db-enquiry.php") {
                                                               echo "db-lact";
                                                           } ?>"><img src="<?php echo $slash; ?>images/icon/tick.png"
                                                                      alt=""/><?php echo $BIZBOOK['LEAD_ENQUIRY']; ?>
                                                        </a>
                                                    </li>
                                                <?php } ?>
                                                <?php if ($footer_row['admin_job_show'] == 1 && $user_details_row['setting_job_show'] == 1) { ?>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>jobs/db-jobs"
                                                           class="<?php if ($current_page == "db-jobs.php") {
                                                               echo "db-lact";
                                                           } ?>"><img
                                                                src="<?php echo $slash; ?>jobs/images/icon/employee.png"
                                                                alt=""/><?php echo $BIZBOOK['JOBS']; ?></a>
                                                    </li>
                                                <?php } ?>
                                                <?php if ($footer_row['admin_product_show'] == 1 && $user_details_row['setting_product_show'] == 1) { ?>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>db-products"
                                                           class="<?php if ($current_page == "db-products.php") {
                                                               echo "db-lact";
                                                           } ?>"><img src="<?php echo $slash; ?>images/icon/cart.png"
                                                                      alt=""/><?php echo $BIZBOOK['ALL_PRODUCTS']; ?>
                                                        </a>
                                                    </li>
                                                <?php } ?>
                                                <?php if ($footer_row['admin_event_show'] == 1 && $user_details_row['setting_event_show'] == 1) { ?>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>db-events"
                                                           class="<?php if ($current_page == "db-events.php") {
                                                               echo "db-lact";
                                                           } ?>"><img
                                                                src="<?php echo $slash; ?>images/icon/calendar.png"
                                                                alt=""/><?php echo $BIZBOOK['EVENTS']; ?></a>
                                                    </li>
                                                <?php } ?>
                                                <?php if ($footer_row['admin_blog_show'] == 1 && $user_details_row['setting_blog_show'] == 1) { ?>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>db-blog-posts"
                                                           class="<?php if ($current_page == "db-blog-posts.php") {
                                                               echo "db-lact";
                                                           } ?>"><img src="<?php echo $slash; ?>images/icon/blog1.png"
                                                                      alt=""/><?php echo $BIZBOOK['BLOG_POSTS']; ?></a>
                                                    </li>
                                                <?php } ?>
                                                <?php if ($footer_row['admin_expert_show'] == 1 && $user_details_row['setting_expert_show'] == 1) { ?>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>service-experts/create-service-expert-profile"
                                                           class="<?php if ($current_page == "create-service-expert-profile.php") {
                                                               echo "db-lact";
                                                           } ?>"><img src="<?php echo $slash; ?>images/icon/profile.png"
                                                                      alt=""/><?php echo $BIZBOOK['ADD_NEW_SERVICE_EXPERT']; ?>
                                                        </a>
                                                    </li>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>service-experts/db-service-expert"
                                                           class="<?php if ($current_page == "db-service-expert.php") {
                                                               echo "db-lact";
                                                           } ?>"><img
                                                                src="<?php echo $slash; ?>images/icon/expert.png"
                                                                alt=""/><?php echo $BIZBOOK['ALL_SERVICE_EXPERT_LEADS']; ?>
                                                        </a>
                                                    </li>
                                                <?php } ?>
                                                <?php if ($footer_row['admin_coupon_show'] == 1 && $user_details_row['setting_coupon_show'] == 1) { ?>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>db-coupons"
                                                           class="<?php if ($current_page == "db-coupons.php") {
                                                               echo "db-lact";
                                                           } ?>"><img src="<?php echo $slash; ?>images/icon/coupons.png"
                                                                      alt=""/><?php echo $BIZBOOK['COUPONS']; ?></a>
                                                    </li>
                                                <?php } ?>
                                                <li>
                                                    <a href="<?php echo $slash; ?>db-promote"
                                                       class="<?php if ($current_page == "db-promote.php") {
                                                           echo "db-lact";
                                                       } ?>"><img src="<?php echo $slash; ?>images/icon/promotion.png"
                                                                  alt=""/><?php echo $BIZBOOK['PROMOTIONS']; ?></a>
                                                </li>
                                                <li>
                                                    <a href="<?php echo $slash; ?>db-seo"
                                                       class="<?php if ($current_page == "db-seo.php") {
                                                           echo "db-lact";
                                                       } ?>"><img src="<?php echo $slash; ?>images/icon/seo.png"
                                                                  alt=""/><?php echo $BIZBOOK['SEO']; ?></a>
                                                </li>
                                                <li>
                                                    <a href="<?php echo $slash; ?>db-point-history"
                                                       class="<?php if ($current_page == "db-point-history.php") {
                                                           echo "db-lact";
                                                       } ?>"><img src="<?php echo $slash; ?>images/icon/point.png"
                                                                  alt=""/><?php echo $BIZBOOK['POINTS_HISTORY']; ?></a>
                                                </li>
                                                <?php
                                            }
                                            ?>

                                            <li>
                                                <a href="<?php echo $slash; ?>db-my-profile"
                                                   class="<?php if ($current_page == "db-my-profile.php" || $current_page == "db-my-profile-edit") {
                                                       echo "db-lact";
                                                   } ?>"><img src="<?php echo $slash; ?>images/icon/profile.png"
                                                              alt=""/><?php echo $BIZBOOK['MY_PROFILE']; ?></a>
                                            </li>
                                            <?php if ($footer_row['admin_job_show'] == 1 && $user_details_row['setting_job_show'] == 1) { ?>
                                            <li>
                                                <a href="<?php echo $slash; ?>jobs/create-job-seeker-profile"
                                                   class="<?php if ($current_page == "create-job-seeker-profile.php") {
                                                       echo "db-lact";
                                                   } ?>"><img src="<?php echo $slash; ?>images/icon/profile.png"
                                                              alt=""/><?php echo $BIZBOOK['PROFI_JOB_SEEKER_TIT']; ?>
                                                </a>
                                            </li>
                                            <li>
                                                <a href="<?php echo $slash; ?>jobs/db-user-applied-jobs"><img
                                                        src="<?php echo $slash; ?>images/icon/job-apply.png"
                                                        alt=""/><?php echo $BIZBOOK['ALL_APPLIED_JOBS']; ?></a>
                                            </li>
                                            <?php } if ($footer_row['admin_expert_show'] == 1 && $user_details_row['setting_expert_show'] == 1) { ?>
                                            <li>
                                                <a href="<?php echo $slash; ?>service-experts/db-my-service-bookings"
                                                   class="<?php if ($current_page == "db-my-service-bookings.php") {
                                                       echo "db-lact";
                                                   } ?>"><img
                                                        src="<?php echo $slash; ?>images/icon/expert-book.png"
                                                        alt=""/><?php echo $BIZBOOK['MY_SERVICE_BOOKINGS']; ?></a>
                                            </li>
                                            <?php } if ($footer_row['admin_listing_show'] == 1 && $user_details_row['setting_listing_show'] == 1) { ?>
                                            <li>
                                                <a href="<?php echo $slash; ?>db-review"
                                                   class="<?php if ($current_page == "db-review.php") {
                                                       echo "db-lact";
                                                   } ?>"><img src="<?php echo $slash; ?>images/icon/dbl13.png"
                                                              alt=""/><?php echo $BIZBOOK['REVIEWS']; ?></a>
                                            </li>
                                            <li>
                                                <a href="<?php echo $slash; ?>db-like-listings"
                                                   class="<?php if ($current_page == "db-like-listings.php") {
                                                       echo "db-lact";
                                                   } ?>"><img src="<?php echo $slash; ?>images/icon/dbl15.png"
                                                              alt=""/><?php echo $BIZBOOK['LIKED_LISTINGS']; ?></a>
                                            </li>
                                            <?php } ?>
                                            <li>
                                                <a href="<?php echo $slash; ?>db-followings"
                                                   class="<?php if ($current_page == "db-followings.php") {
                                                       echo "db-lact";
                                                   } ?>"><img src="<?php echo $slash; ?>images/icon/dbl18.png"
                                                              alt=""/><?php echo $BIZBOOK['FOLLOWINGS']; ?></a>
                                            </li>
                                            <?php
                                            if ($user_details_row['user_type'] == "Service provider") {  //To Check User type is Service provider
                                                ?>
                                                <li>
                                                    <a href="<?php echo $slash; ?>db-post-ads"
                                                       class="<?php if ($current_page == "db-post-ads.php") {
                                                           echo "db-lact";
                                                       } ?>"><img src="<?php echo $slash; ?>images/icon/dbl11.png"
                                                                  alt=""/><?php echo $BIZBOOK['AD_SUMMARY']; ?></a>
                                                </li>
                                                <li>
                                                    <a href="<?php echo $slash; ?>db-payment"
                                                       class="<?php if ($current_page == "db-payment.php") {
                                                           echo "db-lact";
                                                       } ?>"><img src="<?php echo $slash; ?>images/icon/dbl9.png"
                                                                  alt=""><?php echo $BIZBOOK['CHECK_OUT']; ?></a>
                                                </li>
                                                <li>
                                                    <a href="<?php echo $slash; ?>db-invoice-all"
                                                       class="<?php if ($current_page == "db-invoice-all.php") {
                                                           echo "db-lact";
                                                       } ?>"><img src="<?php echo $slash; ?>images/icon/dbl16.png"
                                                                  alt=""/><?php echo $BIZBOOK['PAYMENT_INVOICE']; ?></a>
                                                </li>
                                                <?php
                                            }
                                            ?>
                                            <li>
                                                <a href="<?php echo $slash; ?>db-notifications"
                                                   class="<?php if ($current_page == "db-notifications.php") {
                                                       echo "db-lact";
                                                   } ?>"><img src="<?php echo $slash; ?>images/icon/dbl19.png"
                                                              alt=""/><?php echo $BIZBOOK['NOTIFICATIONS']; ?></a>
                                            </li>
                                            <li>
                                                <a href="<?php echo $slash; ?>how-to"
                                                   class="<?php if ($current_page == "how-to.php") {
                                                       echo "db-lact";
                                                   } ?>" target="_blank"><img
                                                        src="<?php echo $slash; ?>images/icon/dbl17.png"
                                                        alt=""/><?php echo $BIZBOOK['HOW_TOS']; ?>
                                                </a>
                                            </li>
                                            <li>
                                                <a href="<?php echo $slash; ?>db-setting"
                                                   class="<?php if ($current_page == "db-setting.php") {
                                                       echo "db-lact";
                                                   } ?>"><img src="<?php echo $slash; ?>images/icon/dbl210.png"
                                                              alt=""/><?php echo $BIZBOOK['SETTING']; ?></a>
                                            </li>
                                            <li>
                                                <a href="<?php echo $slash; ?>logout"><img
                                                        src="<?php echo $slash; ?>images/icon/dbl12.png"
                                                        alt=""/><?php echo $BIZBOOK['LOG_OUT']; ?></a>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <?php
                            }
                            ?>
                            <!--MOBILE MENU-->
                            <div class="mob-menu">
                                <div class="mob-me-ic"><i class="material-icons">menu</i></div>
                                <div class="mob-me-all">
                                    <div class="mob-me-clo"><i class="material-icons">close</i></div>
                                    <?php
                                    if (!isset($_SESSION['user_name']) && empty($_SESSION['user_name'])) {
                                        ?>
                                        <div class="mv-bus">
                                            <h4></h4>
                                            <ul>
                                                <li>
                                                    <a href="<?php echo $webpage_full_link; ?>pricing-details"><?php echo $BIZBOOK['ADD_BUSINESS']; ?></a>
                                                </li>
                                                <li>
                                                    <a href="<?php echo $webpage_full_link; ?>login"><?php echo $BIZBOOK['SIGN_IN']; ?></a>
                                                </li>
                                                <li>
                                                    <a href="<?php echo $webpage_full_link; ?>login?login=register"><?php echo $BIZBOOK['CREATE_AN_ACCOUNT']; ?></a>
                                                </li>
                                            </ul>
                                        </div>
                                        <?php
                                    } else {
                                        ?>
                                        <div class="mv-pro ud-lhs-s1">
                                            <img
                                                src="<?php echo $slash; ?>images/user/<?php if (($user_details_row['profile_image'] == NULL) || empty($user_details_row['profile_image'])) {
                                                    echo $footer_row['user_default_image'];
                                                } else {
                                                    echo $user_details_row['profile_image'];
                                                } ?>" alt="">
                                            <h4><?php echo $user_details_row['first_name']; ?></h4>
                                            <b><?php echo $BIZBOOK['JOIN_ON']; ?><?php echo dateFormatconverter($user_details_row['user_cdt']) ?></b>
                                        </div>
                                        <div class="mv-pro-menu ud-lhs-s2">
                                            <ul>
                                                <li>
                                                    <a href="<?php echo $slash; ?>dashboard"
                                                       class="<?php if ($current_page == "dashboard.php") {
                                                           echo "db-lact";
                                                       } ?>"><img src="<?php echo $slash; ?>images/icon/dbl1.png"
                                                                  alt=""/> <?php echo $BIZBOOK['MY_DASHBOARD']; ?></a>
                                                </li>
                                                <?php
                                                if ($user_details_row['user_type'] == "Service provider") {  //To Check User type is Service provider
                                                    ?>
                                                    <?php if ($footer_row['admin_listing_show'] == 1 && $user_details_row['setting_listing_show'] == 1) { ?>
                                                        <li>
                                                            <a href="<?php echo $slash; ?>db-all-listing"
                                                               class="<?php if ($current_page == "db-all-listing.php") {
                                                                   echo "db-lact";
                                                               } ?>"><img
                                                                    src="<?php echo $slash; ?>images/icon/shop.png"
                                                                    alt=""/><?php echo $BIZBOOK['ALL_LISTING']; ?></a>
                                                        </li>
                                                        <li>
                                                            <a href="<?php echo $slash; ?>add-listing-start"><img
                                                                    src="<?php echo $slash; ?>images/icon/dbl3.png"
                                                                    alt=""/><?php echo $BIZBOOK['ADD_NEW_LISTING']; ?>
                                                            </a>
                                                        </li>
                                                        <li>
                                                            <a href="<?php echo $slash; ?>db-enquiry"
                                                               class="<?php if ($current_page == "db-enquiry.php") {
                                                                   echo "db-lact";
                                                               } ?>"><img
                                                                    src="<?php echo $slash; ?>images/icon/tick.png"
                                                                    alt=""/><?php echo $BIZBOOK['LEAD_ENQUIRY']; ?>
                                                            </a>
                                                        </li>
                                                    <?php } ?>
                                                    <?php if ($footer_row['admin_job_show'] == 1 && $user_details_row['setting_job_show'] == 1) { ?>
                                                        <li>
                                                            <a href="<?php echo $slash; ?>jobs/db-jobs"
                                                               class="<?php if ($current_page == "db-jobs.php") {
                                                                   echo "db-lact";
                                                               } ?>"><img
                                                                    src="<?php echo $slash; ?>jobs/images/icon/employee.png"
                                                                    alt=""/><?php echo $BIZBOOK['JOBS']; ?></a>
                                                        </li>
                                                    <?php } ?>
                                                    <?php if ($footer_row['admin_product_show'] == 1 && $user_details_row['setting_product_show'] == 1) { ?>
                                                        <li>
                                                            <a href="<?php echo $slash; ?>db-products"
                                                               class="<?php if ($current_page == "db-products.php") {
                                                                   echo "db-lact";
                                                               } ?>"><img
                                                                    src="<?php echo $slash; ?>images/icon/cart.png"
                                                                    alt=""/><?php echo $BIZBOOK['ALL_PRODUCTS']; ?>
                                                            </a>
                                                        </li>
                                                    <?php } ?>
                                                    <?php if ($footer_row['admin_event_show'] == 1 && $user_details_row['setting_event_show'] == 1) { ?>
                                                        <li>
                                                            <a href="<?php echo $slash; ?>db-events"
                                                               class="<?php if ($current_page == "db-events.php") {
                                                                   echo "db-lact";
                                                               } ?>"><img
                                                                    src="<?php echo $slash; ?>images/icon/calendar.png"
                                                                    alt=""/><?php echo $BIZBOOK['EVENTS']; ?></a>
                                                        </li>
                                                    <?php } ?>
                                                    <?php if ($footer_row['admin_blog_show'] == 1 && $user_details_row['setting_blog_show'] == 1) { ?>
                                                        <li>
                                                            <a href="<?php echo $slash; ?>db-blog-posts"
                                                               class="<?php if ($current_page == "db-blog-posts.php") {
                                                                   echo "db-lact";
                                                               } ?>"><img
                                                                    src="<?php echo $slash; ?>images/icon/blog1.png"
                                                                    alt=""/><?php echo $BIZBOOK['BLOG_POSTS']; ?></a>
                                                        </li>
                                                    <?php } ?>
                                                    <?php if ($footer_row['admin_expert_show'] == 1 && $user_details_row['setting_expert_show'] == 1) { ?>
                                                        <li>
                                                            <a href="<?php echo $slash; ?>service-experts/create-service-expert-profile"
                                                               class="<?php if ($current_page == "create-service-expert-profile.php") {
                                                                   echo "db-lact";
                                                               } ?>"><img
                                                                    src="<?php echo $slash; ?>images/icon/profile.png"
                                                                    alt=""/><?php echo $BIZBOOK['ADD_NEW_SERVICE_EXPERT']; ?>
                                                            </a>
                                                        </li>
                                                        <li>
                                                            <a href="<?php echo $slash; ?>service-experts/db-service-expert"
                                                               class="<?php if ($current_page == "db-service-expert.php") {
                                                                   echo "db-lact";
                                                               } ?>"><img
                                                                    src="<?php echo $slash; ?>images/icon/expert.png"
                                                                    alt=""/><?php echo $BIZBOOK['ALL_SERVICE_EXPERT_LEADS']; ?>
                                                            </a>
                                                        </li>
                                                    <?php } ?>
                                                    <?php if ($footer_row['admin_coupon_show'] == 1 && $user_details_row['setting_coupon_show'] == 1) { ?>
                                                        <li>
                                                            <a href="<?php echo $slash; ?>db-coupons"
                                                               class="<?php if ($current_page == "db-coupons.php") {
                                                                   echo "db-lact";
                                                               } ?>"><img
                                                                    src="<?php echo $slash; ?>images/icon/coupons.png"
                                                                    alt=""/><?php echo $BIZBOOK['COUPONS']; ?></a>
                                                        </li>
                                                    <?php } ?>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>db-promote"
                                                           class="<?php if ($current_page == "db-promote.php") {
                                                               echo "db-lact";
                                                           } ?>"><img
                                                                src="<?php echo $slash; ?>images/icon/promotion.png"
                                                                alt=""/><?php echo $BIZBOOK['PROMOTIONS']; ?></a>
                                                    </li>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>db-seo"
                                                           class="<?php if ($current_page == "db-seo.php") {
                                                               echo "db-lact";
                                                           } ?>"><img src="<?php echo $slash; ?>images/icon/seo.png"
                                                                      alt=""/><?php echo $BIZBOOK['SEO']; ?></a>
                                                    </li>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>db-point-history"
                                                           class="<?php if ($current_page == "db-point-history.php") {
                                                               echo "db-lact";
                                                           } ?>"><img src="<?php echo $slash; ?>images/icon/point.png"
                                                                      alt=""/><?php echo $BIZBOOK['POINTS_HISTORY']; ?>
                                                        </a>
                                                    </li>
                                                    <?php
                                                }
                                                ?>

                                                <li>
                                                    <a href="<?php echo $slash; ?>db-my-profile"
                                                       class="<?php if ($current_page == "db-my-profile.php" || $current_page == "db-my-profile-edit") {
                                                           echo "db-lact";
                                                       } ?>"><img src="<?php echo $slash; ?>images/icon/profile.png"
                                                                  alt=""/><?php echo $BIZBOOK['MY_PROFILE']; ?></a>
                                                </li>
                                                <?php if ($footer_row['admin_job_show'] == 1 && $user_details_row['setting_job_show'] == 1) { ?>
                                                <li>
                                                    <a href="<?php echo $slash; ?>jobs/create-job-seeker-profile"
                                                       class="<?php if ($current_page == "create-job-seeker-profile.php") {
                                                           echo "db-lact";
                                                       } ?>"><img src="<?php echo $slash; ?>images/icon/profile.png"
                                                                  alt=""/><?php echo $BIZBOOK['PROFI_JOB_SEEKER_TIT']; ?>
                                                    </a>
                                                </li>
                                                <li>
                                                    <a href="<?php echo $slash; ?>jobs/db-user-applied-jobs"><img
                                                            src="<?php echo $slash; ?>images/icon/job-apply.png"
                                                            alt=""/><?php echo $BIZBOOK['ALL_APPLIED_JOBS']; ?></a>
                                                </li>
                                                <?php } if ($footer_row['admin_expert_show'] == 1 && $user_details_row['setting_expert_show'] == 1) { ?>
                                                <li>
                                                    <a href="<?php echo $slash; ?>service-experts/db-my-service-bookings"
                                                       class="<?php if ($current_page == "db-my-service-bookings.php") {
                                                           echo "db-lact";
                                                       } ?>"><img
                                                            src="<?php echo $slash; ?>images/icon/expert-book.png"
                                                            alt=""/><?php echo $BIZBOOK['MY_SERVICE_BOOKINGS']; ?></a>
                                                </li>
                                                <?php } ?>
                                                <li>
                                                    <a href="<?php echo $slash; ?>db-review"
                                                       class="<?php if ($current_page == "db-review.php") {
                                                           echo "db-lact";
                                                       } ?>"><img src="<?php echo $slash; ?>images/icon/dbl13.png"
                                                                  alt=""/><?php echo $BIZBOOK['REVIEWS']; ?></a>
                                                </li>
                                                <li>
                                                    <a href="<?php echo $slash; ?>db-like-listings"
                                                       class="<?php if ($current_page == "db-like-listings.php") {
                                                           echo "db-lact";
                                                       } ?>"><img src="<?php echo $slash; ?>images/icon/dbl15.png"
                                                                  alt=""/><?php echo $BIZBOOK['LIKED_LISTINGS']; ?></a>
                                                </li>
                                                <li>
                                                    <a href="<?php echo $slash; ?>db-followings"
                                                       class="<?php if ($current_page == "db-followings.php") {
                                                           echo "db-lact";
                                                       } ?>"><img src="<?php echo $slash; ?>images/icon/dbl18.png"
                                                                  alt=""/><?php echo $BIZBOOK['FOLLOWINGS']; ?></a>
                                                </li>
                                                <?php
                                                if ($user_details_row['user_type'] == "Service provider") {  //To Check User type is Service provider
                                                    ?>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>db-post-ads"
                                                           class="<?php if ($current_page == "db-post-ads.php") {
                                                               echo "db-lact";
                                                           } ?>"><img src="<?php echo $slash; ?>images/icon/dbl11.png"
                                                                      alt=""/><?php echo $BIZBOOK['AD_SUMMARY']; ?></a>
                                                    </li>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>db-payment"
                                                           class="<?php if ($current_page == "db-payment.php") {
                                                               echo "db-lact";
                                                           } ?>"><img src="<?php echo $slash; ?>images/icon/dbl9.png"
                                                                      alt=""><?php echo $BIZBOOK['CHECK_OUT']; ?></a>
                                                    </li>
                                                    <li>
                                                        <a href="<?php echo $slash; ?>db-invoice-all"
                                                           class="<?php if ($current_page == "db-invoice-all.php") {
                                                               echo "db-lact";
                                                           } ?>"><img src="<?php echo $slash; ?>images/icon/dbl16.png"
                                                                      alt=""/><?php echo $BIZBOOK['PAYMENT_INVOICE']; ?>
                                                        </a>
                                                    </li>
                                                    <?php
                                                }
                                                ?>
                                                <li>
                                                    <a href="<?php echo $slash; ?>db-notifications"
                                                       class="<?php if ($current_page == "db-notifications.php") {
                                                           echo "db-lact";
                                                       } ?>"><img src="<?php echo $slash; ?>images/icon/dbl19.png"
                                                                  alt=""/><?php echo $BIZBOOK['NOTIFICATIONS']; ?></a>
                                                </li>
                                                <li>
                                                    <a href="<?php echo $slash; ?>how-to"
                                                       class="<?php if ($current_page == "how-to.php") {
                                                           echo "db-lact";
                                                       } ?>" target="_blank"><img
                                                            src="<?php echo $slash; ?>images/icon/dbl17.png"
                                                            alt=""/><?php echo $BIZBOOK['HOW_TOS']; ?>
                                                    </a>
                                                </li>
                                                <li>
                                                    <a href="<?php echo $slash; ?>db-setting"
                                                       class="<?php if ($current_page == "db-setting.php") {
                                                           echo "db-lact";
                                                       } ?>"><img src="<?php echo $slash; ?>images/icon/dbl210.png"
                                                                  alt=""/><?php echo $BIZBOOK['SETTING']; ?></a>
                                                </li>
                                                <li>
                                                    <a href="<?php echo $slash; ?>logout"><img
                                                            src="<?php echo $slash; ?>images/icon/dbl12.png"
                                                            alt=""/><?php echo $BIZBOOK['LOG_OUT']; ?></a>
                                                </li>
                                            </ul>
                                        </div>
                                        <?php
                                    }
                                    ?>
                                    <div class="mv-cate">
                                        <h4><?php echo $BIZBOOK['ALL_CATEGORIES']; ?></h4>
                                        <ul>
                                            <?php foreach (getAllCategoriesPos() as $row) { ?>
                                                <li>
                                                    <a href="<?php echo $ALL_LISTING_URL . urlModifier($row['category_name']); ?>"><?php echo $row['category_name']; ?></a>
                                                </li>
                                            <?php } ?>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            <!--END MOBILE MENU-->
                        </div>
                    </div>
                </div>
            </div>

            <?php if ($current_page == "index.php" || $current_page == "index1.php" || $current_page == "index2.php" || $current_page == "all-category.php") { ?>
                <div class="container">
                    <div class="row">
                        <div class="ban-tit">
                            <h1>
                                <?php if ($current_page == "all-category.php") { ?>
                                    <b><?php echo $BIZBOOK['HOM-BAN-TIT-CAT']; ?></b>
                                <?php } else { ?>
                                    <b><?php echo $BIZBOOK['HOM-BAN-TIT']; ?></b> <?php echo $BIZBOOK['HOM-BAN-SUB-TIT']; ?>
                                <?php } ?>
                            </h1>
                        </div>
                        <div class="ban-search">
                            <form name="filter_form" id="filter_form" class="filter_form">
                                <ul>
                                    <li class="sr-cit">
                                        <select id="city_check" name="city_check" class="chosen-select">
                                            <option value=""><?php echo $BIZBOOK['SELECT_CITY']; ?></option>
                                            <?php
                                            foreach (getAllListingPageCities() as $city_listrow) {

                                                if (strpos($city_listrow['city_id'], ',') !== false) {
                                                    $city_id_array = array_unique(explode(',', $city_listrow['city_id']));
                                                    foreach ($city_id_array as $places) {
                                                        $cityrow = getCity($places);
                                                        ?>
                                                        <option <?php if ($_SESSION['city_check'] === $cityrow['city_id']) {
                                                            echo 'selected';
                                                        } ?>
                                                            value="<?php echo $cityrow['city_id']; ?>"><?php echo $cityrow['city_name']; ?></option>
                                                        <?php
                                                    }
                                                }
                                            }
                                            ?>
                                        </select>
                                    </li>
                                    <li class="sr-sea">
                                        <input type="text" autocomplete="off" id="select-search"
                                               placeholder="<?php echo $BIZBOOK['SEARCHBOX_LABEL']; ?>"
                                               class="search-field">
                                        <ul id="tser-res" class="tser-res tser-res1">
                                            <?php
                                            $si = 1;
                                            foreach (getAllSearch() as $search_header_row) {
                                                ?>
                                                <li>
                                                    <div>
                                                        <h4><?php echo $search_header_row['search_title']; ?></h4>
                                                        <span><?php echo $search_header_row['search_tag_line']; ?></span>
                                                        <a href="<?php echo $search_header_row['search_list_link']; ?>"></a>
                                                    </div>
                                                </li>
                                                <?php
                                            }
                                            ?>
                                        </ul>
                                    </li>
                                    <li class="sr-btn">
                                        <input type="submit" id="filter_submit" name="filter_submit"
                                               value="<?php echo $BIZBOOK['SEARCH']; ?>" class="filter_submit">
                                    </li>
                                </ul>
                            </form>
                        </div>
                        <div class="ban-short-links">
                            <ul>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/shop.png" alt="">
                                        <h4><?php echo $BIZBOOK['ALL_SERVICES']; ?></h4>
                                        <a href="<?php echo $webpage_full_link; ?>all-category" class="fclick"></a>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/expert.png" alt="">
                                        <h4><?php echo $BIZBOOK['SERVICE-EXPERTS-EXPERTS']; ?></h4>
                                        <a href="<?php echo $webpage_full_link; ?>service-experts" class="fclick"></a>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/employee.png" alt="">
                                        <h4><?php echo $BIZBOOK['JOBS']; ?></h4>
                                        <a href="<?php echo $webpage_full_link; ?>jobs" class="fclick"></a>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/places/icons/hot-air-balloon.png" alt="">
                                        <h4><?php echo $BIZBOOK['PLACE-TRAVEL']; ?></h4>
                                        <a href="<?php echo $webpage_full_link; ?>places" class="fclick"></a>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/news.png" alt="">
                                        <h4><?php echo $BIZBOOK['NEWS']; ?></h4>
                                        <a href="<?php echo $webpage_full_link; ?>news" class="fclick"></a>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/calendar.png" alt="">
                                        <h4><?php echo $BIZBOOK['EVENTS']; ?></h4>
                                        <a href="<?php echo $webpage_full_link; ?>events" class="fclick"></a>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/cart.png" alt="">
                                        <h4><?php echo $BIZBOOK['PRODUCTS']; ?></h4>
                                        <a href="<?php echo $webpage_full_link; ?>all-products" class="fclick"></a>
                                    </div>
                                </li>

                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/coupons.png" alt="">
                                        <h4><?php echo $BIZBOOK['COUPONS']; ?></h4>
                                        <a href="<?php echo $webpage_full_link; ?>coupons" class="fclick"></a>
                                    </div>
                                </li>
                                <!--<li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/blog1.png" alt="">
                                        <h4><?php echo $BIZBOOK['BLOGS']; ?></h4>
                                        <a href="<?php echo $webpage_full_link; ?>blog-posts" class="fclick"></a>
                                    </div>
                                </li>-->
                            </ul>
                        </div>
                        <div class="h2-ban-ql">
                            <ul>
                                <?php if ($footer_row['admin_listing_show'] == 1) { ?>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/listing.png" alt="">
                                        <h5><span
                                                class="count1"><?php echo AddingZero_BeforeNumber(getCountCategory()); ?></span><?php echo $BIZBOOK['ALL_SERVICES']; ?>
                                        </h5>
                                        <a href="<?php echo $webpage_full_link; ?>all-category">&nbsp;</a>
                                    </div>
                                </li>
                                <?php } if ($footer_row['admin_expert_show'] == 1) { ?>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/expert.png" alt="">
                                        <h5><span
                                                class="count1"><?php echo AddingZero_BeforeNumber(getCountCategory()); ?></span><?php echo $BIZBOOK['SERVICE-EXPERTS']; ?>
                                        </h5>
                                        <a href="<?php echo $webpage_full_link; ?>service-experts">&nbsp;</a>
                                    </div>
                                </li>
                                <?php } if ($footer_row['admin_job_show'] == 1) { ?>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/employee.png" alt="">
                                        <h5><span class="count1"><?php echo AddingZero_BeforeNumber(getCountCategory()); ?></span><?php echo $BIZBOOK['JOBS']; ?>
                                        </h5>
                                        <a href="<?php echo $webpage_full_link; ?>jobs">&nbsp;</a>
                                    </div>
                                </li>
                                <?php } if ($footer_row['admin_product_show'] == 1) { ?>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/shop.png" alt="">
                                        <h5><span
                                                class="count1"><?php echo AddingZero_BeforeNumber(getCountProduct()); ?></span><?php echo $BIZBOOK['PRODUCTS']; ?>
                                        </h5>
                                        <a href="<?php echo $webpage_full_link; ?>all-products">&nbsp;</a>
                                    </div>
                                </li>
                                <?php } if ($footer_row['admin_event_show'] == 1) { ?>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/event.png" alt="">
                                        <h5><span
                                                class="count1"><?php echo AddingZero_BeforeNumber(getCountEvent()); ?></span><?php echo $BIZBOOK['EVENTS']; ?>
                                        </h5>
                                        <a href="<?php echo $webpage_full_link; ?>events">&nbsp;</a>
                                    </div>
                                </li>
                                <?php } if ($footer_row['admin_coupon_show'] == 1) { ?>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/coupons.png" alt="">
                                        <h5><span
                                                class="count1"><?php echo AddingZero_BeforeNumber(getCountCoupon()); ?></span><?php echo $BIZBOOK['COUPONS']; ?>
                                        </h5>
                                        <a href="<?php echo $webpage_full_link; ?>coupons">&nbsp;</a>
                                    </div>
                                </li>
                                <?php } if ($footer_row['admin_blog_show'] == 1) { ?>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/blog.png" alt="">
                                        <h5><span
                                                class="count1"><?php echo AddingZero_BeforeNumber(getCountBlog()); ?></span><?php echo $BIZBOOK['BLOGS']; ?>
                                        </h5>
                                        <a href="<?php echo $webpage_full_link; ?>blog-posts">&nbsp;</a>
                                    </div>
                                </li>
                                <?php } ?>
                                <li>
                                    <div>
                                        <img src="<?php echo $slash; ?>images/icon/general.png" alt="">
                                        <h5><span
                                                class="count1"><?php echo AddingZero_BeforeNumber(getCountUser()); ?></span><?php echo $BIZBOOK['COMMUNITY']; ?>
                                        </h5>
                                        <a href="<?php echo $webpage_full_link; ?>community">&nbsp;</a>
                                    </div>
                                </li>
                            </ul>
                        </div>

                    </div>
                </div>
            <?php } ?>
        </div>
    </div>
</section>
<!-- END -->