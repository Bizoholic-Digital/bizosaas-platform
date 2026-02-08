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
            <section class="login-reg">
                <div class="container">
                    <div class="row">
                        <div class="login-main add-list add-ncate">
                            <div class="log-bor">&nbsp;</div>
                            <span class="udb-inst">Edit This Job</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Edit This Job</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $job_codea = $_GET['code'];
                                    $job_a_row = getJob($job_codea);

                                    ?>
                                    <form action="update_job.php" class="job_form" id="job_form" name="job_form"
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
                                            <ul>
                                                <li>
                                                    <!--FILED START-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <select name="user_code" id="user_code" class="form-control"
                                                                        required="required">
                                                                    <option value="" disabled >User Name</option>
                                                                    <?php
                                                                    foreach (getAllUser() as $ad_users_row) {
                                                                        ?>
                                                                        <option <?php if ($job_a_row['user_id'] == $ad_users_row['user_id']) {
                                                                            echo "selected";
                                                                        } ?>
                                                                            value="<?php echo $ad_users_row['user_code']; ?>"><?php echo $ad_users_row['first_name']; ?></option>
                                                                        <?php
                                                                    }
                                                                    ?>
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <!--FILED START-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Job Title*</label>
                                                                <input type="text"
                                                                       value="<?php echo $job_a_row['job_title']; ?>"
                                                                       name="job_title" id="job_title"
                                                                       class="form-control" required>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Salary*</label>
                                                                <!--                                    <input type="range" min="0" max="300" value="0"-->
                                                                <!--                                           onchange="updateTextInput(this.value);" class="form-control" id="salsli">-->
                                                                <input type="text" required="required" onkeypress="return isNumber(event)" class="form-control" id="textInput" name="job_salary" value="<?php echo $job_a_row['job_salary']; ?>">
                                                                <!--                                    <span id="salout" class="salout"></span>-->
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">No of openings*</label>
                                                                <input type="text"
                                                                       value="<?php echo $job_a_row['no_of_openings']; ?>"
                                                                       onkeypress="return isNumber(event)"
                                                                       name="no_of_openings"
                                                                       class="form-control" required>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Interview Date</label>
                                                                <input type="date"
                                                                       value="<?php echo $job_a_row['job_interview_date']; ?>"
                                                                       name="job_interview_date" class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Interview Time</label>
                                                                <input type="time"
                                                                       value="<?php echo $job_a_row['job_interview_time']; ?>"
                                                                       name="job_interview_time" class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Role</label>
                                                                <input type="text"
                                                                       value="<?php echo $job_a_row['job_role']; ?>"
                                                                       name="job_role" class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Education & Qualification</label>
                                                                <input type="text"
                                                                       value="<?php echo $job_a_row['educational_qualification']; ?>"
                                                                       name="educational_qualification"
                                                                       class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Location</label>
                                                                <select class="form-control" name="job_location">
                                                                    <option value="">Select Job location</option>
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
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Company logo</label>
                                                                <input type="file" name="company_logo"
                                                                       class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Job category</label>
                                                                <select onChange="getJobSubCategory(this.value);"
                                                                        class="form-control"
                                                                        name="category_id">
                                                                    <option value="">Select Category</option>
                                                                    <?php
                                                                    foreach (getAllJobCategories() as $categories_row) {
                                                                        ?>
                                                                        <option
                                                                            <?php if ($job_a_row['category_id'] == $categories_row['category_id']) {
                                                                                echo "selected";
                                                                            } ?>
                                                                            value="<?php echo $categories_row['category_id']; ?>"><?php echo $categories_row['category_name']; ?></option>
                                                                        <?php
                                                                    }
                                                                    ?>
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Job sub-category</label>
                                                                <select class="form-control" id="sub_category_id"
                                                                        name="sub_category_id">
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
                                                                            <option value="">Job sub-category</option>
                                                                            <?php
                                                                        }
                                                                    }
                                                                    ?>
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Job Type</label>
                                                                <select class="form-control" name="job_type">
                                                                    <option <?php if ($job_a_row['job_type'] == 1) {
                                                                        echo "selected";
                                                                    } ?> value="1">Permanent
                                                                    </option>
                                                                    <option <?php if ($job_a_row['job_type'] == 2) {
                                                                        echo "selected";
                                                                    } ?> value="2">Contract
                                                                    </option>
                                                                    <option <?php if ($job_a_row['job_type'] == 3) {
                                                                        echo "selected";
                                                                    } ?> value="3">Part time
                                                                    </option>
                                                                    <option <?php if ($job_a_row['job_type'] == 4) {
                                                                        echo "selected";
                                                                    } ?> value="4">Freelance
                                                                    </option>
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Year(s) of experience</label>
                                                                <input type="text" onkeypress="return isNumber(event)"
                                                                       value="<?php echo $job_a_row['years_of_experience']; ?>"
                                                                       name="years_of_experience" class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Contact no</label>
                                                                <input type="text" onkeypress="return isNumber(event)"
                                                                       value="<?php echo $job_a_row['contact_number']; ?>"
                                                                       name="contact_number" class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Email id</label>
                                                                <input type="email"
                                                                       value="<?php echo $job_a_row['contact_email_id']; ?>"
                                                                       name="contact_email_id" class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Website</label>
                                                                <input type="text"
                                                                       value="<?php echo $job_a_row['contact_website']; ?>"
                                                                       name="contact_website" class="form-control">
                                                            </div>
                                                            <div class="form-group">
                                                                <label class="tit">Contact person</label>
                                                                <input type="text"
                                                                       value="<?php echo $job_a_row['contact_person']; ?>"
                                                                       name="contact_person" class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Interview location</label>
                                                                <input type="text"
                                                                       value="<?php echo $job_a_row['interview_location']; ?>"
                                                                       name="interview_location" class="form-control">

                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Company Name</label>
                                                                <input type="text"
                                                                       value="<?php echo $job_a_row['job_company_name']; ?>"
                                                                       name="job_company_name" class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Skill set</label>
                                                                <select class="chosen-select form-control" multiple
                                                                        name="skill_set[]">
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
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Job Descriptions</label>
                                    <textarea name="job_description" class="form-control"
                                              id="job_description"><?php echo $job_a_row['job_description']; ?></textarea>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <!--FILED END-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">About your company(small
                                                                    description)</label>
                                                <textarea name="job_small_description"
                                                          class="form-control"><?php echo $job_a_row['job_small_description']; ?></textarea>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </li>
                                            </ul>
                                            <!--FILED END-->
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <button name="job_submit" class="btn btn-primary">Update Now</button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

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
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
<script src="ckeditor/ckeditor.js"></script>
<script>
    CKEDITOR.replace('job_description');
</script>
<script>
    function getJobSubCategory(val) {
        $.ajax({
            type: "POST",
            url: "../job_sub_category_process.php",
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
        document.getElementById('textInput').value = val;
    }
</script>
</body>

</html>