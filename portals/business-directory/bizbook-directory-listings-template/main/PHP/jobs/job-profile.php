<?php
include "job-config-info.php";
include "../header.php";

if($footer_row['admin_job_show'] != 1) {
    header("Location: ".$webpage_full_link."dashboard");
}

$redirect_url = $webpage_full_link . 'dashboard';  //Redirect Url

if ($_GET['code'] == NULL && empty($_GET['code'])) {

    header("Location: $redirect_url");  //Redirect When code parameter is empty
}

//$job_profile_codea = $_GET['code'];
$job_profile_codea1 = str_replace('-', ' ', $_GET['code']);

$job_profile_codea = str_replace('.php', '', $job_profile_codea1);

$job_profile_row = getJobProfileSlug($job_profile_codea); // To Fetch particular User Data

if ($job_profile_row['job_profile_id'] == NULL && empty($job_profile_row['job_profile_id'])) {

    header("Location: $redirect_url");  //Redirect When No User Found in Table
}

$job_profile_id = $job_profile_row['job_profile_id'];

$job_profile_user_id = $job_profile_row['user_id'];

$job_profile_category_id = $job_profile_row['category_id'];

$job_profile_sub_category_id = $job_profile_row['sub_category_id'];

$job_profile_category_row = getJobCategory($job_profile_category_id);

$job_profile_sub_category_row = getJobSubCategory($job_profile_sub_category_id);

$job_category_name = $job_profile_category_row['category_name'];

$job_sub_category_name = $job_profile_sub_category_row['sub_category_name'];

$user_details_row = getUser($job_profile_user_id);

jobprofilepageview($job_profile_id); //Function To Find Page View

?>

<!-- START -->
<section>
    <div class="job-prof-pg">
        <div class="container">
            <div class="row">
                <div class="lhs">
                    <!--START-->
                    <div class="profile">
                        <div class="jpro-ban-bg-img">
                            <span><b><?php if($user_details_row['user_followers'] != ''){ echo substr_count($user_details_row['user_followers'], ",")+1; } else{ echo "0"; }?></b> <?php echo $BIZBOOK['FOLLOWERS']; ?></span>
                            <p><?php echo $BIZBOOK['JOB-INTERVIEW-AVAILABLE-TIME-TO-TALK-LABEL']; ?>:
                                <b><?php echo timeFormatconverter($job_profile_row['available_time_start']); ?></b></p>
                            <img
                                src="<?php echo $slash; ?>jobs/images/jobs/<?php echo $job_profile_row['cover_image']; ?>"
                                alt="">
                        </div>
                        <div class="jpro-ban-tit">
                            <div class="s1">
                                <img
                                    src="<?php if (($job_profile_row['job_profile_image'] == NULL) || empty($job_profile_row['job_profile_image'])) {
                                        echo $slash.'images/user/'.$footer_row['user_default_image'];
                                    } else {
                                        echo $slash.'jobs/images/jobs/'.$job_profile_row['job_profile_image'];
                                    } ?>" alt="">
                            </div>
                            <div class="s2">
                                <h1><?php echo $job_profile_row['profile_name']; ?></h1>
                                <span class="loc"><?php echo $job_profile_row['educational_qualification']; ?></span>
                                <p><?php echo $job_sub_category_name . " - " . $job_profile_row['current_company']; ?></p>
                            </div>
                            <div class="s3">
                                <span class="cta fol"><?php echo $BIZBOOK['MESSAGE']; ?></span>
                                <span class="cta"><?php echo $BIZBOOK['FOLLOW']; ?></span>
                            </div>
                        </div>
                    </div>
                    <!--END-->
                    <!--START-->
                    <div class="jb-pro-bio">
                        <h4><?php echo $BIZBOOK['JOB-INTERVIEW-EMPLOYEE-DETAILS-LABEL']; ?></h4>
                        <ul>
                            <li>
                                <?php echo $BIZBOOK['PHONE']; ?>
                                <span><?php echo $user_details_row['mobile_number']; ?></span>
                            </li>
                            <li>
                                <?php echo $BIZBOOK['EMAIL']; ?>
                                <span><?php echo $user_details_row['email_id']; ?></span>
                            </li>
                            <?php
                            if ($job_profile_row['current_company'] != NULL) {
                                ?>
                                <li>
                                    <?php echo $BIZBOOK['JOB-INTERVIEW-CURRENT-COMPANY-LABEL']; ?>
                                    <span><?php echo $job_profile_row['current_company']; ?></span>
                                </li>
                                <?php
                            }
                            if ($job_profile_row['notice_period'] != NULL) {
                                ?>
                                <li>
                                    <?php echo $BIZBOOK['JOB-INTERVIEW-NOTICE-PERIOD-LABEL']; ?>
                                    <span><?php
                                        $notice_period = $job_profile_row['notice_period'];
                                        if ($notice_period == 1) {
                                            echo $BIZBOOK['JOB_IMMEDIATE_JOINEE'];
                                        } elseif ($notice_period == 2) {
                                            echo $BIZBOOK['JOB_15_DAYS'];
                                        } elseif ($notice_period == 3) {
                                            echo $BIZBOOK['JOB_1_MONTH'];
                                        } elseif ($notice_period == 4) {
                                            echo $BIZBOOK['JOB_2_MONTHS'];
                                        } elseif ($notice_period == 5) {
                                            echo $BIZBOOK['JOB_3_MONTHS'];
                                        } elseif ($notice_period == 6) {
                                            echo $BIZBOOK['JOB_6_MONTHS'];
                                        } elseif ($notice_period == 7) {
                                            echo $BIZBOOK['JOB_1_YEAR'];
                                        } elseif ($notice_period == 8) {
                                            echo $BIZBOOK['JOB_2_YEARS'];
                                        }
                                        ?></span>
                                </li>
                                <?php
                            }
                            if ($job_profile_row['years_of_experience'] != NULL) {
                                ?>
                                <li>
                                    <?php echo $BIZBOOK['OTHER_INFORMATIONS_PLACEHOLDER_LEFT']; ?>
                                    <span><?php echo $job_profile_row['years_of_experience']; ?><?php echo $BIZBOOK['YEARS']; ?></span>
                                </li>
                                <?php
                            }
                            if ($job_profile_row['job_profile_resume'] != NULL) {
                                ?>
                                <li>
                                    <?php echo $BIZBOOK['JOB_APPLI_RESUME']; ?>
                                    <a href="<?php echo $slash; ?>jobs/images/jobs/<?php echo $job_profile_row['job_profile_resume']; ?>"
                                       download="<?php echo $job_profile_row['profile_name'] . ' - Resume'; ?>"><i
                                            class="material-icons">file_download</i> <?php echo $BIZBOOK['DOWNLOAD']; ?>
                                    </a>
                                </li>
                                <?php
                            }
                            ?>
                        </ul>
                    </div>
                    <!--END-->
                    <!--START-->
                    <div class="jpro-bd">
                        <div class="jpro-bd-com">
                            <h4><?php echo $BIZBOOK['OTHER_INFORMATIONS_PLACEHOLDER_LEFT']; ?></h4>
                            <ul>
                                <?php
                                if ($job_profile_row['experience_1'] != NULL) {
                                    ?>
                                    <li><?php echo stripslashes($job_profile_row['experience_1']); ?></li>
                                    <?php
                                }
                                if ($job_profile_row['experience_2'] != NULL) {
                                    ?>
                                    <li><?php echo stripslashes($job_profile_row['experience_2']); ?></li>
                                    <?php
                                }
                                if ($job_profile_row['experience_3'] != NULL) {
                                    ?>
                                    <li><?php echo stripslashes($job_profile_row['experience_3']); ?></li>
                                    <?php
                                }
                                if ($job_profile_row['experience_4'] != NULL) {
                                    ?>
                                    <li><?php echo stripslashes($job_profile_row['experience_4']); ?></li>
                                    <?php
                                }
                                ?>
                            </ul>
                        </div>
                        <div class="jpro-bd-com">
                            <h4><?php echo $BIZBOOK['JOB-SKILL-SET-LABEL']; ?></h4>
                            <?php
                            $skill_set = explode(',', $job_profile_row['skill_set']);
                            foreach ($skill_set as $skill_set_id) {
                                $skill_set_name = getJobSkill($skill_set_id);
                                ?>
                                <span><?php echo $skill_set_name['category_name']; ?></span>
                                <?php
                            }
                            ?>
                        </div>
                        <div class="jpro-bd-com">
                            <h4><?php echo $BIZBOOK['JOB_EDUCATION']; ?></h4>
                            <ul>
                                <?php
                                if ($job_profile_row['education_1'] != NULL) {
                                    ?>
                                    <li><?php echo stripslashes($job_profile_row['education_1']); ?></li>
                                    <?php
                                }
                                if ($job_profile_row['education_2'] != NULL) {
                                    ?>
                                    <li><?php echo stripslashes($job_profile_row['education_2']); ?></li>
                                    <?php
                                }
                                if ($job_profile_row['education_3'] != NULL) {
                                    ?>
                                    <li><?php echo stripslashes($job_profile_row['education_3']); ?></li>
                                    <?php
                                }
                                if ($job_profile_row['education_4'] != NULL) {
                                    ?>
                                    <li><?php echo stripslashes($job_profile_row['education_4']); ?></li>
                                    <?php
                                }
                                ?>
                            </ul>
                        </div>
                        <div class="jpro-bd-com">
                            <h4><?php echo $BIZBOOK['JOB-INTERVIEW-ADDITIONAL-INFORMATION-LABEL']; ?></h4>
                            <?php
                            if ($job_profile_row['additional_info_1'] != NULL) {
                                ?>
                                <span><?php echo stripslashes($job_profile_row['additional_info_1']); ?></span>
                                <?php
                            }
                            if ($job_profile_row['additional_info_2'] != NULL) {
                                ?>
                                <span><?php echo stripslashes($job_profile_row['additional_info_2']); ?></span>
                                <?php
                            }
                            if ($job_profile_row['additional_info_3'] != NULL) {
                                ?>
                                <span><?php echo stripslashes($job_profile_row['additional_info_3']); ?></span>
                                <?php
                            }
                            if ($job_profile_row['additional_info_4'] != NULL) {
                                ?>
                                <span><?php echo stripslashes($job_profile_row['additional_info_4']); ?></span>
                                <?php
                            }
                            ?>
                        </div>
                    </div>
                    <!--END-->
                </div>
                <div class="rhs">
                    <div class="ud-rhs-promo">
                        <h3><?php echo $BIZBOOK['JOB-PROFILE-H1']; ?></h3>
                        <p><?php echo $BIZBOOK['JOB-PROFILE-P']; ?></p>
                        <a href="<?php echo $slash; ?>login"><?php echo $BIZBOOK['JOB-PROFILE-A']; ?></a>
                    </div>
                    <div class="job-rel-pro">
                        <div class="hot-page2-hom-pre">
                            <h4><?php echo $BIZBOOK['JOB-RELATED-PROFILES']; ?></h4>
                            <ul>
                                <?php
                                foreach (getAllCategoryJobProfileLimit($job_profile_category_id, $job_profile_id) as $jobrow) {
                                    $job_related_profile_user_id = $jobrow['user_id'];

                                    $user_details_related_row = getUser($job_related_profile_user_id);
                                    ?>
                                    <li>
                                        <div class="hot-page2-hom-pre-1">
                                            <img
                                                src="<?php echo $slash; ?>images/user/<?php if (($user_details_related_row['profile_image'] == NULL) || empty($user_details_related_row['profile_image'])) {
                                                    echo $footer_row['user_default_image'];
                                                } else {
                                                    echo $user_details_related_row['profile_image'];
                                                } ?>" alt="">
                                        </div>
                                        <div class="hot-page2-hom-pre-2">
                                            <h5><?php echo $jobrow['profile_name']; ?></h5>
                                            <span><b><?php echo $jobrow['educational_qualification']; ?></b>, <?php echo $jobrow['years_of_experience']; ?> <?php echo $BIZBOOK['YEARS']; ?></span>
                                        </div>
                                        <a href="<?php echo $JOB_PROFILE_URL . urlModifier($jobrow['job_profile_slug']); ?>"
                                           class="fclick"></a>
                                    </li>
                                    <?php
                                }
                                ?>
                            </ul>
                        </div>
                    </div>
                    <div class="job-rel-pro">
                        <div class="hot-page2-hom-pre">
                            <h4><?php echo $BIZBOOK['JOB_RELATED_JOB_OPENINGS']; ?></h4>
                            <ul>
                                <?php
                                foreach (getAllCategoryJobLimit5($job_profile_category_id) as $job_rel_row) {
                                    $job_related_profile_user_id = $job_rel_row['user_id'];
                                    ?>
                                    <li>
                                        <div class="hot-page2-hom-pre-1">
                                            <img
                                                src="<?php echo $slash; ?>jobs/images/jobs/<?php echo $job_rel_row['company_logo']; ?>"
                                                alt="">
                                        </div>
                                        <div class="hot-page2-hom-pre-2">
                                            <h5><?php echo $job_rel_row['job_title']; ?></h5>
                                            <span><b><?php echo AddingZero_BeforeNumber($job_rel_row['no_of_openings']); ?><?php echo $BIZBOOK['JOB_OPENINGS']; ?></b>, <?php
                                                $job_type = $job_rel_row['job_type'];
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
                                        </div>
                                        <a href="<?php echo $JOB_URL . urlModifier($job_rel_row['job_slug']); ?>"
                                           class="fclick"></a>
                                    </li>
                                    <?php
                                }
                                ?>
                            </ul>
                        </div>
                    </div>
                    <div class="ud-rhs-promo job-rel-post-jb">
                        <h3><?php echo $BIZBOOK['JOB-PROFILE-POST-H1']; ?></h3>
                        <p><?php echo $BIZBOOK['JOB-PROFILE-POST-P']; ?></p>
                        <a href="<?php echo $slash; ?>jobs/db-jobs"><?php echo $BIZBOOK['JOB-PROFILE-POST-A']; ?></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->


<?php
include "../footer.php";
?>

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link ='<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url ='<?php echo $LOGIN_URL;?>';</script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>
</body>

</html>