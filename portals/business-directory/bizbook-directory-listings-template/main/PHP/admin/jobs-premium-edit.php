<?php
include "header.php";
?>

<?php if ($footer_row['admin_job_show'] != 1 || $admin_row['admin_jobs_options'] != 1) {
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
                            <span class="udb-inst">Edit Premium Jobs</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Edit this Premium Job</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $job_popular_id = $_GET['row'];
                                    $row = getJobPopular($job_popular_id);

                                    ?>
                                    <form name="listing_form" id="listing_form" method="post" action="update_job_premium.php" enctype="multipart/form-data">

                                        <input type="hidden" class="validate" id="job_name_old" name="job_name_old" value="<?php echo $row['job_name']; ?>" required="required">
                                        <input type="hidden" class="validate" id="job_popular_id" name="job_popular_id" value="<?php echo $row['job_popular_id']; ?>" required="required">
                                        <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select name="job_name" class="form-control" id="job_name">

                                                                <?php
                                                                foreach (getAllJob() as $li_row){
                                                                    ?>
                                                                    <option
                                                                        value="<?php echo $li_row['job_id']; ?>" <?php if ($li_row['job_id'] == $row['job_name']) {
                                                                        echo "selected";
                                                                    } ?> ><?php echo $li_row['job_title']; ?>
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
                                                <button type="submit" name="job_premium_submit" class="btn btn-primary">Update</button>
                                            </div>
                                            <div class="col-md-12">
                                                <a href="jobs-premium.php" class="skip">Go to All Jobs Premium >></a>
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
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>