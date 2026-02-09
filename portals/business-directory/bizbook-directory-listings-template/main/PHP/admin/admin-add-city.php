<?php
include "header.php";
?>
<?php if($footer_row['admin_listing_show'] != 1 || $admin_row['admin_city_options'] != 1){
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
                    <span class="udb-inst">New City</span>
                    <div class="log log-1">
                        <div class="login">
                            <h4>Add New City</h4>
                            <?php include "../page_level_message.php"; ?>
                            <span class="add-list-add-btn city-add-btn" data-toggle="tooltip" title="Click to make additional city">+</span>
                            <span class="add-list-rem-btn city-rem-btn" data-toggle="tooltip" title="Click to remove last city">-</span>
                            <form name="city_form" id="city_form" method="post" action="insert_city.php" enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                                <ul>
                                    <li>
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <select name="country_id" required="required" id="country_id"
                                                            class="chosen-select form-control">
                                                        <option value="">Choose Country</option>
                                                        <?php
                                                        //Countries Query
                                                            foreach (getAllCountries() as $countries_row) {
                                                                ?>
                                                                <option <?php if ($_SESSION['country_id'] == $countries_row['country_id']) {
                                                                    echo "selected";
                                                                } ?>
                                                                    value="<?php echo $countries_row['country_id']; ?>"><?php echo $countries_row['country_name']; ?></option>
                                                                <?php
                                                        }
                                                        ?>
                                                    </select>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                    <li>
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <input type="text" name="city_name[]" class="form-control" placeholder="City name *" required>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                </ul>
                                <button type="submit" name="city_submit" class="btn btn-primary">Submit</button>
                            </form>
                            <div class="col-md-12">
                                    <a href="admin-all-city.php" class="skip">Go to All City >></a>
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
    <script src="../js/select-opt.js"></script>
    <script src="js/admin-custom.js"></script>
</body>

</html>