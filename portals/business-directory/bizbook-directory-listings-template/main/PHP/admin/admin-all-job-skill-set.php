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
                <span class="udb-inst">Job Skill Set</span>
                <div class="ud-cen-s2 hcat-cho">
                    <h2>All Job Skill Set</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <a href="admin-add-new-job-skill-set.php" class="db-tit-btn">Add new job skill</a>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Skill Set Name</th>
                            <th>Created date</th>
                            <th>Edit</th>
                            <th>Delete</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si=1;
                        foreach (getAllJobSkill() as $row) {

                            $category_id = $row['category_id'];

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><b class="db-list-rat"><?php echo $row['category_name']; ?></b></td>
                                <td><?php echo dateFormatconverter($row['category_cdt']); ?></td>
                                <td><a href="admin-job-skill-set-edit.php?row=<?php echo $row['category_id']; ?>" class="db-list-edit">Edit</a></td>
                                <td><a href="admin-job-skill-set-delete.php?row=<?php echo $row['category_id']; ?>" class="db-list-edit">Delete</a></td>
                            </tr>
                            <?php
                            $si++;
                        }
                        ?>
                        </tbody>
                    </table>
                </div>
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