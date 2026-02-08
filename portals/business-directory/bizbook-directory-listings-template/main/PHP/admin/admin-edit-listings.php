<?php
include "header.php";
?>

<?php if($footer_row['admin_listing_show'] != 1 || $admin_row['admin_listing_options'] != 1){
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="login-reg">
                <div class="container">
                    <?php
                    $listing_codea = $_GET['code'];
                    $listings_a_row = getListing($listing_codea);

                    ?>
                    <form action="update_listing.php" class="listing_form" id="listing_form"
                          name="listing_form" method="post" enctype="multipart/form-data">
                        
                        <input type="hidden" id="listing_codea" value="<?php echo $listing_codea; ?>"
                               name="listing_codea" class="validate">
                        <input type="hidden" id="listing_id" value="<?php echo $listings_a_row['listing_id']; ?>"
                               name="listing_id" class="validate">
                        <input type="hidden" id="listing_code" value="<?php echo $listings_a_row['listing_code']; ?>"
                               name="listing_code" class="validate">
                        <input type="hidden" id="profile_image_old"
                               value="<?php echo $listings_a_row['profile_image']; ?>" name="profile_image_old"
                               class="validate">
                        <input type="hidden" id="cover_image_old"
                               value="<?php echo $listings_a_row['cover_image']; ?>" name="cover_image_old"
                               class="validate">
                        <input type="hidden" id="gallery_image_old"
                               value="<?php echo $listings_a_row['gallery_image']; ?>" name="gallery_image_old"
                               class="validate">
                        <input type="hidden" id="service_image_old"
                               value="<?php echo $listings_a_row['service_image']; ?>" name="service_image_old"
                               class="validate">
                        <input type="hidden" id="service_1_image_old"
                               value="<?php echo $listings_a_row['service_1_image']; ?>" name="service_1_image_old"
                               class="validate">
                    <div class="row">
                        <div class="login-main add-list posr">
                            <div class="log-bor">&nbsp;</div>
                            <span class="udb-inst">step 1</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Edit Listing Details</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <select name="user_code" id="user_code" class="form-control"
                                                        required="required">
                                                    <option value="" disabled >User Name</option>
                                                    <?php
                                                    foreach (getAllUser() as $ad_users_row) {
                                                        ?>
                                                        <option <?php if ($listings_a_row['user_id'] == $ad_users_row['user_id']) {
                                                            echo "selected";
                                                        } ?>
                                                            value="<?php echo $ad_users_row['user_code']; ?>"><?php echo $ad_users_row['first_name']; ?></option>
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
                                                <input id="listing_name" name="listing_name" type="text" required="required"
                                                       value="<?php echo $listings_a_row['listing_name']; ?>"
                                                       class="form-control" placeholder="Listing name *">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input id="listing_mobile" name="listing_mobile" type="text"
                                                       value="<?php echo $listings_a_row['listing_mobile']; ?>" class="form-control" placeholder="Phone number">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input id="listing_email" name="listing_email" type="text"
                                                       value="<?php echo $listings_a_row['listing_email']; ?>" class="form-control" placeholder="Email id">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input id="listing_whatsapp" name="listing_whatsapp" type="text"
                                                       value="<?php echo $listings_a_row['listing_whatsapp']; ?>" class="form-control"
                                                       placeholder="Whatsapp Number">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input id="listing_website" name="listing_website" type="text"
                                                       value="<?php echo $listings_a_row['listing_website']; ?>" class="form-control"
                                                       placeholder="Webiste(www.rn53themes.net)">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" id="listing_address" name="listing_address" required="required"
                                                       value="<?php echo $listings_a_row['listing_address']; ?>"
                                                       class="form-control" placeholder="Shop address">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->

                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="listing_lat" class="form-control"
                                                       value="<?php echo $listings_a_row['listing_lat']; ?>"
                                                       placeholder="Latitude i.e 40.730610">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="listing_lng" class="form-control"
                                                       value="<?php echo $listings_a_row['listing_lng']; ?>"
                                                       placeholder="Longitude i.e -73.935242">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->

                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <select onChange="getCities(this.value);" name="country_id" required="required"
                                                        class="chosen-select form-control">
                                                    <option value="">Select your Country</option>
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
                                   
                                    <!--FILED END-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <select data-placeholder="Select your Cities" name="city_id[]" id="city_id"
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
                                                <select onChange="getSubCategory(this.value);" name="category_id" id="category_id" class="form-control">
                                                    <option value="">Select Category</option>
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
                                                <select name="sub_category_id[]" id="sub_category_id" multiple class="chosen-select form-control">
                                                    <?php
                                                    foreach (getCategorySubCategories($listings_a_row['category_id']) as $sub_categories_row) {
                                                        ?>
                                                        <option  <?php $catArray = explode(',', $listings_a_row['sub_category_id']);
                                                        foreach($catArray as $cat_Array){
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
                                                          name="listing_description" placeholder="Details about your listing"><?php echo $listings_a_row['listing_description']; ?></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <label>Choose profile image</label>
                                                <input type="file"  name="profile_image" class="form-control">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <label>Choose cover image</label>
                                                <input type="file"  name="cover_image" class="form-control">
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
                                                  placeholder="Enter your service locations... &#10;(i.e) London, Dallas, Wall Street, Opera House"><?php echo $listings_a_row['service_locations']; ?></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->


                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="login-main add-list add-list-ser">
                            <div class="log-bor">&nbsp;</div>
                            <span class="steps">Step 2</span>
                            <div class="log">
                                <div class="login">

                                    <h4>Services provide</h4>
                                    <span class="add-list-add-btn lis-ser-add-btn" title="add new offer">+</span>
                                    <span class="add-list-rem-btn lis-ser-rem-btn" title="remove offer">-</span>
                                    
                                        <ul>
                                            <?php
                                            $listings_a_row_service_id=$listings_a_row['service_id'];
                                            
                                            $serArray = explode(',', $listings_a_row_service_id);
                                            foreach($serArray as $service_Array){
                                                
                                             ?>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <label>Service name:</label>
                                                            <input type="text" name="service_id[]" value="<?php echo $service_Array; ?>" class="form-control"
                                                                   placeholder="Ex: Plumbile">
                                                        </div>
                                                    </div>
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <label>Choose profile image</label>
                                                            <input type="file" name="service_image[]" class="form-control">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                            </li>
                                            <?php
                                            }
                                            ?>

                                        </ul>

                                </div>
                            </div>
                        </div>

                    </div>
                    <div class="row">
                        <div class="login-main add-list">
                            <div class="log-bor">&nbsp;</div>
                            <span class="steps">Step 3</span>
                            <div class="log">
                                <div class="login add-list-off">
                                    <h4>Special offers</h4>
                                    <span class="add-list-add-btn lis-add-off" title="add new offer">+</span>
                                    <span class="add-list-rem-btn lis-add-rem" title="remove offer">-</span>
                                    
                                        <ul>
                                            <?php
                                            $listings_a_row_service_1_name = $listings_a_row['service_1_name'];
                                            $listings_a_row_service_1_price = $listings_a_row['service_1_price'];
                                            $listings_a_row_service_1_detail = $listings_a_row['service_1_detail'];
                                            $listings_a_row_service_1_view_more = $listings_a_row['service_1_view_more'];

                                            $ser_1_name_Array = explode('|', $listings_a_row_service_1_name);
                                            $ser_1_price_Array = explode(',', $listings_a_row_service_1_price);
                                            $ser_1_detail_Array = explode('|', $listings_a_row_service_1_detail);
                                            $ser_1_view_more_Array = explode(',', $listings_a_row_service_1_view_more);

                                            $zipped = array_map(null, $ser_1_name_Array, $ser_1_price_Array, $ser_1_detail_Array, $ser_1_view_more_Array);

                                            foreach($zipped as $tuple) {
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
                                                                <input type="text" class="form-control"
                                                                     value="<?php echo $tuple[0]; ?>"  name="service_1_name[]" placeholder="Offer name *">
                                                            </div>
                                                        </div>
                                                        <div class="col-md-6">
                                                            <div class="form-group">
                                                                <input type="text" class="form-control"
                                                                       value="<?php echo $tuple[1]; ?>" name="service_1_price[]" onkeypress="return isNumber(event)" placeholder="Price">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <!--FILED START-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                            <textarea class="form-control" name="service_1_detail[]"
                                                                       placeholder="Details about this offer"><?php echo $tuple[2]; ?></textarea>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <!--FILED START-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label>Choose offer image</label>
                                                                <input type="file" name="service_1_image[]" class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <!--FILED START-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <input type="text" class="form-control"
                                                                       value="<?php echo $tuple[3]; ?>" name="service_1_view_more[]"  placeholder="View More Link">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                </li>
                                                <?php
                                            }
                                            ?>
                                        </ul>
                                    
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="login-main add-list">
                            <div class="log-bor">&nbsp;</div>
                            <span class="steps">Step 4</span>
                            <div class="log add-list-map">
                                <div class="login add-list-map">
                                    <h4>Video Gallery</h4>
                                    <ul>
                                        <span class="add-list-add-btn lis-add-oadvideo" title="add new video">+</span>
                                        <span class="add-list-rem-btn lis-add-orevideo" title="remove video">-</span>
                                        <?php
                                        $listings_a_row_listing_video = $listings_a_row['listing_video'];

                                        $listings_a_row_listing_videoArray = explode('|', $listings_a_row_listing_video);

                                        foreach ($listings_a_row_listing_videoArray as $tuple) {
                                            ?>
                                            <li>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                        <textarea id="listing_video" name="listing_video[]"
                                                                  class="form-control"
                                                                  placeholder="Paste Your Youtube Url here"><?php echo $tuple; ?></textarea>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                            <?php
                                        }
                                        ?>

                                    </ul>
                                        <h4>Map and 360 view</h4>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <textarea class="form-control" name="google_map"
                                                              placeholder="Shop location"><?php echo $listings_a_row['google_map']; ?></textarea>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <textarea class="form-control" name="360_view" placeholder="360 view"><?php echo $listings_a_row['360_view']; ?></textarea>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->

                                        <h4 class="pt30">Photo gallery</h4>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <input type="file" name="gallery_image[]" class="form-control">
                                                </div>
                                            </div>
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <input type="file" name="gallery_image[]" class="form-control">
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <input type="file" name="gallery_image[]" class="form-control">
                                                </div>
                                            </div>
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <input type="file" name="gallery_image[]" class="form-control">
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <input type="file" name="gallery_image[]" class="form-control">
                                                </div>
                                            </div>
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <input type="file" name="gallery_image[]" class="form-control">
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                    
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="login-main add-list">
                            <div class="log-bor">&nbsp;</div>
                            <span class="steps">Step 5</span>
                            <div class="log">
                                <div class="login add-lis-oth">

                                    <h4>Other informations</h4>
                                    <span class="add-list-add-btn lis-add-oad" title="add new offer">+</span>
                                    <span class="add-list-rem-btn lis-add-ore" title="remove offer">-</span>
                                    
                                        <ul>
                                            <?php
                                            $listings_a_row_listing_info_question = $listings_a_row['listing_info_question'];
                                            $listings_a_row_listing_info_answer = $listings_a_row['listing_info_answer'];

                                            $listings_a_row_listing_info_question_Array = explode(',', $listings_a_row_listing_info_question);
                                            $listings_a_row_listing_info_answer_Array = explode(',', $listings_a_row_listing_info_answer);

                                            $zipped = array_map(null, $listings_a_row_listing_info_question_Array, $listings_a_row_listing_info_answer_Array);

                                            foreach($zipped as $tuple) {
                                                $tuple[0]; // Info question
                                                $tuple[1]; // Info Answer

                                                ?>
                                                <li>
                                                    <!--FILED START-->
                                                    <div class="row">
                                                        <div class="col-md-5">
                                                            <div class="form-group">
                                                                <input type="text" class="form-control"
                                                                       name="listing_info_question[]" value="<?php echo $tuple[0]; ?>"
                                                                       placeholder="Experience">
                                                            </div>
                                                        </div>
                                                        <div class="col-md-2">
                                                            <div class="form-group">
                                                                <i class="material-icons">arrow_forward</i>
                                                            </div>
                                                        </div>
                                                        <div class="col-md-5">
                                                            <div class="form-group">
                                                                <input type="text" class="form-control"
                                                                       name="listing_info_answer[]" value="<?php echo $tuple[1]; ?>"
                                                                       placeholder="20 years">
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

                                            <div class="col-md-12">
                                                <button type="submit" name="listing_submit" class="btn btn-primary">Update Listing</button>
                                            </div>
                                            <div class="col-md-12">
                                                <a href="profile.php" class="skip">Go to Dashboard >></a>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                   
                                </div>
                            </div>
                        </div>
                    </div>
                    </form>
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
<script src="../js/select-opt.js"></script>
<script src="js/admin-custom.js"></script>
<script>
    function getSubCategory(val) {
        $.ajax({
            type: "POST",
            url: "../sub_category_process.php",
            data: 'category_id=' + val,
            success: function (data) {
                $("#sub_category_id").html(data);
                $('#sub_category_id').trigger("chosen:updated");
            }
        });
    }
</script>

<script>
    function getCities(val) {
        $.ajax({
            type: "POST",
            url: "../city_process.php",
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