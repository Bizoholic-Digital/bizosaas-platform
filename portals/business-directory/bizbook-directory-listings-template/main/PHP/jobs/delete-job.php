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

?>

<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg job-form">
    <div class="container">
        <div class="row">
            <div class="login-main add-list">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['JOB-DELETE-THIS-JOB']; ?></span>
                <?php include "../page_level_message.php"; ?>
                <div class="log">
                    <?php
                    $job_codea = $_GET['row'];
                    $job_a_row = getJob($job_codea);

                    ?>
                    <form action="job_trash.php" class="job_form" id="job_form" name="job_form"
                          method="post" enctype="multipart/form-data">

                        <input type="hidden" id="job_codea" value="<?php echo $job_codea; ?>"
                               name="job_codea" class="validate">
                        <input type="hidden" id="job_id" value="<?php echo $job_a_row['job_id']; ?>"
                               name="job_id" class="validate">
                        <input type="hidden" id="job_code"
                               value="<?php echo $job_a_row['job_code']; ?>"
                               name="job_code" class="validate">
                        <input type="hidden" id="company_logo_old"
                               value="<?php echo $job_a_row['company_logo']; ?>" name="company_logo_old"
                               class="validate">

                        <div class="inn">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-TITLE-LABEL']; ?>*</label>
                                    <input type="text" value="<?php echo $job_a_row['job_title']; ?>" readonly="readonly" name="job_title" id="job_title" class="form-control" required>
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-SALARY-LABEL']; ?>*</label>
                                    <!--                                    <input type="range" min="0" max="300" value="0"-->
                                    <!--                                           onchange="updateTextInput(this.value);" class="form-control" id="salsli">-->
                                    <input type="text" readonly="readonly" required="required" onkeypress="return isNumber(event)" class="form-control" id="textInput" name="job_salary" value="<?php echo $job_a_row['job_salary']; ?>">
                                    <!--                                    <span id="salout" class="salout"></span>-->
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-NO-OF-OPENINGS-LABEL']; ?>*</label>
                                    <input type="text" value="<?php echo $job_a_row['no_of_openings']; ?>" onkeypress="return isNumber(event)" readonly="readonly" name="no_of_openings" class="form-control" required>
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-DATE-LABEL']; ?></label>
                                    <input type="date" value="<?php echo $job_a_row['job_interview_date']; ?>" readonly="readonly" name="job_interview_date" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-TIME-LABEL']; ?></label>
                                    <input type="time" value="<?php echo $job_a_row['job_interview_time']; ?>" readonly="readonly" name="job_interview_time" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-ROLE-LABEL']; ?></label>
                                    <input type="text" value="<?php echo $job_a_row['job_role']; ?>" readonly="readonly" name="job_role" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-EDUCATIONAL-LABEL']; ?></label>
                                    <input type="text" value="<?php echo $job_a_row['educational_qualification']; ?>" readonly="readonly" name="educational_qualification" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['LOCATION']; ?></label>
                                    <select disabled="disabled" class="chosen-select" name="job_location">
                                        <option value="1">Chennai</option>
                                        <option value="2">Bangalore</option>
                                        <option value="3">Delhi</option>
                                        <option value="4">Kerala</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-CATEGORY-LABEL']; ?></label>
                                    <select disabled="disabled" class="chosen-select" name="job_location">
                                        <option value=""><?php echo $BIZBOOK['JOB-SELECT-JOB-LOCATION-LABEL']; ?></option>
                                        <?php
                                        foreach (getAllJobCities() as $cities_row) {
                                            ?>
                                            <option
                                                <?php if ($job_a_row['job_location'] == $cities_row['city_id']) {
                                                    echo "selected";
                                                } ?>
                                                value="<?php echo $cities_row['city_id']; ?>"><?php echo $cities_row['city_name']; ?></option>
                                            <?php
                                        }
                                        ?>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-SUB-CATEGORY-LABEL']; ?></label>
                                    <select disabled="disabled" class="chosen-select" id="sub_category_id" name="sub_category_id">
                                        <?php
                                        foreach (getCategoryJobSubCategories($job_a_row['category_id']) as $sub_categories_row) {
                                            if ($job_a_row['sub_category_id'] != 0) {
                                                ?>
                                                <option <?php
                                                if ($sub_categories_row['sub_category_id'] == $job_a_row['sub_category_id']) {
                                                    echo "selected";
                                                } ?>
                                                    value="<?php echo $sub_categories_row['sub_category_id']; ?>"><?php echo $sub_categories_row['sub_category_name']; ?></option>
                                                <?php
                                            } else {
                                                ?>
                                                <option value=""><?php echo $BIZBOOK['SELECT_SUB_CATEGORY']; ?></option>
                                                <?php
                                            }
                                        }
                                        ?>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-TYPE-LABEL']; ?></label>
                                    <select disabled="disabled" class="chosen-select" name="job_type">
                                        <option <?php if ($job_a_row['job_type'] == 1) { echo "selected"; } ?> value="1"><?php echo $BIZBOOK['JOB-PERMANENT']; ?></option>
                                        <option <?php if ($job_a_row['job_type'] == 2) { echo "selected"; } ?> value="2"><?php echo $BIZBOOK['JOB-CONTRACT']; ?></option>
                                        <option <?php if ($job_a_row['job_type'] == 3) { echo "selected"; } ?> value="3"><?php echo $BIZBOOK['JOB-PART-TIME']; ?></option>
                                        <option <?php if ($job_a_row['job_type'] == 4) { echo "selected"; } ?> value="4"><?php echo $BIZBOOK['JOB-FREELANCE']; ?></option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-YEARS-OF-EXPERIENCE-LABEL']; ?></label>
                                    <input type="text" onkeypress="return isNumber(event)" value="<?php echo $job_a_row['years_of_experience']; ?>" readonly="readonly" name="years_of_experience" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-CONTACT-NO-LABEL']; ?></label>
                                    <input type="text" onkeypress="return isNumber(event)" value="<?php echo $job_a_row['contact_number']; ?>" readonly="readonly" name="contact_number" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['COMP-PRO-EMAIL']; ?></label>
                                    <input type="email" value="<?php echo $job_a_row['contact_email_id']; ?>" readonly="readonly" name="contact_email_id" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['COMP-PRO-WEBSITE']; ?></label>
                                    <input type="text" value="<?php echo $job_a_row['contact_website']; ?>" readonly="readonly" name="contact_website" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-CONTACT-PERSON-LABEL']; ?></label>
                                    <input type="text" value="<?php echo $job_a_row['contact_person']; ?>" readonly="readonly" name="contact_person" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-LOCATION-LABEL']; ?></label>
                                    <input type="text" value="<?php echo $job_a_row['interview_location']; ?>" readonly="readonly" name="interview_location" class="form-control">
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
                                    <input type="text" value="<?php echo $job_a_row['job_company_name']; ?>" readonly="readonly" name="job_company_name" class="form-control">
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-SKILL-SET-LABEL']; ?></label>
                                    <select disabled="disabled" class="chosen-select" multiple name="skill_set[]">
                                        <?php
                                        foreach (getAllJobSkill() as $skill_row) {
                                            ?>
                                            <option
                                                <?php $catArray = explode(',', $job_a_row['skill_set']);
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
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-DESCRIPTION-LABEL']; ?></label>
                                    <textarea readonly="readonly" name="job_description" class="form-control"
                                              id="job_description"><?php echo $job_a_row['job_description']; ?></textarea>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['JOB-SMALL-DESCRIPTION-LABEL']; ?></label>
                                    <textarea readonly="readonly" name="job_small_description" class="form-control"><?php echo $job_a_row['job_small_description']; ?></textarea>
                                </div>
                                <div class="form-group">
                                    <button name="job_submit" class="blu-upp"><?php echo $BIZBOOK['DELETE']; ?></button>
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