<?php
include "header.php";
?>

<?php if ($footer_row['admin_news_show'] !=1 || $admin_row['admin_news_options'] != 1) {
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
                            <span class="udb-inst">Edit Social Media</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Edit this Social Media</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $social_media_id = $_GET['row'];
                                    $row = getNewsSocialMedia($social_media_id);

                                    ?>
                                    <form name="home_news_social_media_form" id="home_news_social_media_form" method="post"
                                          action="update_home_news_social_media.php" enctype="multipart/form-data">

                                        <input type="hidden" class="validate" id="social_media_id"
                                               name="social_media_id" value="<?php echo $row['social_media_id']; ?>"
                                               required="required">
                                        <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <div class="row">
                                                                <div class="col-md-12">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               readonly="readonly"
                                                                               id="social_media_name"
                                                                               name="social_media_name"
                                                                               value="<?php echo $row['social_media_name']; ?>"
                                                                               placeholder="social media name *"
                                                                               required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <div class="row">
                                                                <div class="col-md-12">
                                                                    <div class="form-group">
                                                                        <input type="text" class="form-control"
                                                                               id="social_media_count"
                                                                               name="social_media_count"
                                                                               value="<?php echo $row['social_media_count']; ?>"
                                                                               placeholder="i.e 15K *" required>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <div class="row">
                                                                <div class="col-md-12">
                                                                    <div class="form-group">
                                                                        <textarea class="form-control"
                                                                                  id="social_media_link"
                                                                                  required="required"
                                                                                  name="social_media_link"
                                                                                  placeholder="social media link"><?php echo $row['social_media_link']; ?></textarea>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <div class="row">
                                                                <div class="col-md-12">
                                                                    <div class="form-group">
                                                                        <select name="social_media_status"
                                                                                id="social_media_status"
                                                                                class="chosen-select form-control">
                                                                            <option <?php
                                                                            if ($row['social_media_status'] == 1) {
                                                                                echo "selected";

                                                                            } ?>
                                                                                value="1">
                                                                                Active
                                                                            </option>
                                                                            <option <?php
                                                                            if ($row['social_media_status'] == 0) {
                                                                                echo "selected";

                                                                            } ?>
                                                                                value="0">
                                                                                Inactive
                                                                            </option>

                                                                        </select>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->

                                            </li>
                                        </ul>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <button type="submit" name="home_news_social_submit"
                                                        class="btn btn-primary">Update
                                                </button>
                                            </div>
                                            <div class="col-md-12">
                                                <a href="news-home-social-media.php" class="skip">Go to Social Media - News >></a>
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
<script src="js/admin-custom.js"></script>
<script src="http://harvesthq.github.io/chosen/chosen.jquery.js"></script>
</body>

</html>