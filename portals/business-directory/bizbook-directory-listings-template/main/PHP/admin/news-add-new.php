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
                            <span class="udb-inst">new news</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Create News</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <form name="news_form" id="news_form" method="post" action="insert_news.php"
                                          enctype="multipart/form-data">
                                        <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" name="news_title" required="required"
                                                                   class="form-control" placeholder="News title *">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <textarea name="news_description" id="news_description"
                                                                      required="required" class="form-control"
                                                                      placeholder="News details"></textarea>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label>Choose banner image</label>
                                                            <input type="file" name="news_image" required="required"
                                                                   class="form-control">
                                                        </div>
                                                    </div>
                                                </div>

                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select name="category_id" required="required"
                                                                    class="chosen-select form-control" id="category_id">
                                                                <option value="">Select category</option>
                                                                <?php
                                                                foreach (getAllNewsCategories() as $row) {
                                                                    ?>
                                                                    <option
                                                                        value="<?php echo $row['category_id']; ?>"><?php echo $row['category_name']; ?></option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->

                                                <!--FILED END-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group jb-fm-box-hig">
                                                            <h5 data-toggle="collapse" data-target="#jb-expe">SEO
                                                                details</h5>
                                                            <div id="jb-expe" class="collapse coll-box">
                                                                <input type="text" name="seo_title" class="form-control"
                                                                       placeholder="SEO Title">
                                                                <hr>
                                                                <input type="text" name="seo_description"
                                                                       class="form-control"
                                                                       placeholder="Meta descriptions">
                                                                <hr>
                                                                <input type="text" name="seo_keywords"
                                                                       class="form-control" placeholder="Meta keywords">
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        </ul>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <button type="submit" name="news_submit" class="btn btn-primary">
                                                    Submit
                                                </button>
                                            </div>
                                        </div>
                                        <!--FILED END-->
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
<script src="js/admin-custom.js"></script>
<script src="http://harvesthq.github.io/chosen/chosen.jquery.js"></script>
</body>

</html>