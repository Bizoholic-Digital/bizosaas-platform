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
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Applied Jobs list</span>
                <div class="ud-cen-s2">
                    <h2>All Applied Jobs</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Job Title</th>
                            <th>Applied By</th>
                            <th>Applied Date</th>
                            <th>Delete</th>
                            <th>Preview</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php

                        $si = 1;
                        foreach (getAllJobApplied() as $jobrow) {

                            $job_id = $jobrow['job_id'];

                            $job_applied_id = $jobrow['job_applied_id'];

                            $job_profile_id = $jobrow['job_profile_id'];

                            $job_row = getIdJob($job_id);

                            $job_profile_row = getUserJobProfile($job_profile_id);

                            $job_slug = $job_row['job_slug'];

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $job_row['job_title']; ?></td>
                                <td><?php echo $job_profile_row['profile_name']; ?></td>
                                <td><?php echo dateFormatconverter($jobrow['job_applied_cdt']); ?>, <?php echo timeFormatconverter($jobrow['job_applied_cdt']); ?></td>
                                <td><a href="trash_job_applied.php?jobappliedjobappliedjobappliedjobapplied=<?php echo $job_applied_id; ?>&path=2" class="db-list-edit"><span class="material-icons">delete</span></a></td>
                                <td><a href="<?php echo $JOB_URL . urlModifier($job_row['job_slug']); ?>" target="_blank" class="db-list-edit"
                                       title="View user profile page"><span
                                            class="material-icons">visibility</span></a></td>
                            </tr>
                            <?php
                            $si++;
                        }
                        ?>
                        </tbody>
                    </table>
                </div>

            </div>
            <div class="ad-pgnat">
                <ul class="pagination">
                    <li class="page-item"><a class="page-link" href="#">Previous</a></li>
                    <li class="page-item active"><a class="page-link" href="#">1</a></li>
                    <li class="page-item"><a class="page-link" href="#">2</a></li>
                    <li class="page-item"><a class="page-link" href="#">3</a></li>
                    <li class="page-item"><a class="page-link" href="#">Next</a></li>
                </ul>
            </div>
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
</body>

</html>