<?php
include "header.php";
?>
<?php if($admin_row['admin_seo_setting_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                 <section class="login-reg">
		<div class="container">
			<div class="row">
                <div class="login-main add-list add-ncate">
                     <div class="log-bor">&nbsp;</div>
                    <span class="udb-inst">meta tags</span>
                    <div class="log log-1">
                        <div class="login">
                            <?php
                            $seo_page_id = $_GET['row'];
                            $seo_details_row = getSeo($seo_page_id);
                            ?>
                            <h4>Edit SEO <?php echo '- '.$seo_details_row['seo_page_name']; ?></h4>
                            <?php include "../page_level_message.php"; ?>
                             <form name="seo_page_form" id="country_form" method="post" action="update-seo-meta-tags.php" class="cre-dup-form cre-dup-form-show">
                                 <input type="hidden" id="seo_page_id" value="<?php echo $seo_details_row['seo_page_id']; ?>"
                                        name="seo_page_id" class="validate">
                                 <ul>
                                     <li>
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="s-com">
                                                    <div class="form-group">
                                                      <input type="text" name="seo_page_title" value="<?php echo $seo_details_row['seo_page_title']; ?>" class="form-control" placeholder="Title">
                                                    </div>
                                                </div>
                                                <hr>
                                                <div class="s-com">
                                                    <div class="form-group">
                                                        <textarea name="seo_page_keywords" class="form-control" placeholder="Keywords"><?php echo $seo_details_row['seo_page_keywords']; ?></textarea>
                                                    </div>
                                                </div>
                                                <hr>
                                                <div class="s-com">
                                                    <div class="form-group">
                                                        <textarea name="seo_page_description" class="form-control" placeholder="Descriptions"><?php echo $seo_details_row['seo_page_description']; ?></textarea>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                     </li>
                                 </ul>
                                <button type="submit" name="seo_page_submit" class="btn btn-primary">Submit</button>
                            </form>

                        </div>
                    </div>
                </div>
			</div>
		</div>
	</section>

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