<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}
include "dashboard_left_pane.php";
?>
    <!--CENTER SECTION-->
    <div class="ud-main">
   <div class="ud-main-inn ud-no-rhs">
    <div class="ud-cen">
        <div class="log-bor">&nbsp;</div>
        <span class="udb-inst"><?php echo $BIZBOOK['FOLLOWINGS']; ?></span>
        <?php include('config/user_activation_checker.php'); ?>
        <div class="ud-cen-s2">
            <h2><?php echo $BIZBOOK['DB-FOLLOWINGS-FOLLOWING-USERS']; ?></h2>
            <?php include "page_level_message.php"; ?>
            <a href="db-all-users" class="db-tit-btn"><?php echo $BIZBOOK['DB-FOLLOWINGS-VIEW-ALL-USERS']; ?></a>
            <div class="db-fol-grid">
                <ul>
                    <?php

                    foreach (getUserFollowing($_SESSION['user_id']) as $all_user_details_row) {

                        $all_user_id = $all_user_details_row['user_id'];

                        $all_list_count = getCountUserListing($all_user_id);

                        $all_event_count = getCountUserEvent($all_user_id);

                        $all_blog_count = getCountUserBlog($all_user_id);

                        ?>
                        <li>
                            <div class="pro-fol-gr">
                                <div class="db-unfol-user">
                                    <img src="images/user/<?php if (($all_user_details_row['profile_image'] == NULL) || empty($all_user_details_row['profile_image'])) {
                                        echo $footer_row['user_default_image'];
                                    } else {
                                        echo $all_user_details_row['profile_image'];
                                    } ?>" alt="">
                                    <h4><b><?php echo $all_user_details_row['first_name']; ?></b> <?php echo $user_details_row['user_city']; ?></h4>
                                    <a href="<?php echo $PROFILE_URL.urlModifier($all_user_details_row['user_slug']); ?>" target="_blank" class="comm-viw-pro-btn"></a>
                                </div>
                                <div class="count-li">
                                    <span><b><?php echo $all_list_count; ?></b> <?php echo $BIZBOOK['LISTINGS']; ?></span>
                                    <span><b><?php echo $all_event_count; ?></b> <?php echo $BIZBOOK['EVENTS']; ?></span>
                                    <span><b><?php echo $all_blog_count; ?></b> <?php echo $BIZBOOK['BLOGS']; ?></span>
                                </div>
                                <div class="pro-pg-msg">
                                    <span><i class="material-icons">message</i> <?php echo $BIZBOOK['MESSAGES']; ?></span>
                                <span class="userfollow follow-content<?php echo $all_user_id ?>"
                                      data-item="<?php echo $all_user_id; ?>"
                                      data-num="<?php echo $_SESSION['user_id']; ?>"><?php echo $BIZBOOK['UN_FOLLOW']; ?></span>
                                </div>
                            </div>
                        </li>
                        <?php
                    }
                    ?>

                </ul>
            </div>
        </div>
    </div>
<?php
include "dashboard_right_pane.php";
?>