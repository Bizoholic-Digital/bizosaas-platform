<?php
include "header.php";
?>
<?php if($footer_row['admin_listing_show'] != 1 || $admin_row['admin_country_options'] != 1){
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
                    <span class="udb-inst">New Country</span>
                    <div class="log log-1">
                        <div class="login">
                            <h4>Add New Country</h4>
                            <?php include "../page_level_message.php"; ?>
                            <span class="add-list-add-btn count-add-btn" data-toggle="tooltip" title="Click to make additional Country field">+</span>
							<span class="add-list-rem-btn count-rem-btn" data-toggle="tooltip" title="Click to remove last Country field">-</span>
                             <form name="country_form" id="country_form" method="post" action="insert_country.php" enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                                 <ul>
                                     <li>
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                  <input type="text" name="country_name[]" class="form-control" placeholder="Country name *" required>
                                                </div>
                                            </div>
                                        </div>
                                     </li>
                                 </ul>
                                <button type="submit" name="country_submit" class="btn btn-primary">Submit</button>
                            </form>
                            <div class="col-md-12">
                                    <a href="admin-all-country.php" class="skip">Go to All Country >></a>
                                </div>

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