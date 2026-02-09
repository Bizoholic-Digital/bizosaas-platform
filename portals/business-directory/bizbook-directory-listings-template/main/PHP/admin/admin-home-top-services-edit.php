<?php
include "header.php";
?>

<?php if ($admin_row['admin_home_options'] != 1) {
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <section class="login-reg">
                <div class="container">

                    <?php
                    $category_id = $_GET['cat'];

                    $listing_id = $_GET['row'];

                    $category_sql_row = getCategory($category_id);

                    $listing_row = getIdListing($listing_id);

                    $top_service_row = getCategoryTopServiceProviders($category_id);


                    ?>

                    <div class="row">
                        <div class="login-main add-list add-ncate">
                            <div class="log-bor">&nbsp;</div>
                            <span class="udb-inst">Change listing </span>
                            <div class="log log-1">
                                <div class="login">
                                    <?php include "../page_level_message.php"; ?>
                                    <h4>Choose listing for <?php echo $category_sql_row['category_name']; ?></h4>
                                    <form name="home_top_service_listing_form" id="home_top_service_listing_form" method="post" action="update_top_service_listing.php" class="cre-dup-form cre-dup-form-show">
                                        <input type="hidden" class="validate" id="all_top_service_listings" name="all_top_service_listings" value="<?php echo $top_service_row['top_service_provider_listings']; ?>" required="required">
                                        <input type="hidden" class="validate" id="category_id" name="category_id" value="<?php echo $category_id; ?>" required="required">
                                        <input type="hidden" class="validate" id="listing_id_old" name="listing_id_old" value="<?php echo $listing_id; ?>" required="required">
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <select name="listing_id" class="form-control" id="listing_id">
                                                        <?php
                                                        foreach (getAllListingCategory($category_id) as $cat_row) {

                                                            ?>
                                                            <option <?php if($cat_row['listing_id']== $listing_id){ echo "selected"; } ?>
                                                                value="<?php echo $cat_row['listing_id']; ?>"><?php echo $cat_row['listing_name']; ?></option>
                                                            <?php
                                                        }
                                                        ?>
                                                    </select>

                                                </div>
                                            </div>
                                        </div>
                                        </br>
                                        <button type="submit" name="home_top_service_listing_submit" class="btn btn-primary">Submit</button>
                                    </form>
                                    <div class="col-md-12">
                                        <a href="admin-home-top-services.php" class="skip">Go to Top Services >></a>
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