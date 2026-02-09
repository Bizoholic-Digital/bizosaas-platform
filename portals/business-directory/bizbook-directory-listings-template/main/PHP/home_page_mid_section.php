<?php
if ($current_home_page == '1') {
    ?>

    <!-- START -->
    <section>
        <div class="str">
            <div class="container">
                <div class="row">
                    <div class="home-tit">
                        <h2><span><?php echo $BIZBOOK['HOM-EXP-TIT']; ?></span> <?php echo $BIZBOOK['HOM-EXP-TIT1']; ?>
                        </h2>
                        <p><?php echo $BIZBOOK['HOM-EXP-SUB-TIT']; ?></p>
                    </div>
                    <div class="home-city">
                        <ul>
                            <?php
                            foreach (getAllTrendCategories() as $trendrow) {

                                $category_name = $trendrow['category_name'];

                                $category_sql_row = getCategory($category_name);

                                $category_id = $category_sql_row['category_id'];

                                ?>
                                <li>
                                    <div class="hcity">
                                        <div>
                                            <img src="images/services/<?php echo $trendrow['category_bg_image']; ?>"
                                                 alt="">
                                        </div>
                                        <div>
                                            <img src="images/services/<?php echo $trendrow['category_image']; ?>"
                                                 alt="">
                                            <h4><?php echo $category_sql_row['category_name']; ?></h4>
                                            <div class="list-rat-all">

                                                <?php
                                                $sum = $count = $review_count45 = 0;// initiate interger variables
                                                foreach (getAllListingCategory($category_sql_row['category_id']) as $categorywise_listings) {
                                                    $categorywise_listing_id = $categorywise_listings['listing_id'];

                                                    foreach (getListingReview($categorywise_listing_id) as $star_rating_row) {
                                                        if ($star_rating_row["rate_cnt"] > 0) {
                                                            $star_rate_times = $star_rating_row["rate_cnt"];
                                                            $star_sum_rates = $star_rating_row["total_rate"];
                                                            $star_rate_one = $star_sum_rates / $star_rate_times;
                                                            $star_rate_two = number_format($star_rate_one, 1);
                                                            $star_rate = $star_rate_two;

                                                        } else {
                                                            $rate_times = 0;
                                                            $rate_value = 0;
                                                            $star_rate = 0;
                                                        }

                                                    }
                                                    $review_count45 += getCountListingReview($categorywise_listing_id);
                                                    $sum += $star_rate;
                                                    if ($star_rate > 0) {
                                                        $count++; //add 1 on every loop
                                                    }

                                                }
                                                $new_star_rate = number_format($sum / $count, 1);
                                                if ($review_count45 == 0) {
                                                    $new_review_count = 0;
                                                } else {
                                                    $new_review_count = $review_count45;
                                                }


                                                ?>
                                                <b><?php if (AddingZero_BeforeNumber(getCountCategoryListing($category_id)) != 0) {

                                                        if ($new_star_rate != 0) {
                                                            echo $new_star_rate;
                                                        } else {
                                                            echo $BIZBOOK['ALL-LISTING-0-RATINGS'];
                                                        }
                                                    } else {
                                                        echo $BIZBOOK['ALL-LISTING-0-RATINGS'];
                                                    } ?></b>
                                                <?php
                                                if ($new_star_rate != 0 && AddingZero_BeforeNumber(getCountCategoryListing($category_id)) != 0) {
                                                    ?>
                                                    <label class="rat">
                                                        <?php
                                                        for ($i = 1; $i <= ceil($new_star_rate); $i++) {
                                                            ?>
                                                            <i class="material-icons">star</i>
                                                            <?php
                                                        }
                                                        $bal_star_rate = abs(ceil($new_star_rate) - 5);

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
                                                <?php if ($new_review_count > 0 && AddingZero_BeforeNumber(getCountCategoryListing($category_id)) != 0) { ?>
                                                    <span><?php echo $new_review_count; ?><?php echo $BIZBOOK['REVIEWS']; ?></span>
                                                    <?php
                                                }
                                                ?>
                                            </div>
                                            <p><?php echo AddingZero_BeforeNumber(getCountCategoryListing($category_id)); ?><?php echo $BIZBOOK['LISTINGS']; ?></p>
                                        </div>
                                        <a href="<?php echo $ALL_LISTING_URL . urlModifier($category_sql_row['category_slug']); ?>"
                                           class="fclick">&nbsp;</a>
                                    </div>
                                </li>
                                <?php
                            }
                            ?>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- END -->

    <!-- START -->
    <section>
        <div class="hom-mpop-ser">
            <div class="container">
                <div class="hom-mpop-main">
                    <div class="home-tit">
                        <h2><span><?php echo $BIZBOOK['HOM-BEST-TIT']; ?></span>
                        </h2>
                        <p><?php echo $BIZBOOK['HOM-BEST-SUB-TIT']; ?></p>
                    </div>

                    <!-- NEW FEATURE SERVICES -->
                    <div class="hom2-cus-sli">
                        <ul class="multiple-items1">
                            <?php
                            $pop_bus = 1;
                            foreach (getAllFeaturedListing() as $row) {

                                $listing_id = $row['listing_id'];

                                $listing_sql_row = getIdListing($listing_id);
                                $featured_category_id = $listing_sql_row['category_id'];

                                $popular_business_category_sql_row = getCategory($featured_category_id);

                                // List Rating. for Rating of Star
                                foreach (getListingReview($listing_id) as $star_rating_row) {
                                    if ($star_rating_row["rate_cnt"] > 0) {
                                        $star_rate_times = $star_rating_row["rate_cnt"];
                                        $star_sum_rates = $star_rating_row["total_rate"];
                                        $star_rate_one = $star_sum_rates / $star_rate_times;
                                        //$star_rate_one = (($Star_rate_value)/5)*100;
                                        $star_rate_two = number_format($star_rate_one, 1);
                                        $star_rate = $star_rate_two;

                                    } else {
                                        $rate_times = 0;
                                        $rate_value = 0;
                                        $star_rate = 0;
                                    }
                                }

                                ?>
                                <li>
                                    <div class="testmo hom4-prop-box">
                                        <img
                                            src="<?php if ($listing_sql_row['profile_image'] != NULL || !empty($listing_sql_row['profile_image'])) {
                                                echo "images/listings/" . $listing_sql_row['profile_image'];
                                            } else {
                                                echo "images/listings/hot4.jpg";
                                            } ?>" alt="">
                                        <div>
                                            <h4>
                                                <a href="<?php echo $LISTING_URL . urlModifier($listing_sql_row['listing_slug']); ?>"><?php echo $listing_sql_row['listing_name']; ?></a>
                                            </h4>
                                            <?php if ($star_rate != 0) { ?>
                                                <label class="rat">
                                                    <?php
                                                    for ($i = 1; $i <= ceil($star_rate_two); $i++) {
                                                        ?>
                                                        <i class="material-icons">star</i>
                                                        <?php
                                                    }
                                                    $bal_star_rate = abs(ceil($star_rate_two) - 5);

                                                    for ($i = 1; $i <= $bal_star_rate; $i++) {
                                                        ?>
                                                        <i class="material-icons">star_border</i>
                                                        <?php
                                                    }
                                                    ?>
                                                </label>
                                            <?php } ?>
                                            <span><a
                                                    href="#"><?php echo $popular_business_category_sql_row['category_name']; ?></a></span>
                                        </div>
                                        <a href="<?php echo $LISTING_URL . urlModifier($listing_sql_row['listing_slug']); ?>"
                                           class="fclick"></a>
                                    </div>
                                </li>
                                <?php
                                $pop_bus++;
                            }
                            ?>
                        </ul>
                    </div>
                    <!-- END NEW FEATURE SERVICES -->
                </div>
                <div class="hlead-coll">
                    <div class="col-md-6">
                        <div class="hom-cre-acc-left">
                            <h3><?php echo $BIZBOOK['HOM-WHAT-SER']; ?>
                                <span><?php echo $BIZBOOK['HOM-WHAT-BIZ']; ?></span>
                            </h3>
                            <p><?php echo $BIZBOOK['HOM-WHAT-SUB-HEAD']; ?></p>
                            <ul>
                                <li><img src="images/icon/blog.png" alt="">
                                    <div>
                                        <h5><?php echo $BIZBOOK['HOM-WHAT-SER-PO1']; ?></h5>
                                        <p><?php echo $BIZBOOK['HOM-WHAT-SER-PO1-SUB']; ?></p>
                                    </div>
                                </li>
                                <li><img src="images/icon/shield.png" alt="">
                                    <div>
                                        <h5><?php echo $BIZBOOK['HOM-WHAT-SER-PO2']; ?></h5>
                                        <p><?php echo $BIZBOOK['HOM-WHAT-SER-PO2-SUB']; ?></p>
                                    </div>
                                </li>
                                <li><img src="images/icon/general.png" alt="">
                                    <div>
                                        <h5><?php echo $BIZBOOK['HOM-WHAT-SER-PO3']; ?></h5>
                                        <p><?php echo $BIZBOOK['HOM-WHAT-SER-PO3-SUB']; ?></p>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-6">
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
                                       placeholder=""
                                       required>
                                <input type="hidden" class="form-control" name="enquiry_sender_id" value=""
                                       placeholder=""
                                       required>
                                <input type="hidden" class="form-control"
                                       name="enquiry_source"
                                       value="<?php if (isset($_GET["src"])) {
                                           echo $_GET["src"];
                                       } else {
                                           echo "Website";
                                       }; ?>" placeholder="" required>
                                <div class="form-group">
                                    <input type="text" name="enquiry_name" value="" required="required"
                                           class="form-control"
                                           placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>">
                                </div>
                                <div class="form-group">
                                    <input type="email" class="form-control"
                                           placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>"
                                           required="required"
                                           value="" name="enquiry_email"
                                           pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                           title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>">
                                </div>
                                <div class="form-group">
                                    <input type="text" class="form-control" value="" name="enquiry_mobile"
                                           placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>"
                                           pattern="[7-9]{1}[0-9]{9}"
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
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- END -->

    <!-- START -->
    <section>
        <div class="str str-full">
            <div class="container">
                <div class="row">
                    <div class="home-tit">
                        <h2>
                            <span><?php echo $BIZBOOK['HOM-TOPSER-TIT']; ?></span> <?php echo $BIZBOOK['HOM-TOPSER-TIT1']; ?>
                        </h2>
                        <p><?php echo $BIZBOOK['HOM-TOPSER-SUB-TIT']; ?></p>
                    </div>
                    <div class="ho-popu-bod">
                        <!--Top Branding Hotels-->
                        <?php
                        $si = 1;
                        foreach (getAllTopServiceProviders() as $row) {

                            $top_service_category_id = $row['top_service_provider_category_id'];

                            $top_service_listing_id = $row['top_service_provider_listings'];

                            $top_service_category_sql_row = getCategory($top_service_category_id);

                            ?>
                            <div class="col-md-4">
                                <div class="hot-page2-hom-pre-head">
                                    <h4><?php echo $all_texts_row['branding_title']; ?>
                                        <span><?php echo $top_service_category_sql_row['category_name']; ?></span></h4>
                                </div>
                                <div class="hot-page2-hom-pre">
                                    <ul>
                                        <?php
                                        $top_list_array = explode(',', $top_service_listing_id);
                                        $vi = 1;
                                        foreach ($top_list_array as $top_all_listing_array) {
                                            $top_listing_row = getIdListing($top_all_listing_array);
                                            // List Rating. for Rating of Star
                                            foreach (getListingReview($top_listing_row['listing_id']) as $star_rating_row) {
                                                if ($star_rating_row["rate_cnt"] > 0) {
                                                    $star_rate_times = $star_rating_row["rate_cnt"];
                                                    $star_sum_rates = $star_rating_row["total_rate"];
                                                    $star_rate_one = $star_sum_rates / $star_rate_times;
                                                    $star_rate = number_format($star_rate_one, 1);

                                                } else {
                                                    $rate_times = 0;
                                                    $rate_value = 0;
                                                    $star_rate = 0;
                                                }
                                            }
                                            ?>
                                            <!--LISTINGS-->
                                            <li>
                                                <div class="hot-page2-hom-pre-1"><img
                                                        src="<?php if ($top_listing_row['profile_image'] != NULL || !empty($top_listing_row['profile_image'])) {
                                                            echo "images/listings/" . $top_listing_row['profile_image'];
                                                        } else {
                                                            echo "images/listings/hot4.jpg";
                                                        } ?>" alt="">
                                                </div>
                                                <div class="hot-page2-hom-pre-2">
                                                    <h5><?php echo $top_listing_row['listing_name']; ?></h5>
                                                    <span><?php echo $top_listing_row['listing_address']; ?></span>
                                                </div>
                                                <?php if ($star_rate != 0) { ?>
                                                    <div class="hot-page2-hom-pre-3">
                                                        <span><?php echo $star_rate; ?></span>
                                                    </div>
                                                <?php } ?>
                                                <a href="<?php echo $LISTING_URL . urlModifier($top_listing_row['listing_slug']); ?>"
                                                   class="fclick"></a>
                                            </li>
                                            <!--LISTINGS-->
                                            <?php
                                        }
                                        ?>

                                    </ul>
                                </div>
                            </div>
                            <?php
                        }
                        ?>
                        <!--End Top Branding Hotels-->
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- END -->

    <section>
        <div id="demo" class="carousel slide cate-sli caro-home" data-ride="carousel">
            <div class="carousel-inner">
                <?php
                $si = 1;
                foreach (getAllSlider() as $slider_row) {

                    ?>
                    <div class="carousel-item <?php if ($si == 1) { ?>active<?php } ?>">
                        <img src="images/slider/<?php echo $slider_row['slider_photo']; ?>" alt="Los Angeles"
                             width="1100" height="500">
                        <a href="<?php echo $slider_row['slider_link']; ?>" target="_blank"></a>
                    </div>
                    <?php
                    $si++;
                }
                ?>
            </div>
            <a class="carousel-control-prev" href="#demo" data-slide="prev">
                <span class="carousel-control-prev-icon"></span>
            </a>
            <a class="carousel-control-next" href="#demo" data-slide="next">
                <span class="carousel-control-next-icon"></span>
            </a>
        </div>
    </section>

    <!-- START -->
    <section>
        <div class="str count">
            <div class="container">
                <div class="row">
                    <div class="home-tit">
                        <h2><span><?php echo $BIZBOOK['HOM-EVE-TIT']; ?></span> <?php echo $BIZBOOK['HOM-EVE-TIT1']; ?>
                        </h2>
                        <p><?php echo $BIZBOOK['HOM-EVE-SUB-TIT']; ?></p>
                    </div>
                    <div class="hom-event">
                        <div class="hom-eve-com hom-eve-lhs">
                            <?php

                            foreach (getAllTopEventsLimit(1, 2) as $topeventrow_1) { //To Fetch Top Events First Two Rows using position Id

                                $event_name = $topeventrow_1['event_name'];

                                $event_sql_row = getEvent($event_name);

                                $user_id = $event_sql_row['user_id'];

                                $user_details_row = getUser($user_id);

                                ?>
                                <div class="hom-eve-lhs-1 col-md-4">
                                    <div class="eve-box">
                                        <div>
                                            <a href="<?php echo $EVENT_URL . urlModifier($event_sql_row['event_slug']); ?>">
                                                <img src="images/events/<?php echo $event_sql_row['event_image']; ?>"
                                                     alt="">
                                            <span><?php echo dateMonthFormatconverter($event_sql_row['event_start_date']); ?>
                                                <b> <?php echo dateDayFormatconverter($event_sql_row['event_start_date']); ?></b></span>
                                            </a>
                                        </div>
                                        <div>
                                            <h4>
                                                <a href="<?php echo $EVENT_URL . urlModifier($event_sql_row['event_slug']); ?>"><?php echo $event_sql_row['event_name']; ?></a>
                                            </h4>
                                    <span
                                        class="addr"><?php echo $event_sql_row['event_address']; ?></span>
                                            <span class="pho"><?php echo $event_sql_row['event_mobile']; ?></span>
                                        </div>
                                        <div>
                                            <div class="auth">
                                                <img
                                                    src="images/user/<?php if (($user_details_row['profile_image'] == NULL) || empty($user_details_row['profile_image'])) {
                                                        echo "1.jpg";
                                                    } else {
                                                        echo $user_details_row['profile_image'];
                                                    } ?>" alt="">
                                                <b><?php echo $BIZBOOK['EVENT_HOSTED_BY']; ?></b><br>
                                                <h4><?php echo $user_details_row['first_name']; ?></h4>
                                                <a target="_blank"
                                                   href="<?php echo $PROFILE_URL . urlModifier($user_details_row['user_slug']); ?>"
                                                   class="fclick"></a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <?php
                            }
                            ?>
                            <div class="hom-eve-lhs-2 col-md-4">
                                <ul>
                                    <?php

                                    foreach (getAllTopEventsLimit(3, 6) as $topeventrow_2) { //To Fetch Top Events First Two Rows using position Id

                                        $event_name = $topeventrow_2['event_name'];

                                        $event_sql_row = getEvent($event_name);

                                        $user_id = $event_sql_row['user_id'];

                                        $user_details_row = getUser($user_id);

                                        ?>
                                        <li>
                                            <div class="eve-box-list">
                                                <img src="images/events/<?php echo $event_sql_row['event_image']; ?>"
                                                     alt="">
                                                <h4 title="<?php echo $event_sql_row['event_name']; ?>"><?php echo $event_sql_row['event_name']; ?></h4>
                                                <p><?php echo substr(stripslashes($event_sql_row['event_description']), 0, 50); ?></p>
                                            <span><?php echo dateMonthFormatconverter($event_sql_row['event_start_date']); ?>
                                                <b> <?php echo dateDayFormatconverter($event_sql_row['event_start_date']); ?></b></span>
                                                <a href="<?php echo $EVENT_URL . urlModifier($event_sql_row['event_slug']); ?>"
                                                   class="fclick"></a>
                                            </div>
                                        </li>
                                        <?php
                                    }
                                    ?>
                                </ul>
                            </div>

                        </div>
                    </div>

                    <div class="how-wrks">
                        <div class="home-tit">
                            <h2><span><?php echo $BIZBOOK['HOM-HOW-TIT']; ?></span></h2>
                            <p><?php echo $BIZBOOK['HOM-HOW-SUB-TIT']; ?></p>
                        </div>
                        <div class="how-wrks-inn">
                            <ul>
                                <li>
                                    <div>
                                        <span>1</span>
                                        <img src="images/icon/how1.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-1']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-1']; ?></p>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <span>2</span>
                                        <img src="images/icon/how2.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-2']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-2']; ?></p>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <span>3</span>
                                        <img src="images/icon/how3.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-3']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-3']; ?></p>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <span>4</span>
                                        <img src="images/icon/how4.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-4']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-4']; ?></p>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <?php if ($footer_row['admin_mobile_app_feature'] == 1) { ?>
                        <div class="mob-app">
                            <div class="lhs">
                                <img src="images/mobile.png" alt="">
                            </div>
                            <div class="rhs">
                                <h2><?php echo $BIZBOOK['HOM-APP-TIT']; ?>
                                    <span><?php echo $BIZBOOK['HOM-APP-TIT-SUB']; ?></span></h2>
                                <ul>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-1']; ?></li>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-2']; ?></li>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-3']; ?></li>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-4']; ?></li>
                                </ul>
                                <span><?php echo $BIZBOOK['HOM-APP-SEND']; ?></span>
                                <a href="#"><img src="images/gstore.png" alt=""> </a>
                                <a href="#"><img src="images/astore.png" alt=""> </a>
                            </div>
                        </div>
                    <?php } ?>
                </div>
            </div>
        </div>
    </section>
    <!-- END -->
    <?php
} elseif ($current_home_page == '2') {
    ?>

    <!-- START -->
    <section>
        <div class="str">
            <div class="container">
                <div class="row">
                    <div class="home-tit">
                        <h2><span><?php echo $BIZBOOK['HOM-EXP-TIT']; ?></span> <?php echo $BIZBOOK['HOM-EXP-TIT1']; ?>
                        </h2>
                        <p><?php echo $BIZBOOK['HOM-EXP-SUB-TIT']; ?></p>
                    </div>
                    <div class="home-city">
                        <ul>
                            <?php
                            foreach (getAllTrendCategories() as $trendrow) {

                                $category_name = $trendrow['category_name'];

                                $category_sql_row = getCategory($category_name);

                                $category_id = $category_sql_row['category_id'];

                                ?>
                                <li>
                                    <div class="hcity">
                                        <div>
                                            <img src="images/services/<?php echo $trendrow['category_bg_image']; ?>"
                                                 alt="">
                                        </div>
                                        <div>
                                            <img src="images/services/<?php echo $trendrow['category_image']; ?>"
                                                 alt="">
                                            <h4><?php echo $category_sql_row['category_name']; ?></h4>
                                            <div class="list-rat-all">

                                                <?php
                                                $sum = $count = $review_count45 = 0;// initiate interger variables
                                                foreach (getAllListingCategory($category_sql_row['category_id']) as $categorywise_listings) {
                                                    $categorywise_listing_id = $categorywise_listings['listing_id'];

                                                    foreach (getListingReview($categorywise_listing_id) as $star_rating_row) {
                                                        if ($star_rating_row["rate_cnt"] > 0) {
                                                            $star_rate_times = $star_rating_row["rate_cnt"];
                                                            $star_sum_rates = $star_rating_row["total_rate"];
                                                            $star_rate_one = $star_sum_rates / $star_rate_times;
                                                            $star_rate_two = number_format($star_rate_one, 1);
                                                            $star_rate = $star_rate_two;

                                                        } else {
                                                            $rate_times = 0;
                                                            $rate_value = 0;
                                                            $star_rate = 0;
                                                        }

                                                    }
                                                    $review_count45 += getCountListingReview($categorywise_listing_id);
                                                    $sum += $star_rate;
                                                    if ($star_rate > 0) {
                                                        $count++; //add 1 on every loop
                                                    }

                                                }
                                                $new_star_rate = number_format($sum / $count, 1);
                                                if ($review_count45 == 0) {
                                                    $new_review_count = 0;
                                                } else {
                                                    $new_review_count = $review_count45;
                                                }


                                                ?>
                                                <b><?php if (AddingZero_BeforeNumber(getCountCategoryListing($category_id)) != 0) {

                                                        if ($new_star_rate != 0) {
                                                            echo $new_star_rate;
                                                        } else {
                                                            echo $BIZBOOK['ALL-LISTING-0-RATINGS'];
                                                        }
                                                    } else {
                                                        echo $BIZBOOK['ALL-LISTING-0-RATINGS'];
                                                    } ?></b>
                                                <?php
                                                if ($new_star_rate != 0 && AddingZero_BeforeNumber(getCountCategoryListing($category_id)) != 0) {
                                                    ?>
                                                    <label class="rat">
                                                        <?php
                                                        for ($i = 1; $i <= ceil($new_star_rate); $i++) {
                                                            ?>
                                                            <i class="material-icons">star</i>
                                                            <?php
                                                        }
                                                        $bal_star_rate = abs(ceil($new_star_rate) - 5);

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
                                                <?php if ($new_review_count > 0 && AddingZero_BeforeNumber(getCountCategoryListing($category_id)) != 0) { ?>
                                                    <span><?php echo $new_review_count; ?><?php echo $BIZBOOK['REVIEWS']; ?></span>
                                                    <?php
                                                }
                                                ?>
                                            </div>
                                            <p><?php echo AddingZero_BeforeNumber(getCountCategoryListing($category_id)); ?><?php echo $BIZBOOK['LISTINGS']; ?></p>
                                        </div>
                                        <a href="<?php echo $ALL_LISTING_URL . urlModifier($category_sql_row['category_slug']); ?>"
                                           class="fclick">&nbsp;</a>
                                    </div>
                                </li>
                                <?php
                            }
                            ?>
                        </ul>
                    </div>
                    <a href="all-category" class="hom-more"><?php echo $BIZBOOK['HOM-VI-ALL-SER']; ?></a>
                </div>
            </div>
        </div>
    </section>
    <!-- END -->

    <!-- START -->
    <section>
        <div class="str hom2-cus hom4-fea">
            <div class="container">
                <div class="row">
                    <div class="home-tit">
                        <h2><span><?php echo $BIZBOOK['HOM-BEST-TIT']; ?></span>
                        </h2>
                        <p><?php echo $BIZBOOK['HOM-BEST-SUB-TIT']; ?></p>
                    </div>

                    <div class="hom2-cus-sli">
                        <ul class="multiple-items1">
                            <?php
                            $pop_bus = 1;
                            foreach (getAllFeaturedListing() as $row) {

                                $listing_id = $row['listing_id'];

                                $listing_sql_row = getIdListing($listing_id);
                                $featured_category_id = $listing_sql_row['category_id'];

                                $popular_business_category_sql_row = getCategory($featured_category_id);

                                // List Rating. for Rating of Star
                                foreach (getListingReview($listing_id) as $star_rating_row) {
                                    if ($star_rating_row["rate_cnt"] > 0) {
                                        $star_rate_times = $star_rating_row["rate_cnt"];
                                        $star_sum_rates = $star_rating_row["total_rate"];
                                        $star_rate_one = $star_sum_rates / $star_rate_times;
                                        //$star_rate_one = (($Star_rate_value)/5)*100;
                                        $star_rate_two = number_format($star_rate_one, 1);
                                        $star_rate = $star_rate_two;

                                    } else {
                                        $rate_times = 0;
                                        $rate_value = 0;
                                        $star_rate = 0;
                                    }
                                }

                                ?>
                                <li>
                                    <div class="testmo hom4-prop-box">
                                        <img
                                            src="<?php if ($listing_sql_row['profile_image'] != NULL || !empty($listing_sql_row['profile_image'])) {
                                                echo "images/listings/" . $listing_sql_row['profile_image'];
                                            } else {
                                                echo "images/listings/hot4.jpg";
                                            } ?>" alt="">
                                        <div>
                                            <h4>
                                                <a href="<?php echo $LISTING_URL . urlModifier($listing_sql_row['listing_slug']); ?>"><?php echo $listing_sql_row['listing_name']; ?></a>
                                            </h4>
                                            <?php if ($star_rate != 0) { ?>
                                                <label class="rat">
                                                    <?php
                                                    for ($i = 1; $i <= ceil($star_rate_two); $i++) {
                                                        ?>
                                                        <i class="material-icons">star</i>
                                                        <?php
                                                    }
                                                    $bal_star_rate = abs(ceil($star_rate_two) - 5);

                                                    for ($i = 1; $i <= $bal_star_rate; $i++) {
                                                        ?>
                                                        <i class="material-icons">star_border</i>
                                                        <?php
                                                    }
                                                    ?>
                                                </label>
                                            <?php } ?>
                                            <span><a
                                                    href="#"><?php echo $popular_business_category_sql_row['category_name']; ?></a></span>
                                        </div>
                                        <a href="<?php echo $LISTING_URL . urlModifier($listing_sql_row['listing_slug']); ?>"
                                           class="fclick"></a>
                                    </div>
                                </li>
                                <?php
                                $pop_bus++;
                            }
                            ?>
                        </ul>
                        <a href="all-category" class="hom-more"><?php echo $BIZBOOK['HOM-VI-ALL-SER']; ?></a>
                    </div>

                </div>
            </div>
        </div>
    </section>
    <!-- END -->


    <!-- START -->
    <section>
        <div class="str hom2-cus hom4-fea all-serexp">
            <div class="container">
                <div class="row">
                    <div class="home-tit">
                        <h2><span><?php echo $BIZBOOK['TOP-SERVICE-EXPERTS']; ?></span>
                        </h2>
                        <p><?php echo $BIZBOOK['SERVICE-EXPERT-FIND-SERVICE-EXPERT-P']; ?></p>
                    </div>

                    <div class="hom2-cus-sli">
                        <ul class="multiple-items1">
                            <?php
                            $si = 1;
                            foreach (getAllTopExperts() as $expert_profile_row) {

                                $expert_id = $expert_profile_row['expert_id'];

                                $user_id = $expert_profile_row['user_id'];

                                $expert_user_row = getUser($user_id);

                                $user_plan = $expert_user_row['user_plan'];

                                $plan_type_row = getPlanType($user_plan);

                                $expert_profile_category_id = $expert_profile_row['category_id'];

                                $expert_profile_city_id = $expert_profile_row['city_id'];

                                $expert_profile_category_row = getExpertCategory($expert_profile_category_id);

                                $expert_category_name = $expert_profile_category_row['category_name'];

                                $expert_profile_city_row = getExpertCity($expert_profile_city_id);

                                $expert_city_name = $expert_profile_city_row['country_name'];

                                //To calculate the expiry date from user created date starts

                                $start_date_timestamp = strtotime($expert_user_row['user_cdt']);
                                $plan_type_duration = $plan_type_row['plan_type_duration'];

                                $expiry_date_timestamp = strtotime("+$plan_type_duration months", $start_date_timestamp);

                                $expiry_date = date("Y-m-d h:i:s", $expiry_date_timestamp);

                                //To calculate the expiry date from user created date ends

                                ?>
                                <li>
                                    <div class="job-box">
                                        <div class="job-box-img">
                                            <img
                                                src="service-experts/images/services/<?php echo $expert_profile_row['profile_image']; ?>"
                                                alt="">
                                        </div>
                                        <?php if ($expert_profile_row['expert_availability_status'] == 0) { ?>
                                            <div class="ser-exp-ave" title="User currently available">
                                                <span class="ser-avail-yes"></span>
                                            </div>
                                        <?php } ?>

                                        <div class="job-days">
                                            <?php if ($expert_user_row['user_plan'] == 4 || $expert_user_row['user_plan'] == 3) { ?>
                                                <span class="ver"><i class="material-icons"
                                                                     title="Verified expert">verified_user</i></span>
                                                <?php
                                            }
                                            ?>
                                        </div>
                                        <div class="job-box-con">
                                            <h5 class="cate"><?php echo $expert_category_name; ?></h5>
                                            <h4><?php echo $expert_profile_row['profile_name']; ?></h4>
                                            <span><?php echo getIdCountFinishedExpertEnquiries($expert_id); ?> <?php echo $BIZBOOK['SERVICE-EXPERT-SERVICES-DONE']; ?></span>
                                            <span><?php echo $expert_profile_row['years_of_experience']; ?> <?php echo $BIZBOOK['YEARS_EXP']; ?></span>
                                        </div>
                                        <div class="job-box-apl">
                                            <a href="<?php echo $SERVICE_EXPERT_URL . urlModifier($expert_profile_row['expert_slug']); ?>"
                                               class="serexp-cta-more"><?php echo $BIZBOOK['EXP-HOME-JOIN-EMP-CTA1']; ?></a>
                                        </div>
                                    </div>
                                </li>
                                <?php
                            }
                            ?>
                        </ul>
                        <a href="service-experts" class="hom-more"><?php echo $BIZBOOK['HOM-VI-ALL-SER-EXPERTS']; ?></a>
                    </div>

                </div>
            </div>
        </div>
    </section>
    <!-- END -->

    <!-- START -->
    <section>
        <div class="str hom2-cus hom4-fea">
            <div class="container">
                <div class="row">
                    <div class="home-tit">
                        <h2><span><?php echo $BIZBOOK['JOB-HEADER-H4']; ?></span></h2>
                        <p><?php echo $BIZBOOK['HOM-BEST-SUB-TIT']; ?></p>
                    </div>

                    <div class="hom2-cus-sli job-list">
                        <ul class="multiple-items1">
                            <?php
                            $si = 1;

                            foreach (getAllJobPopular() as $row) {

                                $job_name = $row['job_name'];

                                $job_popular_id = $row['job_popular_id'];

                                $job_sql_row = getIdJob($job_name);
                                $job_id = $job_sql_row['job_id'];
                                $total_count_jobs_applied = getCountJobAppliedJob($job_id);

                                ?>
                                <li>
                                    <div class="job-box">
                                        <div class="job-box-img">
                                            <img
                                                src="<?php echo $slash; ?>jobs/images/jobs/<?php echo $job_sql_row['company_logo']; ?>"
                                                alt="">
                                        </div>
                                        <div class="job-days">
                                        <span
                                            class="day"><?php echo time_elapsed_string($job_sql_row['job_cdt']); ?></span>
                                        <span
                                            class="apl"><?php echo $total_count_jobs_applied; ?><?php echo $BIZBOOK['APPLICANTS']; ?></span>
                                        </div>
                                        <div class="job-box-con">
                                            <h4><?php echo $job_sql_row['job_title']; ?></h4>
                                        <span><?php
                                            $job_type = $job_sql_row['job_type'];
                                            if ($job_type == 1) {
                                                echo $BIZBOOK['JOB-PERMANENT'];
                                            } elseif ($job_type == 2) {
                                                echo $BIZBOOK['JOB-CONTRACT'];
                                            } elseif ($job_type == 3) {
                                                echo $BIZBOOK['JOB-PART-TIME'];
                                            } elseif ($job_type == 4) {
                                                echo $BIZBOOK['JOB-FREELANCE'];
                                            }
                                            ?></span>
                                            <span><?php echo $job_sql_row['job_role']; ?></span>
                                            <span><?php echo AddingZero_BeforeNumber($job_sql_row['no_of_openings']); ?><?php echo $BIZBOOK['JOB_OPENINGS']; ?></span>
                                        </div>
                                        <div class="job-box-apl">
                                            <span class="job-box-cta"><?php echo $BIZBOOK['JOB_APPLY_NOW']; ?></span>
                                        </div>
                                        <a href="<?php echo $JOB_URL . urlModifier($job_sql_row['job_slug']); ?>"
                                           class="job-full-cta"></a>
                                    </div>
                                </li>
                                <?php
                            }
                            ?>
                        </ul>
                        <a href="jobs" class="hom-more"><?php echo $BIZBOOK['HOM-VI-ALL-JOB-OPENINGS']; ?></a>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- END -->

    <!-- START -->
    <section>
        <div class="str hom2-cus">
            <div class="container">
                <div class="row">
                    <div class="home-tit">
                        <h2><span><?php echo $BIZBOOK['OUR_ALL_SER']; ?></span></h2>
                        <p><?php echo $BIZBOOK['OUR_ALL_SER_SUB']; ?></p>
                    </div>
                    <div class="our-all-ser">
                        <ul>
                            <li><a href="<?php echo $webpage_full_link; ?>all-category"><img
                                        src="<?php echo $slash; ?>images/icon/shop.png"><?php echo $BIZBOOK['ALL_SERVICES']; ?>
                                </a></li>
                            <li><a href="<?php echo $webpage_full_link; ?>service-experts"><img
                                        src="<?php echo $slash; ?>images/icon/expert.png"><?php echo $BIZBOOK['SERVICE-EXPERTS']; ?>
                                </a></li>
                            <li><a href="<?php echo $webpage_full_link; ?>jobs"><img
                                        src="<?php echo $slash; ?>images/icon/employee.png"><?php echo $BIZBOOK['JOBS']; ?>
                                </a></li>
                            <li><a href="<?php echo $webpage_full_link; ?>news"><img
                                        src="<?php echo $slash; ?>images/icon/news.png"><?php echo $BIZBOOK['NEWS-MAGA']; ?>
                                </a></li>
                            <li><a href="<?php echo $webpage_full_link; ?>events"><img
                                        src="<?php echo $slash; ?>images/icon/calendar.png"><?php echo $BIZBOOK['EVENTS']; ?>
                                </a></li>
                            <li><a href="<?php echo $webpage_full_link; ?>all-products"><img
                                        src="<?php echo $slash; ?>images/icon/cart.png"><?php echo $BIZBOOK['PRODUCTS']; ?>
                                </a></li>
                            <li><a href="<?php echo $webpage_full_link; ?>coupons"><img
                                        src="<?php echo $slash; ?>images/icon/coupons.png"><?php echo $BIZBOOK['COUPONS_AND_DEALS']; ?>
                                </a></li>
                            <li><a href="<?php echo $webpage_full_link; ?>blog-posts"><img
                                        src="<?php echo $slash; ?>images/icon/blog1.png"><?php echo $BIZBOOK['BLOGS']; ?>
                                </a></li>
                            <li><a href="<?php echo $webpage_full_link; ?>community"><img
                                        src="<?php echo $slash; ?>images/icon/11.png"><?php echo $BIZBOOK['COMMUNITY']; ?>
                                </a></li>
                        </ul>
                    </div>

                </div>
            </div>
        </div>
    </section>
    <!-- END -->

    <!--PRICING DETAILS-->
    <section class="<?php if ($footer_row['admin_language'] == 2) {
        echo "lg-arb";
    } ?> pri">
        <div class="container">
            <div class="row">
                <div class="home-tit">
                    <h2>
                        <span><?php echo $BIZBOOK['CHOOSE_YOUR_PLAN']; ?></span></h2>
                </div>
                <div>
                    <ul>
                        <?php
                        $si = 1;
                        foreach (getAllPlanType() as $plan_type_row) {
                            ?>
                            <li>
                                <div class="pri-box">
                                    <div class="c2">
                                        <h4><?php echo $plan_type_row['plan_type_name']; ?><?php echo $BIZBOOK['PLAN']; ?></h4>

                                        <?php if ($plan_type_row['plan_type_id'] == 1) { ?>
                                            <p><?php echo $BIZBOOK['PRICING_GETTING_STARTED']; ?></p>
                                        <?php } elseif ($plan_type_row['plan_type_id'] == 2) { ?>
                                            <p><?php echo $BIZBOOK['PRICING_PERFECT_SMALL_TEAMS']; ?></p>
                                        <?php } elseif ($plan_type_row['plan_type_id'] == 3) { ?>
                                            <p><?php echo $BIZBOOK['PRICING_BEST_VALUE_LARGE']; ?></p>
                                        <?php } else { ?>
                                            <p><?php echo $BIZBOOK['PRICING_MADE_ENTERPRISES']; ?></p>
                                            <?php
                                        } ?>

                                    </div>
                                    <div class="c3">
                                        <h2><span></span><?php if ($plan_type_row['plan_type_price'] == 0) {
                                                echo $BIZBOOK['FREE'];
                                            } else {
                                                echo $footer_row['currency_symbol'] . '' . $plan_type_row['plan_type_price'];
                                            } ?></h2>
                                        <?php if ($plan_type_row['plan_type_id'] == 1) { ?>
                                            <p><?php echo $BIZBOOK['PRICING_SINGLE_USER']; ?></p>
                                        <?php } elseif ($plan_type_row['plan_type_id'] == 2) { ?>
                                            <p><?php echo $BIZBOOK['PRICING_STARTUP_BUSINESS']; ?></p>
                                        <?php } elseif ($plan_type_row['plan_type_id'] == 3) { ?>
                                            <p><?php echo $BIZBOOK['PRICING_MEDIUM_BUSINESS']; ?></p>
                                        <?php } else { ?>
                                            <p><?php echo $BIZBOOK['PRICING_MADE_ENTERPRISES']; ?></p>
                                            <?php
                                        } ?>

                                    </div>
                                    <div class="c5">
                                        <a href="<?php
                                        if (isset($_SESSION['user_id'])) {
                                            echo "db-plan-change";
                                        } else {
                                            echo "login";
                                        } ?>" class="cta1"><?php echo $BIZBOOK['PRICING_GET_START']; ?></a>
                                        <a href="pricing-details" class="cta2"
                                           target="_blank"><?php echo $BIZBOOK['HOM-VI-KNOW-MORE']; ?></a>
                                    </div>
                                </div>
                            </li>
                            <?php
                            $si++;
                        }
                        ?>
                    </ul>
                </div>
            </div>
        </div>
    </section>
    <!--END PRICING DETAILS-->


    <!-- START -->
    <section>
        <div class="str count">
            <div class="container">
                <div class="row">
                    <div class="how-wrks">
                        <div class="home-tit">
                            <h2><span><?php echo $BIZBOOK['HOM-HOW-TIT']; ?></span></h2>
                            <p><?php echo $BIZBOOK['HOM-HOW-SUB-TIT']; ?></p>
                        </div>
                        <div class="how-wrks-inn">
                            <ul>
                                <li>
                                    <div>
                                        <span>1</span>
                                        <img src="images/icon/how1.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-1']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-1']; ?></p>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <span>2</span>
                                        <img src="images/icon/how2.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-2']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-2']; ?></p>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <span>3</span>
                                        <img src="images/icon/how3.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-3']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-3']; ?></p>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <span>4</span>
                                        <img src="images/icon/how4.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-4']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-4']; ?></p>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <?php if ($footer_row['admin_mobile_app_feature'] == 1) { ?>
                        <div class="mob-app">
                            <div class="lhs">
                                <img src="images/mobile.png" alt="">
                            </div>
                            <div class="rhs">
                                <h2><?php echo $BIZBOOK['HOM-APP-TIT']; ?>
                                    <span><?php echo $BIZBOOK['HOM-APP-TIT-SUB']; ?></span></h2>
                                <ul>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-1']; ?></li>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-2']; ?></li>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-3']; ?></li>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-4']; ?></li>
                                </ul>
                                <span><?php echo $BIZBOOK['HOM-APP-SEND']; ?></span>
                                <a href="#"><img src="images/gstore.png" alt=""> </a>
                                <a href="#"><img src="images/astore.png" alt=""> </a>
                            </div>
                        </div>
                    <?php } ?>
                </div>
            </div>
        </div>
    </section>
    <!-- END -->
    <?php
} elseif ($current_home_page == '3') {
    ?>

    <!-- START -->
    <section>
        <div>
            <div class="container">
                <div class="row">
                    <!--<div class="home-tit">
                        <h2><span>Top Services</span> Cras nulla nulla, pulvinar sit amet nunc at, lacinia viverra lectus. Fusce imperdiet ullamcorper metus eu fringilla.</h2>
                    </div>-->
                    <div class="home-tit">
                        <h2><span><?php echo $BIZBOOK['HOM-POP-TIT']; ?></span> <?php echo $BIZBOOK['HOM-POP-TIT1']; ?>
                        </h2>
                        <p><?php echo $BIZBOOK['HOM-POP-SUB-TIT']; ?></p>
                    </div>
                    <div class="land-pack">
                        <ul>
                            <?php
                            foreach (getAllCategories() as $category_sql_row) {
                                ?>
                                <li>
                                    <div class="land-pack-grid">
                                        <div class="land-pack-grid-img">
                                            <img
                                                src="images/services/<?php echo $category_sql_row['category_image']; ?>"
                                                alt="">
                                        </div>
                                        <div class="land-pack-grid-text">
                                            <h4><?php echo $category_sql_row['category_name']; ?>
                                                <span
                                                    class="dir-ho-cat"><?php echo $BIZBOOK['LISTINGS']; ?><?php echo AddingZero_BeforeNumber(getCountCategoryListing($category_sql_row['category_id'])); ?></span>
                                            </h4>
                                        </div>
                                        <a href="<?php echo $ALL_LISTING_URL . urlModifier($category_sql_row['category_slug']); ?>"
                                           class="land-pack-grid-btn"><?php echo $BIZBOOK['VIEW_ALL_LISTINGS']; ?></a>
                                    </div>
                                </li>
                                <?php
                            }
                            ?>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- END -->

    <!-- START -->
    <section>
        <div class="str hom2-cus hom4-fea">
            <div class="container">
                <div class="row">
                    <div class="home-tit">
                        <h2>
                            <span><?php echo $BIZBOOK['HOM-BEST-TIT']; ?></span> <?php echo $BIZBOOK['HOM-BEST-TIT1']; ?>
                        </h2>
                        <p><?php echo $BIZBOOK['HOM-BEST-SUB-TIT']; ?></p>
                    </div>

                    <div class="hom2-cus-sli">
                        <ul class="multiple-items1">
                            <?php
                            $pop_bus = 1;
                            foreach (getAllFeaturedListing() as $row) {

                                $listing_id = $row['listing_id'];

                                $listing_sql_row = getIdListing($listing_id);
                                $featured_category_id = $listing_sql_row['category_id'];

                                $popular_business_category_sql_row = getCategory($featured_category_id);

                                // List Rating. for Rating of Star
                                foreach (getListingReview($listing_id) as $star_rating_row) {
                                    if ($star_rating_row["rate_cnt"] > 0) {
                                        $star_rate_times = $star_rating_row["rate_cnt"];
                                        $star_sum_rates = $star_rating_row["total_rate"];
                                        $star_rate_one = $star_sum_rates / $star_rate_times;
                                        //$star_rate_one = (($Star_rate_value)/5)*100;
                                        $star_rate_two = number_format($star_rate_one, 1);
                                        $star_rate = $star_rate_two;

                                    } else {
                                        $rate_times = 0;
                                        $rate_value = 0;
                                        $star_rate = 0;
                                    }
                                }

                                ?>
                                <li>
                                    <div class="testmo hom4-prop-box">
                                        <img
                                            src="<?php if ($listing_sql_row['profile_image'] != NULL || !empty($listing_sql_row['profile_image'])) {
                                                echo "images/listings/" . $listing_sql_row['profile_image'];
                                            } else {
                                                echo "images/listings/hot4.jpg";
                                            } ?>" alt="">
                                        <div>
                                            <h4>
                                                <a href="<?php echo $LISTING_URL . urlModifier($listing_sql_row['listing_slug']); ?>"><?php echo $listing_sql_row['listing_name']; ?></a>
                                            </h4>
                                            <?php if ($star_rate != 0) { ?>
                                                <label class="rat">
                                                    <?php
                                                    for ($i = 1; $i <= ceil($star_rate_two); $i++) {
                                                        ?>
                                                        <i class="material-icons">star</i>
                                                        <?php
                                                    }
                                                    $bal_star_rate = abs(ceil($star_rate_two) - 5);

                                                    for ($i = 1; $i <= $bal_star_rate; $i++) {
                                                        ?>
                                                        <i class="material-icons">star_border</i>
                                                        <?php
                                                    }
                                                    ?>
                                                </label>
                                            <?php } ?>
                                            <span><a
                                                    href="#"><?php echo $popular_business_category_sql_row['category_name']; ?></a></span>
                                        </div>
                                        <a href="<?php echo $LISTING_URL . urlModifier($listing_sql_row['listing_slug']); ?>"
                                           class="fclick"></a>
                                    </div>
                                </li>
                                <?php
                                $pop_bus++;
                            }
                            ?>
                        </ul>
                    </div>

                </div>
            </div>
        </div>
    </section>
    <!-- END -->

    <!--PRICING DETAILS-->
    <section class="<?php if ($footer_row['admin_language'] == 2) {
        echo "lg-arb";
    } ?> pri">
        <div class="container">
            <div class="row">
                <div class="tit">
                    <h2>
                        <span><?php echo $BIZBOOK['CHOOSE_YOUR_PLAN']; ?></span></h2>
                </div>
                <div>
                    <ul>
                        <?php
                        $si = 1;
                        foreach (getAllPlanType() as $plan_type_row) {
                            ?>
                            <li>
                                <div class="pri-box">
                                    <div class="c2">
                                        <h4><?php echo $plan_type_row['plan_type_name']; ?> plan</h4>

                                        <?php if ($plan_type_row['plan_type_id'] == 1) { ?>
                                            <p><?php echo $BIZBOOK['PRICING_GETTING_STARTED']; ?></p>
                                        <?php } elseif ($plan_type_row['plan_type_id'] == 2) { ?>
                                            <p><?php echo $BIZBOOK['PRICING_PERFECT_SMALL_TEAMS']; ?></p>
                                        <?php } elseif ($plan_type_row['plan_type_id'] == 3) { ?>
                                            <p><?php echo $BIZBOOK['PRICING_BEST_VALUE_LARGE']; ?></p>
                                        <?php } else { ?>
                                            <p><?php echo $BIZBOOK['PRICING_MADE_ENTERPRISES']; ?></p>
                                            <?php
                                        } ?>

                                    </div>
                                    <div class="c3">
                                        <h2><span></span><?php if ($plan_type_row['plan_type_price'] == 0) {
                                                echo $BIZBOOK['FREE'];
                                            } else {
                                                echo $footer_row['currency_symbol'] . '' . $plan_type_row['plan_type_price'];
                                            } ?></h2>
                                        <?php if ($plan_type_row['plan_type_id'] == 1) { ?>
                                            <p><?php echo $BIZBOOK['PRICING_SINGLE_USER']; ?></p>
                                        <?php } elseif ($plan_type_row['plan_type_id'] == 2) { ?>
                                            <p><?php echo $BIZBOOK['PRICING_STARTUP_BUSINESS']; ?></p>
                                        <?php } elseif ($plan_type_row['plan_type_id'] == 3) { ?>
                                            <p><?php echo $BIZBOOK['PRICING_MEDIUM_BUSINESS']; ?></p>
                                        <?php } else { ?>
                                            <p><?php echo $BIZBOOK['PRICING_MADE_ENTERPRISES']; ?></p>
                                            <?php
                                        } ?>

                                    </div>
                                    <div class="c5">
                                        <a href="<?php
                                        if (isset($_SESSION['user_id'])) {
                                            echo "db-plan-change";
                                        } else {
                                            echo "login";
                                        } ?>" class="cta1"><?php echo $BIZBOOK['PRICING_GET_START']; ?></a>
                                        <a href="pricing-details" class="cta2"
                                           target="_blank"><?php echo $BIZBOOK['HOM-VI-KNOW-MORE']; ?></a>
                                    </div>
                                </div>
                            </li>
                            <?php
                            $si++;
                        }
                        ?>
                    </ul>
                </div>
            </div>
        </div>
    </section>
    <!--END PRICING DETAILS-->

    <!-- START -->
    <section class="news-hom-ban-sli">
        <div class="home-tit">
            <h2><span><?php echo $BIZBOOK['HOM-EVE-TIT']; ?></span> <?php echo $BIZBOOK['HOM-EVE-TIT1']; ?></h2>
            <p><?php echo $BIZBOOK['HOM-EVE-SUB-TIT']; ?></p>
        </div>

        <div class="news-hom-ban-sli-inn">
            <ul class="multiple-items2">
                <?php

                foreach (getAllTopEvents() as $topeventrow_1) { //To Fetch Top Events First Two Rows using position Id

                    $event_name = $topeventrow_1['event_name'];

                    $event_sql_row = getEvent($event_name);

                    $user_id = $event_sql_row['user_id'];

                    $user_details_row = getUser($user_id);

                    ?>
                    <li>
                        <div class="news-hban-box">
                            <div class="im">
                                <img src="images/events/<?php echo $event_sql_row['event_image']; ?>" alt="">
                            </div>
                            <div class="txt">
                                <span class="news-cate"><?php echo dateMonthFormatconverter($event_sql_row['event_start_date']); ?> <?php echo dateDayFormatconverter($event_sql_row['event_start_date']); ?></span>
                                <h2><?php echo $event_sql_row['event_name']; ?></h2>
                                <span class="news-date"><?php echo $BIZBOOK['HOM3-OW-POSTED-ON']; ?>: <?php echo dateFormatconverter($event_sql_row['event_cdt']); ?></span>
                            </div>
                            <a href="<?php echo $EVENT_URL . urlModifier($event_sql_row['event_slug']); ?>" class="fclick"></a>
                        </div>
                    </li>
                    <?php
                }
                ?>
            </ul>
        </div>
    </section>
    <!--END-->

    <!-- START -->
    <section>
        <div class="str hom2-cus">
            <div class="container">
                <div class="row">
                    <div class="home-tit">
                        <h2><span><?php echo $BIZBOOK['HOM3-OW-USER-REVIEW']; ?></span></h2>
                        <p><?php echo $BIZBOOK['HOM3-OW-TIT-SUB']; ?></p>
                    </div>
                    <div class="hom2-cus-sli">
                        <ul class="multiple-items">
                            <?php
                            foreach (getTenActiveReviews() as $reviewss_row) {

                                $review_user_id = $reviewss_row['review_user_id'];

                                $listing_id = $reviewss_row['listing_id'];

                                $listing_sql_row = getIdListing($listing_id);

                                $user_details_row = getUser($review_user_id);

                                $featured_category_id = $listing_sql_row['category_id'];

                                $popular_business_category_sql_row = getCategory($featured_category_id);

                                // List Rating. for Rating of Star

                                if ($reviewss_row['price_rating'] > 0) {

                                    $star_rate = $reviewss_row['price_rating'];

                                } else {
                                    $star_rate = 0;
                                }

                                ?>
                                <li>
                                    <div class="testmo">
                                        <img
                                            src="images/user/<?php if (($user_details_row['profile_image'] == NULL) || empty($user_details_row['profile_image'])) {
                                                echo "1.jpg";
                                            } else {
                                                echo $user_details_row['profile_image'];
                                            } ?>" alt="">
                                        <h4><?php echo $user_details_row['first_name']; ?></h4>
                                    <span><?php echo $BIZBOOK['SERVICE-EXPERT-WRITTEN-REVIEW-TO']; ?> <a
                                            href="<?php echo $LISTING_URL . urlModifier($listing_sql_row['listing_slug']); ?>"><?php echo $listing_sql_row['listing_name']; ?></a></span>

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
                                                    <i class="material-icons">star_border</i>
                                                    <?php
                                                }
                                                ?>
                                            </label>
                                            <?php
                                        } ?>
                                        <p><?php echo $reviewss_row['review_message']; ?></p>
                                    </div>
                                </li>
                                <?php
                            } ?>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- END -->

    <!-- START -->
    <section>
        <div class="str count">
            <div class="container">
                <div class="row">

                    <div class="how-wrks">
                        <div class="home-tit">
                            <h2><span><?php echo $BIZBOOK['HOM-HOW-TIT']; ?></span></h2>
                            <p><?php echo $BIZBOOK['HOM-HOW-SUB-TIT']; ?></p>
                        </div>
                        <div class="how-wrks-inn">
                            <ul>
                                <li>
                                    <div>
                                        <span>1</span>
                                        <img src="images/icon/how1.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-1']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-1']; ?></p>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <span>2</span>
                                        <img src="images/icon/how2.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-2']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-2']; ?></p>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <span>3</span>
                                        <img src="images/icon/how3.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-3']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-3']; ?></p>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <span>4</span>
                                        <img src="images/icon/how4.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-4']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-4']; ?></p>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                    <?php if ($footer_row['admin_mobile_app_feature'] == 1) { ?>
                        <div class="mob-app">
                            <div class="lhs">
                                <img src="images/mobile.png" alt="">
                            </div>
                            <div class="rhs">
                                <h2><?php echo $BIZBOOK['HOM-APP-TIT']; ?>
                                    <span><?php echo $BIZBOOK['HOM-APP-TIT-SUB']; ?></span></h2>
                                <ul>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-1']; ?></li>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-2']; ?></li>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-3']; ?></li>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-4']; ?></li>
                                </ul>
                                <span><?php echo $BIZBOOK['HOM-APP-SEND']; ?></span>
                                <form>
                                    <ul>
                                        <li>
                                            <input type="email" placeholder="Enter email id" required></li>
                                        <li>
                                            <input type="submit" value="Get App Link"></li>
                                    </ul>
                                </form>
                                <a href="#"><img src="images/android.png" alt=""> </a>
                                <a href="#"><img src="images/apple.png" alt=""> </a>
                            </div>
                        </div>
                    <?php } ?>
                </div>
            </div>
        </div>
    </section>
    <!-- END -->


    <?php
} elseif ($current_home_page == '4' || $current_home_page == '5' || $current_home_page == '6' || $current_home_page == '7' || $current_home_page == '8' || $current_home_page == '9') {
    ?>


    <!-- START -->
    <section>
        <div class="str hom2-cus hom4-fea">
            <div class="container">
                <div class="row">
                    <div class="home-tit">
                        <h2>
                            <span><?php echo $BIZBOOK['HOM-BEST-TIT']; ?></span> <?php echo $BIZBOOK['HOM-BEST-TIT1']; ?>
                        </h2>
                        <p><?php echo $BIZBOOK['HOM-BEST-SUB-TIT']; ?></p>
                    </div>

                    <!-- NEW FEATURE SERVICES -->
                    <div class="hom2-cus-sli">
                        <ul class="multiple-items1">
                            <?php
                            $pop_bus = 1;
                            foreach (getAllFeaturedListing() as $row) {

                                $listing_id = $row['listing_id'];

                                $listing_sql_row = getIdListing($listing_id);
                                $featured_category_id = $listing_sql_row['category_id'];

                                $popular_business_category_sql_row = getCategory($featured_category_id);

                                // List Rating. for Rating of Star
                                foreach (getListingReview($listing_id) as $star_rating_row) {
                                    if ($star_rating_row["rate_cnt"] > 0) {
                                        $star_rate_times = $star_rating_row["rate_cnt"];
                                        $star_sum_rates = $star_rating_row["total_rate"];
                                        $star_rate_one = $star_sum_rates / $star_rate_times;
                                        //$star_rate_one = (($Star_rate_value)/5)*100;
                                        $star_rate_two = number_format($star_rate_one, 1);
                                        $star_rate = $star_rate_two;

                                    } else {
                                        $rate_times = 0;
                                        $rate_value = 0;
                                        $star_rate = 0;
                                    }
                                }

                                ?>
                                <li>
                                    <div class="testmo hom4-prop-box">
                                        <img
                                            src="<?php if ($listing_sql_row['profile_image'] != NULL || !empty($listing_sql_row['profile_image'])) {
                                                echo "images/listings/" . $listing_sql_row['profile_image'];
                                            } else {
                                                echo "images/listings/hot4.jpg";
                                            } ?>" alt="">
                                        <div>
                                            <h4>
                                                <a href="<?php echo $LISTING_URL . urlModifier($listing_sql_row['listing_slug']); ?>"><?php echo $listing_sql_row['listing_name']; ?></a>
                                            </h4>
                                            <?php if ($star_rate != 0) { ?>
                                                <label class="rat">
                                                    <?php
                                                    for ($i = 1; $i <= ceil($star_rate_two); $i++) {
                                                        ?>
                                                        <i class="material-icons">star</i>
                                                        <?php
                                                    }
                                                    $bal_star_rate = abs(ceil($star_rate_two) - 5);

                                                    for ($i = 1; $i <= $bal_star_rate; $i++) {
                                                        ?>
                                                        <i class="material-icons">star_border</i>
                                                        <?php
                                                    }
                                                    ?>
                                                </label>
                                            <?php } ?>
                                            <span><a
                                                    href="#"><?php echo $popular_business_category_sql_row['category_name']; ?></a></span>
                                        </div>
                                        <a href="<?php echo $LISTING_URL . urlModifier($listing_sql_row['listing_slug']); ?>"
                                           class="fclick"></a>
                                    </div>
                                </li>
                                <?php
                                $pop_bus++;
                            }
                            ?>
                        </ul>
                    </div>
                    <!-- END NEW FEATURE SERVICES -->
                </div>
            </div>
        </div>
    </section>
    <!-- END -->

    <!-- START -->
    <section>
        <div class="str">
            <div class="container">
                <div class="row">
                    <div class="home-tit">
                        <h2><span><?php echo $BIZBOOK['HOM3-OW-TIT']; ?></span></h2>
                        <p><?php echo $BIZBOOK['HOM3-OW-TIT-SUB']; ?></p>
                    </div>
                    <div class="hom2-hom-ban-main">
                        <div class="hom2-hom-ban hom2-hom-ban1">
                            <h2><?php echo $BIZBOOK['HOM3-OW-LHS-TIT']; ?></h2>
                            <p><?php echo $BIZBOOK['HOM3-OW-LHS-SUB']; ?></p>
                            <a href="pricing-details"><?php echo $BIZBOOK['HOM3-OW-LHS-CTA']; ?></a>
                        </div>
                        <div class="hom2-hom-ban hom2-hom-ban2">
                            <h2><?php echo $BIZBOOK['HOM3-OW-RHS-TIT']; ?></h2>
                            <p><?php echo $BIZBOOK['HOM3-OW-RHS-SUB']; ?></p>
                            <a href="login?login=register"><?php echo $BIZBOOK['HOM3-OW-RHS-CTA']; ?></a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- END -->

    <!-- START -->
    <section>
        <div class="str hom2-cus">
            <div class="container">
                <div class="row">
                    <div class="home-tit">
                        <h2><span><?php echo $BIZBOOK['HOM3-OW-USER-REVIEW']; ?></span></h2>
                        <p><?php echo $BIZBOOK['HOM3-OW-TIT-SUB']; ?></p>
                    </div>

                    <div class="hom2-cus-sli">
                        <ul class="multiple-items">
                            <?php
                            foreach (getTenActiveReviews() as $reviewss_row) {

                                $review_user_id = $reviewss_row['review_user_id'];

                                $listing_id = $reviewss_row['listing_id'];

                                $listing_sql_row = getIdListing($listing_id);

                                $user_details_row = getUser($review_user_id);

                                $featured_category_id = $listing_sql_row['category_id'];

                                $popular_business_category_sql_row = getCategory($featured_category_id);

                                // List Rating. for Rating of Star

                                if ($reviewss_row['price_rating'] > 0) {

                                    $star_rate = $reviewss_row['price_rating'];

                                } else {
                                    $star_rate = 0;
                                }

                                ?>
                                <li>
                                    <div class="testmo">
                                        <img
                                            src="images/user/<?php if (($user_details_row['profile_image'] == NULL) || empty($user_details_row['profile_image'])) {
                                                echo "1.jpg";
                                            } else {
                                                echo $user_details_row['profile_image'];
                                            } ?>" alt="">
                                        <h4><?php echo $user_details_row['first_name']; ?></h4>
                                    <span><?php echo $BIZBOOK['SERVICE-EXPERT-WRITTEN-REVIEW-TO']; ?> <a
                                            href="<?php echo $LISTING_URL . urlModifier($listing_sql_row['listing_slug']); ?>"><?php echo $listing_sql_row['listing_name']; ?></a></span>

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
                                                    <i class="material-icons">star_border</i>
                                                    <?php
                                                }
                                                ?>
                                            </label>
                                            <?php
                                        } ?>
                                        <p><?php echo $reviewss_row['review_message']; ?></p>
                                    </div>
                                </li>
                                <?php
                            } ?>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- END -->


    <!-- START -->
    <section>
        <div class="str count">
            <div class="container">
                <div class="row">

                    <div class="how-wrks">
                        <div class="home-tit">
                            <h2><span><?php echo $BIZBOOK['HOM-HOW-TIT']; ?></span></h2>
                            <p><?php echo $BIZBOOK['HOM-HOW-SUB-TIT']; ?></p>
                        </div>
                        <div class="how-wrks-inn">
                            <ul>
                                <li>
                                    <div>
                                        <span>1</span>
                                        <img src="images/icon/how1.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-1']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-1']; ?></p>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <span>2</span>
                                        <img src="images/icon/how2.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-2']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-2']; ?></p>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <span>3</span>
                                        <img src="images/icon/how3.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-3']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-3']; ?></p>
                                    </div>
                                </li>
                                <li>
                                    <div>
                                        <span>4</span>
                                        <img src="images/icon/how4.png" alt="">
                                        <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-4']; ?></h4>
                                        <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-4']; ?></p>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>

                    <?php if ($footer_row['admin_mobile_app_feature'] == 1) { ?>
                        <div class="mob-app">
                            <div class="lhs">
                                <img src="images/mobile.png" alt="">
                            </div>
                            <div class="rhs">
                                <h2><?php echo $BIZBOOK['HOM-APP-TIT']; ?>
                                    <span><?php echo $BIZBOOK['HOM-APP-TIT-SUB']; ?></span></h2>
                                <ul>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-1']; ?></li>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-2']; ?></li>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-3']; ?></li>
                                    <li><?php echo $BIZBOOK['HOM-APP-PO-4']; ?></li>
                                </ul>
                                <span><?php echo $BIZBOOK['HOM-APP-SEND']; ?></span>
                                <form>
                                    <ul>
                                        <li>
                                            <input type="email" placeholder="Enter email id" required></li>
                                        <li>
                                            <input type="submit" value="Get App Link"></li>
                                    </ul>
                                </form>
                                <a href="#"><img src="images/android.png" alt=""> </a>
                                <a href="#"><img src="images/apple.png" alt=""> </a>
                            </div>
                        </div>
                    <?php } ?>
                </div>
            </div>
        </div>
    </section>
    <!-- END -->

    <?php
}
?>