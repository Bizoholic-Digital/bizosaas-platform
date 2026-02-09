<?php
include "header.php";
?>

<?php if($footer_row['admin_listing_show'] != 1 || $admin_row['admin_category_options'] != 1){
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
                    <span class="udb-inst">New Listing Sub Category</span>
                    <div class="log log-1">
                        <div class="login">
                            <h4>Add New Listing Sub Category</h4>
                            <?php include "../page_level_message.php"; ?>
                            <span class="add-list-add-btn scat-add-btn" data-toggle="tooltip" title="Click to create additional Sub Category field">+</span>
							<span class="add-list-rem-btn scat-rem-btn" data-toggle="tooltip" title="Click to remove Sub Category field">-</span>
                            
                             <form  name="sub_category_form" id="sub_category_form" method="post" action="insert_sub_category.php" enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                                 <div class="row">
                                     <div class="col-md-12">
                                        <div class="form-group">
                                            <select name="category_id" class="form-control" id="category_name">
                                                <?php
                                                foreach (getAllCategories() as $row) {
                                                ?>
                                                <option value="<?php echo $row['category_id']; ?>"><?php echo $row['category_name']; ?></option>
                                                    <?php
                                                    }
                                                    ?>
                                            </select>

                                        </div>
                                    </div>
                                </div>
                                 <br>
                                 <ul>
                                     <li>
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                  <input type="text" name="sub_category_name[]" class="form-control" placeholder="Sub category name *" required>
                                                </div>
                                            </div>
                                        </div>
                                     </li>
                                 </ul>
                                <button type="submit" name="sub_category_submit" class="btn btn-primary">Submit</button>
                            </form>
                            <div class="col-md-12">
                                    <a href="admin-all-sub-category.php" class="skip">Go to All Listing Sub Category >></a>
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