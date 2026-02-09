<?php
include "header.php";
?>
<?php if($admin_row['admin_country_options'] != 1){
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
                            <span class="udb-inst">Delete popular tag</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Popular Tag</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $popular_tag_codea = $_GET['row'];
                                    $popular_tag_row = getPopularTags($popular_tag_codea);

                                    ?>
                                    <form name="popular_tags_form" id="popular_tags_form" method="post" action="trash_popular_tags.php" class="cre-dup-form cre-dup-form-show">
                                        <input type="hidden" id="popular_tags_id" value="<?php echo $popular_tag_row['popular_tags_id']; ?>"
                                               name="popular_tags_id" class="validate">
                                        <ul>
                                            <li>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" readonly="readonly" value="<?php echo $popular_tag_row['popular_tags_name']; ?>" required="required" name="popular_tags_name" class="form-control" placeholder="Title text">
                                                        </div>
                                                    </div>
                                                </div>
                                                <hr>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" readonly="readonly" value="<?php echo $popular_tag_row['popular_tags_link']; ?>" required="required" name="popular_tags_link" class="form-control" placeholder="Link">
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        </ul>
                                        <button type="submit" name="popular_tags_submit" class="btn btn-primary">Delete</button>
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