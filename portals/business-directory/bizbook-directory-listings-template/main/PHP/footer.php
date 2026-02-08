<!-- START -->

<span class="btn-ser-need-ani"><img src="<?php echo $slash; ?>images/icon/help.png" alt=""></span>

<div class="ani-quo-form">
    <i class="material-icons ani-req-clo">close</i>
    <div class="tit">
        <h3><?php echo $BIZBOOK['HOM-WHAT-SER']; ?> <span><?php echo $BIZBOOK['HOM-WHAT-BIZ-BOOK-HELP-YOU']; ?></span></h3>
    </div>
    <div class="hom-col-req">
        <div id="home_slide_enq_success" class="log"
             style="display: none;">
            <p><?php echo $BIZBOOK['ENQUIRY_SUCCESSFUL_MESSAGE']; ?></p>
        </div>
        <div id="home_slide_enq_fail" class="log" style="display: none;">
            <p><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></p>
        </div>
        <div id="home_slide_enq_same" class="log" style="display: none;">
            <p><?php echo $BIZBOOK['ENQUIRY_OWN_LISTING_MESSAGE']; ?></p>
        </div>
        <form name="home_slide_enquiry_form" id="home_slide_enquiry_form" method="post" enctype="multipart/form-data">
            <input type="hidden" class="form-control"
                   name="listing_id"
                   value="0"
                   placeholder=""
                   required>
            <input type="hidden" class="form-control"
                   name="listing_user_id"
                   value="0"
                   placeholder=""
                   required>
            <input type="hidden" class="form-control"
                   name="enquiry_sender_id"
                   value=""
                   placeholder=""
                   required>
            <input type="hidden" class="form-control"
                   name="enquiry_source"
                   value="<?php if (isset($_GET["src"])) {
                       echo $_GET["src"];
                   } else {
                       echo "Website";
                   }; ?>"
                   placeholder=""
                   required>
            <div class="form-group">
                <input type="text" name="enquiry_name" value="" required="required" class="form-control"
                       placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>">
            </div>
            <div class="form-group">
                <input type="email" class="form-control" placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>" required="required" value=""
                       name="enquiry_email"
                       pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                       title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>">
            </div>
            <div class="form-group">
                <input type="text" class="form-control" value="" name="enquiry_mobile"
                       placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>" pattern="[7-9]{1}[0-9]{9}"
                       title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>" required="">
            </div>
            <div class="form-group">
                <select name="enquiry_category" id="enquiry_category" class="form-control chosen-select">
                    <option value=""><?php echo $BIZBOOK['SELECT_CATEGORY']; ?></option>
                    <?php
                    foreach (getAllCategories() as $categories_row) {
                        ?>
                        <option
                            value="<?php echo $categories_row['category_id']; ?>"><?php echo $categories_row['category_name']; ?></option>
                        <?php
                    }
                    ?>
                </select>
            </div>
            <div class="form-group">
                <textarea class="form-control" rows="3" name="enquiry_message"
                          placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
            </div>
            <input type="hidden" id="source">
            <button type="submit" id="home_slide_enquiry_submit" name="home_slide_enquiry_submit"
                    class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT_REQUIREMENTS']; ?>
            </button>
        </form>
    </div>
</div>
<!-- END -->

<!-- START -->
<section>
    <div class="full-bot-book">
        <div class="container">
            <div class="row">
                <?php if($footer_row['admin_install_flag'] == 0) { kwohereza($SHYIRAMO); }?>
                <div class="bot-book">
                    <div class="col-md-12 bb-text">
                        <h4><?php echo $BIZBOOK['FOOT-BAN-TIT']; ?></h4>
                        <p><?php echo $BIZBOOK['FOOT-BAN-SUB-TIT']; ?></p>
                        <a href="<?php echo $slash; ?>pricing-details"><?php echo $BIZBOOK['FOOT-BAN-ADD']; ?> <i class="material-icons">arrow_forward</i></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->
<?php if($footer_row['admin_install_flag'] == 1) { unlink("install1.php"); unlink("install2.php"); } ?>
<section class="<?php if($footer_row['admin_language']== 2){ echo "lg-arb";}?> wed-hom-footer">
    <div class="container">
        <div class="row foot-supp">
            <h2><span><?php echo $BIZBOOK['FOOTER-FREE-SUPPORT']; ?>:</span> <?php echo $footer_row['footer_mobile']; ?> &nbsp;&nbsp;|&nbsp;&nbsp; <span><?php echo $BIZBOOK['EMAIL']; ?>:</span> <?php echo $footer_row['admin_primary_email']; ?></h2>
        </div>
        <div class="row wed-foot-link">
            <div class="col-md-4 foot-tc-mar-t-o">
                <h4><?php echo $BIZBOOK['FOOTER-TOP-CATEGORY']; ?></h4>
                <ul>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['top_category_1']))); ?>"><?php echo getCategoryName($footer_row['top_category_1']); ?></a></li>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['top_category_2']))); ?>"><?php echo getCategoryName($footer_row['top_category_2']); ?></a></li>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['top_category_3']))); ?>"><?php echo getCategoryName($footer_row['top_category_3']); ?></a></li>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['top_category_4']))); ?>"><?php echo getCategoryName($footer_row['top_category_4']); ?></a></li>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['top_category_5']))); ?>"><?php echo getCategoryName($footer_row['top_category_5']); ?></a></li>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['top_category_6']))); ?>"><?php echo getCategoryName($footer_row['top_category_6']); ?></a></li>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['top_category_7']))); ?>"><?php echo getCategoryName($footer_row['top_category_7']); ?></a></li>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['top_category_8']))); ?>"><?php echo getCategoryName($footer_row['top_category_8']); ?></a></li>
                </ul>
            </div>
            <div class="col-md-4">
                <h4><?php echo $BIZBOOK['FOOTER-TRENDING-CATEGORY']; ?></h4>
                <ul>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['trend_category_1']))); ?>"><?php echo getCategoryName($footer_row['trend_category_1']); ?></a></li>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['trend_category_2']))); ?>"><?php echo getCategoryName($footer_row['trend_category_2']); ?></a></li>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['trend_category_3']))); ?>"><?php echo getCategoryName($footer_row['trend_category_3']); ?></a></li>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['trend_category_4']))); ?>"><?php echo getCategoryName($footer_row['trend_category_4']); ?></a></li>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['trend_category_5']))); ?>"><?php echo getCategoryName($footer_row['trend_category_5']); ?></a></li>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['trend_category_6']))); ?>"><?php echo getCategoryName($footer_row['trend_category_6']); ?></a></li>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['trend_category_7']))); ?>"><?php echo getCategoryName($footer_row['trend_category_7']); ?></a></li>
                    <li><a href="<?php echo $ALL_LISTING_URL . urlModifier(getCategoryName(strtolower($footer_row['trend_category_8']))); ?>"><?php echo getCategoryName($footer_row['trend_category_8']); ?></a></li>
                </ul>
            </div>
            <div class="col-md-4">
                <h4><?php echo $BIZBOOK['FOOTER-HELP']; ?> &amp; <?php echo $BIZBOOK['FOOTER-SUPPORT']; ?></h4>
                <ul>
                    <li><a href="<?php echo $slash; ?><?php echo $footer_row['footer_page_url_1']; ?>"><?php echo $footer_row['footer_page_name_1']; ?></a>
                    </li>
                    <li><a href="<?php echo $slash; ?><?php echo $footer_row['footer_page_url_2']; ?>"><?php echo $footer_row['footer_page_name_2']; ?></a>
                    </li>
                    <li><a href="<?php echo $slash; ?><?php echo $footer_row['footer_page_url_3']; ?>"><?php echo $footer_row['footer_page_name_3']; ?></a>
                    </li>
                    <li><a href="<?php echo $slash; ?><?php echo $footer_row['footer_page_url_4']; ?>"><?php echo $footer_row['footer_page_name_4']; ?></a>
                    </li>
                    <li><a href="privacy-policy.php"><?php echo $BIZBOOK['pg_pri_tit']; ?></a></li>
                    <li><a href="terms-of-use.php"><?php echo $BIZBOOK['pg_terms_tit']; ?></a></li>
                </ul>
            </div>
        </div>

        <!-- POPULAR TAGS -->
        <div class="row wed-foot-link-pop">
            <div class="col-md-12">
                <h4><?php echo $BIZBOOK['FOOTER-POPULAR-TAGS']; ?></h4>
                <ul>
                    <?php
                    foreach (getAllPopularTags() as $popular_tags_row) {
                        ?>
                        <li><a href="<?php echo $popular_tags_row['popular_tags_link']; ?>"><?php echo $popular_tags_row['popular_tags_name']; ?></a></li>
                        <?php
                    }
                    ?>
                </ul>
            </div>
        </div>
        <!-- POPULAR TAGS -->


        <div class="row wed-foot-link-1">
            <?php if($footer_row['admin_get_in_touch_feature'] == 1) { ?>
            <div class="col-md-4">
                <h4><?php echo $BIZBOOK['FOOTER-GET-IN-TOUCH']; ?></h4>
                <p><?php echo $BIZBOOK['ADDRESS']; ?>: <?php echo $footer_row['footer_address']; ?></p>
                <p><?php echo $BIZBOOK['PHONE']; ?>: <a href="tel:<?php echo $footer_row['footer_mobile']; ?>"><?php echo $footer_row['footer_mobile']; ?></a></p>
                <p><?php echo $BIZBOOK['EMAIL']; ?>: <a href="mailto:<?php echo $footer_row['admin_primary_email']; ?>"><?php echo $footer_row['admin_primary_email']; ?></a></p>
            </div>
            <?php } ?>
            <?php if($footer_row['admin_footer_mobile_app_feature'] == 1) { ?>
            <div class="col-md-4 fot-app">
                <h4><?php echo $BIZBOOK['FOOTER-DOWNLOAD-FREE-MOBILE-APPS']; ?></h4>
                <ul>
                    <li><a href="<?php echo $footer_row['mobile_app_andriod']; ?>"><img src="<?php echo $slash; ?>images/gstore.png" alt=""></a>
                    </li>
                    <li><a href="<?php echo $footer_row['mobile_app_ios']; ?>"><img src="<?php echo $slash; ?>images/astore.png" alt=""></a>
                    </li>
                </ul>
            </div>
            <?php } ?>
            <div class="col-md-4 fot-soc">
                <h4><?php echo $BIZBOOK['FOOTER-SOCIAL-MEDIA']; ?></h4>
                <ul>
                    <li><a target="_blank" href="<?php echo $footer_row['footer_linked_in']; ?>"><img src="<?php echo $slash; ?>images/social/1.png" alt=""></a></li>
                    <li><a target="_blank" href="<?php echo $footer_row['footer_twitter']; ?>"><img src="<?php echo $slash; ?>images/social/2.png" alt=""></a></li>
                    <li><a target="_blank" href="<?php echo $footer_row['footer_fb']; ?>"><img src="<?php echo $slash; ?>images/social/3.png" alt=""></a></li>
                    <li><a target="_blank" href="<?php echo $footer_row['footer_whatsapp']; ?>"><img src="<?php echo $slash; ?>images/social/4.png" alt=""></a></li>
                    <li><a target="_blank" href="<?php echo $footer_row['footer_youtube']; ?>"><img src="<?php echo $slash; ?>images/social/5.png" alt=""></a></li>
                </ul>
            </div>
        </div>
        <?php if($footer_row['admin_country_list_feature'] == 1) { ?>
        <div class="row foot-count">
            <ul>
                <li><a target="_blank" href="http://<?php echo $footer_row['footer_country_url_1']; ?>"><?php echo $footer_row['footer_country_name_1']; ?></a></li>
                <li><a target="_blank" href="http://<?php echo $footer_row['footer_country_url_2']; ?>"><?php echo $footer_row['footer_country_name_2']; ?></a></li>
                <li><a target="_blank" href="http://<?php echo $footer_row['footer_country_url_3']; ?>"><?php echo $footer_row['footer_country_name_3']; ?></a></li>
                <li><a target="_blank" href="http://<?php echo $footer_row['footer_country_url_4']; ?>"><?php echo $footer_row['footer_country_name_4']; ?></a></li>
                <li><a target="_blank" href="http://<?php echo $footer_row['footer_country_url_5']; ?>"><?php echo $footer_row['footer_country_name_5']; ?></a></li>
                <li><a target="_blank" href="http://<?php echo $footer_row['footer_country_url_6']; ?>"><?php echo $footer_row['footer_country_name_6']; ?></a></li>
                <li><a target="_blank" href="http://<?php echo $footer_row['footer_country_url_7']; ?>"><?php echo $footer_row['footer_country_name_7']; ?></a></li>
            </ul>
        </div>
        <?php } ?>
    </div>
</section>

<!-- START -->
<section>
    <div class="cr">
        <div class="container">
            <div class="row">
                <p><?php echo $BIZBOOK['FOOTER-COPYRIGHT']; ?> © <?php echo $footer_row['copyright_year']; ?> <a href="<?php echo $footer_row['copyright_website_link']; ?>" target="_blank"><?php echo $footer_row['copyright_website']; ?></a>. <?php echo $BIZBOOK['FOOTER-PROUDLY-POWERED-BY']; ?> <a href="https://rn53themes.net/" target="_blank">Rn53Themes.net</a></p>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<!-- START -->
<div class="fqui-menu">
    <ul>
        <li><a href="<?php echo $webpage_full_link; ?>"><img src="<?php echo $slash; ?>images/icon/home.png"><?php echo $BIZBOOK['HOME']; ?></a></li>
        <li><span class="mob-sear"><img src="<?php echo $slash; ?>images/icon/search1.png"><?php echo $BIZBOOK['SEARCH']; ?></span></li>
        <li><a href="<?php echo $webpage_full_link; ?>all-category" class="act"><img src="<?php echo $slash; ?>images/icon/shop.png"><?php echo $BIZBOOK['SERVICES']; ?></a></li>
        <li><a href="<?php echo $webpage_full_link; ?>service-experts"><img src="<?php echo $slash; ?>images/icon/expert.png"><?php echo $BIZBOOK['SERVICE-EXPERTS']; ?></a></li>
        <li><a href="<?php echo $webpage_full_link; ?>jobs"><img src="<?php echo $slash; ?>jobs/images/icon/employee.png"><?php echo $BIZBOOK['JOBS']; ?></a></li>
        <li><a href="<?php echo $webpage_full_link; ?>places"><img src="<?php echo $slash; ?>images/places/icons/hot-air-balloon.png"><?php echo $BIZBOOK['PLACE-MENU']; ?></a></li>
        <li><a href="<?php echo $webpage_full_link; ?>news"><img src="<?php echo $slash; ?>images/icon/news.png"><?php echo $BIZBOOK['NEWS-MAGA']; ?></a></li>
        <li><a href="<?php echo $webpage_full_link; ?>events"><img src="<?php echo $slash; ?>images/icon/calendar.png"><?php echo $BIZBOOK['EVENTS']; ?></a></li>
        <li><a href="<?php echo $webpage_full_link; ?>all-products"><img src="<?php echo $slash; ?>images/icon/cart.png"><?php echo $BIZBOOK['PRODUCTS']; ?></a></li>
        <li><a href="<?php echo $webpage_full_link; ?>coupons"><img src="<?php echo $slash; ?>images/icon/coupons.png"><?php echo $BIZBOOK['COUPONS']; ?></a></li>
        <li><a href="<?php echo $webpage_full_link; ?>blog-posts"><img src="<?php echo $slash; ?>images/icon/blog1.png"><?php echo $BIZBOOK['BLOGS']; ?></a></li>
        <li><a href="<?php echo $webpage_full_link; ?>community"><img src="<?php echo $slash; ?>images/icon/11.png"><?php echo $BIZBOOK['COMMUNITY']; ?></a></li>
        <li><span class="btn-ser-need-ani"><img src="<?php echo $slash; ?>images/icon/how1.png"><?php echo $BIZBOOK['SUPPORT']; ?></span></li>
    </ul>
</div>
<!-- END -->