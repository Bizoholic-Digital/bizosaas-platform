<?php
include "header.php";
?>

<?php if($footer_row['admin_job_show'] != 1 || $admin_row['admin_jobs_options'] != 1){
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
                            <span class="udb-inst">New Job Category</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Add New Job Category</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <span class="add-list-add-btn job-cate-add-btn" data-toggle="tooltip" title="Click to make additional category">+</span>
                                    <span class="add-list-rem-btn job-cate-rem-btn" data-toggle="tooltip" title="Click to remove last category">-</span>
                                    <form name="category_form" id="category_form" method="post" action="insert_job_category.php" class="cre-dup-form cre-dup-form-show" enctype="multipart/form-data">
                                        <ul>
                                            <li>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" id="category_name" name="category_name[]" class="form-control" placeholder="Category name *" required>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        </ul>
                                        <button type="submit" name="category_submit" class="btn btn-primary">Submit</button>
                                    </form>
                                    <div class="col-md-12">
                                        <a href="admin-all-job-category.php" class="skip">Go to All Category >></a>
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