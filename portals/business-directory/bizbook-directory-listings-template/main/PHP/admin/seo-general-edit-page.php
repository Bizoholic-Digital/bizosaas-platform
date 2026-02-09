<?php
include "header.php";
?>

<?php if($admin_row['admin_seo_setting_options'] != 1){
    header("Location: profile.php");
}
?>

<!-- START -->
<section>
    <div class="ad-com pg-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <?php
                $page_id = $_GET['row'];
                $details_row = getPage($page_id);
                ?>
                <form name="seo_general_form" id="seo_general_form" method="post" action="update_general_page.php"
                      enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                    <input type="hidden" id="page_id" value="<?php echo $details_row['page_id']; ?>"
                           name="page_id" class="validate">
                    <div class="pg-cen">
                        <div class="s-com pg-tit">
                            <h1>Edit General page</h1>
                            <div class="form-group">
                                <input type="text" value="<?php echo $details_row['page_name']; ?>" name="page_name" required="required" class="form-control">
                            </div>
                        </div>
                        <div class="s-com pg-edita">
                            <div class="form-group">
                                <textarea class="form-control" id="page_description" name="page_description" placeholder="Details about your listing"><?php echo stripslashes($details_row['page_description']); ?></textarea>
                            </div>
                        </div>
                        <div class="s-com pg-cen-tab pg-css">
                            <h4>Custom CSS styles</h4>
                            <div class="inn">
                                <div class="form-group">
                                    <textarea class="form-control" name="page_css" placeholder="Write your CSS styles here"><?php echo stripslashes($details_row['page_css']); ?></textarea>
                                </div>
                            </div>
                        </div>
                        <div class="s-com pg-cen-tab pg-scri">
                            <h4>Custom Js Script</h4>
                            <div class="inn">
                                <div class="form-group">
                                    <textarea class="form-control" name="page_js" placeholder="Write your Script codes here"><?php echo stripslashes($details_row['page_js']); ?></textarea>
                                </div>
                            </div>
                        </div>
                        <div class="s-com pg-cen-tab pg-seo">
                            <h4>SEO settings</h4>
                            <div class="inn">
                                <div class="form-group">
                                    <label>Page title</label>
                                    <input type="text" value="<?php echo $details_row['page_seo_title']; ?>" name="page_seo_title" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label>Page keywords</label>
                                    <input type="text" value="<?php echo stripslashes($details_row['page_seo_keyword']); ?>" name="page_seo_keyword" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label>Page descriptions</label>
                                    <input type="text" value="<?php echo stripslashes($details_row['page_seo_description']); ?>" name="page_seo_description" class="form-control">
                                </div>
                            </div>
                        </div>
                        <div class="s-com pg-cen-tab pg-adv-seo">
                            <h4>Advance SEO settings</h4>
                            <div class="inn">
                                <div class="form-group">
                                    <label>Google schema</label>
                                    <textarea name="page_seo_schema" class="form-control"><?php echo stripslashes($details_row['page_seo_schema']); ?></textarea>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="pg-rhs">
                        <div class="box pub">
                            <h3>Publish</h3>
                            <div class="inn">
                                <ul>
                                    <li>
                                        <label>Status</label>
                                        <div class="form-group">
                                            <select name="page_status">
                                                <option <?php if($details_row['page_status'] == "Publish"){echo "selected";} ?> value="Publish">Publish</option>
                                                <option <?php if($details_row['page_status'] == "Draft"){echo "selected";} ?> value="Draft">Draft</option>
                                            </select>
                                        </div>
                                    </li>
                                    <li>
                                        <label>Visibility</label>
                                        <div class="form-group">
                                            <select name="page_visibilty">
                                                <option <?php if($details_row['page_visibilty'] == "Public"){echo "selected";} ?> value="Public">Public</option>
                                                <option <?php if($details_row['page_visibilty'] == "Private"){echo "selected";} ?> value="Private">Private</option>
                                            </select>
                                        </div>
                                    </li>
                                    <li>
                                        <button name="general_submit" type="submit" class="btn-pub btn-pub">Save changes</button>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="box pub">
                            <h3>Template setting</h3>
                            <div class="inn">
                                <ul>
                                    <li>
                                        <label>Template</label>
                                        <div class="form-group">
                                            <select name="page_template">
                                                <option <?php if($details_row['page_template'] == "Default"){echo "selected";} ?> value="Default">Default</option>
                                                <option <?php if($details_row['page_template'] == "RHS"){echo "selected";} ?> value="RHS">Default with RHS</option>
                                                <option <?php if($details_row['page_template'] == "LHS"){echo "selected";} ?> value="LHS">Default with LHS</option>
                                                <option <?php if($details_row['page_template'] == "Custom"){echo "selected";} ?> value="Custom">Custom</option>
                                            </select>
                                        </div>
                                    </li>
                                </ul>
                                <div class="templ-pre">
                                    <h6>Preview</h6>
                                    <img src="images/template/default.png">
                                    <img src="images/template/default.png">
                                    <img src="images/template/default.png">
                                </div>
                            </div>
                        </div>
                        <div class="box pub">
                            <h3>Page setting</h3>
                            <div class="inn">
                                <ul>
                                    <li>
                                        <label>Show Listing</label>
                                        <div class="form-group">
                                            <select name="page_show_listings">
                                                <option <?php if($details_row['page_show_listings'] == "1"){echo "selected";} ?> value="1">Yes</option>
                                                <option <?php if($details_row['page_show_listings'] == "0"){echo "selected";} ?> value="0">No</option>
                                            </select>
                                        </div>
                                    </li>
                                    <li>
                                        <label>Show Products</label>
                                        <div class="form-group">
                                            <select name="page_show_products">
                                                <option <?php if($details_row['page_show_products'] == "1"){echo "selected";} ?> value="1">Yes</option>
                                                <option <?php if($details_row['page_show_products'] == "0"){echo "selected";} ?> value="0">No</option>
                                            </select>
                                        </div>
                                    </li>
                                    <li>
                                        <label>Show Events</label>
                                        <div class="form-group">
                                            <select name="page_show_events">
                                                <option <?php if($details_row['page_show_events'] == "1"){echo "selected";} ?> value="1">Yes</option>
                                                <option <?php if($details_row['page_show_events'] == "0"){echo "selected";} ?> value="0">No</option>
                                            </select>
                                        </div>
                                    </li>
                                    <li>
                                        <label>Show Blogs</label>
                                        <div class="form-group">
                                            <select name="page_show_blogs">
                                                <option <?php if($details_row['page_show_blogs'] == "1"){echo "selected";} ?> value="1">Yes</option>
                                                <option <?php if($details_row['page_show_blogs'] == "0"){echo "selected";} ?> value="0">No</option>
                                            </select>
                                        </div>
                                    </li>
                                    <li>
                                        <label>Enquiry form</label>
                                        <div class="form-group">
                                            <select name="page_show_enquiry">
                                                <option <?php if($details_row['page_show_enquiry'] == "1"){echo "selected";} ?> value="1">Yes</option>
                                                <option <?php if($details_row['page_show_enquiry'] == "0"){echo "selected";} ?> value="0">No</option>
                                            </select>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>

                        <!--- LISTINGS --->
                        <div class="box pub">
                            <h3>Listings</h3>
                            <div class="inn">
                                <div class="form-group">
                                    <select placeholder="Choose Listings" name="page_listings[]" id="page-new-list-add" multiple class="chosen-select form-control">
                                        <?php
                                        foreach (getAllListing() as $listing_row) {
                                            ?>
                                            <option <?php $catArray = explode(',', $details_row['page_listings']);
                                            foreach ($catArray as $cat_Array) {
                                                if ($listing_row['listing_id'] == $cat_Array) {
                                                    echo "selected";
                                                }
                                            } ?>
                                                value="<?php echo $listing_row['listing_id']; ?>"><?php echo $listing_row['listing_name']; ?></option>
                                            <?php
                                        }
                                        ?>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <!--- END PRODUCTS --->

                        <!--- PRODUCTS --->
                        <div class="box pub">
                            <h3>Products</h3>
                            <div class="inn">
                                <div class="form-group">
                                    <select placeholder="Choose Products" name="page_products[]" id="page-new-pro-add" multiple class="chosen-select form-control">
                                        <?php
                                        foreach (getAllProduct() as $product_row) {
                                            ?>
                                            <option <?php $catArray = explode(',', $details_row['page_products']);
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
                        <!--- END PRODUCTS --->

                        <!--- EVENTS --->
                        <div class="box pub">
                            <h3>Events</h3>
                            <div class="inn">
                                <div class="form-group">
                                    <select placeholder="Choose Events" name="page_events[]" id="page-new-eve-add" multiple class="chosen-select form-control">
                                        <?php
                                        foreach (getAllEvents() as $event_row) {
                                            ?>
                                            <option <?php $catArray = explode(',', $details_row['page_events']);
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
                        <!--- END EVENTS --->

                        <!--- BLOG POST --->
                        <div class="box pub">
                            <h3>Blog posts</h3>
                            <div class="inn">
                                <div class="form-group">
                                    <select placeholder="Choose Blogs" name="page_blogs[]" id="page-new-blog-add" multiple class="chosen-select form-control">
                                        <?php
                                        foreach (getAllBlogs() as $blog_row) {
                                            ?>
                                            <option <?php $catArray = explode(',', $details_row['page_blogs']);
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
                        <!--- END BLOG POST --->

                    </div>
                </form>
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
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
<script src="ckeditor/ckeditor.js"></script>
<script>
    CKEDITOR.replace('page_description');
</script>
</body>

</html>