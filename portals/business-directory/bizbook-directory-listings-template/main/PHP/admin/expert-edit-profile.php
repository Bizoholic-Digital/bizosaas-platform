<?php
include "header.php";
?>

<?php if($footer_row['admin_expert_show'] != 1 || $admin_row['admin_service_expert_options'] != 1){
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Edit This Service expert profile</span>
                <?php
                $expert_ida = $_GET['code'];
                $service_expert_row = getIdExpert($expert_ida);

                ?>
                <form action="update_expert_profile.php" class="expert_profile_form" id="expert_profile_form"
                      name="expert_profile_form" method="post" enctype="multipart/form-data">
                    <input type="hidden" id="cover_image_old"
                           value="<?php echo $service_expert_row['cover_image']; ?>"
                           name="cover_image_old"
                           class="validate">
                    <input type="hidden" id="expert_id"
                           value="<?php echo $service_expert_row['expert_id']; ?>"
                           name="expert_id"
                           class="validate">
                    <input type="hidden" id="profile_image_old"
                           value="<?php echo $service_expert_row['profile_image']; ?>"
                           name="profile_image_old"
                           class="validate">
                    <input type="hidden" id="id_proof_old"
                           value="<?php echo $service_expert_row['id_proof']; ?>"
                           name="id_proof_old"
                           class="validate">
                <div class="ud-cen-s2 job-form">
                    <div class="col-md-12">
                        <div class="form-group">
                            <label class="tit">Choose user *</label>
                            <select class="chosen-select" name="user_id">
                                <?php
                                foreach (getAllUser() as $ad_users_row) {
                                    ?>
                                    <option <?php if ($service_expert_row['user_id'] == $ad_users_row['user_id']) {
                                        echo "selected";
                                    } ?>
                                        value="<?php echo $ad_users_row['user_id']; ?>"><?php echo $ad_users_row['first_name']; ?></option>
                                    <?php
                                }
                                ?>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label class="tit">City</label>
                            <select onChange="getExpertArea(this.value);" class="chosen-select" name="city_id">
                                <option value=""><?php echo "Select City"; ?></option>
                                <?php
                                foreach (getAllExpertCities() as $city_row) {
                                    ?>
                                    <option <?php $catArray = explode(',', $service_expert_row['city_id']);
                                    foreach ($catArray as $cat_Array) {
                                        if ($city_row['country_id'] == $cat_Array) {
                                            echo "selected";
                                        }
                                    } ?>
                                        value="<?php echo $city_row['country_id']; ?>"><?php echo $city_row['country_name']; ?></option>
                                    <?php
                                }
                                ?>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="tit">Service start time</label>
                            <select class="chosen-select" name="available_time_start">
                                <?php
                                $time = '4:00'; // start
                                for ($i = 0; $i <= 19; $i++) {
                                    $prev = date('g:i a', strtotime($time)); // format the start time
                                    $next = strtotime('+60mins', strtotime($time)); // add 60 mins
                                    $time = date('g:i A', $next); // format the next time
                                    ?>
                                    <option <?php if ($service_expert_row['available_time_start'] == $time) {
                                        echo "selected";
                                    } ?> value="<?php echo $time; ?>"><?php echo $time; ?></option>
                                    <?php
                                }
                                ?>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="tit">Service close time</label>
                            <select class="chosen-select" name="available_time_end">
                                <?php
                                $time = '5:00'; // start
                                for ($i = 0; $i <= 18; $i++) {
                                    $prev = date('g:i a', strtotime($time)); // format the start time
                                    $next = strtotime('+60mins', strtotime($time)); // add 60 mins
                                    $time = date('g:i A', $next); // format the next time
                                    ?>
                                    <option <?php if ($service_expert_row['available_time_end'] == $time) {
                                        echo "selected";
                                    } ?> value="<?php echo $time; ?>"><?php echo $time; ?></option>
                                    <?php
                                }
                                ?>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="tit">Profile image</label>
                            <input type="file" name="profile_image" class="form-control">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="form-group">
                            <label class="tit">Work profession</label>
                            <select onChange="getExpertSubCategory(this.value);" class="chosen-select"
                                    name="category_id">
                                <option value=""><?php echo "Select Work Profession"; ?></option>
                                <?php
                                foreach (getAllExpertCategories() as $categories_row) {
                                    ?>
                                    <option <?php
                                        if ($categories_row['category_id'] == $service_expert_row['category_id']) {
                                            echo "selected";
                                    } ?>
                                        value="<?php echo $categories_row['category_id']; ?>"><?php echo $categories_row['category_name']; ?></option>
                                    <?php
                                }
                                ?>
                            </select>
                        </div>
                        <div class="form-group">
                            <label class="tit">Year of experience</label>
                            <input type="text" onkeypress="return isNumber(event)" name="years_of_experience"
                                   value="<?php echo $service_expert_row['years_of_experience']; ?>"
                                   class="form-control">
                        </div>
                        <div class="form-group">
                            <label class="tit">Base fare</label>
                            <input type="text" name="base_fare" onkeypress="return isNumber(event)"
                                   value="<?php echo $service_expert_row['base_fare']; ?>" class="form-control">
                        </div>
                        <div class="form-group">
                            <label class="tit">Profile cover image</label>
                            <input type="file" name="cover_image" class="form-control">
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="form-group">
                            <label class="tit">Services can do</label>
                            <select class="chosen-select" required="required" multiple="multiple" id="sub_category_id"
                                    name="sub_category_id[]">
                                <?php
                                foreach (getAllExpertSubCategories() as $sub_cat_row) {
                                    ?>
                                    <option <?php $catArray = explode(',', $service_expert_row['sub_category_id']);
                                    foreach ($catArray as $cat_Array) {
                                        if ($sub_cat_row['sub_category_id'] == $cat_Array) {
                                            echo "selected";
                                        }
                                    } ?>
                                        value="<?php echo $sub_cat_row['sub_category_id']; ?>"><?php echo $sub_cat_row['sub_category_name']; ?></option>
                                    <?php
                                }
                                ?>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="form-group">
                            <label class="tit">Service Areas</label>
                            <select class="chosen-select" multiple name="area_id[]" id="area_id">
                                <?php
                                foreach (getAllExpertAreas() as $areas_row) {
                                    ?>
                                    <option <?php $catArray = explode(',', $service_expert_row['area_id']);
                                    foreach ($catArray as $cat_Array) {
                                        if ($areas_row['city_id'] == $cat_Array) {
                                            echo "selected";
                                        }
                                    } ?>
                                        value="<?php echo $areas_row['city_id']; ?>"><?php echo $areas_row['city_name']; ?></option>
                                    <?php
                                }
                                ?>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="form-group">
                            <label class="tit">Payment accept</label>
                            <select class="chosen-select" multiple name="payment_id[]">
                                <?php
                                foreach (getAllExpertPayments() as $payment_row) {
                                    ?>
                                    <option <?php $catArray = explode(',', $service_expert_row['payment_id']);
                                    foreach ($catArray as $cat_Array) {
                                        if ($payment_row['payment_id'] == $cat_Array) {
                                            echo "selected";
                                        }
                                    } ?>
                                        value="<?php echo $payment_row['payment_id']; ?>"><?php echo $payment_row['payment_name']; ?></option>
                                    <?php
                                }
                                ?>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="form-group jb-fm-box-hig">
                            <h5 data-toggle="collapse" data-target="#jb-expe">Experience details</h5>
                            <div id="jb-expe" class="collapse coll-box">
                                <input type="text" name="experience_1"
                                       value="<?php echo $service_expert_row['experience_1']; ?>"
                                       class="form-control">
                                <hr>
                                <input type="text" name="experience_2"
                                       value="<?php echo $service_expert_row['experience_2']; ?>"
                                       class="form-control">
                                <hr>
                                <input type="text" name="experience_3"
                                       value="<?php echo $service_expert_row['experience_3']; ?>"
                                       class="form-control">
                                <hr>
                                <input type="text" name="experience_4"
                                       value="<?php echo $service_expert_row['experience_4']; ?>"
                                       class="form-control">
                            </div>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="form-group jb-fm-box-hig">
                            <h5 data-toggle="collapse" data-target="#jb-edu">Education and Qualifications</h5>
                            <div id="jb-edu" class="collapse coll-box">
                                <input type="text" name="education_1"
                                       value="<?php echo $service_expert_row['education_1']; ?>"
                                       class="form-control">
                                <hr>
                                <input type="text" name="education_2"
                                       value="<?php echo $service_expert_row['education_2']; ?>"
                                       class="form-control">
                                <hr>
                                <input type="text" name="education_3"
                                       value="<?php echo $service_expert_row['education_3']; ?>"
                                       class="form-control">
                                <hr>
                                <input type="text" name="education_4"
                                       value="<?php echo $service_expert_row['education_4']; ?>"
                                       class="form-control">
                            </div>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="form-group jb-fm-box-hig">
                            <h5 data-toggle="collapse" data-target="#jb-addi">Additional information</h5>
                            <div id="jb-addi" class="collapse coll-box">
                                <input type="text" name="additional_info_1"
                                       value="<?php echo $service_expert_row['additional_info_1']; ?>"
                                       class="form-control"
                                       placeholder="<?php echo "Extra courses"; ?>">
                                <hr>
                                <input type="text" name="additional_info_2"
                                       value="<?php echo $service_expert_row['additional_info_2']; ?>"
                                       class="form-control"
                                       placeholder="<?php echo "Training details"; ?>">
                                <hr>
                                <input type="text" name="additional_info_3"
                                       value="<?php echo $service_expert_row['additional_info_3']; ?>"
                                       class="form-control"
                                       placeholder="<?php echo "Others 1"; ?>">
                                <hr>
                                <input type="text" name="additional_info_4"
                                       value="<?php echo $service_expert_row['additional_info_4']; ?>"
                                       class="form-control"
                                       placeholder="<?php echo "Others 2"; ?>">
                            </div>
                        </div>
                    </div>
                    <div class="form-group col-md-6 serex-date">
                        <label class="tit"><?php echo "Date of Birth"; ?></label>
                        <input type="text" name="date_of_birth"
                               value="<?php echo $service_expert_row['date_of_birth']; ?>" class="form-control"
                               id="dobfield">
                    </div>

                    <div class="form-group col-md-6 serex-time">
                        <label class="tit"><?php echo "ID proof"; ?></label>
                        <input type="file" name="id_proof" class="form-control">
                    </div>
                    <div class="col-md-12">
                        <div class="form-group">
                            <button name="service_expert_submit" class="btn btn-primary"><?php echo "Submit Now"; ?></button>
                        </div>
                    </div>
                </div>
                </form>
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
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
<script src="../js/select-opt.js"></script>
<script>
    $(function () {
        $("#dobfield").datepicker({
            dateFormat: "yy-mm-dd",
            changeMonth: true,
            changeYear: true,
            maxDate: "-16Y",
            minDate: "-100Y",
            yearRange: "-100:-16"

        });
    });

    CKEDITOR.replace('job_description');
</script>

<script>
    function getExpertSubCategory(val) {
        $.ajax({
            type: "POST",
            url: "../service-experts/expert_sub_category_process.php",
            data: 'category_id=' + val,
            success: function (data) {
                $("#sub_category_id").html(data);
                $('#sub_category_id').trigger("chosen:updated");
            }
        });
    }
</script>
<script>
    function getExpertArea(val) {
        $.ajax({
            type: "POST",
            url: "../service-experts/expert_area_process.php",
            data: 'country_id=' + val,
            success: function (data) {
                $("#area_id").html(data);
                $('#area_id').trigger("chosen:updated");
            }
        });
    }
</script>

</body>

</html>