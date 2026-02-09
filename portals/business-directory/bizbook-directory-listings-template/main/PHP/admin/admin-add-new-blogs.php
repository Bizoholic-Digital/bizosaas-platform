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
                    <span class="udb-inst">new post</span>
                    <div class="log log-1">
                        <div class="login">
                            <h4>Create post</h4>
                            <?php include "../page_level_message.php"; ?>
                            <form name="blog_form" id="blog_form" method="post" action="insert_blog.php" enctype="multipart/form-data">
                                <ul>
										<li>
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <select name="user_id" required="required" class="chosen-select form-control" id="user_id">
                                                    <option value="">Choose a user</option>
                                                    <?php
                                                    foreach (getAllUser() as $row) {
                                                        ?>
                                                        <option value="<?php echo $row['user_id']; ?>"><?php echo $row['first_name']; ?></option>
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
                                                <input type="text" name="blog_name" required="required" class="form-control" placeholder="Post name *">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                  <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea name="blog_description" id="blog_description" required="required" class="form-control" placeholder="Post details"></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
									<!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <label>Choose banner image</label>
                                                <input type="file" name="blog_image" required="required" class="form-control">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div>
                                                <div class="chbox">
                                                    <input type="checkbox" name="isenquiry"  id="evefmenab" checked="">
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
                                            <button type="submit" name="blog_submit" class="btn btn-primary">Submit</button>
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
<script src="../js/select-opt.js"></script>
<script src="ckeditor/ckeditor.js"></script>
<script>
    CKEDITOR.replace('blog_description');
</script>
</body>

</html>