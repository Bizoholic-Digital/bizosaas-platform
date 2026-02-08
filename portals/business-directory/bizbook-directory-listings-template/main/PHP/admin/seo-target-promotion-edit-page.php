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
                <form name="target_promotion_form" id="target_promotion_form" method="post" action="update_target_promotion_page.php"
                      enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                    <input type="hidden" id="page_id" value="<?php echo $details_row['page_id']; ?>"
                           name="page_id" class="validate">
                    <div class="pg-cen">
                        <div class="s-com pg-tit">
                            <h1>Edit Target Promotion Page</h1>
                            <div class="form-group">
                                <input type="text" value="<?php echo $details_row['page_name']; ?>" name="page_name" required="required" class="form-control" placeholder="Page name">
                            </div>
                        </div>
                        <div class="s-com pg-cen-tab pg-css">
                            <h4>Select listing to show this page below:</h4>
                            <div class="inn">
                                <div class="box pub">
                                    <div class="form-group">
                                        <select placeholder="Choose Listings" name="page_listings[]" id="page-new-list-add" multiple required="required" class="chosen-select form-control">
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
                                        <button name="target_submit" type="submit" class="btn-pub btn-pub">Save changes</button>
                                    </li>
                                </ul>
                            </div>
                        </div>
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