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
                    <span class="udb-inst">Sitemap</span>
                    <div class="log log-1">
                        <div class="login">
                            <h4>XML Sitemap</h4>
                            <p><a href="https://www.xml-sitemaps.com/?bizbook-tempate" target="_blank" rel="nofollow">Click here</a> to generate your sitemap then upload to below box.</p>
                            <?php include "../page_level_message.php"; ?>
                             <form name="seo_xml_sitemap_form" id="seo_xml_sitemap_form" method="post" action="update_seo_xml_sitemap.php"
                                   enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                                 <ul>
                                     <li>
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="s-com">
                                                    <h6>Upload XML file:</h6>
                                                    <div class="form-group">
                                                      <input type="file" name="sitemap_file" required="required" class="form-control" placeholder="Download link">
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                     </li>
                                 </ul>
                                <button type="submit" name="seo_xml_sitemap_submit" class="btn btn-primary">Submit</button>
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