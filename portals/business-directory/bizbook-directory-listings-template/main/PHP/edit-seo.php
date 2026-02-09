<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

if (file_exists('config/general_user_authentication.php')) {
    include('config/general_user_authentication.php');
}

?>
<!-- START -->
<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg">
    <div class="container">
        <div class="row">
            <div class="login-main add-list">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['SEO']; ?></span>
                <div class="log">
                    <div class="login add-list-off">
                        <?php
                        $seo_codea = $_GET['code'];
                        $path = $_GET['path'];

                        if ($path == 'listing') {

                            $seos_a_row = getListing($seo_codea);
                            $name = $seos_a_row['listing_name'];
                            $id = $seos_a_row['listing_id'];
                        } elseif ($path == 'event') {
                            $seos_a_row = getEvent($seo_codea);
                            $name = $seos_a_row['event_name'];
                            $id = $seos_a_row['event_id'];
                        } elseif ($path == 'blog') {
                            $seos_a_row = getBlog($seo_codea);
                            $name = $seos_a_row['blog_name'];
                            $id = $seos_a_row['blog_id'];
                        } elseif ($path == 'product') {
                            $seos_a_row = getProduct($seo_codea);
                            $name = $seos_a_row['product_name'];
                            $id = $seos_a_row['product_id'];
                        } else {
                            header("Location: db-seo");
                            exit();
                        }


                        ?>
                        <h4><?php echo $BIZBOOK['EDIT_THIS_SEO']; ?></h4>
                        <?php include "page_level_message.php"; ?>
                        <form action="seo_update.php" class="seo_edit_form" id="seo_edit_form" name="seo_edit_form"
                              method="post" enctype="multipart/form-data">

                            <input type="hidden" id="path" value="<?php echo $path; ?>"
                                   name="path" class="validate">
                            <input type="hidden" id="id" value="<?php echo $id; ?>"
                                   name="id" class="validate">

                            <ul>
                                <li>
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" readonly="readonly" name="seo_name"
                                                       required="required" class="form-control"
                                                       value="<?php echo $name; ?>" placeholder="<?php echo $BIZBOOK['SEO_NAME']; ?>">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" name="seo_title" class="form-control"
                                                       value="<?php echo $seos_a_row['seo_title']; ?>"
                                                       placeholder="<?php echo $BIZBOOK['SEO_TITLE']; ?>">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea class="form-control" required="required"
                                                          name="seo_description" id="seo_description"
                                                          placeholder="<?php echo $BIZBOOK['SEO_DESCRIPTION']; ?>"><?php echo $seos_a_row['seo_description'] ?></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea class="form-control" name="seo_keywords"
                                                          placeholder="<?php echo $BIZBOOK['SEO_KEYWORDS']; ?>"><?php echo $seos_a_row['seo_keywords']; ?></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->

                                </li>
                            </ul>
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <button type="submit" name="seo_submit"
                                            class="btn btn-primary"><?php echo $BIZBOOK['SAVE_CHANGES']; ?></button>
                                </div>
                                <div class="col-md-12">
                                    <a href="dashboard" class="skip"><?php echo $BIZBOOK['GO_TO_USER_DASHBOARD']; ?>
                                        >></a>
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
<!--END PRICING DETAILS-->


<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>
</body>

</html>