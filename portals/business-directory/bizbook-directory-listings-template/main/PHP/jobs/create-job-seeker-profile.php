<?php
include "job-config-info.php";
include "../header.php";

if (file_exists('../config/user_authentication.php')) {
    include('../config/user_authentication.php');
}

if (file_exists('../config/job_page_authentication.php')) {
    include('../config/job_page_authentication.php');
}

$user_id = $_SESSION['user_id'];

$job_profile_row = getUserJobProfile($user_id);

?>

<section class=" login-reg job-form">
    <div class="container">
        <div class="row">
            <div class="login-main add-list">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['JOB-INTERVIEW-EMPLOYEE-PROFILE-LABEL']; ?></span>
                <div class="log">
                    <form action="job_profile_insert.php" class="job_profile_form" id="job_profile_form"
                          name="job_profile_form"
                          method="post" enctype="multipart/form-data">
                        <input type="hidden" id="job_profile_image_old"
                               value="<?php echo $job_profile_row['job_profile_image']; ?>"
                               name="job_profile_image_old"
                               class="validate">
                        <input type="hidden" id="cover_image_old"
                               value="<?php echo $job_profile_row['cover_image']; ?>"
                               name="cover_image_old"
                               class="validate">
                        <input type="hidden" id="root_path"
                               value="<?php echo $slash; ?>"
                               name="root_path"
                               class="validate">
                        <input type="hidden" id="job_profile_resume_old"
                               value="<?php echo $job_profile_row['job_profile_resume']; ?>"
                               name="job_profile_resume_old"
                               class="validate">
                    <div class="inn">
                        <div class="col-md-6">
                            <div class="form-group">
                                <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-EMPLOYEE-NAME-LABEL']; ?>*</label>
                                <input type="text" name="profile_name" value="<?php echo $job_profile_row['profile_name'] != NULL ? $job_profile_row['profile_name'] : $user_details_row['first_name']; ?>" class="form-control" readonly="readonly">
                            </div>
                            <div class="form-group">
                                <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-CURRENT-COMPANY-LABEL']; ?></label>
                                <input type="text" name="current_company" value="<?php echo $job_profile_row['current_company']; ?>" class="form-control">
                            </div>
                            <div class="form-group">
                                <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-NOTICE-PERIOD-LABEL']; ?></label>
                                <select class="chosen-select" name="notice_period">
                                    <option <?php if ($job_profile_row['notice_period'] == 1) { echo "selected"; } ?> value="1"><?php echo $BIZBOOK['JOB_IMMEDIATE_JOINEE']; ?></option>
                                    <option <?php if ($job_profile_row['notice_period'] == 2) { echo "selected"; } ?> value="2"><?php echo $BIZBOOK['JOB_15_DAYS']; ?></option>
                                    <option <?php if ($job_profile_row['notice_period'] == 3) { echo "selected"; } ?> value="3"><?php echo $BIZBOOK['JOB_1_MONTH']; ?></option>
                                    <option <?php if ($job_profile_row['notice_period'] == 4) { echo "selected"; } ?> value="4"><?php echo $BIZBOOK['JOB_2_MONTHS']; ?></option>
                                    <option <?php if ($job_profile_row['notice_period'] == 5) { echo "selected"; } ?> value="5"><?php echo $BIZBOOK['JOB_3_MONTHS']; ?></option>
                                    <option <?php if ($job_profile_row['notice_period'] == 6) { echo "selected"; } ?> value="6"><?php echo $BIZBOOK['JOB_6_MONTHS']; ?></option>
                                    <option <?php if ($job_profile_row['notice_period'] == 7) { echo "selected"; } ?> value="7"><?php echo $BIZBOOK['JOB_1_YEAR']; ?></option>
                                    <option <?php if ($job_profile_row['notice_period'] == 8) { echo "selected"; } ?> value="8"><?php echo $BIZBOOK['JOB_2_YEARS']; ?></option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-EDUCATIONAL-LABEL']; ?></label>
                                <input type="text" name="educational_qualification" value="<?php echo $job_profile_row['educational_qualification']; ?>" class="form-control">
                            </div>
                            <div class="form-group">
                                <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-PROFILE-IMAGE-LABEL']; ?></label>
                                <div class="fil-img-uplo">
                                    <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                    <input type="file" name="job_profile_image" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group">
                                <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-JOB-PROFESSION-LABEL']; ?></label>
                                <select class="chosen-select" required="required" name="sub_category_id">
                                    <option value=""><?php echo $BIZBOOK['SELECT_CATEGORY']; ?></option>
                                    <?php
                                    foreach (getAllJobSubCategories() as $sub_categories_row) {
                                        ?>
                                        <option
                                            <?php if ($job_profile_row['sub_category_id'] == $sub_categories_row['sub_category_id']) {
                                                echo "selected";
                                            } ?>
                                            value="<?php echo $sub_categories_row['sub_category_id']; ?>"><?php echo $sub_categories_row['sub_category_name']; ?></option>
                                        <?php
                                    }
                                    ?>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="tit"><?php echo $BIZBOOK['JOB-YEARS-OF-EXPERIENCE-LABEL']; ?></label>
                                <input type="text" onkeypress="return isNumber(event)" name="years_of_experience" value="<?php echo $job_profile_row['years_of_experience']; ?>" class="form-control">
                            </div>
                            <div class="form-group">
                                <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-AVAILABLE-TIME-TO-TALK-LABEL']; ?></label>
                                <input type="time" name="available_time_start" value="<?php echo $job_profile_row['available_time_start']; ?>" class="form-control">
                            </div>
                            <div class="form-group">
                                <label class="tit"><?php echo $BIZBOOK['JOB_APPLI_RESUME']; ?></label>
                                <div class="fil-img-uplo">
                                    <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                    <input type="file" name="job_profile_resume" accept="application/pdf,application/msword,
  application/vnd.openxmlformats-officedocument.wordprocessingml.document" class="form-control">
                                </div>

                                <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-PROFILE-COVER-IMAGE-LABEL']; ?></label>
                                <div class="fil-img-uplo">
                                    <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                    <input type="file" name="cover_image" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                </div>
                            </div>
                        </div>
                        <div class="col-md-12">
                            <div class="form-group">
                                <label class="tit"><?php echo $BIZBOOK['JOB-SKILL-SET-LABEL']; ?></label>
                                <select class="chosen-select" multiple name="skill_set[]">
                                    <?php
                                    foreach (getAllJobSkill() as $skill_row) {
                                        ?>
                                        <option <?php $catArray = explode(',', $job_profile_row['skill_set']);
                                                foreach ($catArray as $cat_Array) {
                                                    if ($skill_row['category_id'] == $cat_Array) {
                                                        echo "selected";
                                                    }
                                                } ?>
                                            value="<?php echo $skill_row['category_id']; ?>"><?php echo $skill_row['category_name']; ?></option>
                                        <?php
                                    }
                                    ?>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-12">
                            <div class="form-group jb-fm-box-hig">
                                <h5 data-toggle="collapse" data-target="#jb-expe"><?php echo $BIZBOOK['JOB-INTERVIEW-EXPERIENCE-DETAILS-LABEL']; ?></h5>
                                <div id="jb-expe" class="collapse coll-box">
                                    <input type="text" name="experience_1" value="<?php echo stripslashes($job_profile_row['experience_1']); ?>" class="form-control">
                                    <hr>
                                    <input type="text" name="experience_2" value="<?php echo stripslashes($job_profile_row['experience_2']); ?>" class="form-control">
                                    <hr>
                                    <input type="text" name="experience_3" value="<?php echo stripslashes($job_profile_row['experience_3']); ?>" class="form-control">
                                    <hr>
                                    <input type="text" name="experience_4" value="<?php echo stripslashes($job_profile_row['experience_4']); ?>" class="form-control">
                                </div>
                            </div>
                        </div>
                        <div class="col-md-12">
                            <div class="form-group jb-fm-box-hig">
                                <h5 data-toggle="collapse" data-target="#jb-edu"><?php echo $BIZBOOK['JOB-INTERVIEW-EDUCATIONAL-LABEL']; ?></h5>
                                <div id="jb-edu" class="collapse coll-box">
                                    <input type="text" name="education_1" value="<?php echo stripslashes($job_profile_row['education_1']); ?>" class="form-control">
                                    <hr>
                                    <input type="text" name="education_2" value="<?php echo stripslashes($job_profile_row['education_2']); ?>" class="form-control">
                                    <hr>
                                    <input type="text" name="education_3" value="<?php echo stripslashes($job_profile_row['education_3']); ?>" class="form-control">
                                    <hr>
                                    <input type="text" name="education_4" value="<?php echo stripslashes($job_profile_row['education_4']); ?>" class="form-control">
                                </div>
                            </div>
                        </div>
                        <div class="col-md-12">
                            <div class="form-group jb-fm-box-hig">
                                <h5 data-toggle="collapse" data-target="#jb-addi"><?php echo $BIZBOOK['JOB-INTERVIEW-ADDITIONAL-INFORMATION-LABEL']; ?></h5>
                                <div id="jb-addi" class="collapse coll-box">
                                    <input type="text" name="additional_info_1" value="<?php echo stripslashes($job_profile_row['additional_info_1']); ?>" class="form-control" placeholder="<?php echo $BIZBOOK['JOB_EXTRA_COURSES']; ?>">
                                    <hr>
                                    <input type="text" name="additional_info_2" value="<?php echo stripslashes($job_profile_row['additional_info_2']); ?>" class="form-control" placeholder="<?php echo $BIZBOOK['JOB_TRAINING_DETAILS']; ?>">
                                    <hr>
                                    <input type="text" name="additional_info_3" value="<?php echo stripslashes($job_profile_row['additional_info_3']); ?>" class="form-control" placeholder="<?php echo $BIZBOOK['JOB_OTHERS_1']; ?>">
                                    <hr>
                                    <input type="text" name="additional_info_4" value="<?php echo stripslashes($job_profile_row['additional_info_4']); ?>" class="form-control" placeholder="<?php echo $BIZBOOK['JOB_OTHERS_2']; ?>">
                                </div>
                            </div>
                        </div>
                        <div class="col-md-12">
                            <div class="form-group">
                                <button name="job_profile_submit" class="blu-upp"><?php echo $BIZBOOK['SUBMIT_NOW']; ?></button>
                            </div>
                        </div>
                    </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</section>
<?php
include "../footer.php";
?>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="../js/jquery.min.js"></script>
<script src="../js/popper.min.js"></script>
<script src="../js/bootstrap.min.js"></script>
<script src="../js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="../js/custom.js"></script>
<script src="../js/select-opt.js"></script>
<script src="../js/jquery.validate.min.js"></script>
<script src="../js/custom_validation.js"></script>
</body>

</html>