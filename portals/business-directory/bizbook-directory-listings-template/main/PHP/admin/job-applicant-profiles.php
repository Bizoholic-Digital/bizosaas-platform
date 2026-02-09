<?php
include "header.php";
?>

<?php if($admin_row['admin_job_options'] != 1){
    header("Location: profile.php");
}

$job_codea = $_GET['code'];
$job_a_row = getJob($job_codea);

$job_id = $job_a_row['job_id'];

?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Applicants list</span>
                <div class="ud-cen-s2">
                    <h2>Job Applicants</h2>
                    <?php include "../page_level_message.php"; ?>
                    <a href="#" class="db-tit-btn">Download all profiles</a>
                    <p><?php echo "Job" ?> : <?php echo $job_a_row['job_title']; ?></p>
                    <table class="responsive-table bordered">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Applicant name</th>
									<th>Phone</th>
                                    <th>Email</th>
                                    <th>Date</th>
                                    <th>Resume</th>
									<th>Delete</th>
									<th>Preview</th>
								</tr>
							</thead>
							<tbody>
                            <?php

                            $si = 1;
                            foreach (getJobAppliedJob($job_id) as $jobrow) {

                            $job_applied_id = $jobrow['job_applied_id'];

                            $job_profile_id = $jobrow['job_profile_id'];

                            $job_profile_row = getUserJobProfile($job_profile_id);

                            $user_id = $job_profile_row['user_id'];

                            $user_row = getUser($user_id);
                            ?>
                                <tr>
                                    <td><?php echo $si; ?></td>
                                    <td><?php echo $user_row['first_name']; ?></td>
                                    <td><?php echo $user_row['mobile_number']; ?></td>
                                    <td><?php echo $user_row['email_id']; ?></td>
                                    <td><?php echo timeFormatconverter($jobrow['job_applied_cdt']); ?>, <?php echo dateFormatconverter($jobrow['job_applied_cdt']); ?></td>
                                    <td><a href="../jobs/images/jobs/<?php echo $job_profile_row['job_profile_resume']; ?>" download="<?php echo $user_row['first_name'].' - Resume'; ?>" class="db-list-edit" title="Download user profile"><span
                                                class="material-icons">file_download</span></a></td>
                                    <td><a href="trash_job_applied.php?jobappliedjobappliedjobappliedjobapplied=<?php echo $job_applied_id; ?>" class="db-list-edit"><span class="material-icons">delete</span></a></td>
                                    <td><a href="<?php echo $JOB_PROFILE_URL . urlModifier($job_profile_row['job_profile_slug']); ?>" target="_blank" class="db-list-edit"
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
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>