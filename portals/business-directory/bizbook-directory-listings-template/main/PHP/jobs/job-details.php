<?php
include "job-config-info.php";
include "../header.php";

if($footer_row['admin_job_show'] != 1) {
    header("Location: ".$webpage_full_link."dashboard");
}

if (isset($_SESSION['user_id'])) {
    $session_user_id = $_SESSION['user_id'];
}
$user_details_row = getUser($session_user_id);


if ($_GET['code'] == NULL && empty($_GET['code'])) {

    header("Location: all-jobs");
}

$jobcodea1 = str_replace('-', ' ', $_GET['code']);
$jobcodea = str_replace('.php', '', $jobcodea1);

//$jobcodea = $_GET['code'];

$job_row = getSlugJob($jobcodea); //To Fetch the job

$job_id = $job_row['job_id'];
$job_user_id = $job_row['user_id'];
$job_category_id = $job_row['category_id'];

$redirect_url = $webpage_full_link . 'dashboard';  //Redirect Url

if ($job_id == NULL && empty($job_id)) {

    header("Location: $redirect_url");  //Redirect When No Jobs Found in Table
}

jobpageview($job_id); //Function To Find Page View

$usersqlrow = getUser($job_user_id); // To Fetch particular User Data


?>
<!-- START -->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> job-det-pg">
    <div class="container">
        <div class="row">
            <div class="job-det-desc">
                <!---->
                <div class="s1">
                    <h4 class="job-lhs-tit"><?php echo $BIZBOOK['COMPANY-PROFILE-HEADING-LABEL']; ?></h4>
                    <div class="job-comp-pro">
                        <div class="job-comp-img">
                            <img src="<?php echo $slash; ?>jobs/images/jobs/<?php echo $job_row['company_logo']; ?>"
                                 alt="">
                        </div>
                    </div>
                    <div class="job-comp-soc">
                        <ul>
                            <li class="ic-web"><a href="<?php echo $job_row['contact_website']; ?>" target="_blank"><?php echo $job_row['contact_website']; ?></a></li>
                            <li class="ic-user"><?php echo $job_row['contact_person']; ?></li>
                            <li class="ic-eml"><?php echo $job_row['contact_email_id']; ?></li>
                            <li class="ic-pho"><?php echo $job_row['contact_number']; ?></li>

                        </ul>
                    </div>
                    <div class="job-comp-abo">
                        <p><?php echo stripslashes($job_row['job_small_description']); ?></p>
                        <a href="<?php echo $job_row['contact_website']; ?>" target="_blank"
                           class="cta"><?php echo $BIZBOOK['COMP-PRO']; ?></a>
                    </div>
                </div>
                <!---->
                <!---->
                <div class="s2">
                    <div class="lhs">
                        <!--START-->
                        <h1><?php echo $job_row['job_title']; ?></h1>
                        <!--END-->
                        <!--START-->
                        <div class="desc">
                            <p><?php echo stripslashes($job_row['job_description']); ?></p>
                            <div class="jb-skil-set">
                                <h4><?php echo $BIZBOOK['JOB-SKILL-SET-LABEL']; ?>:</h4>
                                <ul>
                                    <?php
                                    $skill_set = explode(',', $job_row['skill_set']);
                                    foreach ($skill_set as $skill_set_id) {
                                        $skill_set_name = getJobSkill($skill_set_id);
                                        ?>
                                        <li><?php echo $skill_set_name['category_name']; ?></li>
                                        <?php
                                    }
                                    ?>
                                </ul>
                            </div>
                        </div>
                        <!--END-->

                        <!--START-->
                        <div class="alpply">
                            <?php
                            if (getCountJobAppliedProfileJob($session_user_id, $job_id) == 0) {
                                ?>
                                <span class="cta-app" data-toggle="modal"
                                      data-target="#apply"><?php echo $BIZBOOK['JOB_APPLY_THIS_JOB_NOW']; ?></span>
                                <?php
                            } else {
                                ?>
                                <span class="cta-app" data-toggle="modal"
                                      data-target="#!"><?php echo $BIZBOOK['JOB_ALREADY_APPLIED_THIS_JOB']; ?></span>
                                <?php
                            }
                            ?>
                        </div>
                        <!--END-->
                    </div>
                </div>
                <!---->
                <!---->
                <div class="s3">
                    <div class="rhs">
                        <!--START-->
                        <div class="job-summ">
                            <h4><?php echo $BIZBOOK['JOB_SUMMARY']; ?></h4>
                            <ul>
                                <li><span><?php echo $BIZBOOK['JOB-VACANCY']; ?>
                                        :</span> <?php echo AddingZero_BeforeNumber($job_row['no_of_openings']); ?></li>
                                <li><span><?php echo $BIZBOOK['JOB-TYPE-LABEL']; ?>:</span> <?php
                                    $job_type = $job_row['job_type'];
                                    if ($job_type == 1) {
                                        echo $BIZBOOK['JOB-PERMANENT'];
                                    } elseif ($job_type == 2) {
                                        echo $BIZBOOK['JOB-CONTRACT'];
                                    } elseif ($job_type == 3) {
                                        echo $BIZBOOK['JOB-PART-TIME'];
                                    } elseif ($job_type == 4) {
                                        echo $BIZBOOK['JOB-FREELANCE'];
                                    }
                                    ?></li>
                                <li><span><?php echo $BIZBOOK['OTHER_INFORMATIONS_PLACEHOLDER_LEFT']; ?>
                                        :</span> <?php echo $job_row['years_of_experience']; ?></li>
                                <li><span><?php echo $BIZBOOK['JOB-LOCATION-LABEL']; ?>
                                        :</span> <?php $job_location_row = getJobCity($job_row['job_location']); echo $job_location_row['city_name']; ?></li>
                                <li><span><?php echo $BIZBOOK['JOB-SALARY-LABEL']; ?>
                                        :</span> <?php echo $footer_row['currency_symbol']; ?><?php echo $job_row['job_salary']; ?>
                                </li>
                                <li><span><?php echo $BIZBOOK['JOB-INTERVIEW-ROLE-LABEL']; ?>
                                        :</span> <?php echo $job_row['job_role']; ?></li>
                                <li><span><?php echo $BIZBOOK['JOB_GENDER']; ?>:</span> Any</li>
                                <li><span><?php echo $BIZBOOK['JOB_EDUCATION']; ?>
                                        :</span> <?php echo $job_row['educational_qualification']; ?></li>
                                <li><span><?php echo $BIZBOOK['DATE']; ?>
                                        :</span> <?php echo dateFormatconverter($job_row['job_interview_date']); ?>
                                </li>
                                <li><span><?php echo $BIZBOOK['TIME']; ?>
                                        :</span><?php echo timeFormatconverter($job_row['job_interview_time']); ?></li>
                                <li><span><?php echo $BIZBOOK['JOB_PUBLISHED_ON']; ?>
                                        :</span> <?php echo dateFormatconverter($job_row['job_cdt']); ?></li>
                            </ul>
                            <?php
                            if (getCountJobAppliedProfileJob($session_user_id, $job_id) == 0) {
                                ?>
                                <span class="cta-app" data-toggle="modal"
                                      data-target="#apply"><?php echo $BIZBOOK['JOB_APPLY_NOW']; ?></span>
                                <?php
                            }else {
                                ?>
                                <span class="cta-app" data-toggle="modal"
                                      data-target="#!"><?php echo $BIZBOOK['JOB_ALREADY_APPLIED']; ?></span>
                                <?php
                            }
                            ?>
                        </div>
                        <!--END-->
                        <!--START-->
                        <div class="shar">
                            <h4><?php echo $BIZBOOK['JOB_SHARE']; ?></h4>
                            <span class="share-new-top share-ic-com" data-toggle="modal" data-target="#sharepop"><i class="material-icons">share</i></span>
                        </div>
                        <!--END-->
                    </div>

                </div>
                <!---->

            </div>

            <!--START-->
            <div class="job-tre">
                <h2><?php echo $BIZBOOK['JOB_RELATED_JOB_OPENINGS']; ?></h2>
                <ul>
                    <?php
                    foreach (getAllCategoryJobLimit($job_category_id, $job_id) as $job_profile_row) {

                        $job_id = $job_profile_row['job_id'];

                        $total_count_jobs_applied = getCountJobAppliedJob($job_id);
                        ?>
                        <li>
                            <div class="inn">
                                <div class="jbtre-img">
                                    <div class="jbtre-img1">
                                        <img
                                            src="<?php echo $slash; ?>jobs/images/jobs/<?php echo $job_profile_row['company_logo']; ?>"
                                            alt="">
                                    </div>
                                    <div class="jbtre-img2">
                                        <h4><?php echo $job_profile_row['job_title']; ?></h4>
                                        <span><?php $job_location_row = getJobCity($job_profile_row['job_location']); echo $job_location_row['city_name']; ?></span>
                                        <div class="jbtre-days">
                                            <span><?php echo time_elapsed_string($job_profile_row['job_cdt']); ?></span>
                                            <span><?php echo $total_count_jobs_applied; ?> <?php echo $BIZBOOK['APPLICANTS']; ?></span>
                                        </div>
                                    </div>
                                </div>
                                <div class="jbtre-con">
                                        <span><?php
                                            $job_type = $job_profile_row['job_type'];
                                            if ($job_type == 1) {
                                                echo $BIZBOOK['JOB-PERMANENT'];
                                            } elseif ($job_type == 2) {
                                                echo $BIZBOOK['JOB-CONTRACT'];
                                            } elseif ($job_type == 3) {
                                                echo $BIZBOOK['JOB-PART-TIME'];
                                            } elseif ($job_type == 4) {
                                                echo $BIZBOOK['JOB-FREELANCE'];
                                            }
                                            ?></span>
                                    <span><?php echo $job_profile_row['job_role']; ?></span>
                                    <span><?php echo AddingZero_BeforeNumber($job_profile_row['no_of_openings']); ?> <?php echo $BIZBOOK['JOB_OPENINGS']; ?></span>
                                </div>
                                <div class="jbtre-sale">
                                    <span><?php echo $BIZBOOK['JOB-SALARY-LABEL']; ?></span>
                                    <span class="empsal"><?php echo $footer_row['currency_symbol']; ?><?php echo $job_profile_row['job_salary']; ?></span>
                                </div>
                                <div class="jbtre-apl">
                                    <span class="job-box-cta"><?php echo $BIZBOOK['JOB_APPLY_NOW']; ?></span>
                                    <span><?php echo $BIZBOOK['JOB_MORE_DETAILS']; ?></span>
                                </div>
                                <a href="<?php echo $JOB_URL . urlModifier($job_profile_row['job_slug']); ?>"
                                   class="job-full-cta"></a>
                            </div>
                        </li>
                        <?php
                    }
                    ?>
                </ul>
            </div>
            <!--END-->
        </div>
    </div>
</section>
<!--END-->


<?php
include "../footer.php";
?>
<section>
    <div class="pop-ups pop-quo">
        <!-- The Modal -->
        <div class="modal fade" id="apply">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="log-bor">&nbsp;</div>
                    <span class="udb-inst"><?php echo $BIZBOOK['JOB_APPLY_THIS_JOB']; ?></span>
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                    <!-- Modal Header -->
                    <div class="quote-pop">
                        <div id="pop_enq_success" class="log" style="display: none;">
                            <p><?php echo $BIZBOOK['JOB_ENQUIRY_SUCCESSFUL_MESSAGE']; ?></p>
                        </div>
                        <div id="pop_enq_same" class="log" style="display: none;">
                            <p><?php echo $BIZBOOK['JOB_ENQUIRY_OWN_JOB_MESSAGE']; ?></p>
                        </div>
                        <div id="pop_enq_already_applied" class="log" style="display: none;">
                            <p><?php echo $BIZBOOK['JOB_ENQUIRY_ALREADY_APPLIED_JOB_MESSAGE']; ?></p>
                        </div>
                        <div id="pop_enq_no_profile" class="log" style="display: none;">
                            <p><?php echo $BIZBOOK['JOB_ENQUIRY_NO_PROFILE_MESSAGE']; ?> </p>
                        </div>
                        <div id="pop_enq_fail" class="log" style="display: none;">
                            <p><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></p>
                        </div>
                        <form method="post" name="popup_job_enquiry_form" id="popup_job_enquiry_form">
                            <input type="hidden" class="form-control" name="job_id"
                                   value="<?php echo $job_row['job_id']; ?>"
                                   placeholder=""
                                   required>
                            <input type="hidden" class="form-control"
                                   name="job_user_id"
                                   value="<?php echo $job_user_id; ?>" placeholder=""
                                   required>
                            <input type="hidden" class="form-control"
                                   name="enquiry_sender_id"
                                   value="<?php echo $session_user_id; ?>"
                                   placeholder=""
                                   required>
                            <input type="hidden" class="form-control"
                                   name="enquiry_source"
                                   value="<?php if (isset($_GET["src"])) {
                                       echo $_GET["src"];
                                   } else {
                                       echo "Website";
                                   }; ?>"
                                   placeholder=""
                                   required>
                            <div class="form-group">
                                <input type="text" name="enquiry_name"
                                       value="<?php echo $user_details_row['first_name'] ?>"
                                       required="required" class="form-control"
                                       placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>">
                            </div>
                            <div class="form-group">
                                <input type="email" class="form-control"
                                       placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>" required="required"
                                       value="<?php echo $user_details_row['email_id'] ?>"
                                       name="enquiry_email"
                                       pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>">
                            </div>
                            <div class="form-group">
                                <input type="text" class="form-control"
                                       value="<?php echo $user_details_row['mobile_number'] ?>"
                                       name="enquiry_mobile"
                                       placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>"
                                       pattern="[7-9]{1}[0-9]{9}"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>"
                                       required>
                            </div>
                            <input type="hidden" id="source">
                            <button <?php if ($session_user_id == NULL || empty($session_user_id)) {
                                ?> disabled="disabled" <?php } ?> type="submit" id="popup_job_enquiry_submit"
                                                                  name="popup_job_enquiry_submit"
                                                                  class="btn btn-primary"><?php if ($session_user_id == NULL || empty($session_user_id)) {
                                    ?><?php echo $BIZBOOK['LOG_IN_TO_SUBMIT']; ?><?php } else { ?><?php echo $BIZBOOK['SUBMIT']; ?><?php } ?></button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>


<!-- SHARE POPUP -->
<div class="modal fade sharepop" id="sharepop">
    <div class="modal-dialog modal-sm">
        <div class="modal-content">

            <!-- Modal Header -->
            <div class="modal-header">
                <h4 class="modal-title">Share now</h4>
                <button type="button" class="close" data-dismiss="modal">&times;</button>
            </div>

            <!-- Modal body -->
            <div class="modal-body">
                <input type="text" value="" id="shareurl">
                <div class="shareurltip">
                    <button onclick="shareurl()" onmouseout="shareurlout()">
                        <span class="shareurltxt" id="myTooltip">Copy to clipboard</span>
                        Copy text                    </button>
                </div>
            </div>

        </div>
    </div>
</div>

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>
</body>
</html>