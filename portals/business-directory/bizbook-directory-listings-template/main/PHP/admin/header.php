<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}


if (file_exists('config/admin_authentication.php')) {
    include('config/admin_authentication.php');
}

if (file_exists('classes/index.function.php')) {
    include('classes/index.function.php');
}

$footer_row = getAllFooter(); //Fetch Footer Data

$admin_row = getAllSuperAdmin(); //Fetch Admin Data

$data_array['website_email_id'] = $footer_row['admin_primary_email'];
$data_array['admin_user_name'] = $admin_row['admin_email'];
$data_array['admin_user_password'] = $admin_row['admin_password'];

$all_texts_row = getAllTexts(); //Fetch All Text Data
?>
<!doctype html>
<html lang="en">

<head>
    <title><?php echo $footer_row['website_address']; ?> - Admin Panel</title>
    <!--== META TAGS ==-->
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <meta name="theme-color" content="#76cef1"/>
    <!--== FAV ICON(BROWSER TAB ICON) ==-->
    <link rel="shortcut icon" href="../images/fav.ico" type="image/x-icon">
    <!--== GOOGLE FONTS ==-->
    <link href="https://fonts.googleapis.com/css?family=Oswald:700|Source+Sans+Pro:300,400,600,700&display=swap"
          rel="stylesheet">

    <!--== WEB ICON FONTS ==-->
    <link rel="preload" as="font" href="css/icon.woff2" type="font/woff2" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <!--== CSS FILES ==-->
    <link rel="stylesheet" href="../css/jquery-ui.css">
    <link rel="stylesheet" href="../css/bootstrap.css">
    <link rel="stylesheet" href="css/admin-style.css">
    <link rel="stylesheet" href="../css/fonts.css">
    <link rel="stylesheet" href="css/dataTables.bootstrap4.min.css">


    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
    <script src="../js/html5shiv.js"></script>
    <script src="../js/respond.min.js"></script>
    <![endif]-->
</head>

<body>


<!-- START -->
<section>
    <div class="ad-head">
        <div class="head-s1">
            <div class="menu">
                <i class="material-icons mopen">menu</i>
                <i class="material-icons mclose">close</i>
            </div>
            <div class="logo">
                <img
                    <?php if ($footer_row['header_logo_width'] != NULL || $footer_row['header_logo_height'] != NULL){ ?>style="<?php if ($footer_row['header_logo_width'] != NULL) { ?>width: <?php echo $footer_row['header_logo_width']; ?>; <?php }
                    if ($footer_row['header_logo_height'] != NULL) { ?>height: <?php echo $footer_row['header_logo_height']; ?>;<?php } ?>"<?php } ?>
                    src="../images/home/<?php echo $footer_row['header_logo']; ?>">
            </div>
        </div>
        <div class="head-s2">
            <div class="head-sear">
                <input type="text" id="top_search" placeholder="Search the listing and users..." class="search-field">
                <ul id="tser-res" class="tser-res">
                    <li><a href="activate.php">Activate template</a></li>
                    <li><a href="updates.php">Bizbook template updates and release</a></li>
                    <li><a href="addons.php">Premium Addons</a></li>
                    <li><a href="admin-add-new-user.php">Add new user</a></li>
                    <li><a href="admin-add-new-listings.php">Add new listing</a></li>
                    <li><a href="admin-add-new-product.php">Add new product</a></li>
                    <li><a href="admin-add-new-event.php">Add new events</a></li>
                    <li><a href="admin-slider-create.php">Add new slider</a></li>
                    <li><a href="profile.php">Dashboard</a></li>
                    <li><a href="profile.php">Profile page</a></li>
                    <li><a href="admin-all-users.php">All users</a></li>
                    <li><a href="admin-new-user-requests.php">New user requests</a></li>
                    <li><a href="admin-new-cod-requests.php">Cash on delivery(COD) requests</a></li>
                    <li><a href="admin-all-users-general.php">General users</a></li>
                    <li><a href="admin-all-users-service-provider.php">Services providers</a></li>
                    <li><a href="admin-free-users.php">Free users</a></li>
                    <li><a href="admin-standard-users.php">Standard users</a></li>
                    <li><a href="admin-premium-users.php">Premium users</a></li>
                    <li><a href="admin-premium-plus-users.php">Premium plus users</a></li>
                    <li><a href="admin-non-paid-users.php">Non-paid users</a></li>
                    <li><a href="admin-paid-users.php">Paid users</a></li>
                    <li><a href="admin-sub-admin-all.php">Sub admin</a></li>
                    <li><a href="admin-sub-admin-create.php">Add new sub admin</a></li>
                    <li><a href="admin-text-changes.php">All text change</a></li>
                    <li><a href="admin-text-changes.php">How to change all static texts</a></li>
                    <li><a href="admin-text-changes.php">Edit webpage texts</a></li>
                    <li><a href="admin-price.php">Pricing plan</a></li>

                    <li><a href="admin-all-listings.php">All listings</a></li>

                    <li><a href="admin-create-duplicate-listing.php">Create duplicate listing</a></li>
                    <li><a href="admin-claim-listing.php">Claim request</a></li>
                    <li><a href="admin-claim-listing.php">Listing & business claim request</a></li>
                    <li><a href="admin-trash-listing.php">Trash listing</a></li>
                    <li><a href="admin-event.php">All events</a></li>

                    <li><a href="admin-all-blogs.php">All blogs posts</a></li>
                    <li><a href="admin-add-new-blogs.php">Add new blog post</a></li>
                    <li><a href="admin-all-products.php">All products</a></li>
                    <li><a href="admin-all-payments.php">All Payments</a></li>

                    <li><a href="admin-all-category.php">All listing category</a></li>
                    <li><a href="admin-add-new-category.php">Add new listing category</a></li>
                    <li><a href="admin-all-sub-category.php">Listing sub categorys</a></li>
                    <li><a href="admin-add-new-sub-category.php">Add new listing sub category</a></li>
                    <li><a href="admin-all-product-category.php">All product category</a></li>
                    <li><a href="admin-add-new-product-category.php">Add new product category</a></li>
                    <li><a href="admin-all-product-sub-category.php">Product sub categorys</a></li>
                    <li><a href="admin-add-new-product-sub-category.php">Add new product sub category</a></li>
                    <li><a href="admin-all-enquiry.php">All enquiry</a></li>
                    <li><a href="admin-saved-enquiry.php">Save enquirys</a></li>
                    <li><a href="admin-all-reviews.php">All reviews</a></li>
                    <li><a href="admin-saved-reviews.php">Save reviews</a></li>
                    <li><a href="admin-all-feedbacks.php">Feedbacks</a></li>
                    <li><a href="admin-notification-all.php">All notifications</a></li>
                    <li><a href="admin-create-notification.php">Send new notifications</a></li>
                    <li><a href="admin-create-notification.php">Create new notifications</a></li>
                    <li><a href="admin-current-ads.php">Current ads</a></li>
                    <li><a href="admin-create-ads.php">Create new ads</a></li>
                    <li><a href="admin-ads-request.php">Ads request and enquiry</a></li>
                    <li><a href="admin-ads-price.php">Ads pricing</a></li>
                    <li><a href="admin-home-category.php">Home page edit optins</a></li>
                    <li><a href="admin-home-category.php">Home page category edit</a></li>
                    <li><a href="admin-trending-category.php">Home page trending category edit</a></li>
                    <li><a href="admin-home-popular-business.php">Home page popular business edit</a></li>
                    <li><a href="admin-home-top-services.php">Home page top services edit</a></li>
                    <li><a href="admin-home-feature-events.php">Home page feature events</a></li>
                    <li><a href="admin-all-city.php">All city</a></li>
                    <li><a href="admin-add-city.php">Add new city</a></li>
                    <li><a href="admin-filter-features.php">Listing filetrs</a></li>
                    <li><a href="admin-filter-category.php">Listing filter category edit</a></li>
                    <li><a href="admin-filter-features.php">Listing feature filter edit</a></li>
                    <li><a href="admin-invoice-create.php">Create new invoice</a></li>
                    <li><a href="admin-send-invoice.php">Send invoice</a></li>
                    <li><a href="admin-send-invoice.php">Send new invoice</a></li>
                    <li><a href="admin-invoice-shared.php">Shared invoices</a></li>
                    <li><a href="admin-import.php">Import data</a></li>
                    <li><a href="admin-export.php">Export data</a></li>
                    <li><a href="admin-price-edit.php?row=1">Edit free pricing plan</a></li>
                    <li><a href="admin-price-edit.php?row=2">Edit standard pricing plan</a></li>
                    <li><a href="admin-price-edit.php?row=3">Edit premium pricing plan</a></li>
                    <li><a href="admin-price-edit.php?row=4">Edit premium plus pricing plan</a></li>
                    <li><a href="admin-payment-credentials.php">Payment gateways</a></li>
                    <li><a href="admin-payment-credentials-edit.php?row=cod">Cash On Delivery Credentials</a></li>
                    <li><a href="admin-payment-credentials-edit.php?row=paypal">PayPal Credentials</a></li>
                    <li><a href="admin-payment-credentials-edit.php?row=stripe">Stripe Credentials</a></li>
                    <li><a href="admin-setting.php">Admin setting</a></li>
                    <li><a href="admin-footer.php">Footer edit</a></li>
                    <li><a href="admin-footer.php">Footer CMS</a></li>
                    <li><a href="admin-dummy-images.php">Dummy image for users</a></li>
                    <li><a href="admin-all-mail.php">Email templates</a></li>
                    <li><a href="admin-all-mail.php">Edit email messages</a></li>
                    <li><a href="admin-slider-all.php">All slider images</a></li>
                    <li><a href="admin-slider-all.php">Edit slider images</a></li>
                    <li><a href="admin-slider-create.php">Create new slider</a></li>
                    <li><a href="admin-security-updates.php">Security and updates notifications</a></li>
                    <li><a href="seo-listing-options.php">Listing category promotions</a></li>
                    <li><a href="seo-listing-options.php">Listing category SEO setting</a></li>
                    <li><a href="seo-target-promotion-all-pages.php">Target listings promotion</a></li>
                    <li><a href="seo-target-promotion-all-pages.php">Target promotion</a></li>
                    <li><a href="seo-target-promotion-all-pages.php">Target listings promotion page</a></li>
                    <li><a href="seo-target-promotion-all-pages.php">Target listing SEO</a></li>
                    <li><a href="seo-target-promotion-add-new-page.php">Add new target listing page</a></li>
                    <li><a href="seo-general-all-pages.php">General promotion SEO setting pages</a></li>
                    <li><a href="seo-general-add-new-page.php">Add new general promotion page</a></li>
                    <li><a href="seo-ebook-all-pages.php">All Ebook pages</a></li>
                    <li><a href="seo-ebook-all-pages.php">Digital promotion pages</a></li>
                    <li><a href="seo-ebook-add-new-page.php">Add new Ebook page</a></li>
                    <li><a href="seo-ebook-add-new-page.php">Add new Digital promotion page</a></li>
                    <li><a href="seo-google-analytics-code.php">Google Analytics</a></li>
                    <li><a href="seo-xml-sitemap.php">XML sitemap</a></li>
                    <li><a href="search-lists.php">All search lists</a></li>
                    <li><a href="search-lists-add.php">Add new search lists</a></li>
                    <li><a href="search-positions.php">Search positions</a></li>
                    <li><a href="seo-google-adsense.php">Google AdSense</a></li>
                    <li><a href="seo-google-adsense.php">Add Google AdSense code</a></li>
                    <li><a href="admin-footer.php">Footer text edit & update</a></li>
                    <li><a href="admin-footer-popular-tags.php">Footer popular tags</a></li>
                    <li><a href="footer-add-popular-tags.php">Add new popular tags</a></li>
                    <li><a href="seo-meta-tags.php">All page Meat tags</a></li>
                    <li><a href="seo-all-listing-options.php">Listing page meta & SEO options</a></li>
                    <li><a href="seo-all-blog-options.php">Blog page meta & SEO options</a></li>
                    <li><a href="seo-all-event-options.php">Events page meta & SEO options</a></li>
                    <li><a href="seo-all-product-options.php">Products page meta & SEO options</a></li>
                    <li><a href="seo-all-job-options.php">Job page meta & SEO options</a></li>
                    <li><a href="seo-all-expert-options.php">Service Expert page meta & SEO options</a></li>
                    <li><a href="expert-users.php">All Service experts</a></li>
                    <li><a href="expert-new-create.php">Add new Service Expert</a></li>
                    <li><a href="expert-leads.php">Service Expert Leads</a></li>
                    <li><a href="expert-admin-info.php">Service Expert - Admin details</a></li>
                    <li><a href="expert-all-category.php">All Expert Category</a></li>
                    <li><a href="expert-add-new-category.php">Add New Expert Category</a></li>
                    <li><a href="expert-home-category-change.php">Service Expert Change Home Page Category positions</a></li>
                    <li><a href="expert-all-sub-category.php">All Expert Sub-Category</a></li>
                    <li><a href="expert-add-new-sub-category.php">Add New Expert Sub Category</a></li>
                    <li><a href="expert-all-city.php">All Service Expert City</a></li>
                    <li><a href="expert-add-new-city.php">Add New Expert City</a></li>
                    <li><a href="expert-all-area.php">All Expert Areas</a></li>
                    <li><a href="expert-add-new-area.php">Add New Area</a></li>
                    <li><a href="expert-payment-accept.php">Expert All Payment Methods</a></li>
                    <li><a href="expert-add-new-payment.php">Add New Expert Payment</a></li>
                    <li><a href="job-all.php">All Job Posts</a></li>
                    <li><a href="job-create.php">Add New Job Post</a></li>
                    <li><a href="admin-all-job-category.php">All Job Category</a></li>
                    <li><a href="admin-all-job-skill-set.php">All Job Skill Set</a></li>
                    <li><a href="admin-add-new-job-skill-set.php">Add New Job Skill Set</a></li>
                    <li><a href="admin-all-job-city.php">All Job City</a></li>
                    <li><a href="admin-coupons.php">All Coupon & Deals details</a></li>
                    <li><a href="admin-add-new-coupons.php">Add New Coupon</a></li>
                    <li><a href="news-all.php">All News & Magazines</a></li>
                    <li><a href="news-add-new.php">Create News</a></li>
                    <li><a href="place-all.php">All Places</a></li>
                    <li><a href="place-add-new.php">Add new Place</a></li>
                    <li><a href="place-all-category.php">All Place Categories</a></li>
                    <li><a href="admin-logo.php">Website Logo update</a></li>
                    <li><a href="color-setting.php">Website Color options</a></li>
                    <li><a href="features-enable-disable.php">Features Enable & Disable</a></li>
                    <li><a href="media-library.php">Media library</a></li>
                    <li><a href="admin-footer.php">Copyright year edit</a></li>
                    <li><a href="admin-social-share.php">Social media Share options</a></li>
                </ul>
            </div>
        </div>
        <div class="head-s3">
            <div class="head-pro">
                <?php
                $admin_row = getAdmin($_SESSION['admin_id']);
                ?>
                <img
                    src="../images/user/<?php if (($admin_row['admin_photo'] == NULL) || empty($admin_row['admin_photo'])) {
                        echo $footer_row['user_default_image'];
                    } else {
                        echo $admin_row['admin_photo'];
                    } ?>" alt="">
                <b>Profile by</b><br>
                <h4><?php echo $admin_row['admin_name']; ?></h4>
                <?php
                if ($_SESSION['admin_id'] == 1) {
                    ?>
                    <a href="admin-setting.php" class="fclick"></a>
                    <?php
                }
                ?>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<!-- START -->
<section>
    <div class="ad-menu-lhs mshow">
        <div class="ad-menu">
            <ul>
                <li class="ic-db">
                    <a href="profile.php" class="<?php if ($current_page == 'profile.php') {
                        echo 'mact';
                    } ?>">Dashboard</a>
                </li>
                <?php if ($admin_row['admin_user_options'] == 1) { ?>

                    <li class="ic-user">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-new-user-requests.php' || $current_page == 'admin-all-users.php' || $current_page == 'admin-new-cod-requests.php' || $current_page == 'admin-non-paid-users.php' || $current_page == 'admin-paid-users.php' || $current_page == 'admin-all-users-general.php' || $current_page == 'admin-all-users-service-provider.php' || $current_page == 'admin-free-users.php' || $current_page == 'admin-standard-users.php' || $current_page == 'admin-premium-users.php' || $current_page == 'admin-premium-plus-users.php' || $current_page == 'admin-add-new-user.function.php') {
                               echo 'mact';
                           } ?>">Users</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-new-user-requests.php">New User Requests</a>
                                </li>
                                <li>
                                    <a href="admin-new-cod-requests.php">New COD Payment Requests</a>
                                </li>
                                <?php
                                foreach (getAllPlanType() as $plan_type_row) {
                                    $name[] = array('name' => $plan_type_row['plan_type_name']);
                                }
                                ?>
                                <li>
                                    <a href="admin-all-users.php">All Users</a>
                                </li>
                                <li>
                                    <a href="admin-all-users-general.php">All Users - General</a>
                                </li>
                                <li>
                                    <a href="admin-all-users-service-provider.php">All Users - Service Providers</a>
                                </li>
                                <li>
                                    <a href="admin-free-users.php"><?php echo $name[0]['name']; ?> Users</a>
                                </li>
                                <li>
                                    <a href="admin-standard-users.php"><?php echo $name[1]['name']; ?> Users</a>
                                </li>
                                <li>
                                    <a href="admin-premium-users.php"><?php echo $name[2]['name']; ?> Users</a>
                                </li>
                                <li>
                                    <a href="admin-premium-plus-users.php"><?php echo $name[3]['name']; ?> Users</a>
                                </li>
                                <li>
                                    <a href="admin-non-paid-users.php">All Non-Paid Users</a>
                                </li>
                                <li>
                                    <a href="admin-paid-users.php">All Paid Users</a>
                                </li>
                                <li>
                                    <a href="admin-add-new-user.php">Add new User</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                <?php }
                if ($admin_row['admin_seo_setting_options'] == 1) { ?>
                    <li><h4>SEO Settings</h4></li>
                    <li class="ic-seo">
                        <a href="#"
                           class="<?php if ($current_page == 'seo-ebook-add-new-page.php' || $current_page == 'seo-ebook-all-pages.php' || $current_page == 'seo-general-all-pages.php' || $current_page == 'seo-general-add-new-page.php' || $current_page == 'seo-target-promotion-all-pages.php' || $current_page == 'seo-all-listing-options.php' || $current_page == 'seo-all-blog-options.php' || $current_page == 'seo-all-event-options.php' || $current_page == 'seo-all-product-options.php' || $current_page == 'seo-all-job-options.php' || $current_page == 'seo-all-expert-options.php' || $current_page == 'seo-target-promotion-add-new-page.php' || $current_page == 'seo-listing-options.php' || $current_page == 'seo-listing-options-edit.php' || $current_page == 'seo-google-analytics-code.php' || $current_page == 'seo-xml-sitemap.php' || $current_page == 'seo-meta-tags.php' || $current_page == 'seo-meta-tags-edit.php') {
                               echo 'mact';
                           } ?>">SEO Settings</a>
                        <div>
                            <h4>
                                Listing category
                                <!-- TOOL TIP -->
                                <div class="ttip-com">
                                    <i class="material-icons">priority_high</i>
                                    <div>This can help you to index your category pages with rich results. You can
                                        change meta title, descriptions, keywords, Short description about your
                                        category, FAQ and google schema(rating, faq and more) for every category.
                                    </div>
                                </div>
                                <!-- END -->
                            </h4>
                            <ol>
                                <li>
                                    <a href="seo-listing-options.php">SEO options</a>
                                </li>
                            </ol>
                            <h4>
                                Target listings promotion
                                <!-- TOOL TIP -->
                                <div class="ttip-com">
                                    <i class="material-icons">priority_high</i>
                                    <div>You can create particular targeting pages with your favorite listing. This can
                                        be helping for end-users can get accurate results, get more leads, target every
                                        small area with google rich results, and more.
                                    </div>
                                </div>
                                <!-- END -->
                            </h4>
                            <ol>
                                <li>
                                    <a href="seo-target-promotion-all-pages.php">All Pages</a>
                                </li>
                                <li>
                                    <a href="seo-target-promotion-add-new-page.php">Add new page</a>
                                </li>
                            </ol>
                            <h4>
                                General promotion pages
                                <!-- TOOL TIP -->
                                <div class="ttip-com">
                                    <i class="material-icons">priority_high</i>
                                    <div>You can create general blog pages with your favorite listing, events, products,
                                        blogs with enquiry form. This page can help you go get more leads and google
                                        index.
                                    </div>
                                </div>
                                <!-- END -->
                            </h4>
                            <ol>
                                <li>
                                    <a href="seo-general-all-pages.php">All Pages</a>
                                </li>
                                <li>
                                    <a href="seo-general-add-new-page.php">Add new page</a>
                                </li>
                            </ol>
                            <h4>
                                E-book & Digital pages
                                <!-- TOOL TIP -->
                                <div class="ttip-com">
                                    <i class="material-icons">priority_high</i>
                                    <div>These pages can help you to promote a product, listing and digital assets with
                                        enquiry form, you can get quality leads and more.
                                    </div>
                                </div>
                                <!-- END -->
                            </h4>
                            <ol>
                                <li>
                                <li>
                                    <a href="seo-ebook-all-pages.php">All Pages</a>
                                </li>
                                <li>
                                    <a href="seo-ebook-add-new-page.php">Add new page</a>
                                </li>
                            </ol>
                            <h4>
                                Google Analytics
                                <!-- TOOL TIP -->
                                <div class="ttip-com">
                                    <i class="material-icons">priority_high</i>
                                    <div>Copy and paste your Google Analytics here... You can get code from Google. This
                                        can helps "tracks and reports website traffic".
                                    </div>
                                </div>
                                <!-- END -->
                            </h4>
                            <ol>
                                <li>
                                <li>
                                    <a href="seo-google-analytics-code.php">Google Analytics Code</a>
                                </li>
                            </ol>
                            <h4>
                                Sitemap
                                <!-- TOOL TIP -->
                                <div class="ttip-com">
                                    <i class="material-icons">priority_high</i>
                                    <div>This allows search engines to crawl the site more efficiently and to find URLs
                                        that may be isolated from the rest of the site's content.
                                    </div>
                                </div>
                                <!-- END -->
                            </h4>
                            <ol>
                                <li>
                                <li>
                                    <a href="seo-xml-sitemap.php">XML Sitemap</a>
                                </li>
                            </ol>
                            <h4>
                                Meta tags
                                <!-- TOOL TIP -->
                                <div class="ttip-com">
                                    <i class="material-icons">priority_high</i>
                                    <div>Meta tags are snippets of text that describe a page's content; the meta tags
                                        don't appear on the page itself, but only in the page's source code. Meta tags
                                        are essentially little content descriptors that help tell search engines what a
                                        web page is about
                                    </div>
                                </div>
                                <!-- END -->
                            </h4>
                            <ol>
                                <li>
                                <li>
                                    <a href="seo-meta-tags.php">All Pages</a>
                                </li>
                                <li>
                                    <a href="seo-all-listing-options.php">Listing SEO options</a>
                                </li>
                                <li>
                                    <a href="seo-all-blog-options.php">Blog SEO options</a>
                                </li>
                                <li>
                                    <a href="seo-all-event-options.php">Event SEO options</a>
                                </li>
                                <li>
                                    <a href="seo-all-product-options.php">Product SEO options</a>
                                </li>
                                <li>
                                    <a href="seo-all-job-options.php">Job SEO options</a>
                                </li>
                                <li>
                                    <a href="seo-all-expert-options.php">Service Expert SEO options</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                <?php } ?>
                <li class="ic-sear">
                    <a href="#"
                       class="<?php if ($current_page == 'search-lists.php' || $current_page == 'search-positions.php' || $current_page == 'search-lists-add.php') {
                           echo 'mact';
                       } ?>">Search Settings</a>
                    <div>
                        <h4>
                            Search list
                            <!-- TOOL TIP -->
                            <div class="ttip-com">
                                <i class="material-icons">priority_high</i>
                                <div>You can create general blog pages with your favorite listing, events, products,
                                    blogs with enquiry form. This page can help you go get more leads and google index.
                                </div>
                            </div>
                            <!-- END -->
                        </h4>
                        <ol>
                            <li>
                                <a href="search-lists.php">Search list</a>
                            </li>
                            <li>
                                <a href="search-lists-add.php">Add new</a>
                            </li>
                        </ol>
                        <h4>
                            Search positions
                            <!-- TOOL TIP -->
                            <div class="ttip-com">
                                <i class="material-icons">priority_high</i>
                                <div>Drog and drop to arrange your search orders. You can change this order depends on
                                    seasons.(Ex: School admission seasons means you can set education related listings
                                    or targetting pages in first position.) It's hels you to getting more leads, user
                                    friendly, end user get accurate results and more.
                                </div>
                            </div>
                            <!-- END -->
                        </h4>
                        <ol>
                            <li>
                                <a href="search-positions.php">Change positions</a>
                            </li>
                        </ol>
                    </div>
                </li>
                <?php
                if ($footer_row['admin_listing_show'] == 1) {
                    if ($admin_row['admin_listing_options'] == 1) { ?>
                        <li><h4>Listings</h4></li>
                        <li class="ic-li">
                            <a href="#"
                               class="<?php if ($current_page == 'admin-all-listings.php' || $current_page == 'admin-add-new-listings.php' || $current_page == 'admin-create-duplicate-listing.php' || $current_page == 'admin-trash-listing.php' || $current_page == 'admin-claim-listing.php') {
                                   echo 'mact';
                               } ?>">listings</a>
                            <div>
                                <ol>
                                    <li>
                                        <a href="admin-all-listings.php">All listings</a>
                                    </li>
                                    <li>
                                        <a href="admin-add-new-listings.php">Add new listings</a>
                                    </li>
                                    <li>
                                        <a href="admin-create-duplicate-listing.php">Create duplicate listings</a>
                                    </li>
                                    <li>
                                        <a href="admin-claim-listing.php">All Claim Requests</a>
                                    </li>
                                    <li>
                                        <a href="admin-trash-listing.php">Trash listings</a>
                                    </li>
                                </ol>
                            </div>
                        </li>

                    <?php }
                    if ($admin_row['admin_category_options'] == 1) { ?>
                        <li class="ic-cat">
                            <a href="#"
                               class="<?php if ($current_page == 'admin-all-category.php' || $current_page == 'admin-add-new-category.php' || $current_page == 'admin-all-sub-category.php' || $current_page == 'admin-add-new-sub-category.php' || $current_page == 'admin-change-position-listing-category.php') {
                                   echo 'mact';
                               } ?>">Listing Category</a>
                            <div>
                                <ol>
                                    <li>
                                        <a href="admin-all-category.php">All Category</a>
                                    </li>
                                    <li>
                                        <a href="admin-add-new-category.php">Add new Category</a>
                                    </li>
                                    <li>
                                        <a href="admin-all-sub-category.php">All Sub Category</a>
                                    </li>
                                    <li>
                                        <a href="admin-add-new-sub-category.php">Add new Sub Category</a>
                                    </li>
                                    <li>
                                        <a href="admin-change-position-listing-category.php">Change Category
                                            Position</a>
                                    </li>
                                </ol>
                            </div>
                        </li>
                    <?php } ?>
                    <li class="ic-poi">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-all-promotions.php' || $current_page == 'admin-promote-now.php' || $current_page == 'admin-all-points.php' || $current_page == 'admin-point-setting.php') {
                               echo 'mact';
                           } ?>">Listing Promotions</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-all-promotions.php">All Promotions</a>
                                </li>
                                <li>
                                    <a href="admin-promote-now.php">Create New Promotions</a>
                                </li>
                                <li>
                                    <a href="admin-all-points.php">All Points History</a>
                                </li>
                                <li>
                                    <a href="admin-point-setting.php">Points Setting</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                    <?php
                    if ($admin_row['admin_enquiry_options'] == 1) { ?>
                        <li class="ic-enq">
                            <a href="#"
                               class="<?php if ($current_page == 'admin-all-enquiry.php' || $current_page == 'admin-saved-enquiry.php') {
                                   echo 'mact';
                               } ?>">Enquiry & Get Quote</a>
                            <div>
                                <ol>
                                    <li>
                                        <a href="admin-all-enquiry.php">All Enquiry</a>
                                    </li>
                                    <li>
                                        <a href="admin-saved-enquiry.php">Saved Enquiry</a>
                                    </li>
                                </ol>
                            </div>
                        </li>

                    <?php }
                    if ($admin_row['admin_review_options'] == 1) { ?>
                        <li class="ic-rev">
                            <a href="#"
                               class="<?php if ($current_page == 'admin-all-reviews.php' || $current_page == 'admin-saved-reviews.php') {
                                   echo 'mact';
                               } ?>">Reviews</a>
                            <div>
                                <ol>
                                    <li>
                                        <a href="admin-all-reviews.php">All Reviews</a>
                                    </li>
                                    <li>
                                        <a href="admin-saved-reviews.php">Saved Reviews</a>
                                    </li>
                                </ol>
                            </div>
                        </li>
                    <?php }
                    if ($admin_row['admin_listing_filter_options'] == 1) { ?>
                        <li class="ic-fil">
                            <a href="#"
                               class="<?php if ($current_page == 'admin-all-filters.php' || $current_page == 'admin-filter-features.php' || $current_page == 'admin-filter-category.php') {
                                   echo 'mact';
                               } ?>">Listing Filter</a>
                            <div>
                                <ol>
                                    <li>
                                        <a href="admin-all-filters.php">All Filters</a>
                                    </li>
                                    <li>
                                        <a href="admin-filter-features.php">Features</a>
                                    </li>
                                </ol>
                            </div>
                        </li>

                    <?php }
                    if ($admin_row['admin_country_options'] == 1) { ?>
                        <li class="ic-cou">
                            <a href="#"
                               class="<?php if ($current_page == 'admin-all-country.php' || $current_page == 'admin-add-country.php') {
                                   echo 'mact';
                               } ?>">Country</a>
                            <div>
                                <ol>
                                    <li>
                                        <a href="admin-all-country.php">All Country</a>
                                    </li>
                                    <li>
                                        <a href="admin-add-country.php">Add New Country</a>
                                    </li>
                                </ol>
                            </div>
                        </li>
                    <?php }
                    if ($admin_row['admin_city_options'] == 1) { ?>
                        <li class="ic-cit">
                            <a href="#"
                               class="<?php if ($current_page == 'admin-all-city.php' || $current_page == 'admin-add-city.php') {
                                   echo 'mact';
                               } ?>">City</a>
                            <div>
                                <ol>
                                    <li>
                                        <a href="admin-all-city.php">All City</a>
                                    </li>
                                    <li>
                                        <a href="admin-add-city.php">Add New City</a>
                                    </li>
                                </ol>
                            </div>
                        </li>
                    <?php }
                }if ($footer_row['admin_expert_show'] == 1) {
                if ($admin_row['admin_service_expert_options'] == 1) { ?>
                    <li><h4>Service Experts</h4></li>
                    <li class="ic-eve">
                        <a href="#"
                           class="<?php if ($current_page == 'expert-users.php' || $current_page == 'expert-new-create.php' || $current_page == 'expert-leads.php' || $current_page == 'expert-general-leads.php' || $current_page == 'expert-admin-info.php') {
                               echo 'mact';
                           } ?>">Service Experts</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="expert-users.php">All Experts</a>
                                </li>
                                <li>
                                    <a href="expert-new-create.php">Add new Expert</a>
                                </li>
                                <li>
                                    <a href="expert-leads.php">All Expert Leads</a>
                                </li>
                                <li>
                                    <a href="expert-general-leads.php">All General Leads</a>
                                </li>
                                <li>
                                    <a href="expert-admin-info.php">Service Expert Admin Info</a>
                                </li>

                            </ol>
                        </div>
                    </li>
                    <li class="ic-cat">
                        <a href="#"
                           class="<?php if ($current_page == 'expert-all-category.php' || $current_page == 'expert-add-new-category.php' || $current_page == 'expert-all-sub-category.php' || $current_page == 'expert-add-new-sub-category.php' || $current_page == 'expert-home-category-change.php') {
                               echo 'mact';
                           } ?>">Experts Category</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="expert-all-category.php">All Category</a>
                                </li>
                                <li>
                                    <a href="expert-add-new-category.php">Add new Category</a>
                                </li>
                                <li>
                                    <a href="expert-home-category-change.php">Homepage Category Order</a>
                                </li>
                                <li>
                                    <a href="expert-all-sub-category.php">All Sub Category</a>
                                </li>
                                <li>
                                    <a href="expert-add-new-sub-category.php">Add new Sub Category</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                    <li class="ic-cit">
                        <a href="#"
                           class="<?php if ($current_page == 'expert-all-city.php' || $current_page == 'expert-add-new-city.php' || $current_page == 'expert-edit-city.php' || $current_page == 'expert-delete-city.php' || $current_page == 'expert-all-area.php' || $current_page == 'expert-add-new-area.php' || $current_page == 'expert-edit-area.php' || $current_page == 'expert-delete-area.php') {
                               echo 'mact';
                           } ?>">Expert Cities & Areas</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="expert-all-city.php">All Expert City</a>
                                </li>
                                <li>
                                    <a href="expert-add-new-city.php">Add New Expert City</a>
                                </li>
                                <li>
                                    <a href="expert-all-area.php">All Expert Areas</a>
                                </li>
                                <li>
                                    <a href="expert-add-new-area.php">Add New Expert Area</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                    <li class="ic-pay-acc">
                        <a href="#"
                           class="<?php if ($current_page == 'expert-payment-accept.php' || $current_page == 'expert-add-new-payment.php' || $current_page == 'expert-delete-payment.php' || $current_page == 'expert-edit-payment.php') {
                               echo 'mact';
                           } ?>">Accept Payment Modes</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="expert-payment-accept.php">Payments types</a>
                                </li>
                                <li>
                                    <a href="expert-add-new-payment.php">Add New Payment type</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                <?php }}if ($footer_row['admin_job_show'] == 1) {
                if ($admin_row['admin_jobs_options'] == 1) { ?>
                    <li><h4>Jobs</h4></li>
                    <li class="ic-eve">
                        <a href="#"
                           class="<?php if ($current_page == 'job-all.php' || $current_page == 'job-applicant-profiles.php' || $current_page == 'job-seeker-details.php' || $current_page == 'job-create.php' || $current_page == 'job-all-applied.php' || $current_page == 'jobs-premium.php' || $current_page == 'jobs-premium-edit.php') {
                               echo 'mact';
                           } ?>">Jobs</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="job-all.php">All Jobs</a>
                                </li>
                                <li>
                                    <a href="job-create.php">Add new Job post</a>
                                </li>
                                <li>
                                    <a href="job-seeker-details.php">Job seeker details</a>
                                </li>
                                <li>
                                    <a href="job-all-applied.php">All Applied Jobs</a>
                                </li>
                                <li>
                                    <a href="jobs-premium.php">Home Page Premium Jobs</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                    <li class="ic-cat">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-all-job-category.php' || $current_page == 'admin-add-new-job-category.php' || $current_page == 'admin-all-job-sub-category.php' || $current_page == 'admin-add-new-job-sub-category.php') {
                               echo 'mact';
                           } ?>">Job Category</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-all-job-category.php">All Category</a>
                                </li>
                                <li>
                                    <a href="admin-add-new-job-category.php">Add new Category</a>
                                </li>
                                <li>
                                    <a href="admin-all-job-sub-category.php">All Sub Category</a>
                                </li>
                                <li>
                                    <a href="admin-add-new-job-sub-category.php">Add new Sub Category</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                    <li class="ic-cat">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-all-job-skill-set.php' || $current_page == 'admin-add-new-job-skill-set.php') {
                               echo 'mact';
                           } ?>">Job Skill Set</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-all-job-skill-set.php">All Skill Set</a>
                                </li>
                                <li>
                                    <a href="admin-add-new-job-skill-set.php">Add new Skill Set</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                    <li class="ic-cit">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-all-job-city.php' || $current_page == 'admin-add-job-city.php') {
                               echo 'mact';
                           } ?>">Job City</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-all-job-city.php">All Job City</a>
                                </li>
                                <li>
                                    <a href="admin-add-job-city.php">Add New Job City</a>
                                </li>
                            </ol>
                        </div>
                    </li>

                <?php }}if ($footer_row['admin_product_show'] == 1) {
                if ($admin_row['admin_product_options'] == 1) { ?>
                    <li><h4>Products</h4></li>
                    <li class="ic-prod">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-all-products.php' || $current_page == 'admin-add-new-product.php') {
                               echo 'mact';
                           } ?>">Products</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-all-products.php">All Products</a>
                                </li>
                                <li>
                                    <a href="admin-add-new-product.php">Add new Product</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                <?php }
                if ($admin_row['admin_product_category_options'] == 1) { ?>
                    <li class="ic-cat">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-all-product-category.php' || $current_page == 'admin-add-new-product-category.php' || $current_page == 'admin-all-product-sub-category.php' || $current_page == 'admin-add-new-product-sub-category.php') {
                               echo 'mact';
                           } ?>">Product Category</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-all-product-category.php">All Category</a>
                                </li>
                                <li>
                                    <a href="admin-add-new-product-category.php">Add new Category</a>
                                </li>
                                <li>
                                    <a href="admin-all-product-sub-category.php">All Sub Category</a>
                                </li>
                                <li>
                                    <a href="admin-add-new-product-sub-category.php">Add new Sub Category</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                <?php } }if ($footer_row['admin_event_show'] == 1){
                if ($admin_row['admin_event_options'] == 1) { ?>
                    <li><h4>Events</h4></li>
                    <li class="ic-eve">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-event.php' || $current_page == 'admin-add-new-event.php') {
                               echo 'mact';
                           } ?>">Events</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-event.php">All Events</a>
                                </li>
                                <li>
                                    <a href="admin-add-new-event.php">Add new Events</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                <?php }}if ($footer_row['admin_blog_show'] == 1){
                if ($admin_row['admin_blog_options'] == 1) { ?>
                    <li><h4>Blogs</h4></li>
                    <li class="ic-blo">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-all-blogs.php' || $current_page == 'admin-add-new-blogs.php') {
                               echo 'mact';
                           } ?>">Blogs</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-all-blogs.php">All Blogs</a>
                                </li>
                                <li>
                                    <a href="admin-add-new-blogs.php">Add new Blogs</a>
                                </li>
                            </ol>
                        </div>
                    </li>


                <?php }}if ($footer_row['admin_coupon_show'] == 1){
                if ($admin_row['admin_feedback_options'] == 1) { ?>
                    <li><h4>Coupon & Deals</h4></li>
                    <li class="ic-coup">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-coupons.php' || $current_page == 'admin-add-new-coupons.php' || $current_page == 'admin-edit-coupons.php') {
                               echo 'mact';
                           } ?>">Coupon and deals</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-coupons.php">All Coupons</a>
                                </li>
                                <li>
                                    <a href="admin-add-new-coupons.php">Add new coupon</a>
                                </li>
                            </ol>
                        </div>
                    </li>

                <?php } }if ($footer_row['admin_news_show'] == 1){
                if ($admin_row['admin_news_options'] == 1) { ?>
                    <li><h4>News & Magazines</h4></li>
                    <li class="ic-news">
                        <a href="#"
                           class="<?php if ($current_page == 'news-all.php' || $current_page == 'news-add-new.php') {
                               echo 'mact';
                           } ?>">All News Posts</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="news-all.php">All News</a>
                                </li>
                                <li>
                                    <a href="news-add-new.php">Add new news</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                    <li class="ic-news">
                        <a href="#"
                           class="<?php if ($current_page == 'news-all-category.php' || $current_page == 'news-add-new-category.php' || $current_page == 'news-category-position.php') {
                               echo 'mact';
                           } ?>">Category</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="news-all-category.php">All Category</a>
                                </li>
                                <li>
                                    <a href="news-add-new-category.php">Add new Category</a>
                                </li>
                                <li>
                                    <a href="news-category-position.php">Category menu order</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                    <li class="ic-news">
                        <a href="#"
                           class="<?php if ($current_page == 'news-home-trending.php' || $current_page == 'news-home-trending-edit.php' || $current_page == 'news-home-trending-position.php' || $current_page == 'news-home-sliders.php' || $current_page == 'news-home-sliders-edit.php' || $current_page == 'news-home-sliders-position.php' || $current_page == 'news-home-sliders-add.php' || $current_page == 'news-home-social-media.php' || $current_page == 'news-home-social-media-edit.php') {
                               echo 'mact';
                           } ?>">News Home Page</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="news-home-trending.php">Trending posts</a>
                                </li>
                                <li>
                                    <a href="news-home-trending-position.php">Trending posts menu order</a>
                                </li>
                                <li>
                                    <a href="news-home-sliders.php">Slider posts</a>
                                </li>
                                <li>
                                    <a href="news-home-sliders-position.php">Slider posts menu order</a>
                                </li>
                                <li>
                                    <a href="news-home-social-media.php">Social Media</a>
                                </li>
                            </ol>
                        </div>
                    </li>

                    <li class="ic-logo">
                        <a class="<?php if ($current_page == 'news-subscribers.php') {
                            echo 'mact';
                        } ?>" href="news-subscribers.php">News Subscribers</a>
                    </li>

                <?php } }if ($footer_row['admin_place_show'] == 1){
                if ($admin_row['admin_news_options'] == 1) { ?>
                    <li><h4>Places</h4></li>
                    <li class="ic-place">
                        <a class="<?php if ($current_page == 'place-all.php' || $current_page == 'place-add-new.php') {
                            echo 'mact';
                        } ?>" href="place-all.php">All Places</a>
                    </li>
                    <li class="ic-cat">
                        <a href="#"
                           class="<?php if ($current_page == 'place-all-category.php' || $current_page == 'place-add-new-category.php' || $current_page == 'place-category-position.php' ) {
                               echo 'mact';
                           } ?>">Category</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="place-all-category.php">All Category</a>
                                </li>
                                <li>
                                    <a href="place-category-position.php">Category menu order</a>
                                </li>
                            </ol>
                        </div>
                    </li>

                    <li class="ic-place">
                        <a class="<?php if ($current_page == 'place-request.php') {
                            echo 'mact';
                        } ?>" href="place-request.php">Place request</a>
                    </li>

                <?php } } ?>
                    <li><h4>Payments</h4></li>
                <?php if ($admin_row['admin_payment_options'] == 1) { ?>
                    <li class="ic-pay">
                        <a class="<?php if ($current_page == 'admin-all-payments.php') {
                            echo 'mact';
                        } ?>" href="admin-all-payments.php">All Payments</a>
                    </li>
                    <?php } if ($admin_row['admin_invoice_options'] == 1) { ?>
                        <li class="ic-inv">
                            <a href="#"
                               class="<?php if ($current_page == 'admin-invoice-create.php' || $current_page == 'admin-send-invoice.php' || $current_page == 'admin-invoice-shared.php') {
                                   echo 'mact';
                               } ?>">Invoice</a>
                            <div>
                                <ol>
                                    <li>
                                        <a href="admin-invoice-create.php">Create new Invoice</a>
                                    </li>
                                    <li>
                                        <a href="admin-send-invoice.php">Send Invoice</a>
                                    </li>
                                    <li>
                                        <a href="admin-invoice-shared.php">Shared Invoices</a>
                                    </li>
                                </ol>
                            </div>
                        </li>
                    <?php }
                    if ($admin_row['admin_listing_price_options'] == 1) { ?>
                        <li class="ic-pri">
                            <a class="<?php if ($current_page == 'admin-price.php') {
                                echo 'mact';
                            } ?>" href="admin-price.php">Pricing Plans</a>
                        </li>
                    <?php }
                    if ($admin_row['admin_payment_options'] == 1) { ?>
                        <li class="ic-pay">
                            <a class="<?php if ($current_page == 'admin-payment-credentials.php') {
                                echo 'mact';
                            } ?>" href="admin-payment-credentials.php">Payment gateway</a>
                        </li>

                    <?php }
                if ($admin_row['admin_ads_options'] == 1) { ?>
                    <li><h4>ADS</h4></li>
                    <li class="ic-ads">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-current-ads.php' || $current_page == 'admin-create-ads.php' || $current_page == 'admin-ads-request.php' || $current_page == 'admin-ads-price.php' || $current_page == 'admin-ads-google-integration.php' || $current_page == 'admin-ads-history.php' || $current_page == 'seo-google-adsense.php') {
                               echo 'mact';
                           } ?>">Ads</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-current-ads.php">Current Ads</a>
                                </li>
                                <li>
                                    <a href="admin-create-ads.php">Create new Ads</a>
                                </li>
                                <li>
                                    <a href="admin-ads-request.php">Ad Request & Enquiry</a>
                                </li>
                                <li>
                                    <a href="admin-ads-price.php">Ad Pricing</a>
                                </li>
                                <li>
                                    <a href="seo-google-adsense.php">Google AdSense</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                <?php } ?>

                <li class="ic-slid">
                    <a href="#"
                       class="<?php if ($current_page == 'admin-slider-all.php' || $current_page == 'admin-slider-create.php' || $current_page == 'admin-slider-edit.php' || $current_page == 'admin-slider-delete.php') {
                           echo 'mact';
                       } ?>">Slider Images</a>
                    <div>
                        <ol>
                            <li>
                                <a href="admin-slider-all.php">All Slider Images</a>
                            </li>
                            <li>
                                <a href="admin-slider-create.php">Add New Slider</a>
                            </li>
                        </ol>
                    </div>
                </li>
                <li><h4>Settings</h4></li>
                <?php if ($admin_row['admin_setting_options'] == 1) { ?>
                    <li class="ic-set">
                        <a class="<?php if ($current_page == 'admin-setting.php') {
                            echo 'mact';
                        } ?>" href="admin-setting.php">Site Setting</a>
                    </li>
                <?php } ?>
                <?php if ($admin_row['admin_appearance_options'] == 1) { ?>
                    <li><h4>Appearance</h4></li>
                    <li class="ic-logo">
                        <a class="<?php if ($current_page == 'admin-logo.php') {
                            echo 'mact';
                        } ?>" href="admin-logo.php">Website Logo</a>
                    </li>
                    <li class="ic-colr">
                        <a class="<?php if ($current_page == 'color-setting.php') {
                            echo 'mact';
                        } ?>" href="color-setting.php">Color Setting</a>
                    </li>
                    <li class="ic-feat">
                        <a class="<?php if ($current_page == 'features-enable-disable.php') {
                            echo 'mact';
                        } ?>" href="features-enable-disable.php">Features Enable & Disable</a>
                    </li>
                    <li class="ic-medi">
                        <a class="<?php if ($current_page == 'media-library.php') {
                            echo 'mact';
                        } ?>" href="media-library.php">Media Library</a>
                    </li>

                <?php }
                if ($admin_row['admin_text_options'] == 1) { ?>
                    <li><h4>CMS</h4></li>
                    <li class="ic-hom">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-home-top-section.php' || $current_page == 'admin-home-top-section-edit.php' || $current_page == 'admin-home-category.php' || $current_page == 'admin-trending-category.php' || $current_page == 'admin-home-top-services.php' || $current_page == 'admin-home-feature-events.php' || $current_page == 'admin-home-youtube-video.php' || $current_page == 'home-page-template.php') {
                               echo 'mact';
                           } ?>">Home Page</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-home-top-section.php">Top Section</a>
                                </li>
                                <li>
                                    <a href="admin-home-category.php">Choose Category</a>
                                </li>
                                <li>
                                    <a href="admin-trending-category.php">Choose Trending Category</a>
                                </li>
                                <li>
                                    <a href="admin-home-popular-business.php">Popular Business</a>
                                </li>
                                <li>
                                    <a href="admin-home-top-services.php">Top Services</a>
                                </li>
                                <li>
                                    <a href="admin-home-feature-events.php">Feature Events</a>
                                </li>
                                <li>
                                    <a href="home-page-template.php">Home page template</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                    <li class="ic-txt">
                        <a class="<?php if ($current_page == 'admin-text-changes.php') {
                            echo 'mact';
                        } ?>" href="admin-text-changes.php">All Text Changes</a>
                    </li>
                <?php }
                if ($admin_row['admin_footer_options'] == 1) { ?>
                    <li class="ic-sub">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-footer.php' || $current_page == 'admin-footer-popular-tags.php') {
                               echo 'mact';
                           } ?>">Footer</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-footer.php">Footer CMS</a>
                                </li>
                                <li>
                                    <a href="admin-footer-popular-tags.php">Footer popular tags</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                <?php }
                if ($_SESSION['admin_id'] == 1) { ?>

                <?php }
                if ($admin_row['admin_dummy_image_options'] == 1) { ?>
                    <li class="ic-dum">
                        <a class="<?php if ($current_page == 'admin-dummy-images.php') {
                            echo 'mact';
                        } ?>" href="admin-dummy-images.php">Dummy Images</a>
                    </li>
                <?php }
                if ($admin_row['admin_mail_template_options'] == 1) { ?>
                    <li class="ic-mail">
                        <a href="admin-all-mail.php"
                           class="<?php if ($current_page == 'admin-all-mail.php' || $current_page == 'admin-mail-view.php') {
                               echo 'mact';
                           } ?>">Mail Templates</a>
                    </li>
                <?php }
                if ($admin_row['admin_mail_template_options'] == 1) { ?>
                    <li class="ic-soci">
                        <a href="admin-social-share.php" class="<?php if ($current_page == 'admin-social-share.php') {
                            echo 'mact';
                        } ?>">Social media share</a>
                    </li>

                <?php }
                if ($admin_row['admin_feedback_options'] == 1) { ?>
                    <li><h4>Others</h4></li>
                    <li class="ic-febk">
                        <a href="#" class="<?php if ($current_page == 'admin-all-feedbacks.php') {
                            echo 'mact';
                        } ?>">Feedbacks</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-all-feedbacks.php">All Feedbacks</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                <?php }
                if ($admin_row['admin_notification_options'] == 1) { ?>
                    <li class="ic-noti">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-notification-all.php' || $current_page == 'admin-create-notification.php') {
                               echo 'mact';
                           } ?>">Send Notifications</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-notification-all.php">All Notifications</a>
                                </li>
                                <li>
                                    <a href="admin-create-notification.php">Create New Notifications</a>
                                </li>
                            </ol>
                        </div>
                    </li>

                <?php }
                if ($admin_row['admin_import_options'] == 1) { ?>
                    <li class="ic-imp">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-import.php' || $current_page == 'admin-export.php') {
                               echo 'mact';
                           } ?>">Import & Export</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-import.php">Import Data</a>
                                </li>
                                <li>
                                    <a href="admin-export.php">Export Data</a>
                                </li>
                            </ol>
                        </div>
                    </li>
                <?php }
                if ($admin_row['admin_sub_admin_options'] == 1) { ?>
                    <li class="ic-sub">
                        <a href="#"
                           class="<?php if ($current_page == 'admin-sub-admin-all.php' || $current_page == 'admin-sub-admin-create.php' || $current_page == 'admin-sub-admin-log.php') {
                               echo 'mact';
                           } ?>">Sub Admin</a>
                        <div>
                            <ol>
                                <li>
                                    <a href="admin-sub-admin-all.php">All Sub Admins</a>
                                </li>
                                <li>
                                    <a href="admin-sub-admin-create.php">Create new Sub Admin</a>
                                </li>
                            </ol>
                        </div>
                    </li>

                <?php }
                if ($admin_row['admin_mail_template_options'] == 1) { ?>
                    <li><h4>Bizbook template </h4></li>
                    <li class="ic-act">
                        <a href="activate.php" class="<?php if ($current_page == 'activate.php') {
                            echo 'mact';
                        } ?>">Activation</a>
                    </li>
                <?php }
                if ($admin_row['admin_mail_template_options'] == 1) { ?>
                    <li class="ic-upd">
                        <a href="updates.php" class="<?php if ($current_page == 'updates.php') {
                            echo 'mact';
                        } ?>">Bizbook updates</a>
                    </li>
                <?php } ?>
                <li class="ic-set">
                    <a href="admin-security-updates.php"
                       class="<?php if ($current_page == 'admin-security-updates.php') {
                           echo 'mact';
                       } ?>">Security & Update News</a>
                </li>
                <li><h4>Sign out </h4></li>
                <li class="ic-lgo">
                    <a href="logout.php">Log out</a>
                </li>
            </ul>
        </div>
    </div>
</section>
<!-- END -->