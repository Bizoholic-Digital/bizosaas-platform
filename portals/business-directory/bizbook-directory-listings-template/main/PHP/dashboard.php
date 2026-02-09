<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

include "dashboard_left_pane.php";

$session_user_id = $user_details_row['user_id'];
?>
<!--CENTER SECTION-->
<div class="ud-main">
   <div class="ud-main-inn">
<div class="ud-cen">
    <?php include('config/user_activation_checker.php'); ?>
    <div class="cd-cen-intr">
        <div class="cd-cen-intr-inn">
            <h2><?php echo $BIZBOOK['USER_DASHBOARD_WELCOME_TITLE']; ?>
                <b><?php echo $user_details_row['first_name']; ?></b></h2>
            <p><?php echo $BIZBOOK['USER_DASHBOARD_WELCOME_P_TAG']; ?></p>
        </div>
    </div>
    <div class="ud-cen-s1">
        <ul>
            <?php
            if ($user_details_row['user_type'] != "Service provider") { ?>
                <li>
                    <div>
                        <b><?php echo AddingZero_BeforeNumber(getCountSentReview($session_user_id)); ?></b>
                        <h4><?php echo $BIZBOOK['ALL_REVIEWS']; ?></h4>
                        <p><?php echo $BIZBOOK['TOTAL_NO_OF_REVIEWS']; ?></p>
                        <a href="db-notifications">&nbsp;</a>
                    </div>
                </li>
                <li>
                    <div>
                        <b><?php echo AddingZero_BeforeNumber(getCountLikedListing($session_user_id)); ?></b>
                        <h4><?php echo $BIZBOOK['LIKED_LISTINGS']; ?></h4>
                        <p><?php echo $BIZBOOK['NO_OF_LIKED_LISTINGS']; ?></p>
                        <a href="db-like-listings">&nbsp;</a>
                    </div>
                </li>
            <?php } else { ?>
                <li>
                    <div>
                        <b><?php echo AddingZero_BeforeNumber(getCountUserListing($session_user_id)); ?></b>
                        <h4><?php echo $BIZBOOK['ALL_LISTING']; ?></h4>
                        <p><?php echo $BIZBOOK['TOTAL_NO_LISTINGS']; ?></p>
                        <a href="db-all-listing">&nbsp;</a>
                    </div>
                </li>
                <li>
                    <div>
                        <b><?php echo AddingZero_BeforeNumber(getCountUserEnquiries($session_user_id)); ?></b>
                        <h4><?php echo $BIZBOOK['ENQUIRIES']; ?></h4>
                        <p><?php echo $BIZBOOK['TOTAL_NO_ENQUIRY']; ?></p>
                        <a href="db-enquiry">&nbsp;</a>
                    </div>
                </li>
            <?php } ?>
            <li>
                <div>
                    <b><?php echo AddingZero_BeforeNumber(getCountUserFollowing($session_user_id)); ?></b>
                    <h4><?php echo $BIZBOOK['FOLLOWINGS']; ?></h4>
                    <p><?php echo $BIZBOOK['TOTAL_NO_FOLLOWINGS']; ?></p>
                    <a href="db-followings">&nbsp;</a>
                </div>
            </li>
        </ul>
    </div>
        <!-- START -->
        <div class="ud-cen-s3 ud-cen-s4">
            <h2><?php echo $BIZBOOK['PROFILE_PAGE']; ?></h2>
            <a href="db-my-profile-edit" class="db-tit-btn"><?php echo $BIZBOOK['EDIT_MY_PROFILE']; ?></a>
            <div class="ud-payment ud-pro-link">
                <div class="pay-lhs">
                    <div class="lis-pro-badg">
                        <div>
                            <img
                                src="images/user/<?php if (($user_details_row['profile_image'] == NULL) || empty($user_details_row['profile_image'])) {
                                    echo $footer_row['user_default_image'];
                                } else {
                                    echo $user_details_row['profile_image'];
                                } ?>" alt="">
                            <h4><?php echo $user_details_row['first_name']; ?></h4>
                            <p><?php echo $BIZBOOK['MEMBER_SINCE']; ?><?php echo dateFormatconverter($user_details_row['user_cdt']) ?></p>
                        </div>
                        <a href="<?php echo $PROFILE_URL . urlModifier($user_details_row['user_slug']); ?>"
                           class="fclick" target="_blank">&nbsp;</a>
                    </div>
                </div>
                <div class="pay-rhs">
                    <ul>
                        <li><b><?php echo $BIZBOOK['NAME']; ?> : </b> <?php echo $user_details_row['first_name']; ?>
                        </li>
                        <li><b><?php echo $BIZBOOK['FOLLOWERS']; ?>
                                : </b> <span><?php $user = getUser($session_user_id);
                                if ($user['user_followers'] == NULL) {
                                    echo "00";
                                } else {
                                    echo AddingZero_BeforeNumber(count(explode(",", $user['user_followers'])));
                                } ?></span></li>
                        <li><b><?php echo $BIZBOOK['CITY']; ?>
                                : </b> <?php if ($user_details_row['user_city'] == NULL) {
                                echo "N/A";
                            } else {
                                echo $user_details_row['user_city'];
                            } ?></li>
                        <li><b><?php echo $BIZBOOK['EMAIL']; ?> : </b> <?php echo $user_details_row['email_id']; ?></li>
                        <li class="pro"><input type="text"
                                               value="<?php echo $PROFILE_URL . urlModifier($user_details_row['user_slug']); ?>"
                                               readonly></li>
                        <li class="pre"><a target="_blank"
                                           href="<?php echo $PROFILE_URL . urlModifier($user_details_row['user_slug']); ?>"><?php echo $BIZBOOK['VIEW_MY_PROFILE_PAGE']; ?></a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <!-- END -->
    <?php
    if ($user_plan_type['plan_type_id'] == 4) {
        $user_id = $_SESSION['user_id'];
        ?>
        <!--            // Company Profile section starts -->
        <?php
        $company_row = getUserCompanyUser($user_id);
        ?>
        <!-- START -->
        <div class="ud-cen-s3 ud-cen-s4">
            <h2><?php echo $BIZBOOK['PROFI_BUSINES_TIT']; ?></h2>
            <a href="company-profile-edit" class="db-tit-btn"><?php echo $BIZBOOK['EDIT_BUSINES_PROFILE']; ?></a>
            <div class="ud-payment ud-pro-link bus-pg">
                <div class="pay-lhs">
                    <div class="lis-pro-badg">
                        <div>
                            <img
                                src="images/user/<?php if (($company_row['company_profile_photo'] == NULL) || empty($company_row['company_profile_photo'])) {
                                    echo $footer_row['user_default_image'];
                                } else {
                                    echo $company_row['company_profile_photo'];
                                } ?>" alt="">
                            <h4><?php if ($company_row['company_name'] != NULL) {
                                    echo $company_row['company_name'];
                                } else {
                                    echo 'N/A';
                                } ?></h4>
                            <p><?php echo $BIZBOOK['MEMBER_SINCE']; ?><?php echo dateFormatconverter($user_details_row['user_cdt']) ?></p>
                        </div>
                        <a href="<?php if ($company_row['company_name'] != NULL) {
                            echo $COMPANY_URL . urlModifier($company_row['company_slug']);
                        } else {
                            echo "#!";
                        } ?>" class="fclick" target="_blank">&nbsp;</a>
                    </div>
                </div>
                <div class="pay-rhs">
                    <ul>
                        <li><b><?php echo $BIZBOOK['NAME']; ?> : </b> <?php if ($company_row['company_name'] != NULL) {
                                echo $company_row['company_name'];
                            } else {
                                echo 'N/A';
                            } ?>
                        </li>
                        <li><b><?php echo $BIZBOOK['PAGE_VIEWS']; ?> : </b>
                            <span><?php echo AddingZero_BeforeNumber(business_pageview_count($company_row['user_id'])); ?></span>
                        </li>
                        <li class="pro"><input type="text"
                                               value="<?php echo $COMPANY_URL . urlModifier($company_row['company_slug']); ?>"
                                               readonly></li>
                        <li class="pre"><a target="_blank"
                                           href="<?php if ($company_row['company_name'] != NULL) {
                                               echo $COMPANY_URL . urlModifier($company_row['company_slug']);
                                           } else {
                                               echo "#!";
                                           } ?>"><?php echo $BIZBOOK['VIEW_BUSINESS_PAGE']; ?></a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <!-- END -->
        <!--            // Company Profile section starts-->

    <?php if ($footer_row['admin_expert_show'] == 1 && $user_details_row['setting_expert_show'] == 1) { ?>

            <!--            // Service Expert Profile section starts -->
            <?php
            if (getCountUserExperts($user_id) > 0) {

                $service_expert_row = getExpertUser($user_id);

                $expert_id = $service_expert_row['expert_id'];

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
                <!-- START -->
                <div class="ud-cen-s3 ud-cen-s4">
                    <h2><?php echo $BIZBOOK['PROFI_SERVICE_EXPERT_TIT']; ?></h2>
                    <a href="service-experts/create-service-expert-profile"
                       class="db-tit-btn"><?php echo $BIZBOOK['EDIT_SERVICE_EXPERT_PROFILE']; ?></a>
                    <div class="ud-payment ud-pro-link bus-pg">
                        <div class="pay-lhs">
                            <div class="lis-pro-badg">
                                <div>
                                    <img
                                        src="<?php echo $slash; ?>service-experts/images/services/<?php echo $service_expert_row['profile_image']; ?>"
                                        alt="">
                                    <h4><?php echo $service_expert_row['profile_name']; ?></h4>
                                    <p><?php echo $BIZBOOK['MEMBER_SINCE']; ?><?php echo dateFormatconverter($user_details_row['user_cdt']) ?></p>
                                    <span class="db-list-rat"><?php echo $star_rate_two; ?></span>
                                </div>
                                <a href="<?php echo $SERVICE_EXPERT_URL . urlModifier($service_expert_row['expert_slug']); ?>"
                                   class="fclick" target="_blank">&nbsp;</a>
                            </div>
                        </div>
                        <div class="pay-rhs">
                            <ul>
                                <li><b><?php echo $BIZBOOK['NAME']; ?>
                                        : </b> <?php echo $service_expert_row['profile_name']; ?>
                                </li>
                                <li><b><?php echo $BIZBOOK['PAGE_VIEWS']; ?> : </b>
                                    <span><?php echo AddingZero_BeforeNumber(expert_profile_pageview_count($service_expert_row['expert_id'])); ?></span>
                                </li>
                                <li class="pro"><input type="text"
                                                       value="<?php echo $SERVICE_EXPERT_URL . urlModifier($service_expert_row['expert_slug']); ?>"
                                                       readonly></li>
                                <li class="pre"><a target="_blank"
                                                   href="<?php echo $SERVICE_EXPERT_URL . urlModifier($service_expert_row['expert_slug']); ?>"><?php echo $BIZBOOK['VIEW_SERVICE_EXPERT_PROFILE_PAGE']; ?></a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
                <!-- END -->
                <!--            // Service Expert Profile section starts-->
                <?php
            }
        }
    }
    ?>
    <?php if ($footer_row['admin_job_show'] == 1 && $user_details_row['setting_job_show'] == 1) { ?>
    <?php

    // If User type was job seeker means we are showing option to add job seeker profile starts here

        $user_id = $_SESSION['user_id'];
        $job_profile_row = getUserJobProfile($user_id);
        ?>
        <!-- START -->
        <div class="ud-cen-s3 ud-cen-s4">
            <h2><?php echo $BIZBOOK['PROFI_JOB_SEEKER_TIT']; ?></h2>
            <a href="jobs/create-job-seeker-profile"
               class="db-tit-btn"><?php echo $BIZBOOK['EDIT_JOB_SEEKER_PROFILE']; ?></a>
            <div class="ud-payment ud-pro-link bus-pg">
                <div class="pay-lhs">
                    <div class="lis-pro-badg">
                        <div>
                            <img
                                src="<?php if (($job_profile_row['job_profile_image'] == NULL) || empty($job_profile_row['job_profile_image'])) {
                                    echo $slash.'images/user/'.$footer_row['user_default_image'];
                                } else {
                                    echo $slash.'jobs/images/jobs/'.$job_profile_row['job_profile_image'];
                                } ?>" alt="">
                            <h4><?php if ($job_profile_row['profile_name'] != NULL) {
                                    echo $job_profile_row['profile_name'];
                                } else {
                                    echo 'N/A';
                                } ?></h4>
                            <p><?php echo $BIZBOOK['MEMBER_SINCE']; ?><?php echo dateFormatconverter($user_details_row['user_cdt']) ?></p>
                        </div>
                        <a href="<?php if ($job_profile_row['profile_name'] != NULL) {
                            echo $JOB_PROFILE_URL . urlModifier($job_profile_row['job_profile_slug']);
                        } else {
                            echo "#!";
                        } ?>" class="fclick" target="_blank">&nbsp;</a>
                    </div>
                </div>
                <div class="pay-rhs">
                    <ul>
                        <li><b><?php echo $BIZBOOK['NAME']; ?>
                                : </b> <?php if ($job_profile_row['profile_name'] != NULL) {
                                echo $job_profile_row['profile_name'];
                            } else {
                                echo 'N/A';
                            } ?>
                        </li>
                        <li><b><?php echo $BIZBOOK['PAGE_VIEWS']; ?> : </b>
                            <span><?php if($job_profile_row['user_id'] != 0){ echo AddingZero_BeforeNumber(job_profile_pageview_count($job_profile_row['user_id'])); } else { echo "00"; } ?></span>
                        </li>
                        <li class="pro"><input type="text"
                                               value="<?php echo $JOB_PROFILE_URL . urlModifier($job_profile_row['job_profile_slug']); ?>"
                                               readonly></li>
                        <li class="pre"><a target="_blank"
                                           href="<?php if ($job_profile_row['profile_name'] != NULL) {
                                               echo $JOB_PROFILE_URL . urlModifier($job_profile_row['job_profile_slug']);
                                           } else {
                                               echo "#!";
                                           } ?>"><?php echo $BIZBOOK['VIEW_JOB_PROFILE_PAGE']; ?></a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <!-- END -->
    <?php } ?>

<!--        // If User type was job seeker means we are showing option to add job seeker profile ends here-->

    <?php
    if ($user_details_row['user_type'] == "Service Provider") { ?>
        <div class="ud-cen-s2">
            <h2><?php echo $BIZBOOK['LISTING_DETAILS']; ?></h2>
            <a href="add-listing-start" class="db-tit-btn"><?php echo $BIZBOOK['ADD_NEW_LISTING']; ?></a>
            <table class="responsive-table bordered">
                <thead>
                <tr>
                    <th><?php echo $BIZBOOK['S_NO']; ?></th>
                    <th><?php echo $BIZBOOK['LISTING_NAME']; ?></th>
                    <th><?php echo $BIZBOOK['RATING']; ?></th>
                    <th><?php echo $BIZBOOK['VIEWS']; ?></th>
                    <th><?php echo $BIZBOOK['STATUS']; ?></th>
                    <th><?php echo $BIZBOOK['EDIT']; ?></th>
                    <th><?php echo $BIZBOOK['DELETE']; ?></th>
                    <th><?php echo $BIZBOOK['PREVIEW']; ?></th>
                </tr>
                </thead>
                <tbody>

                <?php

                $si = 1;
                foreach (getAllListingUser($_SESSION['user_id']) as $listrow) {

                    $reviewlisting_id = $listrow['listing_id'];

                    //  List Rating. for Rating of Star starts

                    foreach (getListingReview($reviewlisting_id) as $Star_rateRow) {

                        if ($Star_rateRow["rate_cnt"] > 0) {
                            $Star_rate_times = $Star_rateRow["rate_cnt"];
                            $Star_sum_rates = $Star_rateRow["total_rate"];
                            $star_rate_one = $Star_sum_rates / $Star_rate_times;
                            $star_rate = number_format($star_rate_one, 1);

                        } else {
                            $rate_times = 0;
                            $rate_value = 0;
                            $star_rate = 0;
                        }
                    }
                    //  List Rating. for Rating of Star Ends

                    ?>

                    <tr>
                        <td><?php echo $si; ?></td>
                        <td><img
                                src="<?php if ($listrow['profile_image'] != NULL || !empty($listrow['profile_image'])) {
                                    echo "images/listings/" . $listrow['profile_image'];
                                } else {
                                    echo "images/listings/hot4.jpg";
                                } ?>"><?php echo $listrow['listing_name']; ?>
                            <span><?php echo dateFormatconverter($listrow['listing_cdt']); ?></span></td>
                        <td><span class="db-list-rat"><?php echo $star_rate; ?></span></td>
                        <td><span
                                class="db-list-rat"><?php echo listing_pageview_count($listrow['listing_id']); ?></span>
                        </td>
                        <td><span class="db-list-ststus"><?php echo $listrow['listing_status']; ?></span></td>
                        <td><a href="edit-listing-step-1?row=<?php echo $listrow['listing_code']; ?>"
                               class="db-list-edit"><?php echo $BIZBOOK['EDIT']; ?></a></td>
                        <td><a href="delete-listing?row=<?php echo $listrow['listing_code']; ?>"
                               class="db-list-edit"><?php echo $BIZBOOK['DELETE']; ?></a></td>
                        <td><a href="<?php echo $LISTING_URL . urlModifier($listrow['listing_slug']); ?>"
                               class="db-list-edit" target="_blank"><?php echo $BIZBOOK['PREVIEW']; ?></a></td>
                    </tr>
                    <?php
                    $si++;
                }
                ?>
                </tbody>
            </table>
        </div>
        <div class="ud-cen-s3">
            <h2><?php echo $BIZBOOK['EVENTS']; ?></h2>
            <a href="create-new-event" class="db-tit-btn"><?php echo $BIZBOOK['ADD_NEW_EVENT']; ?></a>
            <ul>
                <?php foreach (getAllUserEvents($_SESSION['user_id']) as $eventrow) { ?>
                    <li>
                        <div class="db-eve">
                            <a href="<?php echo $EVENT_URL . urlModifier($eventrow['event_slug']); ?>">
                                <img src="images/events/<?php echo $eventrow['event_image']; ?>" alt="">
                                <h5><?php echo $eventrow['event_name']; ?></h5>
                                <span><?php echo $BIZBOOK['CREATED']; ?>
                                    : <?php echo dateFormatconverter($eventrow['event_cdt']); ?></span>
                            </a>
                        </div>
                    </li>
                <?php } ?>
            </ul>
        </div>
        <div class="ud-cen-s3 ud-cen-s4">
            <h2><?php echo $BIZBOOK['BLOG_POSTS']; ?></h2>
            <a href="create-new-blog-post" class="db-tit-btn"><?php echo $BIZBOOK['ADD_NEW_POST']; ?></a>
            <ul>
                <?php foreach (getAllUserBlogs($_SESSION['user_id']) as $blogrow) { ?>
                    <li>
                        <div class="db-eve">
                            <a href="<?php echo $BLOG_URL . urlModifier($blogrow['blog_slug']); ?>">
                                <img src="images/blogs/<?php echo $blogrow['blog_image']; ?>" alt="">
                                <h5><?php echo $blogrow['blog_name']; ?></h5>
                                <span><?php echo $BIZBOOK['CREATED']; ?>
                                    : <?php echo dateFormatconverter($blogrow['blog_cdt']); ?></span>
                            </a>
                        </div>
                    </li>
                <?php } ?>
            </ul>
        </div>
    <?php } ?>

</div>
<?php
include "dashboard_right_pane.php";
?>
<style>
    .ud-cen .log-bor {
        display: none;
    }
</style>