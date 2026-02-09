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
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Home Page Premium Jobs</span>
                <div class="ud-cen-s2 hcat-cho">
                    <h2>Home Page Premium Jobs</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Job Name</th>
                            <th>Edit</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;

                        foreach (getAllJobPopular() as $row) {

                            $job_name = $row['job_name'];

                            $job_popular_id = $row['job_popular_id'];

                            $job_sql_row = getIdJob($job_name);

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $job_sql_row['job_title']; ?></td>
                                <td><a href="jobs-premium-edit.php?row=<?php echo $job_popular_id; ?>"
                                       class="db-list-edit">Edit</a></td>
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
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>

</body>

</html>