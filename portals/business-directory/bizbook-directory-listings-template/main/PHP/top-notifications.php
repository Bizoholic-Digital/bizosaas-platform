<!--TOP NOTIFICATIONS-->

<div class="top-noti">
    <?php
    if ($user_details_row['user_type'] == 'Service provider') {
        $user_type_id = 101;
    } else {
        $user_type_id = 102;
    }

    if ($user_plan_type['plan_type_id'] != NULL || !empty($user_plan_type['plan_type_id'])) {
        $plan_type_id = $user_plan_type['plan_type_id'];
    } else {
        $plan_type_id = 0;
    }

    $user_last_clear_notification = $user_details_row['user_clear_notification_cdt'];

    $all_listing_notification_count = getCountAllUserListingDateEnquiries($session_user_id, $user_last_clear_notification);

    $all_event_notification_count = getCountAllUserEventDateEnquiries($session_user_id, $user_last_clear_notification);

    $all_blog_notification_count = getCountAllUserBlogDateEnquiries($session_user_id, $user_last_clear_notification);

    $all_product_notification_count = getCountAllUserProductDateEnquiries($session_user_id, $user_last_clear_notification);

    $all_expert_notification_count = getCountAllUserExpertDateExpertEnquiries($session_user_id, $user_last_clear_notification);

    $all_job_applied_notification_count = getCountUserAppliedDateJobProfile($session_user_id, $user_last_clear_notification);

    $all_reviews_notification_count = getCountAllUserListingDateReviews($session_user_id, $user_last_clear_notification);

    $all_listing_likes_notification_count = getCpuntAllUserLikedListingDate($session_user_id, $user_last_clear_notification);

    $all_user_notification_count = getCountAllUserNewNotification($user_type_id, $plan_type_id, $user_last_clear_notification);

    $total_notification_count = $all_listing_notification_count + $all_event_notification_count + $all_blog_notification_count
                              + $all_product_notification_count + $all_expert_notification_count + $all_job_applied_notification_count
                              + $all_reviews_notification_count + $all_listing_likes_notification_count + $all_user_notification_count;

    ?>
    <span class="material-icons db-menu-noti"><i
            id="noti-count"><?php echo AddingZero_BeforeNumber($total_notification_count); ?></i>notifications</span>
    <div class="db-noti top-noti-win">
        <span class="material-icons db-menu-clo">close</span>
        <h4><?php echo $BIZBOOK['pg_utype_sp7']; ?></h4>
        <ul id="all-notif-ul">

            <!--     Listings enquiry notification starts-->

            <?php

            if($all_listing_notification_count > 0) {

                foreach (getAllUserListingDateEnquiries($session_user_id, $user_last_clear_notification) as $listing_enquiry_notificationrow) {

                    $enquiry_sender_id = $listing_enquiry_notificationrow['enquiry_sender_id'];
                    $enquiry_listing_id = $listing_enquiry_notificationrow['listing_id'];
                    $enquiry_cdt = $listing_enquiry_notificationrow['enquiry_cdt'];

                    if ($enquiry_sender_id != NULL) {

                        $enquiry_user = getUser($enquiry_sender_id);            // To Fetch user data
                        $enquiry_listing = getIdListing($enquiry_listing_id);   //To Fetch listing data

                        ?>
                        <li>
                            <div>
                                <a target="_blank"
                                   href="<?php echo $PROFILE_URL . urlModifier($enquiry_user['user_slug']); ?>"><?php echo $enquiry_user['first_name']; ?></a><?php echo $BIZBOOK['DB-NOTIFICATION-SEND-LISTING-ENQUIRY']; ?>
                                <a href="<?php echo $LISTING_URL . urlModifier($enquiry_listing['listing_slug']); ?>"><?php echo $enquiry_listing['listing_name']; ?></a>.
                            </div>
                            <span><?php echo $BIZBOOK['DB-NOTIFICATION-ON']; ?><?php echo dateFormatconverter($enquiry_cdt); ?></span>
                        </li>
                        <?php
                    }
                }
            }
            ?>

            <!--      Listings enquiry notification ends-->

            <!--      Events enquiry notification starts-->

            <?php

            if($all_event_notification_count > 0) {

                foreach (getAllUserEventDateEnquiries($session_user_id, $user_last_clear_notification) as $event_enquiry_notificationrow) {

                    $enquiry_sender_id = $event_enquiry_notificationrow['enquiry_sender_id'];
                    $enquiry_event_id = $event_enquiry_notificationrow['event_id'];
                    $enquiry_cdt = $event_enquiry_notificationrow['enquiry_cdt'];

                    if ($enquiry_sender_id != NULL) {

                        $enquiry_user = getUser($enquiry_sender_id);            // To Fetch user data
                        $enquiry_event = getEvent($enquiry_event_id);   //To Fetch Event data

                        ?>
                        <li>
                            <div>
                                <a target="_blank"
                                   href="<?php echo $PROFILE_URL . urlModifier($enquiry_user['user_slug']); ?>"><?php echo $enquiry_user['first_name']; ?></a><?php echo $BIZBOOK['DB-NOTIFICATION-SEND-EVENT-ENQUIRY']; ?>
                                <a href="<?php echo $EVENT_URL . urlModifier($enquiry_event['event_slug']); ?>"><?php echo $enquiry_event['event_name']; ?></a>.
                            </div>
                            <span><?php echo $BIZBOOK['DB-NOTIFICATION-ON']; ?><?php echo dateFormatconverter($enquiry_cdt); ?></span>
                        </li>
                        <?php
                    }
                }
            }
            ?>

            <!--      Events enquiry notification ends-->

            <!--      Blogs enquiry notification starts-->

            <?php
            if($all_blog_notification_count > 0) {

                foreach (getAllUserBlogDateEnquiries($session_user_id, $user_last_clear_notification) as $blog_enquiry_notificationrow) {

                    $enquiry_sender_id = $blog_enquiry_notificationrow['enquiry_sender_id'];
                    $enquiry_blog_id = $blog_enquiry_notificationrow['blog_id'];
                    $enquiry_cdt = $blog_enquiry_notificationrow['enquiry_cdt'];

                    if ($enquiry_sender_id != NULL) {

                        $enquiry_user = getUser($enquiry_sender_id);            // To Fetch user data
                        $enquiry_blog = getBlog($enquiry_blog_id);   //To Fetch Event data

                        ?>
                        <li>
                            <div>
                                <a target="_blank"
                                   href="<?php echo $PROFILE_URL . urlModifier($enquiry_user['user_slug']); ?>"><?php echo $enquiry_user['first_name']; ?></a><?php echo $BIZBOOK['DB-NOTIFICATION-SEND-BLOG-ENQUIRY']; ?>
                                <a href="<?php echo $BLOG_URL . urlModifier($enquiry_blog['blog_slug']); ?>"><?php echo $enquiry_blog['blog_name']; ?></a>.
                            </div>
                            <span><?php echo $BIZBOOK['DB-NOTIFICATION-ON']; ?><?php echo dateFormatconverter($enquiry_cdt); ?></span>
                        </li>
                        <?php
                    }
                }
            }
            ?>

            <!--      Blogs enquiry notification ends-->

            <!--     Products enquiry notification starts-->

            <?php
            if($all_product_notification_count > 0) {

                foreach (getAllUserProductDateEnquiries($session_user_id, $user_last_clear_notification) as $product_enquiry_notificationrow) {

                    $enquiry_sender_id = $product_enquiry_notificationrow['enquiry_sender_id'];
                    $enquiry_product_id = $product_enquiry_notificationrow['product_id'];
                    $enquiry_cdt = $product_enquiry_notificationrow['enquiry_cdt'];

                    if ($enquiry_sender_id != NULL) {

                        $enquiry_user = getUser($enquiry_sender_id);            // To Fetch user data
                        $enquiry_listing = getIdProduct($enquiry_product_id);   //To Fetch listing data

                        ?>
                        <li>
                            <div>
                                <a target="_blank"
                                   href="<?php echo $PROFILE_URL . urlModifier($enquiry_user['user_slug']); ?>"><?php echo $enquiry_user['first_name']; ?></a><?php echo $BIZBOOK['DB-NOTIFICATION-SEND-PRODUCT-ENQUIRY']; ?>
                                <a href="<?php echo $PRODUCT_URL . urlModifier($enquiry_listing['product_slug']); ?>"><?php echo $enquiry_listing['product_name']; ?></a>.
                            </div>
                            <span><?php echo $BIZBOOK['DB-NOTIFICATION-ON']; ?><?php echo dateFormatconverter($enquiry_cdt); ?></span>
                        </li>
                        <?php
                    }
                }
            }
            ?>

            <!--      Products enquiry notification ends-->

            <!--     Service Experts enquiry notification starts-->

            <?php
            if($all_expert_notification_count > 0) {

                foreach (getAllUserExpertDateExpertEnquiries($session_user_id, $user_last_clear_notification) as $service_enquiry_notificationrow) {

                    $enquiry_sender_id = $service_enquiry_notificationrow['enquiry_sender_id'];
                    $enquiry_expert_id = $service_enquiry_notificationrow['expert_id'];
                    $enquiry_cdt = $service_enquiry_notificationrow['enquiry_cdt'];

                    if ($enquiry_sender_id != NULL) {

                        $enquiry_user = getUser($enquiry_sender_id);            // To Fetch user data
                        $enquiry_expert = getIdExpert($enquiry_expert_id);   //To Fetch listing data

                        ?>
                        <li>
                            <div>
                                <a target="_blank"
                                   href="<?php echo $PROFILE_URL . urlModifier($enquiry_user['user_slug']); ?>"><?php echo $enquiry_user['first_name']; ?></a><?php echo $BIZBOOK['DB-NOTIFICATION-SEND-EXPERT-ENQUIRY']; ?>
                                <a href="<?php echo $SERVICE_EXPERT_URL . urlModifier($enquiry_expert['expert_slug']); ?>"><?php echo $enquiry_expert['profile_name']; ?></a>.
                            </div>
                            <span><?php echo $BIZBOOK['DB-NOTIFICATION-ON']; ?><?php echo dateFormatconverter($enquiry_cdt); ?></span>
                        </li>
                        <?php
                    }
                }
            }
            ?>

            <!--      Service Experts enquiry notification ends-->

            <!--     Applied Job notification starts-->

            <?php
            if($all_job_applied_notification_count > 0) {

                foreach (getUserAppliedDateJobProfile($session_user_id, $user_last_clear_notification) as $job_applied_notificationrow) {

                    $job_profile_id = $job_applied_notificationrow['job_profile_id'];
                    $job_id = $job_applied_notificationrow['job_id'];
                    $job_applied_cdt = $job_applied_notificationrow['job_applied_cdt'];

                    if ($job_profile_id != NULL) {

                        $enquiry_user = getUser($job_profile_id);            // To Fetch user data
                        $job_notification = getIdJob($job_id);   //To Fetch listing data

                        ?>
                        <li>
                            <div>
                                <a target="_blank"
                                   href="<?php echo $PROFILE_URL . urlModifier($enquiry_user['user_slug']); ?>"><?php echo $enquiry_user['first_name']; ?></a><?php echo $BIZBOOK['DB-NOTIFICATION-SEND-JOB-APPLIED']; ?>
                                <a href="<?php echo $JOB_URL . urlModifier($job_notification['job_slug']); ?>"><?php echo $job_notification['job_title']; ?></a>.
                            </div>
                            <span><?php echo $BIZBOOK['DB-NOTIFICATION-ON']; ?><?php echo dateFormatconverter($job_applied_cdt); ?></span>
                        </li>
                        <?php
                    }
                }
            }
            ?>

            <!--      Applied Job notification ends-->

            <!--     Listings Review notification starts-->

            <?php
            if($all_reviews_notification_count > 0) {

                foreach (getAllUserLikedListingDate($session_user_id, $user_last_clear_notification) as $listing_likes_notificationrow) {

                    $listing_likes_user_id = $listing_likes_notificationrow['user_id'];
                    $enquiry_listing_id = $listing_likes_notificationrow['listing_id'];
                    $listing_likes_cdt = $listing_likes_notificationrow['listing_likes_cdt'];

                    if ($listing_likes_user_id != NULL) {

                        $enquiry_user = getUser($listing_likes_user_id);            // To Fetch user data
                        $enquiry_listing = getIdListing($enquiry_listing_id);   //To Fetch listing data

                        ?>
                        <li>
                            <div>
                                <a target="_blank"
                                   href="<?php echo $PROFILE_URL . urlModifier($enquiry_user['user_slug']); ?>"><?php echo $enquiry_user['first_name']; ?></a><?php echo $BIZBOOK['DB-NOTIFICATION-SEND-LISTING-LIKES']; ?>
                                <a href="<?php echo $LISTING_URL . urlModifier($enquiry_listing['listing_slug']); ?>"><?php echo $enquiry_listing['listing_name']; ?></a>.
                            </div>
                            <span><?php echo $BIZBOOK['DB-NOTIFICATION-ON']; ?><?php echo dateFormatconverter($listing_likes_cdt); ?></span>
                        </li>
                        <?php
                    }
                }
            }
            ?>

            <!--      Listings Review notification ends-->

            <!--     Listings Likes notification starts-->

            <?php
            if($all_listing_likes_notification_count > 0) {

                foreach (getAllUserLikedListingDate($session_user_id, $user_last_clear_notification) as $listing_review_notificationrow) {

                    $review_user_id = $listing_review_notificationrow['review_user_id'];
                    $enquiry_listing_id = $listing_review_notificationrow['listing_id'];
                    $review_cdt = $listing_review_notificationrow['review_cdt'];

                    if ($review_user_id != NULL) {

                        $enquiry_user = getUser($review_user_id);            // To Fetch user data
                        $enquiry_listing = getIdListing($enquiry_listing_id);   //To Fetch listing data

                        ?>
                        <li>
                            <div>
                                <a target="_blank"
                                   href="<?php echo $PROFILE_URL . urlModifier($enquiry_user['user_slug']); ?>"><?php echo $enquiry_user['first_name']; ?></a><?php echo $BIZBOOK['DB-NOTIFICATION-SEND-LISTING-REVIEW']; ?>
                                <a href="<?php echo $LISTING_URL . urlModifier($enquiry_listing['listing_slug']); ?>"><?php echo $enquiry_listing['listing_name']; ?></a>.
                            </div>
                            <span><?php echo $BIZBOOK['DB-NOTIFICATION-ON']; ?><?php echo dateFormatconverter($review_cdt); ?></span>
                        </li>
                        <?php
                    }
                }
            }
            ?>

            <!--      Listings Likes notification ends-->

            <?php
            if($all_user_notification_count > 0) {

                foreach (getAllUserNewNotification($user_type_id, $plan_type_id, $user_last_clear_notification) as $notificationrow) {
                    ?>
                    <li>
                        <div>
                            <a target="_blank"
                               href="<?php echo $notificationrow['notification_link']; ?>"><?php echo $notificationrow['notification_title']; ?></a>
                            <?php echo $notificationrow['notification_message']; ?>.
                        </div>
                        <span><?php echo $BIZBOOK['DB-NOTIFICATION-ON']; ?><?php echo dateFormatconverter($notificationrow['notification_cdt']) ?></span>
                    </li>
                    <?php
                }
            }
            ?>
        </ul>
        <?php
        if ($total_notification_count >= 1) {
            ?>
            <span id="noti-clr-noti" class="noti-clr-noti"><span class="material-icons">delete</span><?php echo $BIZBOOK['CLEAR-ALL-NOTIFICATIONS']; ?></span>
            <?php
        }
        ?>
        <span <?php if ($total_notification_count >= 1) {
            ?> style="display: none;" <?php } ?> id="no-noti-clr-noti"
                                                 class="no-noti-clr-noti"><?php echo $BIZBOOK['NO-NOTIFICATIONS-TO-SHOW']; ?></span>
    </div>
</div>

<!--END TOP NOTIFICATIONS-->