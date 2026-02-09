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
                            <a href="add-listing-step-1" class="act">
                                <span><?php echo $BIZBOOK['STEP1']; ?></span>
                                <b><?php echo $BIZBOOK['BASIC_INFO']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="#!">
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
            <div class="login-main add-list">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['STEP1']; ?></span>
                <div class="log">
                    <div class="login">
                        <h4><?php echo $BIZBOOK['LISTING_DETAILS']; ?></h4>
                        <?php include "page_level_message.php"; ?>
                        <form action="add-listing-step-2.php" class="listing_form_1" id="listing_form_1"
                              name="listing_form_1" method="post" enctype="multipart/form-data">
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <input id="listing_name" name="listing_name" type="text" required="required"
                                               class="form-control" value="<?php echo $_SESSION['listing_name'] ?>"
                                               placeholder="<?php echo $BIZBOOK['LISTING_NAME_STAR']; ?>">
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <input type="text" name="listing_mobile" class="form-control"
                                               value="<?php echo $_SESSION['listing_mobile'] ?>"
                                               placeholder="<?php echo $BIZBOOK['PHONE_NUMBER']; ?>">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <input type="text" name="listing_email" class="form-control"
                                               value="<?php echo $_SESSION['listing_email'] ?>" 
                                               placeholder="<?php echo $BIZBOOK['EMAIL_ID']; ?>">
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <input type="text" name="listing_whatsapp" class="form-control"
                                               value="<?php echo $_SESSION['listing_whatsapp'] ?>"
                                               placeholder="<?php echo $BIZBOOK['WHATSAPP_PLACEHOLDER']; ?>">
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <input type="text" name="listing_website" class="form-control"
                                               value="<?php echo $_SESSION['listing_website'] ?>"
                                               placeholder="<?php echo $BIZBOOK['WEBSITE']; ?>">
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <input type="text" name="listing_address" class="form-control"
                                               value="<?php echo $_SESSION['listing_address'] ?>"
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
<!--                                               value="--><?php //echo $_SESSION['listing_lat'] ?><!--"-->
<!--                                               placeholder="--><?php //echo $BIZBOOK['LATITUDE_PLACEHOLDER']; ?><!--">-->
<!--                                    </div>-->
<!--                                </div>-->
<!--                                <div class="col-md-6">-->
<!--                                    <div class="form-group">-->
<!--                                        <input type="text" name="listing_lng" class="form-control"-->
<!--                                               value="--><?php //echo $_SESSION['listing_lng'] ?><!--" placeholder="--><?php //echo $BIZBOOK['LONGITUDE_PLACEHOLDER']; ?><!--">-->
<!--                                    </div>-->
<!--                                </div>-->
<!--                            </div>-->
                            <!--FILED END-->

                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <select onChange="getCities(this.value);" name="country_id" required="required" id="country_id"
                                                class="chosen-select form-control">
                                            <option value=""><?php echo $BIZBOOK['SELECT_YOUR_COUNTRY']; ?></option>
                                            <?php
                                            //Countries Query
                                            $admin_countries = $footer_row['admin_countries'];
                                            $catArray = explode(',', $admin_countries);
                                            foreach($catArray as $cat_Array) {

                                                foreach (getMultipleCountry($cat_Array) as $countries_row) {
                                                    ?>
                                                    <option <?php if ($_SESSION['country_id'] == $countries_row['country_id']) {
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
                            
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <select data-placeholder="<?php echo $BIZBOOK['SELECT_YOUR_CITY']; ?>" name="city_id[]" id="city_id" multiple required="required"
                                                class="chosen-select form-control">
                                            <option value=""><?php echo $BIZBOOK['SELECT_YOUR_CITY']; ?></option>

                                        </select>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
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
                                                <option <?php if ($_SESSION['category_id'] == $categories_row['category_id']) {
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
                                        <select data-placeholder="Select Sub Category" name="sub_category_id[]"
                                                id="sub_category_id" multiple class="chosen-select form-control">
                                            <option value=""><?php echo $BIZBOOK['SELECT_SUB_CATEGORY']; ?></option>
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
                                                  placeholder="<?php echo $BIZBOOK['DETAILS_ABOUT_LISTING']; ?>"><?php echo $_SESSION['listing_description'] ?></textarea>
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
                                                  placeholder="<?php echo $BIZBOOK['ENTER_SERVICE_LOCATION']; ?>"><?php echo $_SESSION['service_locations']; ?></textarea>
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <button type="submit" name="listing_submit" class="btn btn-primary"><?php echo $BIZBOOK['NEXT']; ?></button>
                            
                            <!--PROGRESSBAR START-->
                            <div class="progress biz-prog">
                                <div class="progress-bar bg-success progress-bar-striped progress-bar-animated" style="width:20%">20%</div>
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
<script src="js/select-opt.js"></script>
<script type="text/javascript">var webpage_full_link ='<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url ='<?php echo $LOGIN_URL;?>';</script>
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