<?php
include "header.php";
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
                            <span class="udb-inst">Edit Popular Business</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Edit this Popular Business</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $listing_id = $_GET['row'];
                                    $row = getFeaturedListing($listing_id);

                                    ?>
                                    <form name="listing_form" id="listing_form" method="post" action="update_home_popular_business.php" enctype="multipart/form-data">

                                        <input type="hidden" class="validate" id="listing_id_old" name="listing_id_old" value="<?php echo $row['listing_id']; ?>" required="required">
                                        <input type="hidden" class="validate" id="featured_listing_id" name="featured_listing_id" value="<?php echo $row['featured_listing_id']; ?>" required="required">
                                         <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select name="listing_id" class="form-control" id="listing_id">

                                                                <?php
                                                                foreach (getAllListing() as $li_row){
                                                                    ?>
                                                                    <option
                                                                        value="<?php echo $li_row['listing_id']; ?>" <?php if ($li_row['listing_id'] == $row['listing_id']) {
                                                                        echo "selected";
                                                                    } ?> ><?php echo $li_row['listing_name']; ?>
                                                                    </option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->

                                            </li>
                                        </ul>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <button type="submit" name="home_featured_listing_submit" class="btn btn-primary">Update</button>
                                            </div>
                                            <div class="col-md-12">
                                                <a href="admin-home-popular-business.php" class="skip">Go to Popular business >></a>
                                            </div>
                                        </div>
                                        <!--FILED END-->
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