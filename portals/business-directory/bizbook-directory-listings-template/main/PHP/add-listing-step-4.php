<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

if (file_exists('config/general_user_authentication.php')) {
    include('config/general_user_authentication.php');
}

if (file_exists('config/listing_page_authentication.php')) {
    include('config/listing_page_authentication.php');
}
//To check the listings count with current plan starts

$plan_type_listing_count = $user_plan_type['plan_type_listing_count'];
$listing_count_user = getCountUserListing($_SESSION['user_id']);

if($listing_count_user >= $plan_type_listing_count){

    $_SESSION['status_msg'] = $BIZBOOK['LISTINGS_LIMIT_EXCEED_MESSAGE'];

    header('Location: db-all-listing');
}
//To check the listings count with current plan ends

//Get & Process Listing Data
//if ($_SERVER['REQUEST_METHOD'] == 'POST') {

if (isset($_POST['listing_submit'])) {

// Service Provided Details
    $_SESSION['service_1_name'] = $_POST["service_1_name"];
    $_SESSION['service_1_price'] = $_POST["service_1_price"];
    $_SESSION['service_1_detail'] = $_POST["service_1_detail"];
    $_SESSION['service_1_view_more'] = $_POST["service_1_view_more"];


    // ************************  Offer Image Upload Starts  **************************

    $all_service_1_image = $_FILES['service_1_image'];
    $all_service_1_image2 = $_FILES['service_1_image']['name'];

    for ($k = 0; $k < count($all_service_1_image2); $k++) {

        if (!empty($_FILES['service_1_image']['name'][$k])) {
            $file = rand(1000, 100000) . $_FILES['service_1_image']['name'][$k];
            $file_loc = $_FILES['service_1_image']['tmp_name'][$k];
            $file_size = $_FILES['service_1_image']['size'][$k];
            $file_type = $_FILES['service_1_image']['type'][$k];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if(in_array($file_type, $allowed)) {
                $folder = "images/services/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $service_1_image1[] = compressImage($event_image, $file_loc, $folder, $new_size);
            }else{
                $service_1_image1[] = '';
            }
        }
        $service_1_image = implode(",", $service_1_image1);
    }
// ************************  Offer Image Upload ends  **************************
    $_SESSION['service_1_image'] = $service_1_image;

}

//} else {
//
//    header('Location: add-listing-step-1'); 
//}
?>
<!-- START -->
<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg">
    <div class="container">
        <div class="row">
            <div class="add-list-ste">
                <div class="add-list-ste-inn">
                    <ul>
                        <li>
                            <a href="add-listing-step-1">
                                <span><?php echo $BIZBOOK['STEP1']; ?></span>
                                <b><?php echo $BIZBOOK['BASIC_INFO']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="add-listing-step-2">
                                <span><?php echo $BIZBOOK['STEP2']; ?></span>
                                <b><?php echo $BIZBOOK['SERVICES']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="add-listing-step-3">
                                <span><?php echo $BIZBOOK['STEP3']; ?></span>
                                <b><?php echo $BIZBOOK['OFFERS']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="add-listing-step-4" class="act">
                                <span><?php echo $BIZBOOK['STEP4']; ?></span>
                                <b><?php echo $BIZBOOK['MAP']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="#!">
                                <span><?php echo $BIZBOOK['STEP5']; ?></span>
                                <b><?php echo $BIZBOOK['OTHER']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="#!">
                                <span><?php echo $BIZBOOK['STEP6']; ?></span>
                                <b><?php echo $BIZBOOK['DONE']; ?></b>
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="login-main add-list">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['STEP4']; ?></span>
                <div class="log add-list-map">
                    <div class="login add-list-map">
                        <form action="add-listing-step-5.php" class="listing_form_4" id="listing_form_4"
                              name="listing_form_4" method="post" enctype="multipart/form-data">

                            <!--FILED START-->
                            <h4><?php echo $BIZBOOK['PHOTO_GALLERY']; ?></h4>
                            <div>
                                <input type="file" name="gallery_image[]" accept="image/*,.jpg,.jpeg,.png" multiple>
                            </div>
                            <!--FILED END-->
                            <p></p>
                            <h4><?php echo $BIZBOOK['VIDEO_GALLERY']; ?></h4>
                            <!-- TOOL TIP -->
                            <!--<div class="ttip-com">
                                <i class="material-icons">priority_high</i>
                                <div><?php echo $BIZBOOK['VIDEO_GALLERY_INFO']; ?></div>
                            </div>-->
                            <!-- END -->
                            <ul>
                                <span class="add-list-add-btn lis-add-oadvideo" title="add new video">+</span>
                                <span class="add-list-rem-btn lis-add-orevideo" title="remove video">-</span>
                                <?php
                                $listings_a_row_listing_video = $_SESSION['listing_video'];

                                $listings_a_row_listing_video_count = count($listings_a_row_listing_video); //Get count of array

                                if ($listings_a_row_listing_video_count != 0) {

                                    foreach ($listings_a_row_listing_video as $tuple) {
                                        ?>
                                        <li>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <textarea id="listing_video" name="listing_video[]"
                                                                  class="form-control"
                                                                  placeholder="<?php echo $BIZBOOK['PASTE_IFRAME_CODE']; ?>"><?php echo $tuple; ?></textarea>
                                                    </div>
                                                </div>
                                            </div>
                                        </li>
                                        <?php
                                    }
                                } else {
                                    ?>
                                    <li>
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                 <textarea id="listing_video" name="listing_video[]"
                                                           class="form-control"
                                                           placeholder="<?php echo $BIZBOOK['PASTE_IFRAME_CODE']; ?>"></textarea>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                    <?php
                                }
                                ?>
                            </ul>
                            <h4><?php echo $BIZBOOK['MAP_360_VIEW']; ?></h4>
                            
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <textarea id="google_map" name="google_map" class="form-control"
                                                  placeholder="<?php echo $BIZBOOK['SHOP_LOCATION']; ?>"><?php echo $_SESSION['google_map'] ?></textarea>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <textarea id="360_view" name="360_view" class="form-control"
                                                  placeholder="<?php echo $BIZBOOK['360_VIEW']; ?>"><?php echo $_SESSION['360_view'] ?></textarea>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->

<!--                            <h4 class="pt30">--><?php //echo $BIZBOOK['PHOTO_GALLERY']; ?><!--</h4>-->
<!--                            --><?php
//                            //To check the photos count with current plan starts
//
//                            $plan_type_photos_count = $user_plan_type['plan_type_photos_count'];
//
//                            ?>
                            <!--FILED START-->
<!--                            <div class="row">-->
<!--                                --><?php
//                                for($p=1;$p<= $plan_type_photos_count;$p++) {
//                                    ?>
<!--                                    <div class="col-md-6">-->
<!--                                        <div class="form-group">-->
<!--                                            <input type="file" name="gallery_image[]" class="form-control">-->
<!--                                        </div>-->
<!--                                    </div>-->
<!--                                    --><?php
//                                }
//                                ?>
<!--                            </div>-->
                            <!--FILED END-->

                            
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-6">
                                    <a href="add-listing-step-3">
                                        <button type="button" class="btn btn-primary"><?php echo $BIZBOOK['PREVIOUS']; ?></button>
                                    </a>
                                </div>
                                <div class="col-md-6">
                                    <button type="submit" name="listing_submit" class="btn btn-primary"><?php echo $BIZBOOK['NEXT']; ?></button>
                                </div>
                                <div class="col-md-12">
                                    <a href="add-listing-step-5" class="skip"><?php echo $BIZBOOK['SKIP_THIS']; ?> >></a>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--PROGRESSBAR START-->
                            <div class="progress biz-prog">
                                <div class="progress-bar bg-success progress-bar-striped progress-bar-animated" style="width:80%">80%</div>
                            </div>
                            <!--PROGRESSBAR END-->
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!--END PRICING DETAILS-->
<?php
include "footer.php";
?>


<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link ='<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url ='<?php echo $LOGIN_URL;?>';</script>
<script type="text/javascript" src="js/imageuploadify.min.js"></script>
<script src="js/custom.js"></script>
<script type="text/javascript">
    $(document).ready(function() {
        $('input[type="file"]').imageuploadify();
    })
</script>
</body>

</html>