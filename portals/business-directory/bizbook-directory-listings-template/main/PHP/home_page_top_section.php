<?php
if($current_home_page == '2' || $current_home_page == '3') {
    ?>

    <!-- START -->
    <section class="news-top-menu">
        <div class="container">
            <div class="row">
                <div class="news-menu">
                    <ul>
                        <li><a href="<?php echo $webpage_full_link; ?>" class="act"><?php echo $BIZBOOK['HOME']; ?></a></li>
                        <li><a href="<?php echo $webpage_full_link; ?>all-category"><?php echo $BIZBOOK['ALL_SERVICES']; ?></a></li>
                        <li><a href="<?php echo $webpage_full_link; ?>service-experts"><?php echo $BIZBOOK['SERVICE-EXPERTS']; ?></a></li>
                        <li><a href="<?php echo $webpage_full_link; ?>jobs"><?php echo $BIZBOOK['JOBS']; ?></a></li>
                        <li><a href="<?php echo $webpage_full_link; ?>news"><?php echo $BIZBOOK['NEWS']; ?></a></li>
                        <li><a href="<?php echo $webpage_full_link; ?>all-products"><?php echo $BIZBOOK['PRODUCTS']; ?></a></li>
                        <li><a href="<?php echo $webpage_full_link; ?>events"><?php echo $BIZBOOK['EVENTS']; ?></a></li>
                        <li><a href="<?php echo $webpage_full_link; ?>coupons"><?php echo $BIZBOOK['COUPONS']; ?></a></li>
                        <li><a href="<?php echo $webpage_full_link; ?>blog-posts"><?php echo $BIZBOOK['BLOGS']; ?></a></li>
                        <li><a href="<?php echo $webpage_full_link; ?>community"><?php echo $BIZBOOK['COMMUNITY']; ?></a></li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
    <!--END-->

    <?php
}
if ($current_home_page == '4' || $current_home_page == '5' || $current_home_page == '6' || $current_home_page == '7' || $current_home_page == '8' || $current_home_page == '9') {
    ?>

    <!-- START -->
    <section>
        <div class="str hm3-auto-ban">
            <div class="container">
                <div class="row">
                    <div class="lhs">
                        <?php if ($current_home_page == '4') { ?>
                            <span><?php echo $BIZBOOK['HOM-NO1-BEST-CHOICE']; ?></span>
                            <h1><?php echo $BIZBOOK['HOM-FIND-YOUR-RIGHT']; ?><br><b><?php echo $BIZBOOK['HOM-CAR']; ?></b> <?php echo $BIZBOOK['HOM-NOW']; ?></h1>
                            <p><?php echo $BIZBOOK['HOM-P-TAG-PAGE-4']; ?></p>
                            <a href="<?php echo $webpage_full_link; ?>all-category"><?php echo $BIZBOOK['HOM-EXPLORE-PAGE-4']; ?></a>

                        <?php } elseif ($current_home_page == '5') { ?>
                            <span><?php echo $BIZBOOK['HOM-NO1-BEST-CHOICE']; ?></span>
                            <h1><?php echo $BIZBOOK['HOM-FIND-YOUR-RIGHT']; ?><br><b id="changingword"><?php echo $BIZBOOK['HOM-PROPERTY']; ?></b> <?php echo $BIZBOOK['HOM-HERE']; ?></h1>
                            <p><?php echo $BIZBOOK['HOM-P-TAG-PAGE-5']; ?></p>
                            <a href="<?php echo $webpage_full_link; ?>all-category"><?php echo $BIZBOOK['HOM-EXPLORE-PAGE-5']; ?></a>

                        <?php } elseif ($current_home_page == '6') { ?>
                            <span><?php echo $BIZBOOK['HOM-SAY-HELLO-DOCTOR']; ?></span>
                            <h1><?php echo $BIZBOOK['HOM-FIND-YOUR-RIGHT']; ?><br><b id=""><?php echo $BIZBOOK['HOM-DOCTORS']; ?></b> <?php echo $BIZBOOK['HOM-HERE']; ?></h1>
                            <p><?php echo $BIZBOOK['HOM-P-TAG-PAGE-6']; ?></p>
                            <a href="<?php echo $webpage_full_link; ?>all-category"><?php echo $BIZBOOK['HOM-EXPLORE-PAGE-6']; ?></a>

                        <?php } elseif ($current_home_page == '7') { ?>

                            <span><?php echo $BIZBOOK['HOM-NO1-SALON-SPA']; ?></span>
                            <h1><?php echo $BIZBOOK['HOM-FIND-YOUR-RIGHT']; ?><br><b id=""><?php echo $BIZBOOK['HOM-SPA-SALON']; ?></b> <?php echo $BIZBOOK['HOM-NOW']; ?></h1>
                            <p><?php echo $BIZBOOK['HOM-P-TAG-PAGE-7']; ?></p>
                            <a href="<?php echo $webpage_full_link; ?>all-category"><?php echo $BIZBOOK['HOM-EXPLORE-PAGE-7']; ?></a>

                        <?php } elseif ($current_home_page == '8') { ?>

                            <span><?php echo $BIZBOOK['HOM-NO1-HOTEL-BOOKING']; ?></span>
                            <h1><?php echo $BIZBOOK['HOM-FIND-YOUR-RIGHT']; ?><br><b id=""><?php echo $BIZBOOK['HOM-HOTELS-RESORTS']; ?></b> <?php echo $BIZBOOK['HOM-HERE']; ?></h1>
                            <p><?php echo $BIZBOOK['HOM-P-TAG-PAGE-8']; ?></p>
                            <a href="<?php echo $webpage_full_link; ?>all-category"><?php echo $BIZBOOK['HOM-EXPLORE-PAGE-7']; ?></a>

                        <?php } elseif ($current_home_page == '9') { ?>

                            <span><?php echo $BIZBOOK['HOM-RESTURANT-IN-POCKET']; ?></span>
                            <h1><?php echo $BIZBOOK['HOM-ORDER-YOUR']; ?><br><b id=""><?php echo $BIZBOOK['HOM-FOOD-ONLINE']; ?></b> <?php echo $BIZBOOK['HOM-NOW']; ?></h1>
                            <p><?php echo $BIZBOOK['HOM-P-TAG-PAGE-9']; ?></p>
                            <a href="<?php echo $webpage_full_link; ?>all-category"><?php echo $BIZBOOK['HOM-EXPLORE-PAGE-9']; ?></a>
                            
                            <?php
                        }
                        ?>
                    </div>
                    <div class="rhs">
                        <div class="hom-col-req">
                            <div class="log-bor">&nbsp;</div>
                            <span class="udb-inst"><?php echo $BIZBOOK['LEAD-FILL-THE-FORM']; ?></span>
                            <h4><?php echo $BIZBOOK['HOM-WHT-LOOK-TIT']; ?></h4>
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
                                <input type="hidden" class="form-control" name="listing_id" value="0" placeholder=""
                                       required>
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
                                <div class="form-group">
                                    <input type="text" name="enquiry_name" value="" required="required"
                                           class="form-control" placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>">
                                </div>
                                <div class="form-group">
                                    <input type="email" class="form-control" placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>"
                                           required="required" value="" name="enquiry_email"
                                           pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                           title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>">
                                </div>
                                <div class="form-group">
                                    <input type="text" class="form-control" value="" name="enquiry_mobile"
                                           placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>" pattern="[7-9]{1}[0-9]{9}"
                                           title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>"
                                           required="">
                                </div>
                                <div class="form-group">
                                    <select name="enquiry_category" id="enquiry_category" class="form-control">
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
                                <button type="submit" id="home_enquiry_submit" name="home_enquiry_submit"
                                        class="btn btn-primary">
                                    <?php echo $BIZBOOK['SUBMIT_REQUIREMENTS']; ?>
                                </button>
                            </form>
                            <div class="log-bor">&nbsp;</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- END -->
    <?php
}
?>