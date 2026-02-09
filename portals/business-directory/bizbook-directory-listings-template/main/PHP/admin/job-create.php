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
            <section class="login-reg">
                <div class="container">
                    <div class="row">
                        <div class="login-main add-list add-ncate">
                            <div class="log-bor">&nbsp;</div>
                            <span class="udb-inst">Add new Job</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Add New Job</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <form action="insert_job.php" class="job_form" id="job_form" name="job_form"
                                          method="post" enctype="multipart/form-data">
                                        <div class="inn">
                                            <ul>
                                                <li>
                                                    <!--FILED START-->
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <select name="user_code" id="user_code" class="form-control"
                                                                        required="required">
                                                                    <option value="" disabled selected>User Name</option>
                                                                    <?php
                                                                    foreach (getAllUser() as $ad_users_row) {
                                                                        ?>
                                                                        <option
                                                                            value="<?php echo $ad_users_row['user_code']; ?>"><?php echo $ad_users_row['first_name']; ?></option>
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
                                                                <label class="tit">Job Title*</label>
                                                                <input type="text" name="job_title" id="job_title"
                                                                       class="form-control" required>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Salary*</label>
                                                                <!--                                    <input type="range" min="0" max="300" value="0"-->
                                                                <!--                                           onchange="updateTextInput(this.value);" class="form-control" id="salsli">-->
                                                                <input type="text" required="required" onkeypress="return isNumber(event)" id="textInput" class="form-control"  name="job_salary" value="">
                                                                <!--                                    <span id="salout" class="salout"></span>-->
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">No of openings*</label>
                                                                <input type="text" onkeypress="return isNumber(event)"
                                                                       name="no_of_openings" class="form-control"
                                                                       required>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Interview Date</label>
                                                                <input type="date" name="job_interview_date"
                                                                       class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Interview Time</label>
                                                                <input type="time" name="job_interview_time"
                                                                       class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Role</label>
                                                                <input type="text" name="job_role" class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Education & Qualification</label>
                                                                <input type="text" name="educational_qualification"
                                                                       class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
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
                                                                            value="<?php echo $cities_row['city_id']; ?>"><?php echo $cities_row['city_name']; ?></option>
                                                                        <?php
                                                                    }
                                                                    ?>
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Company logo</label>
                                                                <input type="file" name="company_logo"
                                                                       class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Job category</label>
                                                                <select onChange="getJobSubCategory(this.value);"
                                                                        class="form-control" name="category_id">
                                                                    <option value="">Select Category</option>
                                                                    <?php
                                                                    foreach (getAllJobCategories() as $categories_row) {
                                                                        ?>
                                                                        <option
                                                                            value="<?php echo $categories_row['category_id']; ?>"><?php echo $categories_row['category_name']; ?></option>
                                                                        <?php
                                                                    }
                                                                    ?>
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Job sub-category</label>
                                                                <select class="form-control" id="sub_category_id"
                                                                        name="sub_category_id">
                                                                    <option value="">Job sub-category</option>
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Job Type</label>
                                                                <select class="form-control" name="job_type">
                                                                    <option value="1">Permanent</option>
                                                                    <option value="2">Contract</option>
                                                                    <option value="3">Part time</option>
                                                                    <option value="4">Freelance</option>
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Year(s) of experience</label>
                                                                <input type="text" onkeypress="return isNumber(event)"
                                                                       name="years_of_experience" class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Contact no</label>
                                                                <input type="text" onkeypress="return isNumber(event)"
                                                                       name="contact_number" class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Email id</label>
                                                                <input type="email" name="contact_email_id"
                                                                       class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Website</label>
                                                                <input type="text" name="contact_website"
                                                                       class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Contact person</label>
                                                                <input type="text" name="contact_person"
                                                                       class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Interview location</label>
                                                                <input type="text" name="interview_location"
                                                                       class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Company Name</label>
                                                                <input type="text" name="job_company_name"
                                                                       class="form-control">
                                                            </div>
                                                        </div>
                                                    </div>
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
                                                                            value="<?php echo $skill_row['category_id']; ?>"><?php echo $skill_row['category_name']; ?></option>
                                                                        <?php
                                                                    }
                                                                    ?>
                                                                </select>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">Job Descriptions</label>
                                    <textarea name="job_description" class="form-control"
                                              id="job_description"></textarea>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row">
                                                        <div class="col-md-12">
                                                            <div class="form-group">
                                                                <label class="tit">About your company(small description)</label>
                                                            <textarea name="job_small_description"
                                                                      class="form-control"></textarea>
                                                            </div>
                                                        </div>
                                                </li>
                                            </ul>
                                            <div class="form-group">
                                                <button type="submit" name="job_submit" class="btn btn-primary">Submit
                                                    Now
                                                </button>
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