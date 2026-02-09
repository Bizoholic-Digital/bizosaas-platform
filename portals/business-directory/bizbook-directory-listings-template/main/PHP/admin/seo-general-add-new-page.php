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
                <form name="seo_general_form" id="seo_general_form" method="post" action="insert_general_page.php"
                      enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                <div class="pg-cen">
                    <div class="s-com pg-tit">
                        <h1>Add new page</h1>
                        <div class="form-group">
                          <input type="text" name="page_name" required="required" class="form-control">
                        </div>
                    </div>
                    <div class="s-com pg-edita">
                        <div class="form-group">
                            <textarea class="form-control" id="page_description" name="page_description" placeholder="Details about your listing"></textarea>
                        </div>
                    </div>
                    <div class="s-com pg-cen-tab pg-css">
                        <h4>Custom CSS styles</h4>
                        <div class="inn">
                            <div class="form-group">
                                <textarea class="form-control" name="page_css" placeholder="Write your CSS styles here"></textarea>
                            </div>    
                        </div>
                    </div>
                    <div class="s-com pg-cen-tab pg-scri">
                        <h4>Custom Js Script</h4>
                        <div class="inn">
                            <div class="form-group">
                                <textarea class="form-control" name="page_js" placeholder="Write your Script codes here"></textarea>
                            </div>
                        </div>
                    </div>
                    <div class="s-com pg-cen-tab pg-seo">
                        <h4>SEO settings</h4>
                        <div class="inn">
                            <div class="form-group">
                                <label>Page title</label>
                                <input type="text" name="page_seo_title" class="form-control">
                            </div>
                            <div class="form-group">
                                <label>Page keywords</label>
                                <input type="text" name="page_seo_keyword" class="form-control">
                            </div>
                            <div class="form-group">
                                <label>Page descriptions</label>
                                <input type="text" name="page_seo_description" class="form-control">
                            </div>
                        </div>
                    </div>
                    <div class="s-com pg-cen-tab pg-adv-seo">
                        <h4>Advance SEO settings</h4>
                        <div class="inn">
                            <div class="form-group">
                                <label>Google schema</label>
                                <textarea name="page_seo_schema" class="form-control"></textarea>
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
                                            <option value="Publish">Publish</option>
                                            <option value="Draft">Draft</option>
                                        </select>
                                    </div>
                                </li>
                                <li>
                                    <label>Visibility</label>
                                    <div class="form-group">
                                        <select name="page_visibilty">
                                            <option value="Public">Public</option>
                                            <option value="Private">Private</option>
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
                                            <option value="Default">Default</option>
                                            <option value="RHS">Default with RHS</option>
                                            <option value="LHS">Default with LHS</option>
                                            <option value="Custom">Custom</option>
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
                                            <option value="1">Yes</option>
                                            <option value="0">No</option>
                                        </select>
                                    </div>
                                </li>
                                <li>
                                    <label>Show Products</label>
                                    <div class="form-group">
                                        <select name="page_show_products">
                                            <option value="1">Yes</option>
                                            <option value="0">No</option>
                                        </select>
                                    </div>
                                </li>
                                <li>
                                    <label>Show Events</label>
                                    <div class="form-group">
                                        <select name="page_show_events">
                                            <option value="1">Yes</option>
                                            <option value="0">No</option>
                                        </select>
                                    </div>
                                </li>
                                <li>
                                    <label>Show Blogs</label>
                                    <div class="form-group">
                                        <select name="page_show_blogs">
                                            <option value="1">Yes</option>
                                            <option value="0">No</option>
                                        </select>
                                    </div>
                                </li>
                                <li>
                                    <label>Enquiry form</label>
                                    <div class="form-group">
                                        <select name="page_show_enquiry">
                                            <option value="1">Yes</option>
                                            <option value="0">No</option>
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
                                <select placeholder="Choose Listings"  name="page_listings[]" id="page-new-list-add" multiple class="chosen-select form-control">
                                    <?php
                                    foreach (getAllListing() as $listing_row) {
                                        ?>
                                        <option value="<?php echo $listing_row['listing_id']; ?>"><?php echo $listing_row['listing_name']; ?></option>
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
                                        <option value="<?php echo $product_row['product_id']; ?>"><?php echo $product_row['product_name']; ?></option>
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
                                        <option value="<?php echo $event_row['event_id']; ?>"><?php echo $event_row['event_name']; ?></option>
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
                                        <option value="<?php echo $blog_row['blog_id']; ?>"><?php echo $blog_row['blog_name']; ?></option>
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