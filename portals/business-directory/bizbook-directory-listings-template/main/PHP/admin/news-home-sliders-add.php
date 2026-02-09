<?php
include "header.php";
?>

<?php if ($admin_row['admin_news_options'] != 1) {
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
                            <span class="udb-inst">Add Slider Posts</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Add new Slider</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <form name="home_sliders_form" id="home_sliders_form" method="post" action="insert_home_sliders.php" enctype="multipart/form-data">
                                         <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select name="news_id" class="chosen-select form-control" id="news_id">

                                                                <?php
                                                                foreach (getAllNews() as $li_row){
                                                                    ?>
                                                                    <option
                                                                        value="<?php echo $li_row['news_id']; ?>" ><?php echo $li_row['news_title']; ?>
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
                                                <button type="submit" name="home_slider_news_submit" class="btn btn-primary">Submit</button>
                                            </div>
                                            <div class="col-md-12">
                                                <a href="news-home-sliders.php" class="skip">Go to All Sliders >></a>
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