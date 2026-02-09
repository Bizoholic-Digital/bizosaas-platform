<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

if (file_exists('config/general_user_authentication.php')) {
    include('config/general_user_authentication.php');
}

if (file_exists('config/product_page_authentication.php')) {
    include('config/product_page_authentication.php');
}
//To check the Product count with current plan starts

$plan_type_product_count = $user_plan_type['plan_type_product_count'];
$product_count_user = getCountUserProduct($_SESSION['user_id']);

if($product_count_user >= $plan_type_product_count){

    $_SESSION['status_msg'] = $BIZBOOK['PRODUCTS_LIMIT_EXCEED_MESSAGE'];

    header('Location: db-products');
    exit();
}
//To check the Product count with current plan ends

?>
<!-- START -->
<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg">
    <div class="container">
        <div class="row">
            <div class="login-main add-list">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['NEW_PRODUCT']; ?></span>
                <div class="log">
                    <div class="login add-list-off add-pro-fie">
                        <?php include "page_level_message.php"; ?>
                        <h4><?php echo $BIZBOOK['ADD_NEW_PRODUCT']; ?></h4>
                        <form action="product_insert.php" class="product_form" id="product_form" name="product_form"
                              method="post" enctype="multipart/form-data">
                            <ul>
                                <li>
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" name="product_name" id="product_name"
                                                       required="required" class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['PRODUCT_NAME_STAR']; ?>">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <select onChange="getProductSubCategory(this.value);" name="category_id"
                                                        id="category_id" class="chosen-select form-control">
                                                    <option value=""><?php echo $BIZBOOK['SELECT_CATEGORY']; ?></option>
                                                    <?php
                                                    foreach (getAllProductCategories() as $categories_row) {
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
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="product_price" id="product_price" onkeypress="return isNumber(event)"
                                                       required="required" class="form-control" placeholder="<?php echo $BIZBOOK['PRICE']; ?>*">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="product_price_offer" id="product_price_offer" onkeypress="return isNumber(event)"
                                                       class="form-control" placeholder="<?php echo $BIZBOOK['PRODUCT_OFFER']; ?>">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" class="form-control"
                                                       name="product_payment_link"
                                                       id="product_payment_link"
                                                       placeholder="<?php echo $BIZBOOK['PRODUCT_PAYMENT_LINK']; ?>" required>
                                                <!-- INPUT TOOL TIP -->
                                                <div class="inp-ttip">
                                                    <b><?php echo $BIZBOOK['PRODUCT_PAYMENT_LINK_P_TAG']; ?></b>
                                                    <?php echo $BIZBOOK['PRODUCT_PAYMENT_LINK_INFO']; ?>
                                                </div>
                                                <!-- END INPUT TOOL TIP -->
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea class="form-control" required="required"  name="product_description" id="product_description" placeholder="<?php echo $BIZBOOK['PRODUCT_DETAILS']; ?>"></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <label><?php echo $BIZBOOK['PRODUCT_IMAGE_LABEL']; ?></label>
                                                <div class="fil-img-uplo">
                                                    <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                                    <input type="file" name="gallery_image[]" accept="image/*,.jpg,.jpeg,.png" class="form-control" multiple>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="log">
                                                <div class="login add-prod-high-oth">

                                                    <h4><?php echo $BIZBOOK['HIGHLIGHTS']; ?></h4>
                                                    <span class="add-list-add-btn prod-add-high-oad"
                                                          title="add new offer">+</span>
                                                    <span class="add-list-rem-btn prod-add-high-ore"
                                                          title="remove offer">-</span>
                                                    <ul>
                                                        <li>
                                                            <!--FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-12">
                                                                    <div class="form-group">
                                                                        <input type="text"
                                                                               name="product_highlights[]"
                                                                               class="form-control"
                                                                               placeholder="<?php echo $BIZBOOK['HIGHLIGHTS_PLACEHOLDER']; ?>">
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
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="log">
                                                <div class="login add-prod-oth">

                                                    <h4><?php echo $BIZBOOK['SPECIFICATIONS']; ?></h4>
                                                    <span class="add-list-add-btn prod-add-oad"
                                                          title="add new offer">+</span>
                                                    <span class="add-list-rem-btn prod-add-ore"
                                                          title="remove offer">-</span>
                                                    <ul>
                                                        <li>
                                                            <!--FILED START-->
                                                            <div class="row">
                                                                <div class="col-md-5">
                                                                    <div class="form-group">
                                                                        <input type="text"
                                                                               name="product_info_question[]"
                                                                               class="form-control"
                                                                               placeholder="<?php echo $BIZBOOK['SPECIFICATIONS_QUESTION']; ?>">
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-2">
                                                                    <div class="form-group">
                                                                        <i class="material-icons">arrow_forward</i>
                                                                    </div>
                                                                </div>
                                                                <div class="col-md-5">
                                                                    <div class="form-group">
                                                                        <input type="text" name="product_info_answer[]"
                                                                               class="form-control"
                                                                               placeholder="<?php echo $BIZBOOK['SPECIFICATIONS_ANSWER']; ?>">
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
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                               <textarea class="form-control"
                                                         name="product_tags"
                                                         id="product_tags"
                                                         placeholder="<?php echo $BIZBOOK['PRODUCT_TAGS_PLACEHOLDER']; ?>"></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                </li>
                            </ul>
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <button type="submit" name="product_submit" class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
                                </div>
                                <div class="col-md-12">
                                    <a href="dashboard" class="skip"><?php echo $BIZBOOK['GO_TO_USER_DASHBOARD']; ?> >></a>
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
<script type="text/javascript">var webpage_full_link ='<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url ='<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>
<script src="admin/ckeditor/ckeditor.js"></script>
<script>
    CKEDITOR.replace('product_description');
</script>
<script>
    function getProductSubCategory(val) {
        $.ajax({
            type: "POST",
            url: "product_sub_category_process.php",
            data: 'category_id=' + val,
            success: function (data) {
                $("#sub_category_id").html(data);
                $('#sub_category_id').trigger("chosen:updated");
            }
        });
    }
</script>
</body>

</html>