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

if ($listing_count_user >= $plan_type_listing_count) {

    $_SESSION['status_msg'] = $BIZBOOK['LISTINGS_LIMIT_EXCEED_MESSAGE'];

    header('Location: db-all-listing');
}
//To check the listings count with current plan ends

//Get & Process Listing Data
//if ($_SERVER['REQUEST_METHOD'] == 'POST') {

if (isset($_POST['listing_submit'])) {

// Service Provided Details
    $_SESSION['service_id'] = $_POST["service_id"];

    // ************************  Service Image Upload starts  ************************** 

    $all_service_image = $_FILES['service_image'];
    $all_service_image23 = $_FILES['service_image']['name'];

    for ($k = 0; $k < count($all_service_image23); $k++) {

        if (!empty($_FILES['service_image']['name'][$k])) {
            $file = rand(1000, 100000) . $_FILES['service_image']['name'][$k];
            $file_loc = $_FILES['service_image']['tmp_name'][$k];
            $file_size = $_FILES['service_image']['size'][$k];
            $file_type = $_FILES['service_image']['type'][$k];
            $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
            if(in_array($file_type, $allowed)) {
                $folder = "images/services/";
                $new_size = $file_size / 1024;
                $new_file_name = strtolower($file);
                $event_image = str_replace(' ', '-', $new_file_name);
                //move_uploaded_file($file_loc, $folder . $event_image);
                $service_image1[] = compressImage($event_image, $file_loc, $folder, $new_size);
            }else{
                $service_image1[] = '';
            }
        }
        $service_image = implode(",", $service_image1);
    }

// ************************  Service Image Upload ends  **************************

    $_SESSION['service_image'] = $service_image;
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
                            <a href="add-listing-step-3" class="act">
                                <span><?php echo $BIZBOOK['STEP3']; ?></span>
                                <b><?php echo $BIZBOOK['OFFERS']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="#!">
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
                <span class="steps"><?php echo $BIZBOOK['STEP3']; ?></span>
                <div class="log">
                    <div class="login add-list-off">
                        <h4><?php echo $BIZBOOK['SPECIAL_OFFERS']; ?></h4>
                        <span class="add-list-add-btn lis-add-off" title="add new offer">+</span>
                        <span class="add-list-rem-btn lis-add-rem" title="remove offer">-</span>
                        <form action="add-listing-step-4.php" class="listing_form_3" id="listing_form_3"
                              name="listing_form_3" method="post" enctype="multipart/form-data">
                            <ul>
                                <?php
                                $listings_a_row_service_1_name = $_SESSION['service_1_name'];
                                $listings_a_row_service_1_price = $_SESSION['service_1_price'];
                                $listings_a_row_service_1_detail = $_SESSION['service_1_detail'];
                                $listings_a_row_service_1_view_more = $_SESSION['service_1_view_more'];

                                //                                        $ser_1_name_Array = explode(',', $listings_a_row_service_1_name);
                                //                                        $ser_1_price_Array = explode(',', $listings_a_row_service_1_price);
                                //                                        $ser_1_detail_Array = explode(',', $listings_a_row_service_1_detail);

                                $listings_a_row_service_1_name_count = count($listings_a_row_service_1_name); //Get count of array

                                if ($listings_a_row_service_1_name_count != 0) {
                                    $zipped = array_map(null, $listings_a_row_service_1_name, $listings_a_row_service_1_price, $listings_a_row_service_1_detail, $listings_a_row_service_1_view_more);

                                    foreach ($zipped as $tuple) {
                                        $tuple[0]; // offer name
                                        $tuple[1]; // offer Price
                                        $tuple[2]; // offer Detail
                                        $tuple[3]; // offer View more

                                        ?>
                                        <li>
                                            <!--FILED START-->
                                            <div class="row">
                                                <div class="col-md-6">
                                                    <div class="form-group">
                                                        <input type="text" name="service_1_name[]"
                                                               value="<?php echo $tuple[0]; ?>" class="form-control"
                                                               placeholder="<?php echo $BIZBOOK['OFFER_NAME']; ?>">
                                                    </div>
                                                </div>
                                                <div class="col-md-6">
                                                    <div class="form-group">
                                                        <input type="text" name="service_1_price[]"
                                                               onkeypress="return isNumber(event)"
                                                               value="<?php echo $tuple[1]; ?>" class="form-control"
                                                               placeholder="<?php echo $BIZBOOK['PRICE']; ?>">
                                                    </div>
                                                </div>
                                            </div>
                                            <!--FILED END-->
                                            <!--FILED START-->
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                            <textarea name="service_1_detail[]" class="form-control"
                                                                      placeholder="<?php echo $BIZBOOK['DETAILS_ABOUT_OFFER']; ?>"><?php echo $tuple[2]; ?></textarea>
                                                    </div>
                                                </div>
                                            </div>
                                            <!--FILED END-->
                                            <!--FILED START-->
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <div class="fil-img-uplo">
                                                            <span class="dumfil"><?php echo $BIZBOOK['CHOOSE_OFFER_IMAGE']; ?></span>
                                                            <input type="file" name="service_1_image[]" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                            <!--FILED END-->
                                            <!--FILED START-->
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <input type="text" name="service_1_view_more[]"
                                                               value="<?php echo $tuple[3]; ?>" class="form-control"
                                                               placeholder="<?php echo $BIZBOOK['VIEW_MORE_LINK']; ?>">
                                                    </div>
                                                </div>
                                            </div>
                                            <!--FILED END-->
                                        </li>
                                        <?php
                                    }
                                } else {
                                    ?>
                                    <li>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <input type="text" name="service_1_name[]" class="form-control"
                                                           placeholder="<?php echo $BIZBOOK['OFFER_NAME']; ?>">
                                                </div>
                                            </div>
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <input type="text" name="service_1_price[]"
                                                           onkeypress="return isNumber(event)"
                                                           class="form-control"
                                                           placeholder="<?php echo $BIZBOOK['PRICE']; ?>">
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                            <textarea name="service_1_detail[]" class="form-control"
                                                                      placeholder="<?php echo $BIZBOOK['DETAILS_ABOUT_OFFER']; ?>"></textarea>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <div class="fil-img-uplo">
                                                        <span class="dumfil"><?php echo $BIZBOOK['CHOOSE_OFFER_IMAGE']; ?></span>
                                                        <input type="file" name="service_1_image[]" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <input type="text" name="service_1_view_more[]"
                                                           class="form-control"
                                                           placeholder="<?php echo $BIZBOOK['VIEW_MORE_LINK']; ?>">
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                    </li>
                                    <?php
                                }
                                ?>
                            </ul>
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-6">
                                    <a href="add-listing-step-2">
                                        <button type="button"
                                                class="btn btn-primary"><?php echo $BIZBOOK['PREVIOUS']; ?></button>
                                    </a>
                                </div>
                                <div class="col-md-6">
                                    <button type="submit" name="listing_submit"
                                            class="btn btn-primary"><?php echo $BIZBOOK['NEXT']; ?></button>
                                </div>
                                <div class="col-md-12">
                                    <a href="add-listing-step-4" class="skip"><?php echo $BIZBOOK['SKIP_THIS']; ?>
                                        >></a>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--PROGRESSBAR START-->
                            <div class="progress biz-prog">
                                <div class="progress-bar bg-success progress-bar-striped progress-bar-animated" style="width:60%">60%</div>
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
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
</body>

</html>