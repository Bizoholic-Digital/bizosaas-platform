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
                            <span class="udb-inst">Delete This news</span>
                            <?php
                            $news_ida = $_GET['code'];
                            $news_row = getIdNews($news_ida);

                            ?>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Delete News</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <form name="news_form" id="news_form" method="post" action="trash_news.php"
                                          enctype="multipart/form-data">
                                        <input type="hidden" id="news_image_old"
                                               value="<?php echo $news_row['news_image']; ?>"
                                               name="news_image_old"
                                               class="validate">
                                        <input type="hidden" id="news_id"
                                               value="<?php echo $news_row['news_id']; ?>"
                                               name="news_id"
                                               class="validate">
                                        <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" name="news_title" required="required" readonly="readonly"
                                                                   value="<?php echo $news_row['news_title']; ?>" class="form-control" placeholder="News title *">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <textarea name="news_description" id="news_description" readonly="readonly"
                                                                      required="required" class="form-control"
                                                                      placeholder="News details"><?php echo $news_row['news_description']; ?></textarea>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select disabled="disabled" name="category_id" required="required"
                                                                    class="chosen-select form-control" id="category_id">
                                                                <option value="">Select category</option>
                                                                <?php
                                                                foreach (getAllNewsCategories() as $row) {
                                                                    ?>
                                                                    <option <?php
                                                                    if ($row['category_id'] == $news_row['category_id']) {
                                                                        echo "selected";
                                                                    } ?>
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
                                                            <h5 data-toggle="expand" data-target="#jb-expe">SEO
                                                                details</h5>
                                                            <div id="jb-expe" class="expand coll-box">
                                                                <input type="text" readonly="readonly" name="seo_title" class="form-control"
                                                                       value="<?php echo $news_row['seo_title']; ?>" placeholder="SEO Title">
                                                                <hr>
                                                                <input type="text" readonly="readonly" name="seo_description"
                                                                       class="form-control"
                                                                       value="<?php echo $news_row['seo_description']; ?>" placeholder="Meta descriptions">
                                                                <hr>
                                                                <input type="text" readonly="readonly" name="seo_keywords"
                                                                       value="<?php echo $news_row['seo_keywords']; ?>" class="form-control" placeholder="Meta keywords">
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
                                                    Delete
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