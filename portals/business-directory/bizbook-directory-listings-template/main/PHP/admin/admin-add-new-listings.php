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
                    <span class="udb-inst">new listing</span>
                    <div class="log log-1">
                        <div class="login">
                            <h4>Add New Listings</h4>
                            <div class="row cre-dup">
                                <div class="col-md-6">
                                    <a href="admin-add-new-listings-start.php">Create listing from scratch</a>
                                </div>
                                <div class="col-md-6">
                                    <a href="admin-create-duplicate-listing.php">Create duplicate listing</a>
                                </div>
                            </div>
                             <form class="cre-dup-form">
                                  <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                              <select class="form-control">
                                                <option>Choose what listing you going to copy</option>
                                                    <option>The Real Finness for Womens</option>
                                                  <option>Lux Facial and Spa</option>
                                                  <option>3BHK flat for sale</option>
                                                  <option>All in one mechanic shop</option>
                                              </select>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                 <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                              <input type="text" class="form-control" placeholder="Listing name *">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                <button type="submit" class="btn btn-primary">Next</button>
                            </form>
                            <div class="col-md-12">
                                    <a href="profile.php" class="skip">Go to user dashboard >></a>
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