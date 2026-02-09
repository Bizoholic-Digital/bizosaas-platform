<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

include "dashboard_left_pane.php";


$session_user_id = $_SESSION['user_id'];

$user_notification = "select *

    from " . TBL . "listing_likes as s, " . TBL . "reviews as b, " . TBL . "enquiries as c

    where b.listing_user_id = s.listing_user_id and b.listing_user_id = c.listing_user_id AND  b.listing_user_id = '$session_user_id' AND c.listing_user_id = '$session_user_id' AND s.listing_user_id = '$session_user_id' ORDER BY c.enquiry_cdt,b.review_cdt DESC LIMIT 5 ";


$user_notification_query = mysqli_query($conn, $user_notification);

$user_notification_query_count = mysqli_num_rows($user_notification_query);


?>
    <!--CENTER SECTION-->
    <div class="ud-main">
   <div class="ud-main-inn ud-no-rhs">
    <div class="ud-cen">
        <div class="log-bor">&nbsp;</div>
        <span class="udb-inst"><?php echo $BIZBOOK['DB-NOTIFICATION-NOTIFICATIONS']; ?></span>
        <?php include('config/user_activation_checker.php'); ?>
        <div class="ud-cen-s2">
            <h2><?php echo $BIZBOOK['DB-NOTIFICATION-ALL-NOTIFICATIONS']; ?></h2>
            <div class="db-noti">
                <ul>
                    <?php
                    while ($user_notification_row = mysqli_fetch_array($user_notification_query)) {

                        $enquiry_sender_id = $user_notification_row['enquiry_sender_id'];
                        $enquiry_listing_id = $user_notification_row['listing_id'];
                        $enquiry_message = $user_notification_row['enquiry_message'];
                        $enquiry_cdt = $user_notification_row['enquiry_cdt'];

                        $review_user_id = $user_notification_row['review_user_id'];
                        $review_message = $user_notification_row['review_message'];
                        $review_listing_id = $user_notification_row['listing_id'];
                        $review_cdt = $user_notification_row['review_cdt'];

                        $listing_likes_id = $user_notification_row['listing_likes_id'];
                        $listing_likes_user_id = $user_notification_row['user_id'];
                        $listing_likes_listing_id = $user_notification_row['listing_id'];
                        $listing_likes_cdt = $user_notification_row['listing_likes_cdt'];

                        ?>

                        <!--                        // Enquiry Section starts-->

                        <?php

                        if ($enquiry_sender_id != NULL) {

                            $enquiry_user = getUser($enquiry_sender_id);            // To Fetch user data
                            $enquiry_listing = getIdListing($enquiry_listing_id);   //To Fetch listing data

                            ?>

                            <li>
                                <div>
                                    <a target="_blank" href="<?php echo $PROFILE_URL.urlModifier($enquiry_user['user_slug']); ?>"><?php echo $enquiry_user['first_name']; ?></a><?php echo $BIZBOOK['DB-NOTIFICATION-SEND-LISTING-ENQUIRY'];?>
                                    <a href="<?php echo $LISTING_URL.urlModifier($enquiry_listing['listing_slug']); ?>"><?php echo $enquiry_listing['listing_name']; ?></a>.
                                </div>
                                <p><?php echo $enquiry_message; ?></p>
                    <span><?php echo timeFormatconverter($enquiry_cdt) ?><?php echo $BIZBOOK['DB-NOTIFICATION-ON']; ?> <?php echo dateFormatconverter($enquiry_cdt); ?></span>
                            </li>

                            <?php
                        }
                        ?>
                        <!--                        // Enquiry Section ends-->

                        <!--                        // Reviews Section starts-->
                        <?php

                        if ($review_user_id != NULL) {

                            $review_user = getUser($review_user_id);            // To Fetch user data
                            $review_listing = getIdListing($review_listing_id); //To Fetch listing data

                            ?>

                            <li>
                                <div><a target="_blank"
                                        href="<?php echo $PROFILE_URL.urlModifier($review_user['user_slug']); ?>"><?php echo $review_user['first_name']; ?></a><?php echo $BIZBOOK['DB-NOTIFICATION-WRITE-REVIEW']; ?> 
                                    <a href="<?php echo $LISTING_URL.urlModifier($review_listing['listing_slug']); ?>"><?php echo $review_listing['listing_name']; ?></a>.
                                </div>
                                <p><?php echo $review_message; ?></p>
                                <span><?php echo timeFormatconverter($review_cdt) ?><?php echo $BIZBOOK['DB-NOTIFICATION-ON']; ?> <?php echo dateFormatconverter($review_cdt); ?></span>
                            </li>

                            <?php
                        }
                        ?>

                        <!--                        // Reviews Section ends-->

                        <!--                        // Likes Section Starts-->
                        <?php

                        if ($listing_likes_id != NULL) {

                            $listing_likes_user = getUser($listing_likes_user_id);            // To Fetch user data
                            $listing_likes_listing = getIdListing($listing_likes_listing_id); //To Fetch listing data

                            ?>

                            <li>
                                <div>
                                    <a href="<?php echo $PROFILE_URL.urlModifier($listing_likes_user['user_slug']); ?>"><?php echo $listing_likes_user['first_name']; ?></a>
                                    <?php echo $BIZBOOK['DB-NOTIFICATION-LIKE-LISTING']; ?>
                                </div>
                                <span><?php echo timeFormatconverter($listing_likes_cdt) ?><?php echo $BIZBOOK['DB-NOTIFICATION-ON']; ?> <?php echo dateFormatconverter($listing_likes_cdt); ?></span>
                            </li>

                            <?php
                        }
                        ?>


                        <?php
                    }
                    ?>
                    <?php
                    $user_followers_array = explode(",", $user_details_row['user_followers']);
                    foreach ($user_followers_array as $user_followers) {
                        $user_followers_row = getUser($user_followers); // To Fetch particular User Data
                        ?>
                        <li>
                            <div><a href="<?php echo $PROFILE_URL.urlModifier($user_followers_row['user_slug']); ?>" target="_blank">
                                    <?php echo $user_followers_row['first_name']; ?></a> <?php echo $BIZBOOK['DB-NOTIFICATION-START-FOLLOWING']; ?>
                            </div>
                        </li>
                        <?php
                    }
                    ?>


                    <li>
                        <div><?php echo $BIZBOOK['DB-NOTIFICATION-THANK-YOU-MESSAGE']; ?> "<?php echo $footer_row['website_address']; ?>"
                            <?php echo $BIZBOOK['DB-NOTIFICATION-PORTAL']; ?>.
                        </div>
                        <span><?php echo timeFormatconverter($user_details_row['user_cdt']) ?><?php echo $BIZBOOK['DB-NOTIFICATION-ON']; ?> <?php echo dateFormatconverter($user_details_row['user_cdt']); ?></span>
                    </li>
                    <li>
                        <div><?php echo $BIZBOOK['DB-NOTIFICATION-WELCOME-MESSAGE']; ?> "<?php echo $footer_row['website_address']; ?>"
                            <?php echo $BIZBOOK['DB-NOTIFICATION-PORTAL']; ?>.
                        </div>
                        <span><?php echo timeFormatconverter($user_details_row['user_cdt']) ?><?php echo $BIZBOOK['DB-NOTIFICATION-ON']; ?> <?php echo dateFormatconverter($user_details_row['user_cdt']); ?></span>
                    </li>
                </ul>
            </div>
        </div>
    </div>
<?php
include "dashboard_right_pane.php";
?>