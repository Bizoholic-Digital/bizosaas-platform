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
                    <form <?php
                          if(isset($_GET['path'])){
                              if($_GET['path']=="restore"){
                                  echo "action=\"delete_listing.php\"";
                              }elseif($_GET['path']=="trash"){
                                  echo "action=\"trash_listing.php\"";
                              }

                          }else{
                              echo "action=\"delete_listing.php\"";
                          }
                          ?> class="listing_form" id="listing_form"
                          name="listing_form" method="post" enctype="multipart/form-data">

                        <input type="hidden" id="listing_codea" value="<?php echo $listing_codea; ?>"
                               name="listing_codea" class="validate">
                        <input type="hidden" id="listing_id" value="<?php echo $listings_a_row['listing_id']; ?>"
                               name="listing_id" class="validate">
                        <input type="hidden" id="listing_code" value="<?php echo $listings_a_row['listing_code']; ?>"
                               name="listing_code" class="validate">
                        <input type="hidden" id="listing_is_delete" value="<?php echo $listings_a_row['listing_is_delete']; ?>"
                               name="listing_is_delete" class="validate">
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
                                        <h4><?php
                                            if(isset($_GET['path'])){
                                                if($_GET['path']=="restore"){
                                                    echo "Restore";
                                                }elseif($_GET['path']=="trash"){
                                                    echo "Delete Permanently";
                                                }

                                            }else{
                                                echo "Delete";
                                            }
                                            ?> Listing Details</h4>
                                        <?php include "../page_level_message.php"; ?>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <select disabled="disabled" name="user_code" id="user_code" class="form-control"
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
                                                    <input readonly="readonly" id="listing_name" name="listing_name" type="text" required="required"
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
                                                    <input readonly="readonly" id="listing_mobile" name="listing_mobile" type="text"
                                                           value="<?php echo $listings_a_row['listing_mobile']; ?>" class="form-control" placeholder="Phone number">
                                                </div>
                                            </div>
                                            <div class="col-md-6">
                                                <div class="form-group">
                                                    <input readonly="readonly" id="listing_email" name="listing_email" type="text"
                                                           value="<?php echo $listings_a_row['listing_email']; ?>" class="form-control" placeholder="Email id">
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <input readonly="readonly" id="listing_website" name="listing_website" type="text"
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
                                                    <input readonly="readonly" type="text" id="listing_address" name="listing_address" required="required"
                                                           value="<?php echo $listings_a_row['listing_address']; ?>"
                                                           class="form-control" placeholder="Shop address">
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->

                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <select disabled="disabled" name="country_id" required="required" class="form-control">
                                                        <option value="">Select your Country</option>
                                                        <?php
                                                        //Countries Query

                                                        foreach (getAllCountries() as $countries_row) {
                                                            ?>
                                                            <option <?php if ($listings_a_row['country_id'] == $countries_row['country_id']) {
                                                                echo "selected";
                                                            } ?> value="<?php echo $countries_row['country_id']; ?>"><?php echo $countries_row['country_name']; ?></option>
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
                                                    <input readonly="readonly" id="select-city" name="city_id" value="<?php echo $cities_row['city_name']; ?>"
                                                           required="required" type="text" class="form-control" placeholder="City name">
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <select disabled="disabled" name="category_id" id="category_id" class="form-control">
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
                                                    <select disabled="disabled" name="sub_category_id" id="sub_category_id"
                                                            class="form-control">
                                                        <option value="">Select Sub Category</option>
                                                        <?php
                                                        foreach (getAllSubCategories() as $sub_categories_row) {
                                                            ?>
                                                            <option <?php if ($listings_a_row['sub_category_id'] == $sub_categories_row['sub_category_id']) {
                                                                echo "selected";
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
                                                <textarea readonly="readonly" class="form-control" id="listing_description"
                                                          name="listing_description" placeholder="Details about your listing"><?php echo $listings_a_row['listing_description']; ?></textarea>
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
                                                                <input type="text" readonly="readonly" name="service_id[]" value="<?php echo $service_Array; ?>" class="form-control"
                                                                       placeholder="Ex: Plumbile">
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

                                        <ul>
                                            <?php
                                            $listings_a_row_service_1_name=$listings_a_row['service_1_name'];
                                            $listings_a_row_service_1_price=$listings_a_row['service_1_price'];
                                            $listings_a_row_service_1_detail=$listings_a_row['service_1_detail'];

                                            $ser_1_name_Array = explode(',', $listings_a_row_service_1_name);
                                            $ser_1_price_Array = explode(',', $listings_a_row_service_1_price);
                                            $ser_1_detail_Array = explode(',', $listings_a_row_service_1_detail);

                                            $zipped = array_map(null, $ser_1_name_Array, $ser_1_price_Array, $ser_1_detail_Array);

                                            foreach($zipped as $tuple) {
                                                $tuple[0]; // offer name
                                                $tuple[1]; // offer Price
                                                $tuple[2]; // offer Detail

                                                ?>
                                                <li>
                                                    <!--FILED START-->
                                                    <div class="row">
                                                        <div class="col-md-6">
                                                            <div class="form-group">
                                                                <input readonly="readonly" type="text" class="form-control"
                                                                       value="<?php echo $tuple[0]; ?>"  name="service_1_name[]" placeholder="Offer name *">
                                                            </div>
                                                        </div>
                                                        <div class="col-md-6">
                                                            <div class="form-group">
                                                                <input readonly="readonly" type="text" class="form-control"
                                                                       value="<?php echo $tuple[1]; ?>" name="service_1_price[]" placeholder="Price">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <!--FILED START-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                            <textarea readonly="readonly" class="form-control" name="service_1_detail[]"
                                                                      placeholder="Details about this offer"><?php echo $tuple[2]; ?></textarea>
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

                                        <h4>Map and 360 view</h4>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <textarea readonly="readonly" class="form-control" name="google_map"
                                                              placeholder="Shop location"><?php echo $listings_a_row['google_map']; ?></textarea>
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <textarea readonly="readonly" class="form-control" name="360_view" placeholder="360 view"><?php echo $listings_a_row['360_view']; ?></textarea>
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
                                                                <input readonly="readonly" type="text" class="form-control"
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
                                                                <input readonly="readonly" type="text" class="form-control"
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
                                                <button type="submit" name="listing_submit" class="btn btn-primary"><?php
                                                    if(isset($_GET['path'])){
                                                        if($_GET['path']=="restore"){
                                                            echo "Restore";
                                                        }elseif($_GET['path']=="trash"){
                                                            echo "Delete Permanently";
                                                        }

                                                    }else{
                                                        echo "Delete";
                                                    }
                                                    ?> Listing</button>
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
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>