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
                <span class="udb-inst">All Jobs</span>
                <div class="ud-cen-s2">
                    <h2>All Job Posts</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div style="display: none" class="static-success-message log-suc"><p>Job(s) has been Permanently Deleted!!! Please wait for automatic page refresh!! </p></div>
                    <a href="job-create.php" class="db-tit-btn">Add new Job opening</a>
                    <table class="responsive-table bordered" id="pg-resu">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Job name</th>
                                    <th>Job Posted By</th>
									<th>No of Applicant</th>
                                    <th>Applicant profile</th>
                                    <th>Views</th>
									<th>Edit</th>
									<th>Delete</th>
									<th>Preview</th>
                                    <th><input type="checkbox" class="checkall" id="checkall"><input type="button" style="display: none" class='multi-del-btn' id='delete_record' value='Delete' ></th>
                                </tr>
							</thead>
							<tbody>
                            <?php
                            $si = 1;
                            foreach (getAllJob() as $jobrow) {

                                $job_id = $jobrow['job_id'];

                                $user_id = $jobrow['user_id'];

                                $applied_job_count = getCountJobAppliedJob($job_id);

                                $user_row = getUser($user_id);

                                ?>
                                <tr>
                                    <td><?php echo $si; ?></td>
                                    <td><?php echo $jobrow['job_title']; ?><span><?php echo dateFormatconverter($jobrow['job_cdt']); ?></span></td>
                                    <td><span class="db-list-rat"><?php echo $user_row['first_name']; ?></span></td>
                                    <td><span class="db-list-rat"><?php echo AddingZero_BeforeNumber($applied_job_count); ?></span></td>
                                    <td><a href="job-applicant-profiles.php?code=<?php echo $jobrow['job_code']; ?>" class="db-list-rat">View profiles</a></td>
                                    <td><span class="db-list-rat"><?php echo AddingZero_BeforeNumber(job_pageview_count($jobrow['job_id'])); ?></span></td>
                                    <td><a href="job-edit.php?code=<?php echo $jobrow['job_code']; ?>" class="db-list-edit"><span class="material-icons">edit</span></a>
                                    </td>
                                    <td><a href="job-delete.php?code=<?php echo $jobrow['job_code']; ?>" class="db-list-edit"><span class="material-icons">delete</span></a>
                                    </td>
                                    <td><a href="<?php echo $JOB_URL . urlModifier($jobrow['job_slug']); ?>" class="db-list-edit" target="_blank"><span class="material-icons">visibility</span></a>
                                    </td>
                                    <td><input type='checkbox' class='delete_check' id='delcheck_<?php echo $job_id; ?>' onclick='checkcheckbox();' value='<?php echo $job_id; ?>'></td>
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
<script src="../js/select-opt.js"></script>
<script src="../js/select-opt.js"></script>
<script src="https://code.jquery.com/jquery-3.3.1.js"></script>
<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap4.min.js"></script>
<script src="js/admin-custom.js"></script>
<script>
    $(document).ready(function () {
        $('#pg-resu').DataTable({
            "columnDefs": [
                { "bSortable": false, "aTargets": [ 8 ] }
            ]
        });
    });
</script>

<script>
    $('#delete_record').click(function(){

        var deleteids_arr = [];
        // Read all checked checkboxes
        $("input:checkbox[class=delete_check]:checked").each(function () {
            deleteids_arr.push($(this).val());
        });

        // Check checkbox checked or not
        if(deleteids_arr.length > 0){

            // Confirm alert
            var confirmdelete = confirm("Do you really want to Delete records?");
            if (confirmdelete == true) {
                $.ajax({
                    url: 'multiple_delete_users.php',
                    type: 'post',
                    data: {request: 7,deleteids_arr: deleteids_arr},
                    success: function(response){
                        $('.static-success-message').css("display", "block");
                        window.setTimeout(function(){location.reload()},3000)
                    }
                });
            }
        }
    });
</script>
</body>

</html>