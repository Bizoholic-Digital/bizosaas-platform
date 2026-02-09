<?php
include "header.php";
?>

<?php if($footer_row['admin_blog_show'] !=1 || $admin_row['admin_blog_options'] != 1){
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
                            <span class="udb-inst">Delete post</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Delete this post</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $blog_codea = $_GET['row'];
                                    $blogs_a_row = getBlog($blog_codea);
                                    ?>
                                    <form action="trash_blog.php" class="blog_delete_form" id="blog_delete_form" name="blog_delete_form"
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
                                                            <select name="user_id" required="required" disabled="disabled" class="form-control" id="user_id">
                                                                <option value="">Choose a user</option>
                                                                <?php
                                                                foreach (getAllUser() as $row) {

                                                                    ?>
                                                                    <option <?php if($blogs_a_row['user_id']== $row['user_id']){ echo "selected"; } ?>
                                                                        value="<?php echo $row['user_id']; ?>"><?php echo $row['first_name']; ?></option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" name="blog_name"
                                                                   value="<?php echo $blogs_a_row['blog_name']; ?>" readonly="readonly" required="required" class="form-control" placeholder="Post name *">                                            </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <textarea name="blog_description" required="required" readonly="readonly" class="form-control" placeholder="Post details"><?php echo $blogs_a_row['blog_description']?></textarea>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div>
                                                            <div class="chbox">
                                                                <input type="checkbox" disabled="disabled" name="isenquiry" id="evefmenab" <?php if($blogs_a_row['isenquiry'] == 1){ ?>checked="" <?php }?>>
                                                                <label for="evefmenab">Enquiry or Get quote form enable</label>
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
                                                <button type="submit" name="blog_submit" class="btn btn-primary">Delete</button>
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
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>