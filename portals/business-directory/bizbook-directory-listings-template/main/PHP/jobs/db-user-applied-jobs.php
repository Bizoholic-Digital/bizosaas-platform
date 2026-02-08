<?php
include "job-config-info.php";
include "../header.php";

if (file_exists('../config/user_authentication.php')) {
    include('../config/user_authentication.php');
}

if (file_exists('../config/job_page_authentication.php')) {
    include('../config/job_page_authentication.php');
}

include "../dashboard_left_pane.php";

?>
    <!--CENTER SECTION-->
    <div class="ud-main">
   <div class="ud-main-inn ud-no-rhs">
    <div class="ud-cen">
        <div class="log-bor">&nbsp;</div>
        <span class="udb-inst"><?php echo $BIZBOOK['ALL_APPLIED_JOBS']; ?></span>
        <?php include('../config/user_activation_checker.php'); ?>
        <div class="ud-cen-s2">
            <h2><?php echo $BIZBOOK['JOB_APPLI_DETAILS']; ?></h2>
            <?php include "../page_level_message.php"; ?>
            <table class="responsive-table bordered">
                <thead>
                <tr>
                    <th><?php echo $BIZBOOK['S_NO']; ?></th>
                    <th><?php echo $BIZBOOK['JOB-TITLE-LABEL']; ?></th>
                    <th><?php echo $BIZBOOK['JOB_APPLI_DATE']; ?></th>
                    <th><?php echo $BIZBOOK['PREVIEW']; ?></th>
                </tr>
                </thead>
                <tbody>
                <?php
                $si = 1;
                foreach (getJobAppliedJobProfile($_SESSION['user_id']) as $jobrow) {

                    $job_id = $jobrow['job_id'];

                    $job_row = getIdJob($job_id);

                    $job_slug = $job_row['job_slug'];
                    ?>
                    <tr>
                        <td><?php echo $si; ?></td>
                        <td><?php echo $job_row['job_title']; ?></td>
                        <td><?php echo dateFormatconverter($jobrow['job_applied_cdt']); ?>, <?php echo timeFormatconverter($jobrow['job_applied_cdt']); ?></td>
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
<?php
include "../dashboard_right_pane.php";
?>