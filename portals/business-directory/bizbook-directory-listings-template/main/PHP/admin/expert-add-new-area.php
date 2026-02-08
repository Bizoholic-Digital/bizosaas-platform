<?php
include "header.php";
?>
<?php if($footer_row['admin_expert_show'] != 1 || $admin_row['admin_service_expert_options'] != 1){
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
                            <span class="udb-inst">New Area</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Add New Area</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <span class="add-list-add-btn expert-area-add-btn" data-toggle="tooltip" title="Click to make additional Expert Area">+</span>
                                    <span class="add-list-rem-btn expert-area-rem-btn" data-toggle="tooltip" title="Click to remove last Expert Area">-</span>
                                    <form name="city_form" id="city_form" method="post" action="insert_expert_area.php" enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                                        <ul>
                                            <li>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select name="country_id" required="required" id="country_id"
                                                                    class="form-control">
                                                                <option value="">Choose City Name</option>
                                                                <?php
                                                                //Countries Query
                                                                foreach (getAllExpertCities() as $countries_row) {
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
                                                            <input type="text" name="city_name[]" class="form-control" placeholder="Area name *" required>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        </ul>
                                        <button type="submit" name="city_submit" class="btn btn-primary">Submit</button>
                                    </form>
                                    <div class="col-md-12">
                                        <a href="expert-all-area.php" class="skip">Go to All Area >></a>
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
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
</body>

</html>