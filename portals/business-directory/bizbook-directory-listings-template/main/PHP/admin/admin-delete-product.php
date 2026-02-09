<?php
include "header.php";
?>

<?php if($footer_row['admin_product_show'] != 1 || $admin_row['admin_product_options'] != 1){
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
                    $product_codea = $_GET['code'];
                    $products_a_row = getProduct($product_codea);

                    ?>
                    <form action="trash_product.php" class="product_form" id="product_form" name="product_form"
                          method="post" enctype="multipart/form-data">
                        <input type="hidden" id="product_id" value="<?php echo $products_a_row['product_id']; ?>"
                               name="product_id" class="validate">
                        <input type="hidden" id="product_code" value="<?php echo $products_a_row['product_code']; ?>"
                               name="product_code" class="validate">
                        <input type="hidden" id="gallery_image_old"
                               value="<?php echo $products_a_row['gallery_image']; ?>" name="gallery_image_old"
                               class="validate">
                        <div class="row">
                            <div class="login-main add-list posr">
                                <div class="log-bor">&nbsp;</div>
                                <span class="udb-inst">Edit Product Details</span>
                                <div class="log log-1">
                                    <div class="login">
                                        <h4>Edit Product Details</h4>
                                        <?php include "../page_level_message.php"; ?>
                                        <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select disabled="disabled" name="user_code" id="user_code" class="form-control"
                                                                    required="required">
                                                                <option value="" disabled>User Name</option>
                                                                <?php
                                                                foreach (getAllUser() as $ad_users_row) {
                                                                    ?>
                                                                    <option <?php if ($products_a_row['user_id'] == $ad_users_row['user_id']) {
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
                                                            <input type="text" readonly="readonly" name="product_name" id="product_name"
                                                                   required="required" class="form-control"
                                                                   value="<?php echo $products_a_row['product_name']; ?>"
                                                                   placeholder="Product name *">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select disabled="disabled" onChange="getProductSubCategory(this.value);"
                                                                    name="category_id"
                                                                    id="category_id" class="chosen-select form-control">
                                                                <option value="">Select Category</option>
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
                                                            <select disabled="disabled" name="sub_category_id[]" id="sub_category_id"
                                                                    multiple
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
                                                            <input type="text" readonly="readonly" name="product_price" id="product_price"
                                                                   value="<?php echo $products_a_row['product_price']; ?>"
                                                                   required="required" class="form-control"
                                                                   placeholder="Price *">
                                                        </div>
                                                    </div>
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <input type="text" readonly="readonly" name="product_price_offer"
                                                                   id="product_price_offer"
                                                                   value="<?php echo $products_a_row['product_price_offer']; ?>"
                                                                   class="form-control" placeholder="Offer (i.e)50%">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                               <textarea class="form-control"
                                                         name="product_payment_link" readonly="readonly"
                                                         id="product_payment_link"
                                                         placeholder="Product Payment External Link"><?php echo $products_a_row['product_payment_link']; ?></textarea>
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
                                                          placeholder="Product details"><?php echo $products_a_row['product_description']; ?></textarea>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                               
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="log">
                                                            <div class="login add-prod-high-oth">

                                                                <h4>Highlights</h4>
                                                                <ul>
                                                                    <?php
                                                                    $products_a_row_product_highlights = $products_a_row['product_highlights'];

                                                                    $products_a_row_product_highlights_Array = explode('|', $products_a_row_product_highlights);

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
                                                                                               placeholder="(i.e) 1 Year Onsite Warranty">
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

                                                                <h4>Specifications</h4>
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
                                                                                               placeholder="(i.e) Serial Number">
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
                                                                                               placeholder="(i.e) qwerty3421">
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
                                                         placeholder="Product Tags (i.e) electronics,laptop,hp,canon"><?php echo $products_a_row['product_tags']; ?></textarea>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                            </li>
                                        </ul>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <button type="submit" name="product_submit" class="btn btn-primary">
                                                    Delete Product
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
    function getProductSubCategory(val) {
        $.ajax({
            type: "POST",
            url: "../product_sub_category_process.php",
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