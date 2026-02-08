<style>
    .hom-top {
        display: none;
    }

    html {
        scroll-behavior: smooth;
    }
</style>

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

$company_row = getActiveUserCompany($user_codea); // To Fetch particular User Data

if ($company_row['user_id'] == NULL && empty($company_row['user_id'])) {


    header("Location: $redirect_url");  //Redirect When No User Found in Table
}

$profile_user_id = $company_row['user_id'];

businesspageview($profile_user_id); //Function To Find Page View

?>
<!-- START -->
<!-- //template-def //template-rhs -->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> abou-pg comp-pro-pg">
    <div class="com-pro-pg-head">
        <div class="container">
            <div class="row">
                <div class="comp-head">
                    <img src="<?php if (($company_row['company_header_photo'] == NULL) || empty($company_row['company_header_photo']))
                    { echo $slash; ?>images/home/<?php echo $footer_row['header_logo']; }
                    else{ echo $slash; ?>images/user/<?php echo $company_row['company_header_photo'];
                    } ?>" alt="">
                    <ul>
                        <li><a href="#about"><?php echo $BIZBOOK['ABOUT_US']; ?></a></li>
                        <li><a href="#prod"><?php echo $BIZBOOK['PRODUCTS']; ?></a></li>
                        <li><a href="#event"><?php echo $BIZBOOK['EVENTS']; ?></a></li>
                        <li><a href="#blog"><?php echo $BIZBOOK['BLOGS']; ?></a></li>
                        <li><a href="#home_enquiry_form" id="bus-pg-quot"><?php echo $BIZBOOK['LEAD-GET-QUOTE']; ?></a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    <div class="com-pro-pg-banner">
        <img
            src="<?php echo $slash; ?>images/user/<?php if (($company_row['company_banner_photo'] == NULL) || empty($company_row['company_banner_photo'])) {
                echo "images/all-list-bg.jpg";
            } else {
                echo $company_row['company_banner_photo'];
            } ?>" alt="">
    </div>
    <div class="com-pro-pg-bd">
        <div class="container">
            <div class="row">
                <!--START-->
                <div class="box-s1">
                    <div class="pro-pg-logo">
                        <img
                            src="<?php echo $slash; ?>images/user/<?php if (($company_row['company_profile_photo'] == NULL) || empty($company_row['company_profile_photo'])) {
                                echo "images/rn53.png";
                            } else {
                                echo $company_row['company_profile_photo'];
                            } ?>" alt="">
                    </div>
                    <div class="pro-pg-bio">
                        <h1><?php echo $company_row['company_name']; ?> <i class="li-veri" title="Verified"><img
                                    src="<?php echo $slash; ?>images/icon/svg/verified.png"></i></h1>
                        <ul class="bio">
                            <li><span><img
                                        src="<?php echo $slash; ?>images/icon/line/map.png"><?php echo $company_row['company_address']; ?></span>
                            </li>
                            <li><a href="<?php echo $BIZBOOK['TEL']; ?>:<?php echo $company_row['company_mobile']; ?>"><img
                                        src="<?php echo $slash; ?>images/icon/line/phone.png"> <?php echo $company_row['company_mobile']; ?>
                                </a></li>
                            <li><a href="mailto:<?php echo $company_row['company_email_id']; ?>"><img
                                        src="<?php echo $slash; ?>images/icon/line/email.png"> <?php echo $company_row['company_email_id']; ?>
                                </a></li>
                            <?php
                            if($company_row['company_website'] != NULL) {
                                ?>
                                <li><a target="_blank" href="<?php echo $company_row['company_website']; ?>"><img
                                            src="<?php echo $slash; ?>images/icon/line/website.png"> <?php echo $company_row['company_website']; ?>
                                    </a></li>
                                <?php
                            }
                            if($company_row['company_tax'] != NULL) {
                                ?>
                                <li><img src="<?php echo $slash; ?>images/icon/line/website.png">Tax no: <?php echo $company_row['company_tax']; ?>
                                </li>
                                <?php
                            }
                            ?>

                        </ul>
                        <ul class="soc">
                            <?php
                            if ($company_row['company_facebook'] != NULL) {
                                ?>
                                <li><a href="<?php echo $company_row['company_facebook']; ?>" target="_blank"><img
                                            src="<?php echo $slash; ?>images/icon/line/facebook.png"></a></li>
                                <?php
                            }
                            if ($company_row['company_twitter'] != NULL) {
                                ?>
                                <li><a href="<?php echo $company_row['company_twitter']; ?>" target="_blank"><img
                                            src="<?php echo $slash; ?>images/icon/line/twitter.png"></a></li>
                                <?php
                            }
                            if ($company_row['company_instagram'] != NULL) {
                                ?>
                                <li><a href="<?php echo $company_row['company_instagram']; ?>" target="_blank"><img
                                            src="<?php echo $slash; ?>images/icon/line/instagram.png"></a></li>
                                <?php
                            }
                            if ($company_row['company_linkedin'] != NULL) {
                                ?>
                                <li><a href="<?php echo $company_row['company_linkedin']; ?>" target="_blank"><img
                                            src="<?php echo $slash; ?>images/icon/line/linkedin.png"></a></li>
                                <?php
                            }
                            if ($company_row['company_whatsapp'] != NULL) {
                                ?>
                                <li><a href="<?php echo $company_row['company_whatsapp']; ?>" target="_blank"><img
                                            src="<?php echo $slash; ?>images/icon/line/whatsapp.png"></a></li>
                                <?php
                            }
                            if ($company_row['company_youtube'] != NULL) {
                                ?>
                                <li><a href="<?php echo $company_row['company_youtube']; ?>" target="_blank"><img
                                            src="<?php echo $slash; ?>images/icon/line/youtube.png"></a></li>
                                <?php
                            }
                            ?>
                        </ul>
                    </div>
                    <div class="pro-pg-cts">
                        <a href="#home_enquiry_form" class="cta1"><?php echo $BIZBOOK['LEAD-GET-QUOTE']; ?></a>
                        <a href="<?php echo $BIZBOOK['TEL']; ?>:<?php echo $company_row['company_mobile']; ?>" class="cta2"><?php echo $BIZBOOK['CALL_NOW']; ?></a>
                        <?php
                        if ($company_row['company_whatsapp'] != NULL) {
                            ?>
                            <a target="_blank" href="https://wa.me/<?php echo $company_row['company_whatsapp']; ?>"
                               class="cta3"><?php echo $BIZBOOK['WHATSAPP']; ?></a>
                            <?php
                        }
                        ?>
                    </div>
                </div>
                <!--END-->
                <!--START-->
                <div class="box-s2">
                    <div class="lhs">
                        <!--START-->
                        <div class="comp-abo" id="about">
                            <h2><?php echo $BIZBOOK['COMPANY-PROFILE-HEADING-LABEL']; ?></h2>
                            <p><?php echo stripslashes($company_row['company_description']); ?></p>
                        </div>
                        <!--END-->
                        <?php if (!empty($company_row['company_products'])) { ?>
                            <!--START-->
                            <div class="comp-pro" id="prod">
                                <h2><?php echo $BIZBOOK['PRODUCTS']; ?></h2>
                                <?php
                                $company_products_array = explode(',', $company_row['company_products']);
                                foreach ($company_products_array as $tuple) {

                                    $product_row = getIdProduct($tuple);
                                    ?>
                                    <div class="all-pro-box">
                                        <div class="all-pro-img">
                                            <img
                                                src="<?php echo $slash; ?><?php if ($product_row['gallery_image'] != NULL || !empty($product_row['gallery_image'])) {
                                                    echo "images/products/" . array_shift(explode(',', $product_row['gallery_image']));
                                                } else {
                                                    echo "images/products/192201.jpg";
                                                } ?>">
                                        </div>
                                        <div class="all-pro-aut">
                                            <div class="auth">
                                                <a target="_blank"
                                                   href="<?php echo $PRODUCT_URL.urlModifier($product_row['product_slug']); ?>"
                                                   class="fclick">
                                                </a>
                                            </div>
                                        </div>
                                        <div class="all-pro-txt">
                                            <h4><?php echo $product_row['product_name']; ?></h4>
                                            <span class="pri"><b
                                                    class="pro-off"><?php echo $footer_row['currency_symbol']; ?><?php echo $product_row['product_price']; ?></b> <?php if ($product_row['product_price_offer'] != NULL) {
                                                    echo $product_row['product_price_offer']; ?>% off<?php } ?></span>
                                            <div class="links">
                                                <a <?php if ($product_row['product_payment_link'] != NULL){ ?>
                                                    target="_blank"
                                                    href="<?php echo $product_row['product_payment_link'];
                                                    } else {
                                                        echo "#!";
                                                    } ?>"><?php echo $BIZBOOK['BUY_NOW']; ?></a></div>
                                        </div>
                                        <a target="_blank"
                                           href="<?php echo $PRODUCT_URL.urlModifier($product_row['product_slug']); ?>"
                                           class="pro-view-full"></a>
                                    </div>
                                    <?php
                                }
                                ?>
                            </div>
                            <!--END-->
                        <?php } ?>
                        <?php if (!empty($company_row['company_events'])) { ?>
                            <!--START-->
                            <div class="comp-pro" id="event">
                                <h2><?php echo $BIZBOOK['EVENTS']; ?></h2>
                                <?php
                                $company_events_array = explode(',', $company_row['company_events']);
                                foreach ($company_events_array as $tuple) {

                                    $eventrow = getEvent($tuple);
                                    ?>
                                    <div class="land-pack-grid">
                                        <div class="land-pack-grid-img">
                                            <img
                                                src="<?php echo $slash; ?>images/events/<?php echo $eventrow['event_image']; ?>"
                                                alt="">
                                        </div>
                                        <div class="land-pack-grid-text">
                                            <h4><?php echo $eventrow['event_name']; ?></h4>
                                        </div>
                                        <a target="_blank"
                                           href="<?php echo $EVENT_URL.urlModifier($eventrow['event_slug']); ?>"
                                           class="land-pack-grid-btn"></a>
                                    </div>
                                    <?php
                                }
                                ?>
                            </div>
                            <!--END-->
                        <?php } ?>
                        <?php if (!empty($company_row['company_blogs'])) { ?>
                            <!--START-->
                            <div class="comp-pro" id="blog">
                                <h2><?php echo $BIZBOOK['BLOGS']; ?></h2>
                                <?php
                                $company_blogs_array = explode(',', $company_row['company_blogs']);
                                foreach ($company_blogs_array as $tuple) {

                                    $blogrow = getBlog($tuple);
                                    ?>
                                    <div class="land-pack-grid">
                                        <div class="land-pack-grid-img">
                                            <img src="<?php echo $slash; ?>images/blogs/<?php echo $blogrow['blog_image']; ?>"
                                                 alt="">
                                        </div>
                                        <div class="land-pack-grid-text">
                                            <h4><?php echo $blogrow['blog_name']; ?></h4>
                                        </div>
                                        <a target="_blank"
                                           href="<?php echo $BLOG_URL.urlModifier($blogrow['blog_slug']); ?>"
                                           class="land-pack-grid-btn"></a>
                                    </div>
                                    <?php
                                }
                                ?>
                            </div>
                            <!--END-->
                        <?php } ?>
                    </div>
                    <div class="rhs">
                        <div class="cpro-form">
                            <div class="box templ-rhs-eve">
                                <div class="hot-page2-hom-pre-head">
                                    <h4><?php echo $BIZBOOK['LEAD-SEND-ENQUIRY']; ?></h4>
                                </div>
                                <div class="templ-rhs-form">
                                    <div id="home_enq_success" class="log"
                                         style="display: none;">
                                        <p><?php echo $BIZBOOK['ENQUIRY_SUCCESSFUL_MESSAGE']; ?></p>
                                    </div>
                                    <div id="home_enq_fail" class="log" style="display: none;">
                                        <p><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></p>
                                    </div>
                                    <div id="home_enq_same" class="log" style="display: none;">
                                        <p><?php echo $BIZBOOK['ENQUIRY_OWN_LISTING_MESSAGE']; ?></p>
                                    </div>
                                    <form name="home_enquiry_form" id="home_enquiry_form" method="post"
                                          enctype="multipart/form-data">
                                        <input type="hidden" class="form-control" name="listing_id" value="0"
                                               placeholder="" required>
                                        <input type="hidden" class="form-control" name="listing_user_id" value="0"
                                               placeholder="" required>
                                        <input type="hidden" class="form-control" name="enquiry_sender_id" value=""
                                               placeholder="" required>
                                        <input type="hidden" class="form-control"
                                               name="enquiry_source"
                                               value="<?php if (isset($_GET["src"])) {
                                                   echo $_GET["src"];
                                               } else {
                                                   echo "Website";
                                               }; ?>" placeholder="" required>
                                        <div class="form-group ic-user">
                                            <input type="text" name="enquiry_name" value="" required="required"
                                                   class="form-control" placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>" id="ic-user">
                                        </div>
                                        <div class="form-group ic-eml">
                                            <input type="email" class="form-control" placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>"
                                                   required="required" value="" name="enquiry_email"
                                                   pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                                   title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>">
                                        </div>
                                        <div class="form-group ic-pho">
                                            <input type="text" class="form-control" value="" name="enquiry_mobile"
                                                   placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>" pattern="[7-9]{1}[0-9]{9}"
                                                   title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>"
                                                   required="">
                                        </div>
                                        <div class="form-group">
                                            <textarea class="form-control" rows="3" name="enquiry_message"
                                                      placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                                        </div>
                                        <input type="hidden" id="source">
                                        <button type="submit" id="home_enquiry_submit" name="home_enquiry_submit"
                                                class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!--END-->
            </div>
        </div>
    </div>
</section>
<!--END-->


<?php
include "footer.php";
?>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link ='<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url ='<?php echo $LOGIN_URL;?>';</script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>
<script>
    $(document).ready(function () {
        $("#bus-pg-quot").click(function () {
            $("#ic-user").focus();
        });

    });
    ```
</script>
</body>

</html>