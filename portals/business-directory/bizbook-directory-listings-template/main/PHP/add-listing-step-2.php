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


if (isset($_POST['listing_submit'])) {

// Basic Personal Details
    $_SESSION['first_name'] = $_POST["first_name"];
    $_SESSION['last_name'] = $_POST["last_name"];
    $_SESSION['mobile_number'] = $_POST["mobile_number"];
    $_SESSION['email_id'] = $_POST["email_id"];

    $_SESSION['register_mode'] = "Direct";
    $_SESSION['user_status'] = "Inactive";

// Common Listing Details
    $_SESSION['listing_name'] = $_POST["listing_name"];
    $_SESSION['listing_mobile'] = $_POST["listing_mobile"];
    $_SESSION['listing_email'] = $_POST["listing_email"];
    $_SESSION['listing_website'] = $_POST["listing_website"];
    $_SESSION['listing_whatsapp'] = $_POST["listing_whatsapp"];
    $_SESSION['listing_address'] = $_POST["listing_address"];
    $_SESSION['listing_lat'] = $_POST["listing_lat"];
    $_SESSION['listing_lng'] = $_POST["listing_lng"];
    $_SESSION['listing_description'] = $_POST["listing_description"];
    $_SESSION['category_id'] = $_POST["category_id"];
    $_SESSION['sub_category_id'] = $_POST["sub_category_id"];
    $_SESSION['country_id'] = $_POST["country_id"];
    $_SESSION['service_locations'] = $_POST["service_locations"];
//        $state_id = $_POST["state_id"];


    $_SESSION['state_id'] = "1";

    $_SESSION['city_id'] = $_POST["city_id"];


    //************************  Profile Image Upload starts  **************************

    if (!empty($_FILES['profile_image']['name'])) {
        $file = rand(1000, 100000) . $_FILES['profile_image']['name'];
        $file_loc = $_FILES['profile_image']['tmp_name'];
        $file_size = $_FILES['profile_image']['size'];
        $file_type = $_FILES['profile_image']['type'];
        $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
        if(in_array($file_type, $allowed)) {
            $folder = "images/listings/";
            $new_size = $file_size / 1024;
            $new_file_name = strtolower($file);
            $event_image = str_replace(' ', '-', $new_file_name);
            //move_uploaded_file($file_loc, $folder . $event_image);
            $profile_image = compressImage($event_image, $file_loc, $folder, $new_size);
        }else{
            $profile_image = '';
        }
    }

    $_SESSION['profile_image'] = $profile_image;

//************************  Profile Image Upload Ends  **************************

//************************  Cover Image Upload starts  **************************

    if (!empty($_FILES['cover_image']['name'])) {
        $file = rand(1000, 100000) . $_FILES['cover_image']['name'];
        $file_loc = $_FILES['cover_image']['tmp_name'];
        $file_size = $_FILES['cover_image']['size'];
        $file_type = $_FILES['cover_image']['type'];
        $allowed = array("image/jpeg", "image/pjpeg", "image/png", "image/gif", "image/webp", "image/svg", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.openxmlformats-officedocument.wordprocessingml.template");
        if(in_array($file_type, $allowed)) {
            $folder = "images/listing-ban/";
            $new_size = $file_size / 1024;
            $new_file_name = strtolower($file);
            $event_image = str_replace(' ', '-', $new_file_name);
            //move_uploaded_file($file_loc, $folder . $event_image);
            $cover_image = compressImage($event_image, $file_loc, $folder, $new_size);
        }else{
            $cover_image = '';
        }
    }

    $_SESSION['cover_image'] = $cover_image;

//************************  Cover Image Upload ends  **************************


    if ($_SESSION['listing_name'] == NULL || empty($_SESSION['listing_name'])) {
        header('Location: add-listing-step-1');
    }
}

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
                            <a href="add-listing-step-2" class="act">
                                <span><?php echo $BIZBOOK['STEP2']; ?></span>
                                <b><?php echo $BIZBOOK['SERVICES']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="#!">
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
            <div class="login-main add-list add-list-ser">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['STEP2']; ?></span>
                <div class="log">
                    <div class="login">
                        <h4><?php echo $BIZBOOK['SERVICES_PROVIDE']; ?></h4>
                        <?php include "page_level_message.php"; ?>
                        <span class="add-list-add-btn lis-ser-add-btn" title="add new offer">+</span>
                        <span class="add-list-rem-btn lis-ser-rem-btn" title="remove offer">-</span>
                        <form action="add-listing-step-3.php" class="listing_form_2" id="listing_form_2"
                              name="listing_form_2" method="post" enctype="multipart/form-data">

                            <input id="listing_name" name="listing_name" type="hidden"
                                   value="<?php echo $_SESSION['listing_name']; ?>"
                                   required="required" class="validate">

                            <input id="listing_mobile" name="listing_mobile" type="hidden"
                                   value="<?php echo $_SESSION['listing_mobile']; ?>"
                                   required="required" class="validate">

                            <input id="listing_email" name="listing_email" type="hidden"
                                   value="<?php echo $_SESSION['listing_email']; ?>"
                                   required="required" class="validate">


                            <input id="listing_website" name="listing_website" type="hidden"
                                   value="<?php echo $_SESSION['listing_website']; ?>"
                                   required="required" class="validate">

                            <input id="category_id" name="category_id" type="hidden"
                                   value="<?php echo $_SESSION['category_id']; ?>"
                                   required="required" class="validate">

                            <input id="sub_category_id" name="sub_category_id" type="hidden"
                                   value="<?php echo $_SESSION['sub_category_id']; ?>"
                                   required="required" class="validate">

                            <input id="listing_description" name="listing_description" type="hidden"
                                   value="<?php echo $_SESSION['listing_description']; ?>"
                                   required="required" class="validate">

                            <input id="mobile_number" <?php if (!empty($_SESSION['user_name'])) {
                                echo "readonly";
                            } ?> name="mobile_number" value="<?php if (!empty($_SESSION['user_name'])) {
                                echo $user_details_row['mobile_number'];
                            } else {
                            } ?>" required="required" type="hidden" class="validate">

                            <input id="email_id" <?php if (!empty($_SESSION['user_name'])) {
                                echo "readonly";
                            } ?> name="email_id" value="<?php if (!empty($_SESSION['user_name'])) {
                                echo $user_details_row['email_id'];
                            } else {
                            } ?>" required="required" type="hidden" class="validate">

                            <input id="listing_address" name="listing_address"
                                   value="<?php echo $_SESSION['listing_address']; ?>"
                                   required="required" type="hidden" class="validate">

                            <input id="city_id" name="city_id" value="<?php echo $_SESSION['city_id']; ?>"
                                   required="required"
                                   type="hidden" class="validate">

                            <input id="country_id" name="country_id" value="<?php echo $_SESSION['country_id']; ?>"
                                   required="required"
                                   type="hidden" class="validate">

                            <input id="profile_image" name="profile_image"
                                   value="<?php echo $_SESSION['profile_image']; ?>" required="required"
                                   type="hidden" class="validate">

                            <input id="cover_image" name="cover_image" value="<?php echo $_SESSION['cover_image']; ?>"
                                   required="required"
                                   type="hidden" class="validate">


                            <ul>
                                <?php
                                $service_id_1 = $_SESSION['service_id'];
                                $service_id_count = count($service_id_1);

                                if ($service_id_count != 0) {
                                    foreach ($service_id_1 as $service_Array) {
                                        ?>
                                        <li>
                                            <!--FILED START-->
                                            <div class="row">
                                                <div class="col-md-6">
                                                    <div class="form-group">
                                                        <label><?php echo $BIZBOOK['SERVICE_NAME']; ?>:</label>
                                                        <input type="text" name="service_id[]" class="form-control"
                                                               value="<?php echo $service_Array; ?>"
                                                               placeholder="<?php echo $BIZBOOK['SERVICE_NAME_PLACEHOLDER']; ?>">
                                                    </div>
                                                </div>
                                                <div class="col-md-6">
                                                    <div class="form-group">
                                                        <div class="fil-img-uplo">
                                                            <span class="dumfil"><?php echo $BIZBOOK['SERVICE_NAME']; ?></span>
                                                            <input type="file" name="service_image[]" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                                        </div>
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
                                                    <label><?php echo $BIZBOOK['SERVICE_NAME']; ?>:</label>
                                                    <input type="text" name="service_id[]" class="form-control"
                                                           placeholder="<?php echo $BIZBOOK['SERVICE_NAME_PLACEHOLDER']; ?>">
                                                </div>
                                            </div>
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <div class="fil-img-uplo">
                                                        <span class="dumfil"><?php echo $BIZBOOK['SERVICE_NAME']; ?></span>
                                                        <input type="file" name="service_image[]" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                    </li>
                                    <li>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <label><?php echo $BIZBOOK['SERVICE_NAME']; ?></label>
                                                    <input type="text" name="service_id[]" class="form-control"
                                                           placeholder="<?php echo $BIZBOOK['SERVICE_NAME_PLACEHOLDER']; ?>">
                                                </div>
                                            </div>
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <div class="fil-img-uplo">
                                                        <span class="dumfil"><?php echo $BIZBOOK['SERVICE_NAME_IMAGE']; ?></span>
                                                        <input type="file" name="service_image[]" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                                    </div>
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
                                    <a href="add-listing-step-1">
                                        <button type="button"
                                                class="btn btn-primary"><?php echo $BIZBOOK['PREVIOUS']; ?></button>
                                    </a>
                                </div>
                                <div class="col-md-6">
                                    <button type="submit" name="listing_submit"
                                            class="btn btn-primary"><?php echo $BIZBOOK['NEXT']; ?></button>
                                </div>
                                <div class="col-md-12">
                                    <a href="add-listing-step-3" class="skip"><?php echo $BIZBOOK['SKIP_THIS']; ?>
                                        >></a>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--PROGRESSBAR START-->
                            <div class="progress biz-prog">
                                <div class="progress-bar bg-success progress-bar-striped progress-bar-animated" style="width:40%">40%</div>
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