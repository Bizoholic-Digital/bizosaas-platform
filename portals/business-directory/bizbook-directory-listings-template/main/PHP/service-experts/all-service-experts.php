<?php
include "expert-config-info.php";
include "../header.php";

if($footer_row['admin_expert_show'] != 1) {
    header("Location: ".$webpage_full_link."dashboard");
}

if (isset($_SESSION['user_id'])) {
    $session_user_id = $_SESSION['user_id'];
}

$user_details_row = getUser($session_user_id);

if (isset($_GET['category'])) {


    $category_search_slug1 = str_replace('-', ' ', $_GET['category']);

    $category_search_slug = str_replace('.php', '', $category_search_slug1);

    $cat_search_row = getSlugExpertCategory($category_search_slug);  //Fetch Category Id using category name

    $category_id = $cat_search_row['category_id'];

    $category_slug = $cat_search_row['category_slug'];

    $category_search_name = $cat_search_row['category_name'];

    $category_search_query = "AND FIND_IN_SET($category_id, T1.category_id)";


}


//Service Availability Check starts
if (isset($_REQUEST['availability'])) {

    $get_availability = $_REQUEST['availability'];

    if ($get_availability != 3) {

        $service_availability_search_query = 'AND T1.expert_availability_status = ' . $get_availability ;

    }

}

//Service Availability Check Ends


//Service Verified Check starts
if (isset($_REQUEST['verified']) && !empty($_REQUEST['verified'])) {

    $get_verified = $_REQUEST['verified'];

if ($get_verified == 2) {

    $service_verified_search_query = 'AND T1.user_plan >= ' . $get_verified . '';
}

}

//Service Verified Check Ends

//Service Ratings Check starts
if (isset($_REQUEST['ratings']) && !empty($_REQUEST['ratings'])) {

    $get_ratings = $_REQUEST['ratings'];

    $service_rating_start_query = ', T3.*';
    $service_rating_end_query = "INNER JOIN `" . TBL . "expert_reviews` AS T3 ON T1.expert_id = T3.expert_id";

    $service_rating_search_query = 'AND T3.expert_rating = ' . $get_ratings . '';

}

//Service Ratings Check Ends

//Service Ratings Order By Check starts
if (isset($_REQUEST['sort_by']) && !empty($_REQUEST['sort_by'])) {

    $get_rating_order = $_REQUEST['sort_by'];

    if ($get_rating_order != 0) {

        $service_sort_by_search_query = 'AND T2.enquiry_status = 500';
        $service_start_search_query = ', T2.enquiry_id, T2.enquiry_status, COUNT(T2.enquiry_id) as top';
        $service_end_search_query = "INNER JOIN " . TBL . "expert_enquiries AS T2 ON T1.expert_id = T2.expert_id";

        if ($get_rating_order == 2) {

            $service_sort_by_search_order_query = 'ORDER BY top DESC';
        }

        if ($get_rating_order == 1) {

            $service_sort_by_search_order_query = 'ORDER BY top ASC';
        }
    }else{
        $service_sort_by_search_order_query = 'ORDER BY T1.expert_id DESC';
    }

}else{
    $service_sort_by_search_order_query = 'ORDER BY T1.expert_id DESC';
}

//Service Ratings Order By Check Ends

//Service Expert Location Check starts
if (isset($_REQUEST['city']) && !empty($_REQUEST['city'])) {

    $get_city = $_REQUEST['city'];

    if (strstr($get_city, ',')) {
        $data56 = explode(',', $get_city);
        $sub_cat_array2 = array();
        foreach ($data56 as $c) {
            $sub_cat_array2[] = "FIND_IN_SET($c,T1.city_id)";

        }
        $expert_location_search_query = 'AND (' . implode(' OR ', $sub_cat_array2) . ')';
    } else {
        $expert_location_search_query = 'AND (FIND_IN_SET(' . $get_city . ',T1.city_id))';

    }
}

//Service Expert Type Check Ends


?>
<style>
    .hom2-cus-sli ul {
        position: relative;
        overflow: hidden;
        padding: 20px 20px 0
    }

    .slick-arrow {
        width: 50px;
        height: 50px;
        border-radius: 50px;
        background: #fff;
        border: 1px solid #ededed;
        color: #ffffff03;
        position: absolute;
        z-index: 9;
        top: 38%
    }

    .slick-arrow:before {
        content: 'chevron_left';
        font-size: 27px;
        top: 4px;
        left: 9px
    }

    .slick-prev {
        left: 14px
    }

    .slick-next {
        right: 14px
    }

    .slick-next:before {
        content: 'chevron_right';
        font-size: 27px
    }
</style>

<!-- START -->
<section>
    <div class="all-listing all-jobs all-serexp">
        <!--FILTER ON MOBILE VIEW-->
        <div class="fil-mob fil-mob-act">
            <h4>Listing filters <i class="material-icons">filter_list</i></h4>
        </div>
        <div class="container">
            <div class="row">
                <div class="col-md-3 fil-mob-view">
                    <!--- START --->
                    <div class="filt-com">
                        <div class="job-alert">
                            <h5><?php echo $BIZBOOK['SERVICE-EXPERTS-ALL-HEADER-TEXT']; ?></h5>
                            <p><?php echo $BIZBOOK['SERVICE-EXPERTS-ALL-P-TEXT']; ?></p>
                            <a href="#" data-toggle="modal"
                               data-target="#allexpfrm"><?php echo $BIZBOOK['SERVICE-EXPERTS-ALL-A-TEXT']; ?></a>
                        </div>
                    </div>
                    <!--- END --->
                    <!--- START --->
                    <div class="filt-com lhs-cate">
                        <h4><?php echo $BIZBOOK['ALL-LISTING-CATEGORIES']; ?></h4>
                        <div class="form-group">
                            <select name="cat_check" id="cat_check" class="cat_check chosen-select">
                                <option value=""><?php echo $BIZBOOK['SELECT_CATEGORY']; ?></option>
                                <?php
                                foreach (getAllActiveExpertCategoriesPos() as $categories_row) {
                                    ?>
                                    <option <?php if ($category_slug == $categories_row['category_slug']) {
                                        echo 'selected';
                                    } ?>
                                        value="<?php echo urlModifier($categories_row['category_slug']); ?>"><?php echo $categories_row['category_name']; ?></option>
                                    <?php
                                }
                                ?>
                            </select>
                        </div>
                    </div>
                    <!--- END --->
                    <!--- START --->
                    <div class="filt-com lhs-loc">
                        <h4><?php echo $BIZBOOK['SERVICE-EXPERT-LOCATION']; ?></h4>
                        <div class="form-group">
                            <select class="city_check chosen-select" name="city_check" id="city_check">
                                <option value=""><?php echo $BIZBOOK['SELECT_CITY']; ?></option>
                                <?php
                                $expert_location_qry = getAllExpertsGroupByCity();

                                foreach ($expert_location_qry as $expert_location_row) {

                                    $expert_location = $expert_location_row['city_id'];

                                    $expert_city_row = getExpertCity($expert_location);

                                    ?>
                                    <option <?php if ($get_city == $expert_city_row['country_id']) {
                                        echo 'selected';
                                    } ?>
                                        value="<?php echo $expert_city_row['country_id']; ?>"><?php echo $expert_city_row['country_name']; ?></option>
                                    <?php
                                }
                                ?>
                            </select>
                        </div>
                    </div>
                    <!--- END --->

                    <!--- START --->
                    <div class="filt-com lhs-rati lhs-avail">
                        <h4><?php echo $BIZBOOK['SERVICE-EXPERT-AVAILABILITY']; ?></h4>
                        <ul>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="3" name="expert_avail" class="availability_check"
                                           id="avail1"
                                        <?php if ($get_availability == 3 || $get_availability == '') {
                                            echo 'checked';
                                        } ?>/>
                                    <label for="avail1"><?php echo $BIZBOOK['SERVICE-EXPERT-ALL-LABEL']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="0" name="expert_avail" class="availability_check"
                                           id="avail2"
                                        <?php if ($get_availability == 0) {
                                            echo 'checked';
                                        } ?>/>
                                    <label
                                        for="avail2"><?php echo $BIZBOOK['SERVICE-EXPERT-AVAILABLE-LABEL']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="1" name="expert_avail" class="availability_check"
                                           id="avail3"
                                        <?php if ($get_availability == 1) {
                                            echo 'checked';
                                        } ?>/>
                                    <label for="avail3"><?php echo $BIZBOOK['SERVICE-EXPERT-BUSY-LABEL']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="2" name="expert_avail" class="availability_check"
                                           id="avail4"
                                        <?php if ($get_availability == 2) {
                                            echo 'checked';
                                        } ?>/>
                                    <label
                                        for="avail4"><?php echo $BIZBOOK['SERVICE-EXPERT-CLOSED-TODAY-LABEL']; ?></label>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <!--- END --->

                    <!--- START --->
                    <div class="filt-com lhs-rati lhs-ver">
                        <h4><?php echo $BIZBOOK['SERVICE-EXPERT-VERIFIED-LABEL']; ?></h4>
                        <ul>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="1" name="expert_veri" class="expert_veri" id="exver1"
                                        <?php if ($get_verified == 1 || $get_verified == '') {
                                            echo 'checked';
                                        } ?>/>
                                    <label for="exver1"><?php echo $BIZBOOK['SERVICE-EXPERT-ALL-LABEL']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="2" name="expert_veri" class="expert_veri" id="exver2"
                                        <?php if ($get_verified == 2) {
                                            echo 'checked';
                                        } ?>/>
                                    <label
                                        for="exver2"><?php echo $BIZBOOK['SERVICE-EXPERT-VERIFIED-EXPERTS-LABEL']; ?></label>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <!--- END --->

                    <!--- START --->
                    <div class="filt-com lhs-rati">
                        <h4><?php echo $BIZBOOK['SERVICE-EXPERT-RATING-LABEL']; ?></h4>
                        <ul>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="0" name="expert_rat" class="rating_check" id="exrat6"
                                        <?php if ($get_ratings == 0 || $get_ratings == '') {
                                            echo 'checked';
                                        } ?>/>
                                    <label for="exrat6"><?php echo $BIZBOOK['SERVICE-EXPERT-ALL-LABEL']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="5" name="expert_rat" class="rating_check" id="exrat1"
                                        <?php if ($get_ratings == 5) {
                                            echo 'checked';
                                        } ?>/>
                                    <label for="exrat1">5 <?php echo $BIZBOOK['SERVICE-EXPERT-STAR-LABEL']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="4" name="expert_rat" class="rating_check" id="exrat2"
                                        <?php if ($get_ratings == 4) {
                                            echo 'checked';
                                        } ?>/>
                                    <label for="exrat2">4 <?php echo $BIZBOOK['SERVICE-EXPERT-STAR-LABEL']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="3" name="expert_rat" class="rating_check" id="exrat3"
                                        <?php if ($get_ratings == 3) {
                                            echo 'checked';
                                        } ?>/>
                                    <label for="exrat3">3 <?php echo $BIZBOOK['SERVICE-EXPERT-STAR-LABEL']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="2" name="expert_rat" class="rating_check" id="exrat4"
                                        <?php if ($get_ratings == 2) {
                                            echo 'checked';
                                        } ?>/>
                                    <label for="exrat4">2 <?php echo $BIZBOOK['SERVICE-EXPERT-STAR-LABEL']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="1" name="expert_rat" class="rating_check" id="exrat5"
                                        <?php if ($get_ratings == 1) {
                                            echo 'checked';
                                        } ?>/>
                                    <label for="exrat5">1 <?php echo $BIZBOOK['SERVICE-EXPERT-STAR-LABEL']; ?></label>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <!--- END --->
                    <!--- START --->
                    <div class="filt-com lhs-rati lhs-ver">
                        <h4><?php echo $BIZBOOK['SERVICE-EXPERT-SERVICES-DONE']; ?></h4>
                        <ul>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="0" name="expert_ser_cou" class="expert_ser_cou"
                                           id="exsercou1" <?php if ($get_rating_order == 0 || $get_rating_order == '') {
                                        echo 'checked';
                                    } ?>/>
                                    <label for="exsercou1"><?php echo $BIZBOOK['SERVICE-EXPERT-ALL-LABEL']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="2" name="expert_ser_cou" class="expert_ser_cou"
                                           id="exsercou2" <?php if ($get_rating_order == 2) {
                                        echo 'checked';
                                    } ?>/>
                                    <label
                                        for="exsercou2"><?php echo $BIZBOOK['SERVICE-EXPERT-HIGH-LOW-LABEL']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="rbbox">
                                    <input type="radio" value="1" name="expert_ser_cou" class="expert_ser_cou"
                                           id="exsercou3" <?php if ($get_rating_order == 1) {
                                        echo 'checked';
                                    } ?>/>
                                    <label
                                        for="exsercou3"><?php echo $BIZBOOK['SERVICE-EXPERT-LOW-HIGH-LABEL']; ?></label>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <!--- END --->
                </div>
                <?php
                $expertssql = "SELECT T1.* $service_start_search_query $service_rating_start_query FROM " . TBL . "experts AS T1 $service_end_search_query $service_rating_end_query WHERE T1.expert_status= 'Active' $category_search_query $service_availability_search_query $expert_location_search_query $service_verified_search_query $service_rating_search_query $service_sort_by_search_query $service_sort_by_search_order_query";

                $expertrs = mysqli_query($conn, $expertssql);
                $total_experts = mysqli_num_rows($expertrs);

                ?>
                <div class="col-md-9">
                    <?php

                    if (mysqli_num_rows($expertrs) > 0) {
                        ?>
                        <div
                            class="job-ser-cnt"><?php echo $BIZBOOK['JOB-SHOWING']; ?> <?php echo AddingZero_BeforeNumber($total_experts); ?> <?php echo $BIZBOOK['SERVICE-EXPERTS']; ?></div>
                        <div class="job-list">
                            <ul>
                                <?php
                                while ($expertrow = mysqli_fetch_array($expertrs)) {

                                    $expert_id = $expertrow['expert_id'];
                                    $expert_user_id = $expertrow['user_id'];

                                    $usersqlrow = getUser($expert_user_id); // To Fetch particular User Data

                                    // Service Expert Rating. for Rating of Star Starts

                                    foreach (getExpertReview($expert_id) as $star_rating_row) {
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

                                   // Service Expert Rating. for Rating of Star Ends

                                    ?>
                                    <li>
                                        <div class="job-box">
                                            <div class="job-box-img">
                                                <img
                                                    src="<?php echo $slash; ?>service-experts/images/services/<?php echo $expertrow['profile_image']; ?>"
                                                    alt="">
                                            </div>
                                            <?php if($expertrow['expert_availability_status'] == 0){ ?>
                                            <div class="ser-exp-ave" title="User currently available">
                                                <span class="ser-avail-yes"></span>
                                            </div>
                                            <?php } ?>
                                            <div class="job-days">
                                                <?php if ($usersqlrow['user_plan'] == 4 || $usersqlrow['user_plan'] == 3) { ?>
                                                    <span class="ver"><i class="material-icons" title="Verified expert">verified_user</i></span>
                                                    <?php
                                                }
                                                ?>
                                                <?php
                                                if ($star_rate_two != 0) {
                                                    ?>
                                                    <span class="rat"
                                                          title="User rating 5 out of"><?php echo $star_rate_two; ?></span>
                                                    <?php
                                                }
                                                ?>
                                            </div>
                                            <div class="job-box-con">
                                                <h4><?php echo $expertrow['profile_name']; ?></h4>
                                                <span><?php echo getIdCountFinishedExpertEnquiries($expert_id); ?> <?php echo $BIZBOOK['SERVICE-EXPERT-SERVICES-DONE']; ?></span>
                                                <span><?php echo $expertrow['years_of_experience']; ?> <?php echo $BIZBOOK['SERVICE-EXPERT-YEARS-TEXT']; ?><?php echo $BIZBOOK['SERVICE-EXPERT-EXP']; ?></span>
                                            </div>
                                            <div class="job-box-apl">
                                        <span class="job-box-cta" data-toggle="modal"
                                              data-target="#expfrm<?php echo $expert_id; ?>"><?php echo $BIZBOOK['SERVICE-EXPERT-CONTACT-ME']; ?></span>
                                                <a href="<?php echo $SERVICE_EXPERT_URL . urlModifier($expertrow['expert_slug']); ?>"
                                                   class="serexp-cta-more"><?php echo $BIZBOOK['SERVICE-EXPERT-MORE-DETAILS']; ?></a>
                                            </div>
                                        </div>
                                    </li>
                                    <!--  Quick View box starts  -->
                                    <!-- START -->
                                    <section>
                                        <div class="pop-ups pop-quo">
                                            <!-- The Modal -->
                                            <div class="modal fade" id="expfrm<?php echo $expert_id; ?>">
                                                <div class="modal-dialog">
                                                    <div class="modal-content">
                                                        <div class="log-bor">&nbsp;</div>
                                                        <span class="udb-inst">Contact</span>
                                                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                                                        <!-- Modal Header -->
                                                        <div class="quote-pop">
                                                            <div id="expert_pop_enq_success" class="log" style="display: none;"><p><?php echo $BIZBOOK['SERVICE_EXPERT_ENQUIRY_SUCCESSFUL_MESSAGE']; ?></p>
                                                            </div>
                                                            <div id="expert_pop_enq_same" class="log" style="display: none;"><p><?php echo $BIZBOOK['SERVICE_EXPERT_ENQUIRY_OWN_JOB_MESSAGE']; ?></p>
                                                            </div>
                                                            <div id="expert_pop_enq_fail" class="log" style="display: none;"><p><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></p>
                                                            </div>
                                                            <div class="ser-exp-wel"><?php echo $BIZBOOK['SERVICE-EXPERT-HEY-LABEL']; ?> <b><?php echo $expertrow['profile_name']; ?></b></div>
                                                            <form method="post" name="expert_all_enquiry_form"
                                                                  id="expert_all_enquiry_form">
                                                                <input type="hidden" class="form-control"
                                                                       name="expert_id"
                                                                       value="<?php echo $expert_id; ?>"
                                                                       placeholder=""
                                                                       required>
                                                                <input type="hidden" class="form-control"
                                                                       name="expert_user_id"
                                                                       value="<?php echo $expert_user_id; ?>" placeholder=""
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
                                                                    <input type="text" name="enquiry_name"
                                                                           value="<?php echo $user_details_row['first_name'] ?>"
                                                                           required="required" class="form-control"
                                                                           placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>">
                                                                </div>
                                                                <div class="form-group">
                                                                    <input type="email" class="form-control"
                                                                           placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>" required="required"
                                                                           value="<?php echo $user_details_row['email_id'] ?>"
                                                                           name="enquiry_email"
                                                                           pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                                                           title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>">
                                                                </div>
                                                                <div class="form-group">
                                                                    <input type="text" class="form-control"
                                                                           value="<?php echo $user_details_row['mobile_number'] ?>"
                                                                           name="enquiry_mobile"
                                                                           placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>"
                                                                           pattern="[7-9]{1}[0-9]{9}"
                                                                           title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>"
                                                                           required>
                                                                </div>
                                                                <div class="form-group">
                                                                    <select class="chosen-select" required="required" name="enquiry_category">
                                                                        <option value=""><?php echo $BIZBOOK['SELECT_CATEGORY']; ?></option>
                                                                        <?php
                                                                        foreach (getAllActiveExpertCategoriesPos() as $lead_categories_row) {
                                                                            ?>
                                                                            <option value="<?php echo $lead_categories_row['category_id']; ?>"><?php echo $lead_categories_row['category_name']; ?></option>
                                                                            <?php
                                                                        }
                                                                        ?>
                                                                    </select>
                                                                </div>
                                                                <div class="form-group col-md-6 serex-date">
                                                                    <input type="text" class="form-control" name="enquiry_date"
                                                                           placeholder="<?php echo $BIZBOOK['SERVICE-EXPERT-PREFERRED-DATE']; ?>" id="newdate">
                                                                </div>
                                                                <div class="form-group col-md-6 serex-time">
                                                                    <select class="chosen-select" name="enquiry_time">
                                                                        <option value=""><?php echo $BIZBOOK['SERVICE-EXPERT-PREFERRED-TIME']; ?></option>
                                                                        <?php
                                                                        $start_time = $expertrow['available_time_start'];
                                                                        $new_start_time1 = strtotime('-60mins', strtotime($start_time));
                                                                        $new_start_time = date('g:i A', $new_start_time1); // format the next time

                                                                        $end_time = $expertrow['available_time_end'];
                                                                        $new_end_time1 = strtotime('+60mins', strtotime($end_time));
                                                                        $new_end_time = date('g:i A', $new_end_time1); // format the next time

                                                                         $workingHours = (((strtotime($new_end_time) - strtotime($start_time)) / 3600)-1);

                                                                        $time = $new_start_time; // start
                                                                        for ($i = 0; $i <= $workingHours; $i++) {
                                                                            $prev = date('g:i a', strtotime($time)); // format the start time
                                                                            $next = strtotime('+60mins', strtotime($time)); // add 60 mins
                                                                            $time = date('g:i A', $next); // format the next time
                                                                            ?>
                                                                            <option value="<?php echo $time; ?>"><?php echo $time; ?></option>
                                                                            <?php
                                                                        }
                                                                        ?>
                                                                    </select>
                                                                </div>
                                                                <div class="form-group">
                                                                    <textarea class="form-control" name="enquiry_location" id="enquiry_location" placeholder="<?php echo $BIZBOOK['LEAD-LOCATION-PLACEHOLDER']; ?>"></textarea>
                                                                </div>
                                                                <div class="form-group">
                                                                    <textarea class="form-control" name="enquiry_message" id="enquiry_message" placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                                                                </div>
                                                                <input type="hidden" name="" id="source">
                                                                <button <?php if ($session_user_id == NULL || empty($session_user_id)) {
                                                                    ?> disabled="disabled" <?php } ?> type="submit" id="expert_all_enquiry_submit"
                                                                                                      name="expert_all_enquiry_submit"
                                                                                                      class="btn btn-primary"><?php if ($session_user_id == NULL || empty($session_user_id)) {
                                                                        ?> <?php echo $BIZBOOK['LOG_IN_TO_SUBMIT']; ?> <?php } else { ?><?php echo $BIZBOOK['SUBMIT']; ?> <?php } ?>
                                                                </button>
                                                            </form>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </section>
                                    <!-- END -->
                                    <!--  Quick View box ends  -->
                                    <?php
                                }
                                ?>
                            </ul>
                        </div>
                        <?php
                    } else {
                        ?>
                        <span style="    font-size: 21px;
    color: #bfbfbf;
    letter-spacing: 1px;
    /* background: #525252; */
    text-shadow: 0px 0px 2px #fff;
    text-transform: uppercase;
    text-align: center!important;
    margin-top: 5%;"><?php echo $BIZBOOK['SERVICE_EXPERTS_NO_SERVICE_EXPERTS_MESSAGE']; ?></span>
                        <?php
                    }
                    ?>
                </div>
            </div>
        </div>
    </div>
</section>

<!--  Quick View box starts  -->
<!-- START -->
<section>
    <div class="pop-ups pop-quo">
        <!-- The Modal -->
        <div class="modal fade" id="allexpfrm">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="log-bor">&nbsp;</div>
                    <span class="udb-inst">Contact</span>
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                    <!-- Modal Header -->
                    <div class="quote-pop">
                        <div id="expert_pop_enq_common_success" class="log" style="display: none;"><p><?php echo $BIZBOOK['SERVICE_EXPERT_ENQUIRY_SUCCESSFUL_MESSAGE']; ?></p>
                        </div>
                        <div id="expert_pop_enq_common_same" class="log" style="display: none;"><p><?php echo $BIZBOOK['SERVICE_EXPERT_ENQUIRY_OWN_JOB_MESSAGE']; ?></p>
                        </div>
                        <div id="expert_pop_enq_common_fail" class="log" style="display: none;"><p><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></p>
                        </div>
                        <div class="ser-exp-wel"><?php echo $BIZBOOK['SERVICE-EXPERT-ENQUIRY-DEFAULT-P-MESSAGE']; ?></div>
                        <form method="post" name="expert_all_enquiry_common_form"
                              id="expert_all_enquiry_common_form">
                            <input type="hidden" class="form-control"
                                   name="general_id"
                                   value="<?php echo 1; ?>" placeholder=""
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
                                <input type="text" name="enquiry_name"
                                       value="<?php echo $user_details_row['first_name'] ?>"
                                       required="required" class="form-control"
                                       placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>">
                            </div>
                            <div class="form-group">
                                <input type="email" class="form-control"
                                       placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>" required="required"
                                       value="<?php echo $user_details_row['email_id'] ?>"
                                       name="enquiry_email"
                                       pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>">
                            </div>
                            <div class="form-group">
                                <input type="text" class="form-control"
                                       value="<?php echo $user_details_row['mobile_number'] ?>"
                                       name="enquiry_mobile"
                                       placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>"
                                       pattern="[7-9]{1}[0-9]{9}"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>"
                                       required>
                            </div>
                            <div class="form-group">
                                <select class="chosen-select" required="required" name="enquiry_category">
                                    <option value=""><?php echo $BIZBOOK['SELECT_CATEGORY']; ?></option>
                                    <?php
                                    foreach (getAllActiveExpertCategoriesPos() as $lead_categories_row) {
                                        ?>
                                        <option value="<?php echo $lead_categories_row['category_id']; ?>"><?php echo $lead_categories_row['category_name']; ?></option>
                                        <?php
                                    }
                                    ?>
                                </select>
                            </div>
                            <div class="form-group col-md-6 serex-date">
                                <input type="text" class="form-control" name="enquiry_date"
                                       placeholder="<?php echo $BIZBOOK['SERVICE-EXPERT-PREFERRED-DATE']; ?>" id="newdate">
                            </div>
                            <div class="form-group col-md-6 serex-time">
                                <select class="chosen-select" name="enquiry_time">
                                    <option value=""><?php echo $BIZBOOK['SERVICE-EXPERT-PREFERRED-TIME']; ?></option>
                                    <?php
                                    $start_time = "6:00 AM";
                                    $new_start_time1 = strtotime('-60mins', strtotime($start_time));
                                    $new_start_time = date('g:i A', $new_start_time1); // format the next time

                                    $end_time = "10:00 PM";
                                    $new_end_time1 = strtotime('+60mins', strtotime($end_time));
                                    $new_end_time = date('g:i A', $new_end_time1); // format the next time

                                    $workingHours = (((strtotime($new_end_time) - strtotime($start_time)) / 3600)-1);

                                    $time = $new_start_time; // start
                                    for ($i = 0; $i <= $workingHours; $i++) {
                                        $prev = date('g:i a', strtotime($time)); // format the start time
                                        $next = strtotime('+60mins', strtotime($time)); // add 60 mins
                                        $time = date('g:i A', $next); // format the next time
                                        ?>
                                        <option value="<?php echo $time; ?>"><?php echo $time; ?></option>
                                        <?php
                                    }
                                    ?>
                                </select>
                            </div>
                            <div class="form-group">
                                <textarea class="form-control" name="enquiry_location" id="enquiry_location" placeholder="<?php echo $BIZBOOK['LEAD-LOCATION-PLACEHOLDER']; ?>"></textarea>
                            </div>
                            <div class="form-group">
                                <textarea class="form-control" name="enquiry_message" id="enquiry_message" placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                            </div>
                            <input type="hidden" name="" id="source">
                            <button <?php if ($session_user_id == NULL || empty($session_user_id)) {
                                ?> disabled="disabled" <?php } ?> type="submit" id="expert_all_enquiry_common_submit"
                                                                  name="expert_all_enquiry_common_submit"
                                                                  class="btn btn-primary"><?php if ($session_user_id == NULL || empty($session_user_id)) {
                                    ?> <?php echo $BIZBOOK['LOG_IN_TO_SUBMIT']; ?> <?php } else { ?><?php echo $BIZBOOK['SUBMIT']; ?> <?php } ?>
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->
<!--  Quick View box ends  -->

<!-- END -->
<?php
include "../footer.php";
?>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script src="<?php echo $slash; ?>js/select-opt.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>service-experts/js/expert_filter.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>
</body>
</html>