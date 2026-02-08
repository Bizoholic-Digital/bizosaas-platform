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
                <span class="steps"><?php echo $BIZBOOK['DELETE_PRODUCT']; ?></span>
                <div class="log">
                    <div class="login add-list-off">
                        <?php
                        $product_codea = $_GET['code'];
                        $products_a_row = getProduct($product_codea);

                        ?>

                        <h4><?php echo $BIZBOOK['DELETE_THIS_PRODUCT']; ?></h4>
                        <?php include "page_level_message.php"; ?>
                        <form action="product_trash.php" class="product_form" id="product_form" name="product_form"
                              method="post" enctype="multipart/form-data">
                            <input type="hidden" id="product_id" value="<?php echo $products_a_row['product_id']; ?>"
                                   name="product_id" class="validate">
                            <input type="hidden" id="product_code"
                                   value="<?php echo $products_a_row['product_code']; ?>"
                                   name="product_code" class="validate">
                            <input type="hidden" id="gallery_image_old"
                                   value="<?php echo $products_a_row['gallery_image']; ?>" name="gallery_image_old"
                                   class="validate">
                            <ul>
                                <li>
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" readonly="readonly" name="product_name"
                                                       id="product_name"
                                                       required="required" class="form-control"
                                                       value="<?php echo $products_a_row['product_name']; ?>"
                                                       placeholder="<?php echo $BIZBOOK['PRODUCT_NAME_STAR']; ?>">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <select disabled="disabled"
                                                        onChange="getProductSubCategory(this.value);" name="category_id"
                                                        id="category_id" class="chosen-select form-control">
                                                    <option value=""><?php echo $BIZBOOK['SELECT_CATEGORY']; ?></option>
                                                    <?php
                                                    foreach (getAllProductCategories() as $categories_row) {
                                                        ?>
                                                        <option <?php if ($products_a_row['category_id'] == $categories_row['category_id']) {
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
                                                <select disabled="disabled" name="sub_category_id[]"
                                                        id="sub_category_id" multiple
                                                        class="chosen-select form-control">

                                                    <?php
                                                    foreach (getCategoryProductSubCategories($products_a_row['category_id']) as $sub_categories_row) {
                                                        ?>
                                                        <option <?php $catArray = explode(',', $products_a_row['sub_category_id']);
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
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" readonly="readonly" name="product_price"
                                                       id="product_price"
                                                       value="<?php echo $products_a_row['product_price']; ?>"
                                                       required="required" class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['PRICE']; ?>*">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" readonly="readonly" name="product_price_offer"
                                                       id="product_price_offer"
                                                       value="<?php echo $products_a_row['product_price_offer']; ?>"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['PRODUCT_OFFER']; ?>">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                               <textarea class="form-control" readonly="readonly"
                                                         name="product_payment_link"
                                                         id="product_payment_link"
                                                         placeholder="<?php echo $BIZBOOK['PRODUCT_PAYMENT_LINK']; ?>"><?php echo $products_a_row['product_payment_link']; ?></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea class="form-control" required="required" readonly="readonly"
                                                          name="product_description" id="product_description"
                                                          placeholder="<?php echo $BIZBOOK['PRODUCT_DETAILS']; ?>"><?php echo $products_a_row['product_description']; ?></textarea>
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
                                                    <ul>
                                                        <?php
                                                        $products_a_row_product_highlights = $products_a_row['product_highlights'];

                                                        $products_a_row_product_highlights_Array = explode(',', $products_a_row_product_highlights);

                                                        foreach ($products_a_row_product_highlights_Array as $tuple) {

                                                            ?>

                                                            <li>
                                                                <!--FILED START-->
                                                                <div class="row">
                                                                    <div class="col-md-12">
                                                                        <div class="form-group">
                                                                            <input type="text" readonly="readonly"
                                                                                   name="product_highlights[]"
                                                                                   value="<?php echo $tuple; ?>"
                                                                                   class="form-control"
                                                                                   placeholder="<?php echo $BIZBOOK['HIGHLIGHTS_PLACEHOLDER']; ?>">
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
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="log">
                                                <div class="login add-prod-oth">

                                                    <h4><?php echo $BIZBOOK['SPECIFICATIONS']; ?></h4>
                                                    <ul>
                                                        <?php
                                                        $products_a_row_product_info_question = $products_a_row['product_info_question'];
                                                        $products_a_row_product_info_answer = $products_a_row['product_info_answer'];

                                                        $products_a_row_product_info_question_Array = explode(',', $products_a_row_product_info_question);
                                                        $products_a_row_product_info_answer_Array = explode(',', $products_a_row_product_info_answer);

                                                        $zipped = array_map(null, $products_a_row_product_info_question_Array, $products_a_row_product_info_answer_Array);

                                                        foreach ($zipped as $tuple) {
                                                            $tuple[0]; // Info question
                                                            $tuple[1]; // Info Answer

                                                            ?>
                                                            <li>
                                                                <!--FILED START-->
                                                                <div class="row">
                                                                    <div class="col-md-5">
                                                                        <div class="form-group">
                                                                            <input type="text" readonly="readonly"
                                                                                   class="form-control"
                                                                                   name="product_info_question[]"
                                                                                   value="<?php echo $tuple[0]; ?>"
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
                                                                            <input type="text" readonly="readonly"
                                                                                   class="form-control"
                                                                                   name="product_info_answer[]"
                                                                                   value="<?php echo $tuple[1]; ?>"
                                                                                   placeholder="<?php echo $BIZBOOK['SPECIFICATIONS_ANSWER']; ?>">
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
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                               <textarea class="form-control" readonly="readonly"
                                                         name="product_tags"
                                                         id="product_tags"
                                                         placeholder="<?php echo $BIZBOOK['PRODUCT_TAGS_PLACEHOLDER']; ?>"><?php echo $products_a_row['product_tags']; ?></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                </li>
                            </ul>
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <button type="submit" name="product_submit"
                                            class="btn btn-primary"><?php echo $BIZBOOK['DELETE_PRODUCT']; ?></button>
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