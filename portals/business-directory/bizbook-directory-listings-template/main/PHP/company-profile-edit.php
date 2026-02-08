<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

//To redirect the general type user to dashboard to avoid using this page And only Premium pls user can access this page

if ($user_details_row['user_type'] == "General" || $user_details_row['user_plan'] != 4) {
    header("Location: dashboard");
}

$user_id = $_SESSION['user_id'];

$company_row = getUserCompanyUser($user_id);

?>
<!-- START -->
<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg edit-comp-pro">
    <div class="container">
        <div class="row">
            <div class="login-main add-list">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['COMP-PRO']; ?></span>
                <div class="log">
                    <div class="login add-list-off comp-pro-edit">
                        <?php include "page_level_message.php"; ?>
                        <h4><?php echo $BIZBOOK['COMP-PRO-EDIT']; ?></h4>
                        <form action="company_profile_insert.php" class="company_profile_form" id="company_profile_form"
                              name="company_profile_form"
                              method="post" enctype="multipart/form-data">
                            <input type="hidden" id="company_profile_photo_old"
                                   value="<?php echo $company_row['company_profile_photo']; ?>"
                                   name="company_profile_photo_old"
                                   class="validate">
                            <input type="hidden" id="company_banner_photo_old"
                                   value="<?php echo $company_row['company_banner_photo']; ?>"
                                   name="company_banner_photo_old"
                                   class="validate">
                            <input type="hidden" id="company_header_photo_old"
                                   value="<?php echo $company_row['company_header_photo']; ?>"
                                   name="company_header_photo_old"
                                   class="validate">
                            <ul>
                                <li>
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <h6><?php echo $BIZBOOK['COMP-PRO-INFO']; ?></h6>
                                            <div class="form-group">
                                                <input type="text" name="company_name" id="company_name"
                                                       value="<?php echo $company_row['company_name']; ?>"
                                                       required="required" class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['COMP-PRO-NAME']; ?>">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" name="company_address"
                                                       value="<?php echo $company_row['company_address']; ?>"
                                                       id="company_address" required="required" class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['COMP-PRO-ADDRESS']; ?>">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="company_mobile" id="company_mobile"
                                                       value="<?php echo $company_row['company_mobile']; ?>"
                                                       required="required" class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['COMP-PRO-PHONE']; ?>">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="company_email_id" id="company_email_id"
                                                       value="<?php echo $company_row['company_email_id']; ?>"
                                                       required="required" class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['COMP-PRO-EMAIL']; ?>">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="company_website" id="company_website"
                                                       value="<?php echo $company_row['company_website']; ?>"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['COMP-PRO-WEBSITE']; ?>">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->

                                    <!--FILED START-->
                                    <h6><?php echo $BIZBOOK['COMP-PRO-TAX-DETAILS']; ?>:</h6>
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" name="company_tax" id="company_tax"
                                                       value="<?php echo $company_row['company_tax']; ?>"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['COMP-PRO-TAX-GST']; ?>">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->

                                    <!--FILED START-->
                                    <h6><?php echo $BIZBOOK['SOCIAL_MEDIA']; ?>:</h6>
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="company_facebook" id="company_facebook"
                                                       value="<?php echo $company_row['company_facebook']; ?>"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['COMP-PRO-FB']; ?>">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="company_twitter" id="company_twitter"
                                                       value="<?php echo $company_row['company_twitter']; ?>"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['COMP-PRO-TWITTER']; ?>">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="company_linkedin" id="company_linkedin"
                                                       value="<?php echo $company_row['company_linkedin']; ?>"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['COMP-PRO-LINKEDIN']; ?>">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="company_instagram" id="company_instagram"
                                                       value="<?php echo $company_row['company_instagram']; ?>"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['COMP-PRO-INSTAGRAM']; ?>">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="company_youtube" id="company_youtube"
                                                       value="<?php echo $company_row['company_youtube']; ?>"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['COMP-PRO-YOUTUBE']; ?>">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="company_whatsapp" id="company_whatsapp"
                                                       value="<?php echo $company_row['company_whatsapp']; ?>"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['COMP-PRO-WHAPP']; ?>">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->

                                    <!--FILED START-->
                                    <h6><?php echo $BIZBOOK['COMPANY-PROFILE-HEADING-LABEL']; ?>:</h6>
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea class="form-control" required="required"
                                                          name="company_description" id="company_description"
                                                          placeholder="<?php echo $BIZBOOK['PRODUCT_DETAILS']; ?>"><?php echo $company_row['company_description']; ?></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->

                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <label><?php echo $BIZBOOK['COMPANY-PROFILE-LOGO-LABEL']; ?>:</label>
                                            <div class="form-group">
                                                <div class="fil-img-uplo">
                                                    <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                                    <input type="file" name="comp-head-logo" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                                </div>
                                            </div>
                                        </div>

                                    </div>
                                    <div class="row">
                                        <div class="col-md-6">
                                            <label><?php echo $BIZBOOK['COMPANY-PROFILE-BANNER-LABEL']; ?>:</label>
                                            <div class="form-group">
                                                <div class="fil-img-uplo">
                                                    <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                                    <input type="file" name="comp-top-logo" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <label><?php echo $BIZBOOK['COMPANY-PROFILE-BACKGROUND-LABEL']; ?>:</label>
                                            <div class="form-group">
                                                <div class="fil-img-uplo">
                                                    <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                                    <input type="file" name="comp-bann-logo" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                                </div>
                                            </div>
                                        </div>

                                    </div>
                                    <!--FILED END-->

                                    <!--FILED START-->
                                    <h6><?php echo $BIZBOOK['COMPANY-PROFILE-CHOOSE-PRODUCTS']; ?>:</h6>
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <select data-placeholder="Select products" multiple="multiple"
                                                        name="company_products[]" id="company_products"
                                                        class="chosen-select form-control">
                                                    <option disabled
                                                            value=""><?php echo $BIZBOOK['COMP-PRO-CHOO-PROD']; ?></option>
                                                    <?php
                                                    foreach (getAllProductUser($user_id) as $product_row) {
                                                        ?>
                                                        <option <?php $catArray = explode(',', $company_row['company_products']);
                                                        foreach ($catArray as $cat_Array) {
                                                            if ($product_row['product_id'] == $cat_Array) {
                                                                echo "selected";
                                                            }
                                                        } ?>
                                                            value="<?php echo $product_row['product_id']; ?>"><?php echo $product_row['product_name']; ?></option>
                                                        <?php
                                                    }
                                                    ?>
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->

                                    <!--FILED START-->
                                    <h6><?php echo $BIZBOOK['COMPANY-PROFILE-CHOOSE-EVENTS']; ?>:</h6>
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <select data-placeholder="Select events" multiple="multiple"
                                                        name="company_events[]" id="company_events"
                                                        class="chosen-select form-control">
                                                    <option disabled
                                                            value=""><?php echo $BIZBOOK['COMP-PRO-CHOO-EVENTS']; ?></option>
                                                    <?php
                                                    foreach (getAllUserEvents($user_id) as $event_row) {
                                                        ?>
                                                        <option <?php $catArray = explode(',', $company_row['company_events']);
                                                        foreach ($catArray as $cat_Array) {
                                                            if ($event_row['event_id'] == $cat_Array) {
                                                                echo "selected";
                                                            }
                                                        } ?>
                                                            value="<?php echo $event_row['event_id']; ?>"><?php echo $event_row['event_name']; ?></option>
                                                        <?php
                                                    }
                                                    ?>
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->

                                    <!--FILED START-->
                                    <h6><?php echo $BIZBOOK['COMPANY-PROFILE-CHOOSE-BLOGS']; ?>:</h6>
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <select data-placeholder="Select blogs" multiple="multiple"
                                                        name="company_blogs[]" id="company_blogs"
                                                        class="chosen-select form-control">
                                                    <option disabled
                                                            value=""><?php echo $BIZBOOK['COMP-PRO-CHOO-BLOG']; ?></option>
                                                    <?php
                                                    foreach (getAllUserBlogs($user_id) as $blog_row) {
                                                        ?>
                                                        <option <?php $catArray = explode(',', $company_row['company_blogs']);
                                                        foreach ($catArray as $cat_Array) {
                                                            if ($blog_row['blog_id'] == $cat_Array) {
                                                                echo "selected";
                                                            }
                                                        } ?>
                                                            value="<?php echo $blog_row['blog_id']; ?>"><?php echo $blog_row['blog_name']; ?></option>
                                                        <?php
                                                    }
                                                    ?>
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->

                                    <!--FILED START-->
                                    <h6><?php echo $BIZBOOK['COMPANY-PROFILE-SEO-LABEL']; ?></h6>
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea class="form-control" name="company_seo_description"
                                                          id="company_seo_description"
                                                          placeholder="<?php echo $BIZBOOK['COMP-PRO-SEO-DESC']; ?>"><?php echo $company_row['company_seo_description']; ?></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea class="form-control" name="company_seo_keywords"
                                                          id="company_seo_keywords"
                                                          placeholder="<?php echo $BIZBOOK['COMP-PRO-SEO-KEYWORDS']; ?>"><?php echo $company_row['company_seo_keywords']; ?></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                </li>
                            </ul>
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <button type="submit" name="company_profile_submit"
                                            class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
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
<script src="admin/ckeditor/ckeditor.js"></script>
<script>
    CKEDITOR.replace('company_description');
</script>

</body>

</html>