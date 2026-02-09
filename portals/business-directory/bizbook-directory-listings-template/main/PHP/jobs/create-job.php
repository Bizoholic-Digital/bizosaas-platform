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

//To check the jobs count with current plan starts

$plan_type_job_count = $user_plan_type['plan_type_job_count'];
$job_count_user = getCountUserJob($_SESSION['user_id']);

if ($job_count_user >= $plan_type_job_count) {

    $_SESSION['status_msg'] = $BIZBOOK['JOBS_LIMIT_EXCEED_MESSAGE'];

    header('Location: db-jobs');
    exit();
}
//To check the jobs count with current plan ends

?>

<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg job-form">
    <div class="container">
        <div class="row">
            <div class="login-main add-list">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['JOB-POST-NEW-JOB']; ?></span>
                <?php include "../page_level_message.php"; ?>
                <div class="log">
                    <form action="job_insert.php" class="job_form" id="job_form" name="job_form"
                          method="post" enctype="multipart/form-data">
                        <div class="inn">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-TITLE-LABEL']; ?>*</label>
                                    <input type="text" name="job_title" id="job_title" class="form-control" required>
                                </div>
                                <div class="form-group prfix-inp">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-SALARY-LABEL']; ?>*</label>
                                    <i class="prfix"><?php echo $footer_row['currency_symbol']; ?></i>
                                    <input type="text" required="required" onkeypress="return isNumber(event)" id="textInput" class="form-control"  name="job_salary" value="">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-NO-OF-OPENINGS-LABEL']; ?>*</label>
                                    <input type="text" onkeypress="return isNumber(event)" name="no_of_openings" class="form-control" required>
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-DATE-LABEL']; ?></label>
                                    <input type="text" name="job_interview_date" class="form-control" id="newdate">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-TIME-LABEL']; ?></label>
                                    <input type="time" name="job_interview_time" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-ROLE-LABEL']; ?></label>
                                    <input type="text" name="job_role" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-EDUCATIONAL-LABEL']; ?></label>
                                    <input type="text" name="educational_qualification" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['LOCATION']; ?></label>
                                    <select class="chosen-select" name="job_location">
                                        <option value=""><?php echo $BIZBOOK['JOB-SELECT-JOB-LOCATION-LABEL']; ?></option>
                                        <?php
                                        foreach (getAllJobCities() as $cities_row) {
                                            ?>
                                            <option
                                                value="<?php echo $cities_row['city_id']; ?>"><?php echo $cities_row['city_name']; ?></option>
                                            <?php
                                        }
                                        ?>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-COMPANY-LOGO-LABEL']; ?></label>
                                    <div class="fil-img-uplo">
                                        <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                        <input type="file" name="company_logo" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-CATEGORY-LABEL']; ?></label>
                                    <select onChange="getJobSubCategory(this.value);" class="chosen-select" name="category_id">
                                        <option value=""><?php echo $BIZBOOK['SELECT_CATEGORY']; ?></option>
                                        <?php
                                        foreach (getAllJobCategories() as $categories_row) {
                                            ?>
                                            <option value="<?php echo $categories_row['category_id']; ?>"><?php echo $categories_row['category_name']; ?></option>
                                            <?php
                                        }
                                        ?>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-SUB-CATEGORY-LABEL']; ?></label>
                                    <select class="chosen-select" id="sub_category_id" name="sub_category_id">
                                        <option value=""><?php echo $BIZBOOK['SELECT_SUB_CATEGORY']; ?></option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-TYPE-LABEL']; ?></label>
                                    <select class="chosen-select" name="job_type">
                                        <option value="1"><?php echo $BIZBOOK['JOB-PERMANENT']; ?></option>
                                        <option value="2"><?php echo $BIZBOOK['JOB-CONTRACT']; ?></option>
                                        <option value="3"><?php echo $BIZBOOK['JOB-PART-TIME']; ?></option>
                                        <option value="4"><?php echo $BIZBOOK['JOB-FREELANCE']; ?></option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-YEARS-OF-EXPERIENCE-LABEL']; ?></label>
                                    <input type="text" onkeypress="return isNumber(event)" name="years_of_experience" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-CONTACT-NO-LABEL']; ?></label>
                                    <input type="text" onkeypress="return isNumber(event)" name="contact_number" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['COMP-PRO-EMAIL']; ?></label>
                                    <input type="email" name="contact_email_id" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['COMP-PRO-WEBSITE']; ?></label>
                                    <input type="text" name="contact_website" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-CONTACT-PERSON-LABEL']; ?></label>
                                    <input type="text" name="contact_person" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-LOCATION-LABEL']; ?></label>
                                    <input type="text" name="interview_location" class="form-control">
                                    <!-- INPUT TOOL TIP -->
                                    <div class="inp-ttip">
                                        <b>Map location</b>
                                        Get your interview location link from google map and use here.
                                    </div>
                                    <!-- END INPUT TOOL TIP -->
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-COMPANY-NAME-LABEL']; ?></label>
                                    <input type="text" name="job_company_name" class="form-control">
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-SKILL-SET-LABEL']; ?></label>
                                    <select class="chosen-select" multiple name="skill_set[]">
                                        <?php
                                        foreach (getAllJobSkill() as $skill_row) {
                                            ?>
                                            <option value="<?php echo $skill_row['category_id']; ?>"><?php echo $skill_row['category_name']; ?></option>
                                            <?php
                                        }
                                        ?>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-DESCRIPTION-LABEL']; ?></label>
                                    <textarea name="job_description" class="form-control"
                                              id="job_description"></textarea>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-SMALL-DESCRIPTION-LABEL']; ?></label>
                                    <textarea name="job_small_description" class="form-control"></textarea>
                                </div>
                                <div class="form-group">
                                    <button name="job_submit" class="blu-upp"><?php echo $BIZBOOK['SUBMIT_NOW']; ?></button>
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
<script src="../admin/ckeditor/ckeditor.js"></script>
<script>
    CKEDITOR.replace('job_description');
</script>
<script>
    function getJobSubCategory(val) {
        $.ajax({
            type: "POST",
            url: "job_sub_category_process.php",
            data: 'category_id=' + val,
            success: function (data) {
                $("#sub_category_id").html(data);
                $('#sub_category_id').trigger("chosen:updated");
            }
        });
    }
</script>
<script>
    var slider = document.getElementById("salsli");
    var output = document.getElementById("salout");
    output.innerHTML = slider.value;

    slider.oninput = function () {
        output.innerHTML = this.value + "K";
    }
</script>
<script>
    function updateTextInput(val) {
        document.getElementById('textInput').value=val;
    }
</script>
</body>

</html>