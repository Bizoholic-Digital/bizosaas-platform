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
                <span class="steps"><?php echo $BIZBOOK['DELETE_BLOG_POST']; ?></span>
                <div class="log">
                    <div class="login add-list-off">
                        <?php
                        $blog_codea = $_GET['code'];
                        $blogs_a_row = getBlog($blog_codea);

                        ?>
                        <h4><?php echo $BIZBOOK['DELETE_THIS_BLOG_POST']; ?></h4>
                        <form action="blog_delete.php" class="blog_delete_form" id="blog_delete_form"
                              name="blog_delete_form"
                              method="post" enctype="multipart/form-data">

                            <input type="hidden" id="blog_id" value="<?php echo $blogs_a_row['blog_id']; ?>"
                                   name="blog_id" class="validate">
                            <input type="hidden" id="blog_image_old"
                                   value="<?php echo $blogs_a_row['blog_image']; ?>" name="blog_image_old"
                                   class="validate">

                            <ul>
                                <li>
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" name="blog_name"
                                                       value="<?php echo $blogs_a_row['blog_name']; ?>"
                                                       readonly="readonly" class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['POST_NAME']; ?>*">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea name="blog_description" readonly="readonly"
                                                          class="form-control"
                                                          placeholder="<?php echo $BIZBOOK['POST_DETAILS']; ?>"><?php echo $blogs_a_row['blog_description'] ?></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="isenquiry"
                                                           id="evefmenab"
                                                           <?php if ($blogs_a_row['isenquiry'] == 1){ ?>checked="" <?php } ?>>
                                                    <label
                                                        for="evefmenab"><?php echo $BIZBOOK['ENQUIRY_BOX_ENABLE']; ?></label>
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
                                    <button type="submit" name="blog_submit"
                                            class="btn btn-primary"><?php echo $BIZBOOK['DELETE_BLOG']; ?></button>
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
</body>

</html>