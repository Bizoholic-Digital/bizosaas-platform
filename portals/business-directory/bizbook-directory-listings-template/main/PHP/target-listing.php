<?php
include "header.php";

if (isset($_SESSION['user_id'])) {
    $session_user_id = $_SESSION['user_id'];
}


if ($_GET['code'] == NULL && empty($_GET['code'])) {

    header("Location: $redirect_url");  //Redirect When code parameter is empty
}

$page_codea1 = str_replace('-', ' ', $_GET['code']);
$page_codea = str_replace('.php', '', $page_codea1);

$page_row = getActivePageSlugwithoutStatus(1,$page_codea); // To Fetch particular Target Listing Data

if ($page_row['page_id'] == NULL && empty($page_row['page_id'])) {


    header("Location: $redirect_url");  //Redirect When No User Found in Table
}

$page_id = $page_row['page_id'];
seopageview($page_id); //Function To Find Page View

?>
<!-- START -->
<section>
    <div class="all-listing all-listing-pg">
        <!--FILTER ON MOBILE VIEW-->
        <div class="fil-mob fil-mob-act">
            <h4><?php echo $BIZBOOK['ALL-LISTING-LISTING-FILTERS']; ?> <i class="material-icons">filter_list</i></h4>
        </div>
        <div class="all-list-bre">
            <div class="container sec-all-list-bre">
                <div class="row">
                    
                        <h1><?php echo $page_row['page_name']; ?></h1>
                       
                    <ul>
                        <li><a href="<?php echo $webpage_full_link; ?>"><?php echo $BIZBOOK['HOME']; ?></a></li>
                        <li><a href="<?php echo $webpage_full_link.'all-listing'; ?>"><?php echo $BIZBOOK['ALL_CATEGORY']; ?></a></li>
                            <li>
                                <a href="<?php echo $TARGET_LISTING_URL.urlModifier($page_row['page_slug']); ?>"><?php echo $page_row['page_name']; ?></a>
                            </li>
                           
                    </ul>
                </div>
            </div>
        </div>
        <div class="container">
            <div class="row">
                <?php
                foreach (getAllListingFilter() as $all_listing_filter_row) {

                    ?>
                    <div class="col-md-3 fil-mob-view">
                        <div class="all-filt">
                            <span class="fil-mob-clo"><i class="material-icons">close</i></span>
                            <?php if ($all_listing_filter_row['service_filter'] == "Active") {
                                ?>
                                <!--START-->
                                <div class="filt-alist-near">
                                    <div class="tit"><h4><?php echo $BIZBOOK['ALL-LISTING-TOP-SERVICE-PROVIDERS']; ?></h4></div>
                                    <div class="near-ser-list">
                                        <ul>
                                            <?php
                                            $nearby_listsql = "SELECT " . TBL . "listings.*, " . TBL . "users.user_plan FROM " . TBL . "listings

                                            LEFT JOIN " . TBL . "users ON " . TBL . "listings.user_id = " . TBL . "users.user_id  WHERE " . TBL . "listings.listing_status= 'Active'

                                            AND " . TBL . "listings.listing_is_delete != '2' $category_search_query 

                                            ORDER BY " . TBL . "users.user_plan DESC," . TBL . "listings.listing_id DESC LIMIT 5 ";

                                            $nearby_listrs = mysqli_query($conn, $nearby_listsql);
                                            while ($nearby_listrow = mysqli_fetch_array($nearby_listrs)) {
                                                ?>
                                                <li>
                                                    <div class="near-bx">
                                                        <div class="ne-1">
                                                            <img
                                                                src="<?php echo $slash; ?><?php if ($nearby_listrow['profile_image'] != NULL || !empty($nearby_listrow['profile_image'])) {
                                                                    echo "images/listings/" . $nearby_listrow['profile_image'];
                                                                } else {
                                                                    echo "images/listings/hot4.jpg";
                                                                } ?>">
                                                        </div>
                                                        <div class="ne-2">
                                                            <h5><?php echo $nearby_listrow['listing_name']; ?></h5>
                                                            <p><?php echo $BIZBOOK['CITY'].':'; ?> <?php echo $nearby_listrow['listing_address']; ?></p>
                                                        </div>
                                                        <div class="ne-3">
                                                            <span>5.0</span>
                                                        </div>
                                                        <a href="<?php echo $LISTING_URL.urlModifier($listrow['listing_slug']); ?>"><?php echo $listrow['listing_name']; ?></a>
                                                    </div>
                                                </li>
                                                <?php
                                            }
                                            ?>
                                        </ul>
                                    </div>
                                </div>

                                <!--END-->
                                <!--START-->
                                <div class="filt-com lhs-search">
                                    <form>
                                        <ul>
                                            <li>
                                                <input type="text" id="search" placeholder="<?php echo $BIZBOOK['ALL-LISTING-SEARCH-SERVICE']; ?>">
                                            </li>
                                            <li>
                                                <input type="submit" value="">
                                            </li>
                                        </ul>
                                    </form>
                                </div>

                                <!--END-->
                            <?php }
                            if ($all_listing_filter_row['category_filter'] == "Active") {
                                ?>
                                <!--START-->
                                <div class="filt-com lhs-cate">
                                    <h4><?php echo $BIZBOOK['ALL-LISTING-CATEGORIES']; ?></h4>
                                    <div class="dropdown">
                                        <select onChange="SubcategoryFilter(this.value);" class="cat_check"
                                                name="cat_check" id="cat_check" class="chosen-select ">
                                            <option value=""><?php echo $BIZBOOK['SELECT_CATEGORY']; ?></option>
                                            <?php
                                            foreach (getAllActiveCategoriesPos() as $categories_row) {
                                                ?>
                                                ?>
                                                <option <?php if ($category_id === $categories_row['category_id']) {
                                                    echo 'selected';
                                                } ?>
                                                    value="<?php echo $categories_row['category_id']; ?>"><?php echo $categories_row['category_name']; ?></option>
                                                <?php
                                            }
                                            ?>
                                        </select>
                                    </div>
                                </div>
                                <!--END-->

                                <!--START-->
                                <div class="sub_cat_section filt-com lhs-sub">
                                    <h4><?php echo $BIZBOOK['ALL-LISTING-SUB-CATEGORY']; ?></h4>
                                    <ul>
                                        <?php
                                        if (isset($_GET['category'])) {
                                            $sub_category_qry = getCategorySubCategories($category_id);
                                        } else {
                                            $sub_category_qry = getAllSubCategories();
                                        }
                                        foreach ($sub_category_qry as $sub_category_row) { ?>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" class="sub_cat_check" name="sub_cat_check"
                                                           value="<?php echo $sub_category_row['sub_category_id']; ?>"
                                                           id="<?php echo $sub_category_row['sub_category_name']; ?>"/>
                                                    <label
                                                        for="<?php echo $sub_category_row['sub_category_name']; ?>"><?php echo $sub_category_row['sub_category_name']; ?></label>
                                                </div>
                                            </li>
                                            <?php
                                        }
                                        ?>
                                    </ul>
                                </div>
                                <!--END-->

                            <?php }
                            if ($all_listing_filter_row['feature_filter'] == "Active") {
                                ?>
                                <!--START-->
                                <div class="filt-com lhs-featu">
                                    <h4><?php echo $BIZBOOK['ALL-LISTING-FEATURES']; ?></h4>
                                    <ul>
                                        <?php
                                        foreach (getAllActiveFeaturedFilter() as $featuredfilterrow) {
                                            ?>

                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" name="feature_check"
                                                           value="<?php echo $featuredfilterrow['all_featured_filter_value']; ?>"
                                                           class="feature_check"
                                                           id="<?php echo $featuredfilterrow['all_featured_filter_value']; ?>"/>
                                                    <label
                                                        for="<?php echo $featuredfilterrow['all_featured_filter_value']; ?>"><?php echo $featuredfilterrow['all_featured_filter_name']; ?></label>
                                                </div>
                                            </li>
                                            <?php
                                        }
                                        ?>
                                    </ul>
                                </div>
                                <!--END-->
                            <?php }
                            ?>

                            <?php
                            if ($all_listing_filter_row['rating_filter'] == "Active") {
                                ?>
                                <!--START-->
                                <div class="filt-com lhs-rati">
                                    <h4><?php echo $BIZBOOK['RATINGS']; ?></h4>
                                    <ul>
                                        <li>
                                            <div class="rbbox">
                                                <input type="radio" value="5" name="rating_check"
                                                       class="rating_check"
                                                       id="rb1"/>
                                                <label for="rb1">
                                                    <i class="material-icons">star</i>
                                                    <i class="material-icons">star</i>
                                                    <i class="material-icons">star</i>
                                                    <i class="material-icons">star</i>
                                                    <i class="material-icons">star</i>
                                                </label>
                                            </div>
                                        </li>
                                        <li>
                                            <div class="rbbox">
                                                <input type="radio" value="4" name="rating_check"
                                                       class="rating_check"
                                                       id="rb2"/>
                                                <label for="rb2">
                                                    <i class="material-icons">star</i>
                                                    <i class="material-icons">star</i>
                                                    <i class="material-icons">star</i>
                                                    <i class="material-icons">star</i>
                                                    <i class="material-icons">star_border</i>
                                                </label>
                                            </div>
                                        </li>
                                        <li>
                                            <div class="rbbox">
                                                <input type="radio" value="3" name="rating_check"
                                                       class="rating_check"
                                                       id="rb3"/>
                                                <label for="rb3">
                                                    <i class="material-icons">star</i>
                                                    <i class="material-icons">star</i>
                                                    <i class="material-icons">star</i>
                                                    <i class="material-icons">star_border</i>
                                                    <i class="material-icons">star_border</i>
                                                </label>
                                            </div>
                                        </li>
                                        <li>
                                            <div class="rbbox">
                                                <input type="radio" value="2" name="rating_check"
                                                       class="rating_check"
                                                       id="rb4"/>
                                                <label for="rb4">
                                                    <i class="material-icons">star</i>
                                                    <i class="material-icons">star</i>
                                                    <i class="material-icons">star_border</i>
                                                    <i class="material-icons">star_border</i>
                                                    <i class="material-icons">star_border</i>
                                                </label>
                                            </div>
                                        </li>
                                        <li>
                                            <div class="rbbox">
                                                <input type="radio" value="1" name="rating_check"
                                                       class="rating_check"
                                                       id="rb5"/>
                                                <label for="rb5">
                                                    <i class="material-icons">star</i>
                                                    <i class="material-icons">star_border</i>
                                                    <i class="material-icons">star_border</i>
                                                    <i class="material-icons">star_border</i>
                                                    <i class="material-icons">star_border</i>
                                                </label>
                                            </div>
                                        </li>
                                    </ul>
                                </div>
                                <!--END-->
                                <?php
                            }
                            ?>
                            <!--START-->
                            <div class="filt-com lhs-ads">
                                <ul>
                                    <li>
                                        <div class="ads-box">
                                            <?php
                                            $ad_position_id = 4;   //Ad position on All Listing page Left
                                            $get_ad_row = getAds($ad_position_id);
                                            $ad_enquiry_photo = $get_ad_row['ad_enquiry_photo'];
                                            ?>
                                            <a href="<?php echo stripslashes($get_ad_row['ad_link']); ?>">
                                                <span><?php echo $BIZBOOK['AD']; ?></span>

                                                <img
                                                    src="<?php echo $slash; ?>images/ads/<?php if ($ad_enquiry_photo != NULL || !empty($ad_enquiry_photo)) {
                                                        echo $ad_enquiry_photo;
                                                    } else {
                                                        echo "ads1.jpg";
                                                    } ?>" alt="">
                                            </a>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                            <!--END-->

                            <div class="all-list-filt-form">
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
                                    <form name="home_slide_enquiry_form" id="home_slide_enquiry_form" method="post"
                                          enctype="multipart/form-data">
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
                                            <input type="text" name="enquiry_name" value="" required="required"
                                                   class="form-control"
                                                   placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>">
                                        </div>
                                        <div class="form-group">
                                            <input type="email" class="form-control" placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>"
                                                   required="required" value=""
                                                   name="enquiry_email"
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
                                            <textarea class="form-control" rows="3" name="enquiry_message" placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                                        </div>
                                        <input type="hidden" id="source">
                                        <button type="submit" id="home_slide_enquiry_submit"
                                                name="home_slide_enquiry_submit"
                                                class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT_REQUIREMENTS']; ?>
                                        </button>
                                    </form>
                                </div>
                            </div>
                            <!-- END -->
                        </div>
                    </div>
                    <?php
                }
                ?>
                <div class="col-md-9">
                    <div class="f2">
                        <div class="vfilter">
                            <i class="material-icons ic1 <?php if (isset($_GET['grid'])) {
                                echo "act";
                            } ?>" title="Grid view">apps</i>
                            <i class="material-icons ic2 <?php if (isset($_GET['list'])) {
                                echo "act";
                            } elseif (!isset($_GET['grid']) && !isset($_GET['list'])) {
                                echo "act";
                            } ?>" title="List view">format_list_bulleted</i>
                            <i class="material-icons ic3" title="Map view">location_on</i>
                        </div>
                    </div>

                    <!-- LISTING INN FILTER -->
                    <div class="list-filt-v2">
                        <ul>
                            <li>
                                <div class="chbox">
                                    <input type="checkbox" name="lfv2-all" value="" id="lfv2-all" checked/>
                                    <label for="lfv2-all"><?php echo $BIZBOOK['ALL-LISTING-FILTER-ALL']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="chbox">
                                    <input type="checkbox" name="lfv2-pop" value="" id="lfv2-pop"/>
                                    <label for="lfv2-pop"><?php echo $BIZBOOK['ALL-LISTING-FILTER-POPULAR']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="chbox">
                                    <input type="checkbox" name="lfv2-op" value="" id="lfv2-op"/>
                                    <label for="lfv2-op"><?php echo $BIZBOOK['ALL-LISTING-FILTER-OPEN']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="chbox">
                                    <input type="checkbox" name="lfv2-tru" value="" id="lfv2-tru"/>
                                    <label for="lfv2-tru"><?php echo $BIZBOOK['ALL-LISTING-FILTER-VERIFIED']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="chbox">
                                    <input type="checkbox" name="lfv2-near" value="" id="lfv2-near"/>
                                    <label for="lfv2-near"><?php echo $BIZBOOK['ALL-LISTING-FILTER-NEARBY']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="chbox">
                                    <input type="checkbox" name="lfv2-off" value="" id="lfv2-off"/>
                                    <label for="lfv2-off"><?php echo $BIZBOOK['ALL-LISTING-FILTER-OFFERS']; ?></label>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <!-- END LISTING INN FILTER -->

                    <div class="all-list-sh all-listing-total">
                        <!--ADS-->
                        <div class="ban-ati-com ads-all-list">
                            <?php
                            $ad_position_id = 2;   //Ad position on All Listing page Top
                            $get_ad_row = getAds($ad_position_id);
                            $ad_enquiry_photo = $get_ad_row['ad_enquiry_photo'];
                            ?>
                            <a href="<?php echo stripslashes($get_ad_row['ad_link']); ?>"><span><?php echo $BIZBOOK['AD']; ?></span><img
                                    src="<?php echo $slash; ?>images/ads/<?php if ($ad_enquiry_photo != NULL || !empty($ad_enquiry_photo)) {
                                        echo $ad_enquiry_photo;
                                    } else {
                                        echo "59040boat-728x90.png";
                                    } ?>"></a>
                        </div>
                        <!--ADS-->
                        <ul>
                            <?php

                            $page_listings = explode(',', $page_row['page_listings']);

                            if ($page_listings > 0) {

                            foreach ($page_listings as $listing_id) {

                                $listrow = getIdListing($listing_id);

                                    $listing_id = $listrow['listing_id'];
                                    $list_user_id = $listrow['user_id'];

                                    $usersqlrow = getUser($list_user_id); // To Fetch particular User Data

                                    // $star_rating_row = getListingReview($listing_id); // List Rating. for Rating of Star
                                    foreach (getListingReview($listing_id) as $star_rating_row) {
                                        if ($star_rating_row["rate_cnt"] > 0) {
                                            $star_rate_times = $star_rating_row["rate_cnt"];
                                            $star_sum_rates = $star_rating_row["total_rate"];
                                            $star_rate_one = $star_sum_rates / $star_rate_times;
                                            //$star_rate_one = (($Star_rate_value)/5)*100;
                                            $star_rate_two = number_format($star_rate_one, 1);
                                            $star_rate = floatval($star_rate_two);

                                        } else {
                                            $rate_times = 0;
                                            $rate_value = 0;
                                            $star_rate = 0;
                                        }
                                    }
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

                                    <li>
                                        <div class="eve-box">
                                            <!---LISTING IMAGE--->
                                            <div class="al-img">
                                                <?php
                                                if($listrow['listing_open'] == 1){
                                                    ?>
                                                    <span class="open-stat"><?php echo $BIZBOOK['OPEN']; ?></span>
                                                    <?php
                                                }
                                                ?>
                                                <a href="<?php echo $LISTING_URL.urlModifier($listrow['listing_slug']); ?>">
                                                    <img
                                                        src="<?php echo $slash; ?><?php if ($listrow['profile_image'] != NULL || !empty($listrow['profile_image'])) {
                                                            echo "images/listings/" . $listrow['profile_image'];
                                                        } else {
                                                            echo "images/listings/hot4.jpg";
                                                        } ?>">
                                                </a>

                                            </div>
                                            <!---END LISTING IMAGE--->

                                            <!---LISTING NAME--->
                                            <div>
                                                <h4>
                                                    <a href="<?php echo $LISTING_URL.urlModifier($listrow['listing_slug']); ?>"><?php echo $listrow['listing_name']; ?></a>
                                                    <i class="li-veri"><img src="<?php echo $slash; ?>images/icon/svg/verified.png"></i>
                                                </h4>
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
                                                    <a href="<?php echo $LISTING_URL.urlModifier($listrow['listing_slug']); ?>">View
                                                        more</a>
                                                    <a href="<?php echo $BIZBOOK['TEL']; ?>:<?php
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
                                           data-id='<?php echo $listing_id ?>'><img src="<?php echo $slash; ?>images/icon/svg/like.svg"></i></span>
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
                                                            <form method="post" name="all_enquiry_form"
                                                                  id="all_enquiry_form">
                                                                <input type="hidden" class="form-control"
                                                                       name="listing_id"
                                                                       value="<?php echo $listing_id ?>"
                                                                       placeholder=""
                                                                       required>
                                                                <input type="hidden" class="form-control"
                                                                       name="listing_user_id"
                                                                       value="<?php echo $list_user_id; ?>"
                                                                       placeholder=""
                                                                       required>
                                                                <input type="hidden" class="form-control"
                                                                       name="enquiry_sender_id"
                                                                       value="<?php echo $session_user_id; ?>"
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
                                                                        <textarea class="form-control" rows="3"
                                                                                  name="enquiry_message"
                                                                                  placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                                                                </div>
                                                                <input type="hidden" id="source">
                                                                <button type="submit" id="all_enquiry_submit"
                                                                        name="enquiry_submit"
                                                                        class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
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

                        <!--ADS-->
                        <div class="ban-ati-com ads-all-list">
                            <?php
                            $ad_position_id = 3;   //Ad position on All Listing page Bottom
                            $get_ad_row = getAds($ad_position_id);
                            $ad_enquiry_photo = $get_ad_row['ad_enquiry_photo'];
                            ?>
                            <a href="<?php echo stripslashes($get_ad_row['ad_link']); ?>"><span><?php echo $BIZBOOK['AD']; ?></span><img
                                    src="<?php echo $slash; ?>images/ads/<?php if ($ad_enquiry_photo != NULL || !empty($ad_enquiry_photo)) {
                                        echo $ad_enquiry_photo;
                                    } else {
                                        echo "59040boat-728x90.png";
                                    } ?>"></a>
                        </div>
                        <!--ADS-->
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<!-- START -->
<section>
    <div class="list-map">
        <?php
        include "listing-map-view.php";
        ?>
    </div>
</section>
<!-- END -->

<!-- START -->
<section>
    <div class="list-foot">
        <div class="container">
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
                        <b><?php if($new_star_rate != 0){ echo $new_star_rate; } else { echo $BIZBOOK['ALL-LISTING-0-RATINGS'];} ?></b>

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
                    if($cat_search_row['category_name'] != NULL) {
                        ?>
                        <h2><?php echo $cat_search_row['category_name']; ?></h2>
                        <?php
                    }
                    if($cat_search_row['category_description'] != NULL) {
                        ?>
                        <p><?php echo stripslashes($cat_search_row['category_name']); ?></p>
                        <?php
                    }
                    ?>
                </div>
                <?php
                if($cat_search_row['category_faq_1_ques'] != NULL || $cat_search_row['category_faq_2_ques'] != NULL
                    || $cat_search_row['category_faq_3_ques'] != NULL || $cat_search_row['category_faq_4_ques'] != NULL
                    || $cat_search_row['category_faq_5_ques'] != NULL || $cat_search_row['category_faq_6_ques'] != NULL
                    || $cat_search_row['category_faq_7_ques'] != NULL || $cat_search_row['category_faq_8_ques'] != NULL) {
                    ?>
                    <div class="list-foot-faq">
                        <h3><?php echo $BIZBOOK['FAQ']; ?></h3>
                        <div class="how-to-coll">
                            <ul>
                                <?php if($cat_search_row['category_faq_1_ques'] != NULL ) { ?>
                                    <li>
                                        <h4><?php echo $cat_search_row['category_faq_1_ques']; ?></h4>
                                        <?php if($cat_search_row['category_faq_1_ans'] != NULL ) { ?>
                                            <div>
                                                <p><?php echo $cat_search_row['category_faq_1_ans']; ?></p>
                                            </div>
                                        <?php } ?>
                                    </li>
                                <?php } ?>

                                <?php if($cat_search_row['category_faq_2_ques'] != NULL ) { ?>
                                    <li>
                                        <h4><?php echo $cat_search_row['category_faq_2_ques']; ?></h4>
                                        <?php if($cat_search_row['category_faq_2_ans'] != NULL ) { ?>
                                            <div>
                                                <p><?php echo $cat_search_row['category_faq_2_ans']; ?></p>
                                            </div>
                                        <?php } ?>
                                    </li>
                                <?php } ?>

                                <?php if($cat_search_row['category_faq_3_ques'] != NULL ) { ?>
                                    <li>
                                        <h4><?php echo $cat_search_row['category_faq_3_ques']; ?></h4>
                                        <?php if($cat_search_row['category_faq_3_ans'] != NULL ) { ?>
                                            <div>
                                                <p><?php echo $cat_search_row['category_faq_3_ans']; ?></p>
                                            </div>
                                        <?php } ?>
                                    </li>
                                <?php } ?>

                                <?php if($cat_search_row['category_faq_4_ques'] != NULL ) { ?>
                                    <li>
                                        <h4><?php echo $cat_search_row['category_faq_4_ques']; ?></h4>
                                        <?php if($cat_search_row['category_faq_4_ans'] != NULL ) { ?>
                                            <div>
                                                <p><?php echo $cat_search_row['category_faq_4_ans']; ?></p>
                                            </div>
                                        <?php } ?>
                                    </li>
                                <?php } ?>

                                <?php if($cat_search_row['category_faq_5_ques'] != NULL ) { ?>
                                    <li>
                                        <h4><?php echo $cat_search_row['category_faq_5_ques']; ?></h4>
                                        <?php if($cat_search_row['category_faq_5_ans'] != NULL ) { ?>
                                            <div>
                                                <p><?php echo $cat_search_row['category_faq_5_ans']; ?></p>
                                            </div>
                                        <?php } ?>
                                    </li>
                                <?php } ?>

                                <?php if($cat_search_row['category_faq_6_ques'] != NULL ) { ?>
                                    <li>
                                        <h4><?php echo $cat_search_row['category_faq_6_ques']; ?></h4>
                                        <?php if($cat_search_row['category_faq_6_ans'] != NULL ) { ?>
                                            <div>
                                                <p><?php echo $cat_search_row['category_faq_6_ans']; ?></p>
                                            </div>
                                        <?php } ?>
                                    </li>
                                <?php } ?>

                                <?php if($cat_search_row['category_faq_7_ques'] != NULL ) { ?>
                                    <li>
                                        <h4><?php echo $cat_search_row['category_faq_7_ques']; ?></h4>
                                        <?php if($cat_search_row['category_faq_7_ans'] != NULL ) { ?>
                                            <div>
                                                <p><?php echo $cat_search_row['category_faq_7_ans']; ?></p>
                                            </div>
                                        <?php } ?>
                                    </li>
                                <?php } ?>

                                <?php if($cat_search_row['category_faq_8_ques'] != NULL ) { ?>
                                    <li>
                                        <h4><?php echo $cat_search_row['category_faq_8_ques']; ?></h4>
                                        <?php if($cat_search_row['category_faq_8_ans'] != NULL ) { ?>
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
        </div>
    </div>
</section>
<!-- END -->

<?php
if($page_row['page_seo_schema'] != NULL) {
    ?>
    <!-- WEBSITE SCHEMA STARTS -->
    <h2 style="display: none"><?php echo $page_row['page_seo_schema']; ?></h2>
    <!-- WEBSITE SCHEMA ENDS -->
    <?php
}
?>

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
<script src="<?php echo $slash; ?>js/listing_filter.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>

<script>
    <?php
    if (isset($_GET['map'])) {
    ?>
    $(".all-list-bre, .all-listing").hide();
    $(".list-map").show();

    <?php
    }if (isset($_GET['grid'])) {
    ?>
    $(".list-map").hide();
    $(".all-list-bre, .all-listing").show();
    $('.all-list-sh').removeClass('cview3');
    $('.all-list-sh').addClass('cview1');

    <?php
    }if (isset($_GET['list'])) {
    ?>
    $(".list-map").hide();
    $(".all-list-bre, .all-listing").show();
    $('.all-list-sh').removeClass('cview1');
    $('.all-list-sh').removeClass('cview3');

    <?php
    }?>
</script>
<script>
    function SubcategoryFilter(val) {
        breadcrumbs(val);                        //Function call to change breadcrumb
        footerCategoryInfo(val);                        //Function call to change footer category data
        topServiceCategory(val);                        //Function call to change footer category data
        $(".sub_cat_section").css("opacity", 0);
        $.ajax({
            type: "POST",
            url: "<?php echo $slash; ?>sub_category_filter.php",
            data: 'category_id=' + val,
            success: function (data) {
                if (data == null) {
                    $(".sub_cat_section").remove();
                } else {
                    $(".sub_cat_section").html(data);
                    $(".sub_cat_section").css("opacity", 1);
                }

            }
        });
    }
</script>

<script>
    function breadcrumbs(val) {
        $(".sec-all-list-bre").css("opacity", 0);
        $.ajax({
            type: "POST",
            url: "<?php echo $slash; ?>category_filter_breadcrumb.php",
            data: 'category_id=' + val,
            success: function (data) {
                if (data == null) {
                    $(".sec-all-list-bre").css("opacity", 1);
                } else {
                    $(".sec-all-list-bre").html(data);
                    $(".sec-all-list-bre").css("opacity", 1);
                }

            }
        });
    }
</script>
<script>
    function footerCategoryInfo(val) {
        $(".sec-all-foot-cat-info").css("opacity", 0);
        $.ajax({
            type: "POST",
            url: "<?php echo $slash; ?>category_filter_footer.php",
            data: 'category_id=' + val,
            success: function (data) {
                if (data == null) {
                    $(".sec-all-foot-cat-info").css("opacity", 1);
                } else {
                    $(".sec-all-foot-cat-info").html(data);
                    $(".sec-all-foot-cat-info").css("opacity", 1);
                }

            }
        });
    }
</script>

<script>
    function topServiceCategory(val) {
        $(".top-ser-secti-prov").css("opacity", 0);
        $.ajax({
            type: "POST",
            url: "<?php echo $slash; ?>category_filter_top_provider_section.php",
            data: 'category_id=' + val,
            success: function (data) {
                if (data == null) {
                    $(".top-ser-secti-prov").css("opacity", 1);
                } else {
                    $(".top-ser-secti-prov").html(data);
                    $(".top-ser-secti-prov").css("opacity", 1);
                }

            }
        });
    }
</script>

<script>

    var scr_he = window.innerHeight;
    var fiscr_he = scr_he;
    if (scr_he >= 450) {
        $(".list-map-resu").css("height", fiscr_he);
    }
</script>

<!-- ALL SCHEMA -->


<?php
if($cat_search_row['category_google_schema'] != NULL) {
    ?>
    <!-- WEBSITE SCHEMA STARTS -->
    <h2 style="display: none"><?php echo $cat_search_row['category_google_schema']; ?></h2>
    <!-- WEBSITE SCHEMA ENDS -->
    <?php
}
?>

<script>
//    <!--- REVIEW SCHEMA -->
    <?php

    $page_listings = array_shift(explode(',', $page_row['page_listings']));

    if (count($page_listings) > 0) {

//    foreach ($page_listings as $listing_id) {

    $listrow_review_schema = getIdListing($page_listings);

    $listrs_review_schema_listing_id = $listrow_review_schema['listing_id'];
    $total_reviews = getCountListingReview($listrs_review_schema_listing_id);
    foreach (getListingReview($listrs_review_schema_listing_id) as $star_rating_row_review_schema) {
        if ($star_rating_row_review_schema["rate_cnt"] > 0) {
            $star_rate_times = $star_rating_row_review_schema["rate_cnt"];
            $star_sum_rates = $star_rating_row_review_schema["total_rate"];
            $star_rate_one = $star_sum_rates / $star_rate_times;
            //$star_rate_one = (($Star_rate_value)/5)*100;
            $star_rate_two = number_format($star_rate_one, 1);
            $star_rate_review_schema = floatval($star_rate_two);

        } else {
            $rate_times = 0;
            $rate_value = 0;
            $star_rate_review_schema = 0;
        }
    }
    if($total_reviews == 0){
        $new_count = 1;
    }else{
        $new_count = $total_reviews;
    }

    if($star_rate_review_schema == 0){
        $new_star_rate_review_schemat = 1;
    }else{
        $new_star_rate_review_schemat = $star_rate_review_schema;
    }

    ?>
</script>
    <script type="application/ld+json">
{
    "@context":"http:\/\/schema.org",
    "@type":"Review",
    "itemReviewed":
        {
            "@type":"LocalBusiness",
            "name":"<?php echo $listrow_review_schema['listing_name']; ?>",
            "image":"<?php echo $slash; ?><?php if ($listrow_review_schema['profile_image'] != NULL || !empty($listrow_review_schema['profile_image'])) {
            echo "images/listings/" . $listrow_review_schema['profile_image'];
        } else {
            echo "images/listings/hot4.jpg";
        } ?>",
            "url":"<?php echo $actual_link = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . "://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]"; ?>",
            "address":
            {
                "@type":"PostalAddress",
                "addressLocality":"<?php echo $listrow_review_schema['listing_address']; ?>",
                "telephone": "<?php echo $listrow_review_schema['listing_mobile']; ?>"
            },

                "priceRange": "1"
        },
        "author":"Users",
        "ReviewRating":
        {
            "@type":"AggregateRating",
            "ratingValue":"<?php echo $new_star_rate_review_schemat; ?>",
            "ratingCount":"<?php echo $new_count; ?>",
            "bestRating":"5"
        }
}

        </script>


<!-- ORGANIZATION SCHEMA -->
    <script type="application/ld+json">[
{
    "@context": "http://schema.org",
    "@type":"Organization",
    "name":"<?php echo $listrow_review_schema['listing_name']; ?>",
    "url":"<?php echo $LISTING_URL . urlModifier($listrow_review_schema['listing_slug']); ?>",
    "logo":"<?php echo $slash; ?><?php if ($listrow_review_schema['profile_image'] != NULL || !empty($listrow_review_schema['profile_image'])) {
            echo "images/listings/" . $listrow_review_schema['profile_image'];
        } else {
            echo "images/listings/hot4.jpg";
        } ?>",
    "sameAs":   [
        "<?php echo $listrow_review_schema['fb_link']; ?>",
        "<?php echo $listrow_review_schema['gplus_link']; ?>",
        "<?php echo $listrow_review_schema['twitter_link']; ?>"
        ]
}]

        </script>
<?php
//}
}
?>

<!-- LIST ITEM SCHEMA -->
<script type="application/ld+json">
		{
		"@context": "http://schema.org",
    	"@type": "ItemList",
    	"itemListElement" : [

    	<?php
    $page_listings = explode(',', $page_row['page_listings']);

     $total_count_list = count($page_listings);

    if ($page_listings > 0) {
        $si = 1;
        $comma = ',';
    foreach ($page_listings as $listing_id) {


    $listrow_list_item_schema = getIdListing($listing_id);

            ?>
            {
                "@type":"ListItem",
                "position":<?php echo $si; ?>,
                "url":"<?php echo $LISTING_URL . urlModifier($listrow_list_item_schema['listing_slug']); ?>"
            }<?php if ($total_count_list != $si) {
                echo $comma;
            } ?>

            <?php
            $si++;
        }
    }
    ?>
            ]
        }


</script>

</body>

</html>