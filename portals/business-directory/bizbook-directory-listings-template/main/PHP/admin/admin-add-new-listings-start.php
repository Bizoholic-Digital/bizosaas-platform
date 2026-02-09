<?php
include "header.php";
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="login-reg">
                <div class="container">
                    <form action="insert_listing.php" class="listing_form" id="listing_form"
                          name="listing_form" method="post" enctype="multipart/form-data">
                        <div class="row">
                            <div class="login-main add-list posr">
                                <div class="log-bor">&nbsp;</div>
                                <span class="udb-inst">step 1</span>
                                <div class="log log-1">
                                    <div class="login">
                                        <h4>Listing Details</h4>
                                        <?php include "../page_level_message.php"; ?>

                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <select name="user_code" id="user_code" class="form-control"
                                                            required="required">
                                                        <option value="" disabled selected>User Name</option>
                                                        <?php
                                                        foreach (getAllUser() as $ad_users_row) {
                                                            ?>
                                                            <option
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
                                                    <input id="listing_name" name="listing_name" type="text"
                                                           required="required" class="form-control"
                                                           placeholder="Listing name *">
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <input type="text" name="listing_mobile" class="form-control"
                                                           placeholder="Phone number">
                                                </div>
                                            </div>
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <input type="text" name="listing_email" class="form-control"
                                                           placeholder="Email id">
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <input type="text" name="listing_whatsapp" class="form-control"
                                                           placeholder="Whatsapp Number">
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <input type="text" name="listing_website" class="form-control"
                                                           placeholder="Webiste(www.rn53themes.net)">
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <input type="text" name="listing_address" required="required" class="form-control"
                                                           placeholder="Shop address">
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->

                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <input type="text" name="listing_lat" class="form-control"
                                                           placeholder="Latitude i.e 40.730610">
                                                </div>
                                            </div>
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <input type="text" name="listing_lng" class="form-control"
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
                                                            class="form-control">
                                                        <option value="">Select your Country</option>
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
                                                    <select data-placeholder="Select your Cities" name="city_id[]" id="city_id" multiple required="required"
                                                            class="chosen-select form-control">
                                                        <option value="">Select your Cities</option>

                                                    </select>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <select onChange="getSubCategory(this.value);" name="category_id" id="category_id" class="form-control">
                                                        <option value="">Select Category</option>
                                                        <?php
                                                        foreach (getAllCategories() as $categories_row) {
                                                            ?>
                                                            <option
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
                                                    <select  data-placeholder="Select Sub Category" name="sub_category_id[]" id="sub_category_id" multiple class="chosen-select form-control">
                                                        <option value="">Select Sub Category</option>
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
                                                              placeholder="Details about your listing"></textarea>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <label>Choose profile image</label>
                                                    <input type="file" name="profile_image" class="form-control">
                                                </div>
                                            </div>
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <label>Choose cover image</label>
                                                    <input type="file" name="cover_image" class="form-control">
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
                                                  placeholder="Enter your service locations... &#10;(i.e) London, Dallas, Wall Street, Opera House"></textarea>
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
                                                <li>
                                                    <!--FILED START-->
                                                    <div class="row">
                                                        <div class="col-md-6">
                                                            <div class="form-group">
                                                                <label>Service name:</label>
                                                                <input type="text" name="service_id[]"
                                                                       class="form-control"
                                                                       placeholder="Ex: Plumbile">
                                                            </div>
                                                        </div>
                                                        <div class="col-md-6">
                                                            <div class="form-group">
                                                                <label>Choose profile image</label>
                                                                <input type="file" name="service_image[]"
                                                                       class="form-control">
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
                                                                <label>Service name:</label>
                                                                <input type="text" name="service_id[]"
                                                                       class="form-control"
                                                                       placeholder="Ex: bike service">
                                                            </div>
                                                        </div>
                                                        <div class="col-md-6">
                                                            <div class="form-group">
                                                                <label>Choose profile image</label>
                                                                <input type="file" name="service_image[]"
                                                                       class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                </li>
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
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <input type="text" name="service_1_name[]"
                                                                   class="form-control"
                                                                   placeholder="Offer name *">
                                                        </div>
                                                    </div>
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <input type="text" name="service_1_price[]"
                                                                   class="form-control" onkeypress="return isNumber(event)"
                                                                   placeholder="Price">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                        <textarea class="form-control" name="service_1_detail[]"
                                                                  placeholder="Details about this offer"></textarea>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label>Choose offer image</label>
                                                            <input type="file" name="service_1_image[]"
                                                                   class="form-control">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" name="service_1_view_more[]"
                                                                   class="form-control"  placeholder="View More Link">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                            </li>
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
                                                <li>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                 <textarea id="listing_video" name="listing_video[]"
                                                           class="form-control"
                                                           placeholder="Paste Your Youtube Url here"></textarea>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </li>
                                        </ul>
                                        <h4>Map and 360 view</h4>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                <textarea class="form-control" name="google_map"
                                                          placeholder="Shop location"></textarea>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                <textarea class="form-control" name="360_view"
                                                          placeholder="360 view"></textarea>
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
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-5">
                                                        <div class="form-group">
                                                            <input type="text" name="listing_info_question[]"
                                                                   class="form-control" placeholder="Experience">
                                                        </div>
                                                    </div>
                                                    <div class="col-md-2">
                                                        <div class="form-group">
                                                            <i class="material-icons">arrow_forward</i>
                                                        </div>
                                                    </div>
                                                    <div class="col-md-5">
                                                        <div class="form-group">
                                                            <input type="text" name="listing_info_answer[]"
                                                                   class="form-control" placeholder="20 years">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                            </li>
                                            <!--FILED START-->
                                            <li>
                                                <div class="row">
                                                    <div class="col-md-5">
                                                        <div class="form-group">
                                                            <input type="text" name="listing_info_question[]"
                                                                   class="form-control" placeholder="Parking">
                                                        </div>
                                                    </div>
                                                    <div class="col-md-2">
                                                        <div class="form-group">
                                                            <i class="material-icons">arrow_forward</i>
                                                        </div>
                                                    </div>
                                                    <div class="col-md-5">
                                                        <div class="form-group">
                                                            <input type="text" name="listing_info_answer[]"
                                                                   class="form-control" placeholder="yes">
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                            <!--FILED END-->
                                            <!--FILED START-->
                                            <li>
                                                <div class="row">
                                                    <div class="col-md-5">
                                                        <div class="form-group">
                                                            <input type="text" name="listing_info_question[]"
                                                                   class="form-control" placeholder="Smoking">
                                                        </div>
                                                    </div>
                                                    <div class="col-md-2">
                                                        <div class="form-group">
                                                            <i class="material-icons">arrow_forward</i>
                                                        </div>
                                                    </div>
                                                    <div class="col-md-5">
                                                        <div class="form-group">
                                                            <input type="text" name="listing_info_answer[]"
                                                                   class="form-control" placeholder="yes">
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                            <!--FILED END-->
                                            <!--FILED START-->
                                            <li>
                                                <div class="row">
                                                    <div class="col-md-5">
                                                        <div class="form-group">
                                                            <input type="text" name="listing_info_question[]"
                                                                   class="form-control" placeholder="Take Out">
                                                        </div>
                                                    </div>
                                                    <div class="col-md-2">
                                                        <div class="form-group">
                                                            <i class="material-icons">arrow_forward</i>
                                                        </div>
                                                    </div>
                                                    <div class="col-md-5">
                                                        <div class="form-group">
                                                            <input type="text" name="listing_info_answer[]"
                                                                   class="form-control" placeholder="yes">
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                            <!--FILED END-->

                                        </ul>
                                        <!--FILED START-->
                                        <div class="row">
                                            <!--                                        <div class="col-md-6">-->
                                            <!--                                            <button type="submit" class="btn btn-primary">Previous</button>-->
                                            <!--                                        </div>-->
                                            <div class="col-md-12">
                                                <button type="submit" name="listing_submit" class="btn btn-primary">
                                                    Submit
                                                    Listing
                                                </button>
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
<script src="ckeditor/ckeditor.js"></script>
<script>
    CKEDITOR.replace('listing_description');
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