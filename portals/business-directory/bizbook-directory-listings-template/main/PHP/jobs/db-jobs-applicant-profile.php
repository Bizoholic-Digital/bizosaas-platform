<?php
include "job-config-info.php";
include "../header.php";

if (file_exists('../config/user_authentication.php')) {
    include('../config/user_authentication.php');
}

if (file_exists('../config/general_user_authentication.php')) {
    include('../config/general_user_authentication.php');
}

if (file_exists('../config/job_page_authentication.php')) {
    include('../config/job_page_authentication.php');
}

include "../dashboard_left_pane.php";

$job_codea = $_GET['code'];
$job_a_row = getJob($job_codea);

$job_id = $job_a_row['job_id'];

?>
    <!--CENTER SECTION-->
    <div class="ud-main">
   <div class="ud-main-inn ud-no-rhs">
    <div class="ud-cen">
        <div class="log-bor">&nbsp;</div>
        <span class="udb-inst"><?php echo $BIZBOOK['JOB_ALL_APPLI_PROFILE']; ?></span>
        <?php include('../config/user_activation_checker.php'); ?>
        <div class="ud-cen-s2">
            <h2><?php echo $BIZBOOK['JOB_APPLI_DETAILS']; ?></h2>
            <?php include "../page_level_message.php"; ?>
<!--            <a href="#" class="db-tit-btn">--><?php //echo $BIZBOOK['JOB_APPLI_DOWNLOAD']; ?><!--</a>-->
            <p><?php echo $BIZBOOK['JOB']; ?> : <?php echo $job_a_row['job_title']; ?></p>
            <table class="responsive-table bordered">
                <thead>
                <tr>
                    <th><?php echo $BIZBOOK['S_NO']; ?></th>
                    <th><?php echo $BIZBOOK['JOB_APPLI_NAME']; ?></th>
                    <th><?php echo $BIZBOOK['JOB_APPLI_PHONE']; ?></th>
                    <th><?php echo $BIZBOOK['JOB_APPLI_EMAIL']; ?></th>
                    <th><?php echo $BIZBOOK['JOB_APPLI_DATE']; ?></th>
                    <th><?php echo $BIZBOOK['JOB_APPLI_RESUME']; ?></th>
                    <th><?php echo $BIZBOOK['DELETE']; ?></th>
                    <th><?php echo $BIZBOOK['PREVIEW']; ?></th>
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
                        <td><a href="<?php echo $slash; ?>jobs/images/jobs/<?php echo $job_profile_row['job_profile_resume']; ?>" download="<?php echo $user_row['first_name'].' - Resume'; ?>" class="db-list-edit" title="Download user profile"><span
                                    class="material-icons">file_download</span></a></td>
                        <td><a href="job_applied_trash.php?jobappliedjobappliedjobappliedjobapplied=<?php echo $job_applied_id; ?>&&code=<?php echo $job_codea; ?>" class="db-list-edit"><span class="material-icons">delete</span></a></td>
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
<?php
include "../dashboard_right_pane.php";
?>