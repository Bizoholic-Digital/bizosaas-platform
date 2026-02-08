<?php
include "header.php";

if ($admin_row['admin_seo_setting_options'] != 1) {
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
                <form name="seo_ebook_form" id="seo_ebook_form" method="post" action="update_ebook_page.php"
                      enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                    <input type="hidden" id="page_id" value="<?php echo $details_row['page_id']; ?>"
                           name="page_id" class="validate">
                    <input type="hidden" id="page_image_old" value="<?php echo $details_row['page_image']; ?>"
                           name="page_image_old" class="validate">
                    <div class="pg-cen">
                        <div class="s-com pg-tit">
                            <h1>Edit E-Book page</h1>
                            <div class="form-group">
                                <input type="text" name="page_name" value="<?php echo $details_row['page_name']; ?>" required="required" class="form-control" placeholder="Banner title">
                            </div>
                        </div>
                        <div class="s-com">
                            <div class="form-group">
                                <input type="text" name="page_name_2" value="<?php echo $details_row['page_name_2']; ?>" required="required" class="form-control"
                                       placeholder="Banner sub title">
                            </div>
                        </div>
                        <div class="s-com">
                            <div class="form-group">
                                <input type="text" name="page_download_link" value="<?php echo $details_row['page_download_link']; ?>" required="required" class="form-control" placeholder="Download link">
                            </div>
                        </div>
                        <div class="s-com">
                            <h6>Ebook preview image:</h6>
                            <div class="form-group">
                                <input type="file" name="page_image" class="form-control" placeholder="Download link">
                            </div>
                        </div>
                        <div class="s-com pg-edita">
                            <h6>Page descriptions:</h6>
                            <div class="form-group">
                                <textarea class="form-control" id="page_description" name="page_description"
                                          placeholder="Details about your listing"><?php echo stripslashes($details_row['page_description']); ?></textarea>
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
                                    <textarea class="form-control" name="page_js"
                                              placeholder="Write your Script codes here"><?php echo stripslashes($details_row['page_js']); ?></textarea>
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
                                        <button name="ebook_submit" type="submit" class="btn-pub btn-pub">Save changes</button>
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
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
<script src="ckeditor/ckeditor.js"></script>
<script>
    CKEDITOR.replace('page_description');
</script>
</body>

</html>