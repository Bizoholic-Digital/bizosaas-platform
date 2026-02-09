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
                            <span class="udb-inst">Edit Trending News</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Edit this Trending News</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $trending_news_id = $_GET['row'];
                                    $row = getNewsTrending($trending_news_id);

                                    ?>
                                    <form name="home_news_trending_form" id="home_news_trending_form" method="post" action="update_home_news_trending.php" enctype="multipart/form-data">

                                        <input type="hidden" class="validate" id="news_id_old" name="news_id_old" value="<?php echo $row['news_id']; ?>" required="required">
                                        <input type="hidden" class="validate" id="trending_news_id" name="trending_news_id" value="<?php echo $row['trending_news_id']; ?>" required="required">
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
                                                                        value="<?php echo $li_row['news_id']; ?>" <?php if ($li_row['news_id'] == $row['news_id']) {
                                                                        echo "selected";
                                                                    } ?> ><?php echo stripslashes($li_row['news_title']); ?>
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
                                                <button type="submit" name="home_news_trend_submit" class="btn btn-primary">Update</button>
                                            </div>
                                            <div class="col-md-12">
                                                <a href="news-home-trending.php" class="skip">Go to Trending News >></a>
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
<script src="js/admin-custom.js"></script> <script src="http://harvesthq.github.io/chosen/chosen.jquery.js"></script>
</body>

</html>