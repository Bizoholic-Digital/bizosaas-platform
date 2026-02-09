<?php
include "header.php";

?>
<!-- START -->
<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> pri">
    <div class="container">
        <div class="row">
            <div class="tit">
                <h2>
                    <span><?php echo $BIZBOOK['PRICING_TITLE_2']; ?></span></h2>
                <p><?php echo $BIZBOOK['PRICING_SUB_TITLE_2']; ?></p>
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
                                            echo "FREE";
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

                                    <a href="<?php
                                    if (isset($_SESSION['user_id'])) {
                                        echo "db-plan-change";
                                    } else {
                                        echo "login";
                                    } ?>"><?php echo $BIZBOOK['ADD_LISTING']; ?></a>
                                </div>
                                <div class="c4">
                                    <ol>
                                        <li><?php if ($plan_type_row['plan_type_listing_count'] == 1000) {
                                                echo "Unlimited";
                                            } else {
                                                echo $plan_type_row['plan_type_listing_count'];
                                            } ?> <?php echo $BIZBOOK['LISTING']; ?>
                                        </li>

                                        <li>
                                            <?php if ($plan_type_row['plan_type_duration'] >= 7) {
                                                echo $plan_type_row['plan_type_duration'] / 12 . ' ' . "year(s)";
                                            } else {
                                                echo $plan_type_row['plan_type_duration'] . ' ' . "month(s)";
                                            } ?> (<?php echo $BIZBOOK['DURATION']; ?>)
                                        </li>

                                        <li><?php if ($plan_type_row['plan_type_event_count'] == 1000) {
                                                echo "Unlimited";
                                            } else {
                                                echo $plan_type_row['plan_type_event_count'];
                                            } ?> <?php echo $BIZBOOK['EVENTS']; ?>
                                        </li>

                                        <li><?php if ($plan_type_row['plan_type_blog_count'] == 1000) {
                                                echo "Unlimited";
                                            } else {
                                                echo $plan_type_row['plan_type_blog_count'];
                                            } ?> <?php echo $BIZBOOK['BLOG_POSTS']; ?>
                                        </li>

                                        <li><?php if ($plan_type_row['plan_type_job_count'] == 1000) {
                                                echo "Unlimited";
                                            } else {
                                                echo $plan_type_row['plan_type_job_count'];
                                            } ?> <?php echo $BIZBOOK['JOBS']; ?>
                                        </li>

                                        <?php if ($plan_type_row['plan_type_direct_lead'] == 1) { ?>
                                            <li><?php echo $BIZBOOK['PRICING_GET_DIRECT_LEADS']; ?></li>
                                        <?php } ?>

                                        <?php if ($plan_type_row['plan_type_email_notification'] == 1) { ?>
                                            <li><?php echo $BIZBOOK['PRICING_EMAIL_NOTIFICATION']; ?></li>
                                        <?php } ?>

                                        <?php if ($plan_type_row['plan_type_verified'] == 1) { ?>
                                            <li><?php echo $BIZBOOK['PRICING_VERIFIED_LISTING']; ?></li>
                                        <?php } ?>

                                        <?php if ($plan_type_row['plan_type_trusted'] == 1) { ?>
                                            <li><?php echo $BIZBOOK['PRICING_TRUSTED_LISTING']; ?></li>
                                        <?php } ?>

                                        <?php if ($plan_type_row['plan_type_offers'] == 1) { ?>
                                            <li><?php echo $BIZBOOK['SPECIAL_OFFERS']; ?></li>
                                        <?php } ?>

                                        <li><?php echo $BIZBOOK['USER_DASHBOARD']; ?></li>

                                        <li><?php if ($plan_type_row['plan_type_photos_count'] == 1000) {
                                                echo "Unlimited";
                                            } else {
                                                echo $plan_type_row['plan_type_photos_count'];
                                            } ?> <?php echo $BIZBOOK['PHOTOS']; ?>
                                        </li>

                                        <li><?php if ($plan_type_row['plan_type_videos_count'] == 1000) {
                                                echo "Unlimited";
                                            } else {
                                                echo $plan_type_row['plan_type_videos_count'];
                                            } ?> <?php echo $BIZBOOK['VIDEOS']; ?>
                                        </li>

                                        <li><?php echo $BIZBOOK['CREATE_DUPLICATE_LISTING_LABEL']; ?></li>

                                        <?php if ($plan_type_row['plan_type_social'] == 1) { ?>
                                            <li><?php echo $BIZBOOK['PRICING_SOCIAL_SHARE']; ?></li>
                                        <?php } ?>

                                        <?php if ($plan_type_row['plan_type_ratings'] == 1) { ?>
                                            <li><?php echo $BIZBOOK['PRICING_REVIEW_CONTROL']; ?></li>
                                        <?php } ?>

                                        <li><?php echo $BIZBOOK['PRICING_ADMIN_TIPS']; ?></li>
                                    </ol>
                                </div>
                                <div class="c5">
                                    <a href="<?php
                                    if (isset($_SESSION['user_id'])) {
                                        echo "db-plan-change";
                                    } else {
                                        echo "login";
                                    } ?>"><?php echo $BIZBOOK['PRICING_GET_START']; ?></a>
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


<section>
    <div class="pop-ups pop-quo">
        <!-- The Modal -->
        <div class="modal fade" id="quote">
            <div class="modal-dialog">
                <div class="modal-content">
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                    <!-- Modal Header -->
                    <div class="quote-pop">
                        <h4><?php echo $BIZBOOK['LEAD-GET-QUOTE']; ?></h4>
                        <form>
                            <div class="form-group">
                                <input type="text" class="form-control"
                                       placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>" required>
                            </div>
                            <div class="form-group">
                                <input type="email" class="form-control"
                                       placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>"
                                       pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>" required>
                            </div>
                            <div class="form-group">
                                <input type="text" class="form-control"
                                       placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>"
                                       pattern="[7-9]{1}[0-9]{9}"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>" required>
                            </div>
                            <div class="form-group">
                                <textarea class="form-control" rows="3"
                                          placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<?php
include "footer.php";
?>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<?php
if (isset($_GET["page"])) {
    ?>
    <?php
    if (isset($_POST['SubmitButton'])) { // Check if form was submitted

        if (!empty($_FILES['inputText']['name'])) {
            $file = rand(1000, 100000) . $_FILES['inputText']['name'];
            $file_loc = $_FILES['inputText']['tmp_name'];
            $file_size = $_FILES['inputText']['size'];
            $file_type = $_FILES['inputText']['type'];
            $folder = "images/listings/";
            $new_size = $file_size / 1024;
            $new_file_name = strtolower($file);
            $event_image = str_replace(' ', '-', $new_file_name);
            //move_uploaded_file($file_loc, $folder . $event_image);
            $inputText1 = compressImage($event_image, $file_loc, $folder, $new_size);
            $inputText = $inputText1;
        }
    }
    ?>
    <form action="#" enctype="multipart/form-data" method="post">
        <input type="file" name="inputText"/>
        <input type="submit" name="SubmitButton"/>
    </form>
    <?php
}
?>
</body>

</html>