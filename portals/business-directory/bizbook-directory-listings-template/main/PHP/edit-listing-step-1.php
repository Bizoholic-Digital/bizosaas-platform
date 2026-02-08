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

if ($_GET['row'] == NULL && empty($_GET['row'])) {

    header("Location: db-all-listing");
}

if (!isset($_SESSION['listing_codea']) || empty($_SESSION['listing_codea'])) {
    $listing_codea = $_GET['row'];
} else {
    $listing_codea = $_SESSION['listing_codea'];
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
                            <a href="edit-listing-step-1?row=<?php echo $listing_codea; ?>" class="act">
                                <span><?php echo $BIZBOOK['STEP1']; ?></span>
                                <b><?php echo $BIZBOOK['BASIC_INFO']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="edit-listing-step-2?row=<?php echo $listing_codea; ?>">
                                <span><?php echo $BIZBOOK['STEP2']; ?></span>
                                <b><?php echo $BIZBOOK['SERVICES']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="edit-listing-step-3?row=<?php echo $listing_codea; ?>">
                                <span><?php echo $BIZBOOK['STEP3']; ?></span>
                                <b><?php echo $BIZBOOK['OFFERS']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="edit-listing-step-4?row=<?php echo $listing_codea; ?>">
                                <span><?php echo $BIZBOOK['STEP4']; ?></span>
                                <b><?php echo $BIZBOOK['MAP']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="edit-listing-step-5?row=<?php echo $listing_codea; ?>">
                                <span><?php echo $BIZBOOK['STEP5']; ?></span>
                                <b><?php echo $BIZBOOK['OTHER']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="edit-listing-step-6?row=<?php echo $listing_codea; ?>">
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
                <span class="steps"><?php echo $BIZBOOK['STEP1']; ?></span>
                <div class="log">
                    <div class="login">
                        <h4><?php echo $BIZBOOK['LISTING_DETAILS']; ?></h4>
                        <?php include "page_level_message.php"; ?>
                        <?php
                        $listing_codea = $_GET['row'];
                        $listings_a_row = getListing($listing_codea);

                        ?>
                        <form action="listing_update.php" id="listing_form_1"
                              name="listing_form_1" method="post" enctype="multipart/form-data">

                            <input type="hidden" id="src_path" value="edit-1"
                                   name="src_path" class="validate">
                            <input type="hidden" id="listing_codea" value="<?php echo $listing_codea; ?>"
                                   name="listing_codea" class="validate">
                            <input type="hidden" id="listing_id" value="<?php echo $listings_a_row['listing_id']; ?>"
                                   name="listing_id" class="validate">
                            <input type="hidden" id="listing_code"
                                   value="<?php echo $listings_a_row['listing_code']; ?>"
                                   name="listing_code" class="validate">
                            <input type="hidden" id="profile_image_old"
                                   value="<?php echo $listings_a_row['profile_image']; ?>" name="profile_image_old"
                                   class="validate">
                            <input type="hidden" id="cover_image_old"
                                   value="<?php echo $listings_a_row['cover_image']; ?>" name="cover_image_old"
                                   class="validate">

                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <input id="listing_name" name="listing_name" type="text" required="required"
                                               value="<?php echo $listings_a_row['listing_name']; ?>"
                                               class="form-control"
                                               placeholder="<?php echo $BIZBOOK['LISTING_NAME_STAR']; ?>">
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <input id="listing_mobile" name="listing_mobile" type="text"
                                               value="<?php echo $listings_a_row['listing_mobile']; ?>"
                                               class="form-control"
                                               placeholder="<?php echo $BIZBOOK['PHONE_NUMBER']; ?>">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <input id="listing_email" name="listing_email" type="text"
                                               value="<?php echo $listings_a_row['listing_email']; ?>"
                                               class="form-control" placeholder="<?php echo $BIZBOOK['EMAIL_ID']; ?>">
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <input id="listing_whatsapp" name="listing_whatsapp" type="text"
                                               value="<?php echo $listings_a_row['listing_whatsapp']; ?>"
                                               class="form-control"
                                               placeholder="<?php echo "Whatsapp Number (e.g. +919876543210)"; ?>">
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <input id="listing_website" name="listing_website" type="text"
                                               value="<?php echo $listings_a_row['listing_website']; ?>"
                                               class="form-control"
                                               placeholder="<?php echo $BIZBOOK['WEBSITE']; ?>">
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <input type="text" id="listing_address" name="listing_address"
                                               required="required"
                                               value="<?php echo $listings_a_row['listing_address']; ?>"
                                               class="form-control"
                                               placeholder="<?php echo $BIZBOOK['SHOP_ADDRESS']; ?>">
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
<!--                            <div class="row">-->
<!--                                <div class="col-md-6">-->
<!--                                    <div class="form-group">-->
<!--                                        <input type="text" name="listing_lat" class="form-control"-->
<!--                                               value="--><?php //echo $listings_a_row['listing_lat'] ?><!--"-->
<!--                                               placeholder="--><?php //echo $BIZBOOK['LATITUDE_PLACEHOLDER']; ?><!--">-->
<!--                                    </div>-->
<!--                                </div>-->
<!--                                <div class="col-md-6">-->
<!--                                    <div class="form-group">-->
<!--                                        <input type="text" name="listing_lng" class="form-control"-->
<!--                                               value="--><?php //echo $listings_a_row['listing_lng'] ?><!--"-->
<!--                                               placeholder="--><?php //echo $BIZBOOK['LONGITUDE_PLACEHOLDER']; ?><!--">-->
<!--                                    </div>-->
<!--                                </div>-->
<!--                            </div>-->
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <select onChange="getCities(this.value);" name="country_id" required="required"
                                                class="chosen-select form-control">
                                            <option value=""><?php echo $BIZBOOK['SELECT_YOUR_COUNTRY']; ?></option>
                                            <?php
                                            //Countries Query
                                            $admin_countries = $footer_row['admin_countries'];
                                            $catArray = explode(',', $admin_countries);
                                            foreach ($catArray as $cat_Array) {

                                                foreach (getMultipleCountry($cat_Array) as $countries_row) {
                                                    ?>
                                                    <option <?php if ($listings_a_row['country_id'] == $countries_row['country_id']) {
                                                        echo "selected";
                                                    } ?>
                                                        value="<?php echo $countries_row['country_id']; ?>"><?php echo $countries_row['country_name']; ?></option>
                                                    <?php
                                                }
                                            }
                                            ?>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <select data-placeholder="<?php echo $BIZBOOK['SELECT_YOUR_CITY']; ?>"
                                                name="city_id[]" id="city_id"
                                                multiple required="required"
                                                class="chosen-select form-control">
                                            <?php
                                            $cityArray = explode(',', $listings_a_row['city_id']);
                                            foreach ($cityArray as $cit_Array) {
                                                ?>
                                                <option <?php
                                                echo "selected";

                                                $city_row = getCity($cit_Array);

                                                ?>
                                                    value="<?php echo $city_row['city_id']; ?>"><?php echo $city_row['city_name']; ?></option>
                                                <?php
                                            }
                                            ?>

                                        </select>
                                    </div>
                                </div>
                            </div>
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <select onChange="getSubCategory(this.value);" name="category_id"
                                                id="category_id" class="chosen-select form-control">
                                            <option value=""><?php echo $BIZBOOK['SELECT_CATEGORY']; ?></option>
                                            <?php
                                            foreach (getAllCategories() as $categories_row) {
                                                ?>
                                                <option <?php if ($listings_a_row['category_id'] == $categories_row['category_id']) {
                                                    echo "selected";
                                                } ?>
                                                    value="<?php echo $categories_row['category_id']; ?>"><?php echo $categories_row['category_name']; ?></option>
                                                <?php
                                            }
                                            ?>
                                        </select>

                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <select name="sub_category_id[]" id="sub_category_id" multiple
                                                class="chosen-select form-control">
                                           
                                            <?php
                                            foreach (getCategorySubCategories($listings_a_row['category_id']) as $sub_categories_row) {
                                                ?>
                                                <option <?php $catArray = explode(',', $listings_a_row['sub_category_id']);
                                                foreach ($catArray as $cat_Array) {
                                                    if ($sub_categories_row['sub_category_id'] == $cat_Array) {
                                                        echo "selected";

                                                    }

                                                } ?>
                                                    value="<?php echo $sub_categories_row['sub_category_id']; ?>"><?php echo $sub_categories_row['sub_category_name']; ?></option>
                                                <?php
                                            }
                                            ?>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                                <textarea class="form-control" id="listing_description"
                                                          name="listing_description"
                                                          placeholder="<?php echo $BIZBOOK['DETAILS_ABOUT_LISTING']; ?>"><?php echo $listings_a_row['listing_description']; ?></textarea>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label><?php echo $BIZBOOK['CHOOSE_PROFILE_IMAGE']; ?></label>
                                        <div class="fil-img-uplo">
                                            <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                            <input type="file" name="profile_image" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label><?php echo $BIZBOOK['CHOOSE_COVER_IMAGE']; ?></label>
                                        <div class="fil-img-uplo">
                                            <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                            <input type="file" name="cover_image" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <textarea class="form-control" id="service_locations"
                                                  name="service_locations"
                                                  placeholder="<?php echo $BIZBOOK['ENTER_SERVICE_LOCATION']; ?>"><?php echo $listings_a_row['service_locations']; ?></textarea>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <button name="listing_submit" type="submit"
                                            class="btn btn-primary"><?php echo $BIZBOOK['SAVE_AND_EXIT']; ?></button>
                                </div>
                                <div class="col-md-12">
                                    <a href="edit-listing-step-2?row=<?php echo $_GET['row']; ?>"
                                       class="skip"><?php echo $BIZBOOK['SKIP_THIS']; ?>>></a>
                                </div>
                                <div class="col-md-12">
                                    <a href="dashboard" class="skip"><?php echo $BIZBOOK['GO_TO_USER_DASHBOARD']; ?>
                                        >></a>
                                </div>
                            </div>
                            <!--FILED END-->
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
<script src="js/select-opt.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>
<script>
    function getSubCategory(val) {
        $.ajax({
            type: "POST",
            url: "sub_category_process.php",
            data: 'category_id=' + val,
            success: function (data) {
                $("#sub_category_id").html(data);
                $('#sub_category_id').trigger("chosen:updated");
            }
        });
    }
</script>
<script src="admin/ckeditor/ckeditor.js"></script>
<script>
    CKEDITOR.replace('listing_description');
</script>
<script>
    function getCities(val) {
        $.ajax({
            type: "POST",
            url: "city_process.php",
            data: 'country_id=' + val,
            success: function (data) {
                $("#city_id").html(data);
                $('#city_id').trigger("chosen:updated");
            }
        });
    }
</script>
</body>

</html>