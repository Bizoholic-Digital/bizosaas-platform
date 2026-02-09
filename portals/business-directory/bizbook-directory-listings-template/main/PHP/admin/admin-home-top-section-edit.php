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
                    
                    $top_section_id = $_GET['row'];

                    $top_section_row = getHomePageTopSection($top_section_id);
                    
                    ?>

                    <div class="row">
                        <div class="login-main add-list add-ncate">
                            <div class="log-bor">&nbsp;</div>
                            <span class="udb-inst">Change Home Page Top Section</span>
                            <div class="log log-1">
                                <div class="login">
                                    <?php include "../page_level_message.php"; ?>
                                    <h4>Change Home Page Top Section</h4>
                                    <form action="update_home_top_section.php" class="home_top_section_edit_form" id="home_top_section_edit_form" name="home_top_section_edit_form"
                                          method="post" enctype="multipart/form-data">
                                        <input type="hidden" id="top_section_id" value="<?php echo $top_section_row['top_section_id']; ?>"
                                               name="top_section_id" class="validate">
                                        <input type="hidden" id="top_section_image_old"
                                               value="<?php echo $top_section_row['top_section_image']; ?>" name="top_section_image_old"
                                               class="validate">
                                        <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" name="top_section_title" required="required" class="form-control"
                                                                   value="<?php echo $top_section_row['top_section_title']; ?>" placeholder="Title *">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <textarea class="form-control" required="required" id="top_section_description" name="top_section_description"
                                                                      placeholder="Small Description *"><?php echo $top_section_row['top_section_description']?></textarea>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" name="top_section_link_text" required="required" class="form-control"
                                                                   value="<?php echo $top_section_row['top_section_link_text']; ?>"  placeholder="Button Name *">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" name="top_section_link"  class="form-control"
                                                                   value="<?php echo $top_section_row['top_section_link']; ?>"  placeholder="Button Link">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label>Choose icon image</label>
                                                            <input type="file" name="top_section_image" class="form-control">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                            </li>
                                        </ul>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <button type="submit" name="top_section_submit" class="btn btn-primary">Save Changes</button>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                    </form>
                                    <div class="col-md-12">
                                        <a href="admin-home-top-section.php" class="skip">Go to Home Page Top Section >></a>
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