<?php
include "header.php";
?>

<?php if ($admin_row['admin_appearance_options'] != 1) {
    header("Location: profile.php");
}

if (isset($_GET["q"])) {
    $q = $_GET["q"];
} else {
    $q = 0;
};
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">All Media</span>
                <div class="ud-cen-s2">
                    <div class="top-tools">
                        <h2>All User Media/Images</h2>
                        <div style="display: none" class="static-success-message log-suc"><p>Selected Images have been
                                Permanently Deleted!!! Please wait for automatic page refresh!! </p></div>
                        <ul>
                            <li>
                                <span id="delete_record" class="tol-btn">Delete selected</span>
                            </li>
                            <li>
                                <button class="tol-btn med-sel-all-cta">Select all images</button>
                            </li>
                            <li>
                                <div class="form-group">
                                    <select class="form-control"
                                            onchange="this.options[this.selectedIndex].value && (window.location = 'media-library.php?q='+this.options[this.selectedIndex].value);"
                                            id="sel1">
                                        <option name="" <?php if($q == 0){ echo "selected"; } ?> value="0" id="">All images</option>
                                        <option name="" <?php if($q == 1){ echo "selected"; } ?> value="1" id="">Listing images</option>
                                        <option name="" <?php if($q == 2){ echo "selected"; } ?> value="2" id="">Event images</option>
                                        <option name="" <?php if($q == 3){ echo "selected"; } ?> value="3" id="">Product images</option>
                                        <option name="" <?php if($q == 4){ echo "selected"; } ?> value="4" id="">Service expert images</option>
                                        <option name="" <?php if($q == 5){ echo "selected"; } ?> value="5" id="">Job images</option>
                                        <option name="" <?php if($q == 6){ echo "selected"; } ?> value="6" id="">Discount images</option>
                                        <option name="" <?php if($q == 7){ echo "selected"; } ?> value="7" id="">Ads images</option>
                                        <option name="" <?php if($q == 8){ echo "selected"; } ?> value="8" id="">Blog images</option>
                                        <option name="" <?php if($q == 9){ echo "selected"; } ?> value="9" id="">Profile images</option>
                                        <option name="" <?php if($q == 10){ echo "selected"; } ?> value="10" id="">Listing services images</option>
                                        <option name="" <?php if($q == 11){ echo "selected"; } ?> value="11" id="">Listing gallery images</option>
<!--                                        <option name="" value="11" id="">Slide images</option>-->
<!--                                        <option name="" value="12" id="">User images</option>-->
                                    </select>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <div class="med-lib">
                        <?php
                        if ($q == 0 || $q == 1) {
                            ?>
                            <div class="list-images">
                                <p class="media-p-tag">Listing images</p>
                                <ul>
                                    <?php
                                    $si = 1;
                                    foreach (getAllListing() as $listing_row) {
                                        $user_row = getUser($listing_row['user_id']);
                                        ?>
                                        <li>
                                            <input
                                                value="list_prof-^^-<?php echo $listing_row['profile_image']; ?>-^^-<?php echo $listing_row['listing_id']; ?>"
                                                type="checkbox" class="med-lib-input"
                                                id="medlib-listing-<?php echo $si; ?>"/>
                                            <label for="medlib-listing-<?php echo $si; ?>">
                                                <img
                                                    src="../images/listings/<?php echo $listing_row['profile_image']; ?>"/>
                                            </label>
                                            <div class="inp-ttip">
                                                <ul>
                                                    <li><b>User</b>: <?php echo $user_row['first_name']; ?></li>
                                                    <li>
                                                        <b>Page</b>: <?php echo $LISTING_URL . urlModifier($listing_row['listing_slug']); ?>
                                                    </li>
                                                    <li><b>Image
                                                            path</b>: <?php echo $webpage_full_link . "images/listings/" . $listing_row['profile_image']; ?>
                                                    </li>
                                                    <li>
                                                        <b>Date</b>: <?php echo dateFormatconverter($listing_row['listing_cdt']); ?>
                                                    </li>
                                                </ul>
                                            </div>
                                        </li>
                                        <?php
                                        $si++;
                                    }
                                    ?>
                                </ul>
                            </div>
                            <?php
                        }
                        if ($q == 0 || $q == 2) {
                            ?>
                            <div class="event-images">
                                <p class="media-p-tag">Event images</p>
                                <ul>
                                    <?php
                                    $si = 1;
                                    foreach (getAllEvents() as $events_row) {
                                        $user_row = getUser($events_row['user_id']);
                                        ?>
                                        <li>
                                            <input
                                                value="event-^^-<?php echo $events_row['event_image']; ?>-^^-<?php echo $events_row['event_id']; ?>"
                                                type="checkbox" class="med-lib-input"
                                                id="medlib-events-<?php echo $si; ?>"/>
                                            <label for="medlib-events-<?php echo $si; ?>">
                                                <img src="../images/events/<?php echo $events_row['event_image']; ?>"/>
                                            </label>
                                            <div class="inp-ttip">
                                                <ul>
                                                    <li><b>User</b>: <?php echo $user_row['first_name']; ?></li>
                                                    <li>
                                                        <b>Page</b>: <?php echo $EVENT_URL . urlModifier($events_row['event_slug']); ?>
                                                    </li>
                                                    <li><b>Image
                                                            path</b>: <?php echo $webpage_full_link . "images/events/" . $events_row['event_image']; ?>
                                                    </li>
                                                    <li>
                                                        <b>Date</b>: <?php echo dateFormatconverter($events_row['event_cdt']); ?>
                                                    </li>
                                                </ul>
                                            </div>
                                        </li>
                                        <?php
                                        $si++;
                                    }
                                    ?>
                                </ul>
                            </div>
                            <?php
                        }
                        if ($q == 0 || $q == 3) {
                            ?>
                            <div class="product-images">
                                <p class="media-p-tag">Product images</p>
                                <ul>
                                    <?php
                                    $si = 1;
                                    foreach (getAllProduct() as $product_row) {
                                        $user_row = getUser($product_row['user_id']);

                                        $gallery_image_array = $product_row['gallery_image'];
                                        $gallery_image = explode(',', $gallery_image_array);

                                        $p = 1;
                                        foreach ($gallery_image as $item) {
                                            ?>
                                            <li>
                                                <input
                                                    value="product-^^-<?php echo $item; ?>-^^-<?php echo $product_row['product_id']; ?>"
                                                    type="checkbox" class="med-lib-input"
                                                    id="medlib-products-<?php echo $si; ?>"/>
                                                <label for="medlib-products-<?php echo $si; ?>">
                                                    <img src="../images/products/<?php echo $item; ?>"/>
                                                </label>
                                                <div class="inp-ttip">
                                                    <ul>
                                                        <li><b>User</b>: <?php echo $user_row['first_name']; ?></li>
                                                        <li>
                                                            <b>Page</b>: <?php echo $PRODUCT_URL . urlModifier($product_row['product_slug']); ?>
                                                        </li>
                                                        <li><b>Image
                                                                path</b>: <?php echo $webpage_full_link . "images/products/" . $item; ?>
                                                        </li>
                                                        <li>
                                                            <b>Date</b>: <?php echo dateFormatconverter($product_row['product_cdt']); ?>
                                                        </li>
                                                    </ul>
                                                </div>
                                            </li>
                                            <?php
                                            $si++;
                                        }
                                    }
                                    ?>
                                </ul>
                            </div>
                            <?php
                        }
                        if ($q == 0 || $q == 4) {
                            ?>
                            <div class="expert-images">
                                <p class="media-p-tag">Service Expert images</p>
                                <ul>
                                    <?php
                                    $si = 1;
                                    foreach (getAllExperts() as $experts_row) {
                                        $user_row = getUser($experts_row['user_id']);
                                        ?>
                                        <li>
                                            <input
                                                value="expert-^^-<?php echo $experts_row['profile_image']; ?>-^^-<?php echo $experts_row['expert_id']; ?>"
                                                type="checkbox" class="med-lib-input"
                                                id="medlib-experts-<?php echo $si; ?>"/>
                                            <label for="medlib-experts-<?php echo $si; ?>">
                                                <img
                                                    src="../service-experts/images/services/<?php echo $experts_row['profile_image']; ?>"/>
                                            </label>
                                            <div class="inp-ttip">
                                                <ul>
                                                    <li><b>User</b>: <?php echo $user_row['first_name']; ?></li>
                                                    <li>
                                                        <b>Page</b>: <?php echo $SERVICE_EXPERT_URL . urlModifier($experts_row['expert_slug']); ?>
                                                    </li>
                                                    <li><b>Image
                                                            path</b>: <?php echo $webpage_full_link . "service-experts/images/services/" . $experts_row['profile_image']; ?>
                                                    </li>
                                                    <li>
                                                        <b>Date</b>: <?php echo dateFormatconverter($experts_row['expert_cdt']); ?>
                                                    </li>
                                                </ul>
                                            </div>
                                        </li>
                                        <?php
                                        $si++;
                                    }
                                    ?>
                                </ul>
                            </div>
                            <?php
                        }
                        if ($q == 0 || $q == 5) {
                            ?>
                            <div class="job-images">
                                <p class="media-p-tag">Job images</p>
                                <ul>
                                    <?php
                                    $si = 1;
                                    foreach (getAllJob() as $jobs_row) {
                                        $user_row = getUser($jobs_row['user_id']);
                                        ?>
                                        <li>
                                            <input
                                                value="job-^^-<?php echo $jobs_row['company_logo']; ?>-^^-<?php echo $jobs_row['job_id']; ?>"
                                                type="checkbox" class="med-lib-input"
                                                id="medlib-jobs-<?php echo $si; ?>"/>
                                            <label for="medlib-jobs-<?php echo $si; ?>">
                                                <img
                                                    src="../jobs/images/jobs/<?php echo $jobs_row['company_logo']; ?>"/>
                                            </label>
                                            <div class="inp-ttip">
                                                <ul>
                                                    <li><b>User</b>: <?php echo $user_row['first_name']; ?></li>
                                                    <li>
                                                        <b>Page</b>: <?php echo $JOB_URL . urlModifier($jobs_row['job_slug']); ?>
                                                    </li>
                                                    <li><b>Image
                                                            path</b>: <?php echo $webpage_full_link . "jobs/images/jobs/" . $jobs_row['company_logo']; ?>
                                                    </li>
                                                    <li>
                                                        <b>Date</b>: <?php echo dateFormatconverter($jobs_row['job_cdt']); ?>
                                                    </li>
                                                </ul>
                                            </div>
                                        </li>
                                        <?php
                                        $si++;
                                    }
                                    ?>
                                </ul>
                            </div>
                            <?php
                        }
                        if ($q == 0 || $q == 6) {
                            ?>
                            <div class="discount-images">
                                <p class="media-p-tag">Discount images</p>
                                <ul>
                                    <?php
                                    $si = 1;
                                    foreach (getAllCoupons() as $coupons_row) {
                                        $user_row = getUser($coupons_row['user_id']);
                                        ?>
                                        <li>
                                            <input
                                                value="coupon-^^-<?php echo $coupons_row['coupon_photo']; ?>-^^-<?php echo $coupons_row['coupon_id']; ?>"
                                                type="checkbox" class="med-lib-input"
                                                id="medlib-coupons-<?php echo $si; ?>"/>
                                            <label for="medlib-coupons-<?php echo $si; ?>">
                                                <img src="../images/user/<?php echo $coupons_row['coupon_photo']; ?>"/>
                                            </label>
                                            <div class="inp-ttip">
                                                <ul>
                                                    <li><b>User</b>: <?php echo $user_row['first_name']; ?></li>
                                                    <li><b>Image
                                                            path</b>: <?php echo $webpage_full_link . "images/user/" . $coupons_row['coupon_photo']; ?>
                                                    </li>
                                                    <li>
                                                        <b>Date</b>: <?php echo dateFormatconverter($coupons_row['coupon_cdt']); ?>
                                                    </li>
                                                </ul>
                                            </div>
                                        </li>
                                        <?php
                                        $si++;
                                    }
                                    ?>
                                </ul>
                            </div>
                            <?php
                        }
                        if ($q == 0 || $q == 7) {
                            ?>
                            <div class="ads-images">
                                <p class="media-p-tag">Ads images</p>
                                <ul>
                                    <?php
                                    $si = 1;
                                    foreach (getAllActiveAdsEnquiry() as $ads_row) {
                                        $user_row = getUser($ads_row['user_id']);
                                        ?>
                                        <li>
                                            <input
                                                value="ads-^^-<?php echo $ads_row['ad_enquiry_photo']; ?>-^^-<?php echo $ads_row['all_ads_enquiry_id']; ?>"
                                                type="checkbox" class="med-lib-input"
                                                id="medlib-ads-<?php echo $si; ?>"/>
                                            <label for="medlib-ads-<?php echo $si; ?>">
                                                <img src="../images/ads/<?php echo $ads_row['ad_enquiry_photo']; ?>"/>
                                            </label>
                                            <div class="inp-ttip">
                                                <ul>
                                                    <li><b>User</b>: <?php echo $user_row['first_name']; ?></li>
                                                    <li><b>Image
                                                            path</b>: <?php echo $webpage_full_link . "images/ads/" . $ads_row['ad_enquiry_photo']; ?>
                                                    </li>
                                                    <li>
                                                        <b>Date</b>: <?php echo dateFormatconverter($ads_row['ad_enquiry_cdt']); ?>
                                                    </li>
                                                </ul>
                                            </div>
                                        </li>
                                        <?php
                                        $si++;
                                    }
                                    ?>
                                </ul>
                            </div>
                            <?php
                        }
                        if ($q == 0 || $q == 8) {
                            ?>
                            <div class="blog-images">
                                <p class="media-p-tag">Blogs images</p>
                                <ul>
                                    <?php
                                    $si = 1;
                                    foreach (getAllBlogs() as $blog_row) {
                                        $user_row = getUser($blog_row['user_id']);
                                        ?>
                                        <li>
                                            <input
                                                value="blog-^^-<?php echo $blog_row['blog_image']; ?>-^^-<?php echo $blog_row['blog_id']; ?>"
                                                type="checkbox" class="med-lib-input"
                                                id="medlib-blog-<?php echo $si; ?>"/>
                                            <label for="medlib-blog-<?php echo $si; ?>">
                                                <img src="../images/blogs/<?php echo $blog_row['blog_image']; ?>"/>
                                            </label>
                                            <div class="inp-ttip">
                                                <ul>
                                                    <li><b>User</b>: <?php echo $user_row['first_name']; ?></li>
                                                    <li>
                                                        <b>Page</b>: <?php echo $BLOG_URL . urlModifier($blog_row['blog_slug']); ?>
                                                    </li>
                                                    <li><b>Image
                                                            path</b>: <?php echo $webpage_full_link . "images/blogs/" . $blog_row['blog_image']; ?>
                                                    </li>
                                                    <li>
                                                        <b>Date</b>: <?php echo dateFormatconverter($blog_row['blog_cdt']); ?>
                                                    </li>
                                                </ul>
                                            </div>
                                        </li>
                                        <?php
                                        $si++;
                                    }
                                    ?>
                                </ul>
                            </div>
                            <?php
                        }
                        if ($q == 0 || $q == 9) {
                            ?>
                            <div class="profile-images">
                                <p class="media-p-tag">Profile images</p>
                                <ul>
                                    <?php
                                    $si = 1;
                                    foreach (getAllUser() as $user_profile_row) {

                                        ?>
                                        <li>
                                            <input
                                                value="user_profile-^^-<?php echo $user_profile_row['profile_image']; ?>-^^-<?php echo $user_profile_row['user_id']; ?>"
                                                type="checkbox" class="med-lib-input"
                                                id="medlib-user-profile-<?php echo $si; ?>"/>
                                            <label for="medlib-user-profile-<?php echo $si; ?>">
                                                <img
                                                    src="../images/user/<?php echo $user_profile_row['profile_image']; ?>"/>
                                            </label>
                                            <div class="inp-ttip">
                                                <ul>
                                                    <li><b>User</b>: <?php echo $user_profile_row['first_name']; ?></li>
                                                    <li>
                                                        <b>Page</b>: <?php echo $PROFILE_URL . urlModifier($user_profile_row['user_slug']); ?>
                                                    </li>
                                                    <li><b>Image
                                                            path</b>: <?php echo $webpage_full_link . "images/user/" . $user_profile_row['profile_image']; ?>
                                                    </li>
                                                    <li>
                                                        <b>Date</b>: <?php echo dateFormatconverter($user_profile_row['user_cdt']); ?>
                                                    </li>
                                                </ul>
                                            </div>
                                        </li>
                                        <?php
                                        $si++;
                                    }
                                    ?>
                                </ul>
                            </div>
                            <?php
                        }
                        if ($q == 0 || $q == 10) {
                            ?>
                            <div class="listing-service-images">
                                <p class="media-p-tag">Listing Services images</p>
                                <ul>
                                    <?php
                                    $si = 1;
                                    foreach (getAllNotNullServiceListing() as $listing_service_row) {

                                        $user_row = getUser($listing_service_row['user_id']);

                                        $service_image_array = $listing_service_row['service_image'];
                                        $service_image = explode(',', $service_image_array);

                                        $p = 1;
                                        foreach ($service_image as $item) {
                                            ?>
                                            <li>
                                                <input
                                                    value="listing_service-^^-<?php echo $item; ?>-^^-<?php echo $listing_service_row['listing_id']; ?>"
                                                    type="checkbox" class="med-lib-input"
                                                    id="medlib-listing_service-<?php echo $si; ?>"/>
                                                <label for="medlib-listing_service-<?php echo $si; ?>">
                                                    <img src="../images/services/<?php echo $item; ?>"/>
                                                </label>
                                                <div class="inp-ttip">
                                                    <ul>
                                                        <li><b>User</b>: <?php echo $user_row['first_name']; ?></li>
                                                        <li>
                                                            <b>Page</b>: <?php echo $LISTING_URL . urlModifier($listing_service_row['listing_slug']); ?>
                                                        </li>
                                                        <li><b>Image
                                                                path</b>: <?php echo $webpage_full_link . "images/services/" . $item; ?>
                                                        </li>
                                                        <li>
                                                            <b>Date</b>: <?php echo dateFormatconverter($listing_service_row['listing_cdt']); ?>
                                                        </li>
                                                    </ul>
                                                </div>
                                            </li>
                                            <?php
                                            $si++;
                                        }
                                    }
                                    ?>
                                </ul>
                            </div>
                            <?php
                        } if ($q == 0 || $q == 11) {
                            ?>
                            <div class="listing-service-images">
                                <p class="media-p-tag">Listing Gallery images</p>
                                <ul>
                                    <?php
                                    $si = 1;
                                    foreach (getAllNotNullGalleryListing() as $listing_gallery_row) {

                                        $user_row = getUser($listing_gallery_row['user_id']);

                                        $gallery_image_array = $listing_gallery_row['gallery_image'];
                                        $gallery_image = explode(',', $gallery_image_array);

                                        $p = 1;
                                        foreach ($gallery_image as $item) {
                                            ?>
                                            <li>
                                                <input
                                                    value="listing_gallery-^^-<?php echo $item; ?>-^^-<?php echo $listing_gallery_row['listing_id']; ?>"
                                                    type="checkbox" class="med-lib-input"
                                                    id="medlib-listing_gallery-<?php echo $si; ?>"/>
                                                <label for="medlib-listing_gallery-<?php echo $si; ?>">
                                                    <img src="../images/listings/<?php echo $item; ?>"/>
                                                </label>
                                                <div class="inp-ttip">
                                                    <ul>
                                                        <li><b>User</b>: <?php echo $user_row['first_name']; ?></li>
                                                        <li>
                                                            <b>Page</b>: <?php echo $LISTING_URL . urlModifier($listing_gallery_row['listing_slug']); ?>
                                                        </li>
                                                        <li><b>Image
                                                                path</b>: <?php echo $webpage_full_link . "images/listings/" . $item; ?>
                                                        </li>
                                                        <li>
                                                            <b>Date</b>: <?php echo dateFormatconverter($listing_gallery_row['listing_cdt']); ?>
                                                        </li>
                                                    </ul>
                                                </div>
                                            </li>
                                            <?php
                                            $si++;
                                        }
                                    }
                                    ?>
                                </ul>
                            </div>
                            <?php
                        }
                        ?>
                        <!--                        <div class="slide-images">-->
                        <!--                            <p class="media-p-tag">Slide images</p>-->
                        <!--                            <ul>-->
                        <!--                                <li>-->
                        <!--                                    <input type="checkbox" id="medlib1" />-->
                        <!--                                    <label for="medlib1">-->
                        <!--                                        <img src="../images/blogs/19399pexels-adriaan-greyling-764835.jpg" />-->
                        <!--                                    </label>-->
                        <!--                                    <div class="inp-ttip">-->
                        <!--                                        <ul>-->
                        <!--                                            <li><b>User</b>: John smith</li>-->
                        <!--                                            <li><b>Page</b>: https://bizbookdirectorytemplate.com/listing/happy-facial-new-york</li>-->
                        <!--                                            <li><b>Image path</b>: https://bizbookdirectorytemplate.com/images/listings/99073s7.jpeg</li>-->
                        <!--                                            <li><b>Date</b>: 12 Dec 2021</li>-->
                        <!--                                        </ul>-->
                        <!--                                    </div>-->
                        <!--                                </li>-->
                        <!--                                <li>-->
                        <!--                                    <input type="checkbox" id="medlib2" />-->
                        <!--                                    <label for="medlib2"><img src="../images/blogs/789251.jpg" /></label>-->
                        <!--                                    <div class="inp-ttip">-->
                        <!--                                        <ul>-->
                        <!--                                            <li><b>User</b>: John smith</li>-->
                        <!--                                            <li><b>Page</b>: https://bizbookdirectorytemplate.com/listing/happy-facial-new-york</li>-->
                        <!--                                            <li><b>Image path</b>: https://bizbookdirectorytemplate.com/images/listings/99073s7.jpeg</li>-->
                        <!--                                            <li><b>Date</b>: 12 Dec 2021</li>-->
                        <!--                                        </ul>-->
                        <!--                                    </div>-->
                        <!--                                </li>-->
                        <!--                                <li>-->
                        <!--                                    <input type="checkbox" id="medlib3" />-->
                        <!--                                    <label for="medlib3"><img src="../images/blogs/97000this-is-neat.jpg" /></label>-->
                        <!--                                    <div class="inp-ttip">-->
                        <!--                                        <ul>-->
                        <!--                                            <li><b>User</b>: John smith</li>-->
                        <!--                                            <li><b>Page</b>: https://bizbookdirectorytemplate.com/listing/happy-facial-new-york</li>-->
                        <!--                                            <li><b>Image path</b>: https://bizbookdirectorytemplate.com/images/listings/99073s7.jpeg</li>-->
                        <!--                                            <li><b>Date</b>: 12 Dec 2021</li>-->
                        <!--                                        </ul>-->
                        <!--                                    </div>-->
                        <!--                                </li>-->
                        <!--                            </ul>-->
                        <!--                        </div>-->
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="../js/jquery.min.js"></script>
<script src="../js/popper.min.js"></script>
<script src="../js/bootstrap.min.js"></script>
<script src="../js/jquery-ui.js"></script>
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
<script>
    $('.med-sel-all-cta').click(function () {
        $('.med-lib ul li input').prop('checked', true);
    });
    //INPUT FOCUS TOOL TIP SHOW
    $(".med-lib label").hover(function () {
        $(this).siblings(".inp-ttip").fadeIn();
    });
    $(".med-lib label").mouseleave(function () {
        $(this).siblings(".inp-ttip").fadeOut();
    });
</script>

<script>
    $('#delete_record').click(function () {

        var deleteids_arr = [];
        // Read all checked checkboxes
        $("input:checkbox[class=med-lib-input]:checked").each(function () {
            deleteids_arr.push($(this).val());
        });

        // Check checkbox checked or not
        if (deleteids_arr.length > 0) {
            // Confirm alert
            var confirmdelete = confirm("Do you really want to Delete selected Image(s)?");
            if (confirmdelete == true) {
                $.ajax({
                    url: 'multiple_user_media_delete.php',
                    type: 'post',
                    data: {deleteids_arr: deleteids_arr},
                    success: function (response) {
                        //alert(response);
                        $('.static-success-message').css("display", "block");
                        window.setTimeout(function () {
                            location.reload()
                        }, 3000)
                    }
                });
            }
        }
    });
</script>
</body>

</html>