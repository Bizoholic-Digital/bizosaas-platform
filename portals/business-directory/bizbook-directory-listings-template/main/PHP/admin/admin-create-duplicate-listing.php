<?php
include "header.php";
?>

<?php if($footer_row['admin_listing_show'] != 1 || $admin_row['admin_listing_options'] != 1){
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
                <div class="login-main add-list posr">
                     <div class="log-bor">&nbsp;</div>
                    <span class="udb-inst">Duplicate listing</span>
                    <div class="log log-1">
                        <div class="login">
                            <h4>Create New Duplicate Listings</h4>
                             <form name="duplicate_listing_form" action="insert_duplicate_listing.php" id="duplicate_listing_form" method="post" class="cre-dup-form cre-dup-form-show">
                                  <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <select name="listing_id" id="listing_id" class="chosen-select form-control"
                                                        required="required">
                                                    <option value="" disabled selected>Listing Name</option>
                                                    <?php
                                                    $listsql = "SELECT * FROM " . TBL . "listings  WHERE  listing_is_delete != '2' ORDER BY listing_id DESC";

                                                    $listrs = mysqli_query($conn,$listsql);

                                                    $list_count = mysqli_num_rows($listrs);

                                                    while ($listrow = mysqli_fetch_array($listrs)) {
                                                        ?>
                                                        <option
                                                            value="<?php echo $listrow['listing_code']; ?>"><?php echo $listrow['listing_name']; ?></option>
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
                                             <select name="user_code" id="user_code" class="chosen-select form-control"
                                                     required="required">
                                                 <option value="" disabled selected>Choose User</option>
                                                 <?php
                                                 foreach (getAllUser() as $ad_users_row) {
                                                     ?>
                                                     <option
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
                                              <input type="text" name="listing_name" required="required" class="form-control" placeholder="Listing name *">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                <button type="submit" name="listing_submit" class="btn btn-primary">Create Now</button>
                            </form>
                            <div class="col-md-12">
                                    <a href="user-profile-service-provider.html" class="skip">Go to user dashboard >></a>
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