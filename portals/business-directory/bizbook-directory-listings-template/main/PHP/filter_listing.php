<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */


if (file_exists('config/info.php')) {
    include('config/info.php');
}
if (isset($_SESSION['user_id'])) {
    $session_user_id = $_SESSION['user_id'];
}
$user_details_row = getUser($session_user_id); //Fetch User data

//Pagination Code Starts Here
$numberOfPages = 8;
$limit = 15;
if (isset($_GET["page"])) {
    $page = $_GET["page"];
} else {
    $page = 1;
};
$start_from = ($page - 1) * $limit;

//Pagination Code Ends Here


$scheck = $_REQUEST['scheck'];
$cat_check = $_REQUEST['cat_check'];
$sub_cat_check = $_REQUEST['sub_cat_check'];
$feature_check = $_REQUEST['feature_check'];
$city_check = $_REQUEST['city_check'];
$rating_check = $_REQUEST['rating_check'];

$check_all = $_REQUEST['lfv2_all_check'];
$check_popular = $_REQUEST['lfv2_pop_check'];
$check_open = $_REQUEST['lfv2_op_check'];
$check_trusted = $_REQUEST['lfv2_tru_check'];
$check_nearby = $_REQUEST['lfv2_near_check'];
$check_offers = $_REQUEST['lfv2_offer_check'];


$WHERE = array();
$inner = $w = '';
$order = 'ORDER BY';

// Open Check starts
if ($check_all == 'on') {
    $WHERE[] = 't1.listing_open = 1';
    $WHERE[] = 't1.listing_type_id = 4';
    $WHERE[] = "t1.service_1_name != '";
} else {

// Open Check starts
    if ($check_open == 'on') {
        $WHERE[] = 't1.listing_open = 1';
    }

// Popular Check starts
    if ($check_popular == 'on') {
        $order = " ORDER BY (select count(t5.listing_id) from `" . TBL . "page_views`) DESC,";
        $inner = "INNER JOIN `" . TBL . "page_views` AS t5  ON t1.listing_id = t5.listing_id";

    }

// Trusted Check starts
    if ($check_trusted == 'on') {
        $WHERE[] = '(t4.user_plan = 4 OR t4.user_plan = 3 OR t4.user_plan = 2)';
    }

// Nearby Check starts
    if ($check_nearby == 'on') {
        $current_lat = $_SESSION['latitude'];
        $current_long = $_SESSION['longitude'];
        $WHERE[] = "(t1.listing_lat <= $current_lat OR t1.listing_lng <= $current_long)";
    }

// Offers Check starts
    if ($check_offers == 'on') {
        $WHERE[] = "t1.service_1_name != ''";
    }
}


// Category Check starts
if (!empty($cat_check)) {
    if (strstr($cat_check, ',')) {
        $data2 = explode(',', $cat_check);
        $cat_array = array();
        foreach ($data2 as $c) {
            $cat_array[] = "FIND_IN_SET($c,t1.category_id)";

        }
        $WHERE[] = '(' . implode(' OR ', $cat_array) . ')';
    } else {
        $WHERE[] = '(FIND_IN_SET(' . $cat_check . ',t1.category_id))';

    }
}

// Category Check Ends


//Sub Category Check starts
if (!empty($sub_cat_check)) {
    if (strstr($sub_cat_check, ',')) {
        $data2 = explode(',', $sub_cat_check);
        $sub_cat_array = array();
        foreach ($data2 as $c) {
            $sub_cat_array[] = "FIND_IN_SET($c,t1.sub_category_id)";

        }
        $WHERE[] = '(' . implode(' OR ', $sub_cat_array) . ')';
    } else {
        $WHERE[] = '(FIND_IN_SET(' . $sub_cat_check . ',t1.sub_category_id))';

    }
}

//Sub Category Check Ends

//City Check starts
if (!empty($city_check)) {

    if (strstr($city_check, ',')) {
        $data8 = explode(',', $city_check);
        $cityarray = array();
        foreach ($data8 as $ci) {
            $cityarray[] = "FIND_IN_SET($ci,t1.city_id)";

        }
        $WHERE[] = '(' . implode(' OR ', $cityarray) . ')';
    } else {
        $WHERE[] = '(FIND_IN_SET(' . $city_check . ',t1.city_id))';

    }

}

//City Check Ends


//Rating Check Starts

if (!empty($rating_check)) {
    if (strstr($rating_check, ',')) {
        $data3 = explode(',', $rating_check);
        $rate_array = array();
        foreach ($data3 as $c) {
            $rate_array[] = "t2.price_rating = $c";
        }
        $WHERE[] = '(' . implode(' OR ', $rate_array) . ')';
    } else {
        $WHERE[] = '(t2.price_rating = ' . $rating_check . ')';
    }

    $inner = "INNER JOIN `" . TBL . "reviews` AS t2 ON t1.listing_id = t2.listing_id";

}

//Rating Check Ends

if (!empty($price_range)) {
    $data3 = explode('-', $price_range);
    $WHERE[] = "(t1.product_rate between $data3[0] and $data3[1])";
}

if (!empty($scheck)) {
    if (strstr($scheck, ',')) {
        $data3 = explode(',', $scheck);
        $sarray = array();
        foreach ($data3 as $c) {
            $sarray[] = "t2.size_id = $c";
        }
        $WHERE[] = '(' . implode(' OR ', $sarray) . ')';
    } else {
        $WHERE[] = '(t2.size_id = ' . $scheck . ')';
    }

    $inner = 'INNER JOIN `product_size_quantity` AS t2 ON t1.product_id = t2.product_id';

}

if (!empty($category_id)) {
    if (strstr($category_id, ',')) {
        $data4 = explode(',', $category_id);
        $ctarray = array();
        foreach ($data4 as $ct) {
            $ctarray[] = "t1.product_category_id = $ct";
        }
        $WHERE[] = '(' . implode(' OR ', $ctarray) . ')';
    } else {
        $WHERE[] = '(t1.product_category_id = ' . $category_id . ')';
    }
}

$w = implode(' AND ', $WHERE);
if (!empty($w)) {
    $w = 'WHERE ' . $w;
    $q = 'AND ';
} else {
    $q = 'WHERE ';
}

$query = mysqli_query($conn, "SELECT DISTINCT  t1 . * , t4.user_plan FROM " . TBL . "listings AS t1 LEFT JOIN " . TBL . "users AS t4 ON t1.user_id = t4.user_id $inner $w $q listing_status= 'Active' AND listing_is_delete != '2' $order t1.display_position DESC, t4.user_plan DESC,t1.listing_id DESC ");

$total_count_listings = mysqli_num_rows($query);
?>

<div class="all-list-sh all-listing-total">
    <div class="container ser-re-hu ser-re-cout"><?php echo $BIZBOOK['ALL-LISTING-TOTAL-OF']; ?> <?php echo $total_count_listings; ?> <?php echo $BIZBOOK['ALL-LISTING-BUSINESS-RESULTS-FOUND']; ?></div>
    <ul class="all-list-wrapper">
        <?php
        if ($total_count_listings > 0) {

            while ($listrow = mysqli_fetch_array($query)) {

                $listing_id = $listrow['listing_id'];
                $list_user_id = $listrow['user_id'];

                $usersqlrow = getUser($list_user_id); // To Fetch particular User Data

//                $star_rating_row = getListingReview($listing_id); // List Rating. for Rating of Star
                foreach (getListingReview($listing_id) as $star_rating_row) {
                    if ($star_rating_row["rate_cnt"] > 0) {
                        $star_rate_times = $star_rating_row["rate_cnt"];
                        $star_sum_rates = $star_rating_row["total_rate"];
                        $star_rate_one = $star_sum_rates / $star_rate_times;
                        $star_rate_two = number_format($star_rate_one, 1);
                        $star_rate = floatval($star_rate_two);

                    } else {
                        $rate_times = 0;
                        $rate_value = 0;
                        $star_rate = 0;
                    }
                }

                $review_count = getCountListingReview($listing_id); //Listing Reviews Count

                $listing_likes_total = getCountUserLikedListing($listing_id, $session_user_id); // To get count of likes

                if ($listing_likes_total >= 1) {
                    $check_listing_likes_total = 0;
                    $active_listing_likes = 'sav-act';
                } else {
                    $check_listing_likes_total = 1;
                    $active_listing_likes = '';
                }
                
                //Likes Query Ends
                ?>

                <li class="all-list-item">
                    <div class="eve-box">
                        <!---LISTING IMAGE--->
                        <div class="al-img">
                            <?php
                            if ($listrow['listing_open'] == 1) {
                                ?>
                                <span class="open-stat"><?php echo $BIZBOOK['OPEN']; ?></span>
                                <?php
                            }
                            ?>
                            <a href="<?php echo $LISTING_URL . urlModifier($listrow['listing_slug']); ?>">
                                <img
                                    src="<?php echo $webpage_full_link; ?><?php if ($listrow['profile_image'] != NULL || !empty($listrow['profile_image'])) {
                                        echo "images/listings/" . $listrow['profile_image'];
                                    } else {
                                        echo "images/listings/hot4.jpg";
                                    } ?>">
                            </a>

                        </div>
                        <!---END LISTING IMAGE--->

                        <!---LISTING NAME--->
                        <div class="list-con">
                            <h4>
                                <a href="<?php echo $LISTING_URL . urlModifier($listrow['listing_slug']); ?>"><?php echo $listrow['listing_name']; ?></a>
                                <?php if ($listrow['user_plan'] == 4 || $listrow['user_plan'] == 3 || $listrow['user_plan'] == 2) { ?>
                                    <i class="li-veri"><img src="<?php echo $webpage_full_link; ?>images/icon/svg/verified.png"></i>
                                <?php } ?>
                            </h4>
                            <div class="list-rat-all">
                                <?php
                                if ($star_rate != 0) {
                                    ?>
                                    <b><?php echo $star_rate_two; ?></b>
                                    <?php
                                } ?>
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
                                ?><?php
                                if ($star_rate != 0) {
                                    ?>
                                    <span><?php echo $review_count; ?> <?php echo $BIZBOOK['REVIEWS']; ?></span>
                                    <?php
                                } else {
                                    ?>
                                    <span><?php echo $BIZBOOK['NO_REVIEWS_YET']; ?></span>
                                    <?php
                                }
                                ?>
                            </div>
                            <span
                                class="addr"><?php echo $listrow['listing_address']; ?></span>
                                        <span class="pho"><?php
                                            if ($listrow['listing_mobile'] != NULL || $usersqlrow['mobile_number'] != NULL) {

                                                if ($list_user_id == 1) {
                                                    echo $listrow['listing_mobile'];
                                                } else {
                                                    echo $usersqlrow['mobile_number'];
                                                } ?>
                                                <?php
                                            }
                                            ?></span>
                                        <span class="mail"><?php
                                            if ($usersqlrow['email_id'] != NULL) {

                                                echo $usersqlrow['email_id'];
                                                ?>
                                                <?php
                                            }
                                            ?></span>

                            <div class="links">
                                <?php if ($session_user_id != NULL || !empty($session_user_id)) {
                                    ?>
                                    <a href="#" data-toggle="modal"
                                        <?php
                                        if ($list_user_id != 1) { ?>
                                            data-target="#quote<?php echo $listing_id ?>"
                                            <?php
                                        }
                                        ?> class="quo"><?php echo $BIZBOOK['LEAD-GET-QUOTE']; ?></a>
                                    <?php
                                } else { ?>
                                    <a href="<?php echo $LOGIN_URL; ?>"><?php echo $BIZBOOK['LEAD-GET-QUOTE']; ?></a>
                                    <?php
                                }
                                ?>
                                <a href="<?php echo $LISTING_URL . urlModifier($listrow['listing_slug']); ?>"><?php echo $BIZBOOK['VIEW_MORE']; ?></a>
                                <a href="Tel:<?php
                                if ($listrow['listing_mobile'] != NULL || $usersqlrow['mobile_number'] != NULL) {
                                    if ($list_user_id == 1) {
                                        echo $listrow['listing_mobile'];
                                    } else {
                                        echo $usersqlrow['mobile_number'];
                                    } ?> <?php } ?>"><?php echo $BIZBOOK['CALL_NOW']; ?></a>
                                <a href="https://wa.me/<?php
                                if ($listrow['listing_whatsapp'] != NULL) {
                                    echo $listrow['listing_whatsapp'];
                                } else {
                                    if ($listrow['listing_mobile'] != NULL || $usersqlrow['mobile_number'] != NULL) {

                                        if ($list_user_id == 1) {
                                            echo $listrow['listing_mobile'];
                                        } else {
                                            echo $usersqlrow['mobile_number'];
                                        }
                                    }
                                }
                                ?>" class="what" target="_blank"><?php echo $BIZBOOK['WHATSAPP']; ?></a>
                            </div>

                        </div>
                        <!---END LISTING NAME--->

                        <!---SAVE--->
                                    <span class="enq-sav" data-toggle="tooltip"
                                          title="<?php if ($active_listing_likes == '') { ?>Click to like this listing<?php } else { ?> Click to Unlike this listing <?php } ?>">
                                        <i class="l-like Animatedheartfunc<?php echo $listing_id ?> <?php echo $active_listing_likes; ?>"
                                           data-for="<?php echo listing_total_like_count($listing_id); ?>"
                                           data-section="<?php echo $check_listing_likes_total; ?>"
                                           data-num="<?php echo $list_user_id; ?>"
                                           data-item="<?php echo $session_user_id; ?>"
                                           data-id='<?php echo $listing_id ?>'><img src="<?php echo $webpage_full_link; ?>images/icon/svg/like.svg"></i></span>
                        <!---END SAVE--->
                    </div>
                </li>


                <!--  Get Quote Pop up box starts  -->
                <section>
                    <div class="pop-ups pop-quo">
                        <!-- The Modal -->
                        <div class="modal fade" id="quote<?php echo $listing_id ?>">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="log-bor">&nbsp;</div>
                                    <span class="udb-inst"><?php echo $BIZBOOK['LEAD-SEND-ENQUIRY']; ?></span>
                                    <button type="button" class="close"
                                            data-dismiss="modal">&times;</button>
                                    <!-- Modal Header -->
                                    <div class="quote-pop">
                                        <h4><?php echo $BIZBOOK['LEAD-GET-QUOTE']; ?></h4>
                                        <div id="enq_success" class="log"
                                             style="display: none;">
                                            <p><?php echo $BIZBOOK['ENQUIRY_SUCCESSFUL_MESSAGE']; ?></p>
                                        </div>
                                        <div id="enq_fail" class="log" style="display: none;">
                                            <p><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></p>
                                        </div>
                                        <div id="enq_same" class="log" style="display: none;">
                                            <p><?php echo $BIZBOOK['ENQUIRY_OWN_LISTING_MESSAGE']; ?></p>
                                        </div>
                                        <form method="post" name="enquiry_form" id="enquiry_form">
                                            <input type="hidden" class="form-control" name="listing_id"
                                                   value=""
                                                   placeholder=""
                                                   required>
                                            <input type="hidden" class="form-control"
                                                   name="listing_user_id"
                                                   value="<?php echo $list_user_id; ?>" placeholder=""
                                                   required>
                                            <input type="hidden" class="form-control"
                                                   name="enquiry_sender_id"
                                                   value="<?php echo $session_user_id; ?>"
                                                   placeholder=""
                                                   required>
                                            <div class="form-group">
                                                <input type="text" readonly name="enquiry_name"
                                                       value="<?php echo $user_details_row['first_name'] ?>"
                                                       required="required" class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>">
                                            </div>
                                            <div class="form-group">
                                                <input type="email" class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>" readonly="readonly"
                                                       value="<?php echo $user_details_row['email_id'] ?>"
                                                       name="enquiry_email"
                                                       pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                                       title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>" required>
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
                                                <textarea class="form-control" rows="3" name="enquiry_message"
                                                          placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                                            </div>
                                            <input type="hidden" id="source">
                                            <button type="submit" id="enquiry_submit" name="enquiry_submit"
                                                    class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?>
                                            </button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
                <!--  Get Quote Pop up box ends  -->
                
                <?php
            }
        } else {
            ?>
            <span style="    font-size: 21px;
    color: #bfbfbf;
    letter-spacing: 1px;
    /* background: #525252; */
    text-shadow: 0px 0px 2px #fff;
    text-transform: uppercase;
    margin-top: 5%;"><?php echo $BIZBOOK['LISTINGS_NO_LISTINGS_MESSAGE']; ?></span>
            <?php
        }
        ?>

    </ul>
    <div id="all-list-pagination-container"></div>
</div>

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->

<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link ='<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url ='<?php echo $LOGIN_URL;?>';</script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>js/listing_filter.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>
<script src="<?php echo $slash; ?>js/jquery.simplePagination.min.js"></script>
<script>
    function listings_paginate() {
        var items = $(".all-list-wrapper .list-item");
        var numItems = items.length;
        var perPage = 10;

        items.slice(perPage).hide();

        $('#all-list-pagination-container').pagination({
            items: numItems,
            itemsOnPage: perPage,
            prevText: "&laquo;",
            nextText: "&raquo;",
            onPageClick: function (pageNumber) {
                var showFrom = perPage * (pageNumber - 1);
                var showTo = showFrom + perPage;
                items.hide().slice(showFrom, showTo).show();
            }
        });
        return true;
    }
</script>