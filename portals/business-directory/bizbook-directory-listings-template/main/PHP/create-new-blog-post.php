<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

if (file_exists('config/general_user_authentication.php')) {
    include('config/general_user_authentication.php');
}

if (file_exists('config/blog_page_authentication.php')) {
    include('config/blog_page_authentication.php');
}
//To check the blogs count with current plan starts

$plan_type_blog_count = $user_plan_type['plan_type_blog_count'];
$blog_count_user = getCountUserBlog($_SESSION['user_id']);

if ($blog_count_user >= $plan_type_blog_count) {

    $_SESSION['status_msg'] = $BIZBOOK['BLOGS_LIMIT_EXCEED_MESSAGE'];

    header('Location: db-blog-posts');
    exit();
}
//To check the blogs count with current plan ends

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
                <span class="steps"><?php echo $BIZBOOK['ADD_NEW_BLOG_POST']; ?></span>
                <div class="log">
                    <div class="login add-list-off">

                        <h4><?php echo $BIZBOOK['CREATE_BLOG_POST']; ?></h4>
                        <form action="blog_insert.php" class="blog_form" id="blog_form" name="blog_form"
                              method="post" enctype="multipart/form-data">
                            <ul>
                                <li>
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" name="blog_name" required="required"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['POST_NAME']; ?>*">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <!--<div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <div class="bixedtr">
                                                    <div class="biz-toolbar bixedtr-tools"></div>
                                                    <div id='bizeditor' class="bizeditorpan" contenteditable>
                                                      <h2>Hero Heading</h2>
                                                      <p>Try making some changes here. Add your own text here..</p>
                                                       <p>Try making some changes here. Add your own text here..</p>
                                                      <h4>Hero heading 2</h4>
                                                      <p>Try making some changes here. Add your own text or maybe an image.</p>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>-->
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea name="blog_description" id="blog_description"
                                                          required="required" class="form-control"
                                                          placeholder="<?php echo $BIZBOOK['POST_DETAILS']; ?>"></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <label><?php echo $BIZBOOK['CHOOSE_BANNER_IMAGE']; ?></label>
                                                <div class="fil-img-uplo">
                                                    <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                                    <input type="file" name="blog_image" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                                </div>       
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div>
                                                <div class="chbox">
                                                    <input type="checkbox" name="isenquiry" id="evefmenab" checked="">
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
                                            class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
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