<?php

//database configuration
if (file_exists('config/info.php')) {
    include('config/info.php');
}

$category_id = $_POST['category_id'];

$cat_search_row = getCategory($category_id);  //Fetch Category Id using category name


//get matched data from category table

    ?>
    <div class="row">
        <div class="list-foot-abo">
            <?php
            foreach (getAllListingCategory($cat_search_row['category_id']) as $categorywise_listings) {
                $categorywise_listing_id = $categorywise_listings['listing_id'];

                foreach (getListingReview($categorywise_listing_id) as $star_rating_row) {
                    if ($star_rating_row["rate_cnt"] > 0) {
                        $star_rate_times = $star_rating_row["rate_cnt"];
                        $star_sum_rates = $star_rating_row["total_rate"];
                        $star_rate_one = $star_sum_rates / $star_rate_times;
                        //$star_rate_one = (($Star_rate_value)/5)*100;
                        $star_rate_two = number_format($star_rate_one, 1);
//                                $star_rate = floatval($star_rate_two);
                        $star_rate = $star_rate_two;

                    } else {
                        $rate_times = 0;
                        $rate_value = 0;
                        $star_rate = 0;
                    }
                    $review_count = getCountListingReview($categorywise_listing_id);
                }
                $new_star_rate = $star_rate;
                $new_review_count = $review_count;
            }
            ?>
            <div class="list-rat-all">
                <h4><?php echo $BIZBOOK['ALL-LISTING-OVERALL-RATING']; ?></h4>
                <b><?php if ($new_star_rate != 0) {
                        echo $new_star_rate;
                    } else {
                        echo $BIZBOOK['ALL-LISTING-0-RATINGS'];
                    } ?></b>

                <?php
                if ($new_star_rate != 0) {
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
                <?php if ($new_review_count > 0) { ?>
                    <span><?php echo $new_review_count; ?> <?php echo $BIZBOOK['REVIEWS']; ?></span>
                    <?php
                }
                ?>
            </div>
            <?php
            if ($cat_search_row['category_name'] != NULL) {
                ?>
                <h2><?php echo $cat_search_row['category_name']; ?></h2>
                <?php
            }
            if ($cat_search_row['category_description'] != NULL) {
                ?>
                <?php echo stripslashes($cat_search_row['category_description']); ?>
                <?php
            }
            ?>
        </div>
        <?php
        if ($cat_search_row['category_faq_1_ques'] != NULL || $cat_search_row['category_faq_2_ques'] != NULL
            || $cat_search_row['category_faq_3_ques'] != NULL || $cat_search_row['category_faq_4_ques'] != NULL
            || $cat_search_row['category_faq_5_ques'] != NULL || $cat_search_row['category_faq_6_ques'] != NULL
            || $cat_search_row['category_faq_7_ques'] != NULL || $cat_search_row['category_faq_8_ques'] != NULL
        ) {
            ?>
            <div class="list-foot-faq">
                <h3><?php echo $BIZBOOK['FAQ']; ?></h3>
                <div class="how-to-coll">
                    <ul>
                        <?php if ($cat_search_row['category_faq_1_ques'] != NULL) { ?>
                            <li>
                                <h4><?php echo $cat_search_row['category_faq_1_ques']; ?></h4>
                                <?php if ($cat_search_row['category_faq_1_ans'] != NULL) { ?>
                                    <div>
                                        <p><?php echo $cat_search_row['category_faq_1_ans']; ?></p>
                                    </div>
                                <?php } ?>
                            </li>
                        <?php } ?>

                        <?php if ($cat_search_row['category_faq_2_ques'] != NULL) { ?>
                            <li>
                                <h4><?php echo $cat_search_row['category_faq_2_ques']; ?></h4>
                                <?php if ($cat_search_row['category_faq_2_ans'] != NULL) { ?>
                                    <div>
                                        <p><?php echo $cat_search_row['category_faq_2_ans']; ?></p>
                                    </div>
                                <?php } ?>
                            </li>
                        <?php } ?>

                        <?php if ($cat_search_row['category_faq_3_ques'] != NULL) { ?>
                            <li>
                                <h4><?php echo $cat_search_row['category_faq_3_ques']; ?></h4>
                                <?php if ($cat_search_row['category_faq_3_ans'] != NULL) { ?>
                                    <div>
                                        <p><?php echo $cat_search_row['category_faq_3_ans']; ?></p>
                                    </div>
                                <?php } ?>
                            </li>
                        <?php } ?>

                        <?php if ($cat_search_row['category_faq_4_ques'] != NULL) { ?>
                            <li>
                                <h4><?php echo $cat_search_row['category_faq_4_ques']; ?></h4>
                                <?php if ($cat_search_row['category_faq_4_ans'] != NULL) { ?>
                                    <div>
                                        <p><?php echo $cat_search_row['category_faq_4_ans']; ?></p>
                                    </div>
                                <?php } ?>
                            </li>
                        <?php } ?>

                        <?php if ($cat_search_row['category_faq_5_ques'] != NULL) { ?>
                            <li>
                                <h4><?php echo $cat_search_row['category_faq_5_ques']; ?></h4>
                                <?php if ($cat_search_row['category_faq_5_ans'] != NULL) { ?>
                                    <div>
                                        <p><?php echo $cat_search_row['category_faq_5_ans']; ?></p>
                                    </div>
                                <?php } ?>
                            </li>
                        <?php } ?>

                        <?php if ($cat_search_row['category_faq_6_ques'] != NULL) { ?>
                            <li>
                                <h4><?php echo $cat_search_row['category_faq_6_ques']; ?></h4>
                                <?php if ($cat_search_row['category_faq_6_ans'] != NULL) { ?>
                                    <div>
                                        <p><?php echo $cat_search_row['category_faq_6_ans']; ?></p>
                                    </div>
                                <?php } ?>
                            </li>
                        <?php } ?>

                        <?php if ($cat_search_row['category_faq_7_ques'] != NULL) { ?>
                            <li>
                                <h4><?php echo $cat_search_row['category_faq_7_ques']; ?></h4>
                                <?php if ($cat_search_row['category_faq_7_ans'] != NULL) { ?>
                                    <div>
                                        <p><?php echo $cat_search_row['category_faq_7_ans']; ?></p>
                                    </div>
                                <?php } ?>
                            </li>
                        <?php } ?>

                        <?php if ($cat_search_row['category_faq_8_ques'] != NULL) { ?>
                            <li>
                                <h4><?php echo $cat_search_row['category_faq_8_ques']; ?></h4>
                                <?php if ($cat_search_row['category_faq_8_ans'] != NULL) { ?>
                                    <div>
                                        <p><?php echo $cat_search_row['category_faq_8_ans']; ?></p>
                                    </div>
                                <?php } ?>
                            </li>
                        <?php } ?>

                    </ul>
                </div>
            </div>
            <?php
        }
        ?>
    </div>