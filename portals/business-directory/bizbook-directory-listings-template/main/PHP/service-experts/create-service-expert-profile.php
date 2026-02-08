<?php
include "expert-config-info.php";
include "../header.php";

if (file_exists('../config/general_user_authentication.php')) {
    include('../config/general_user_authentication.php');
}

if (file_exists('../config/expert_page_authentication.php')) {
    include('../config/expert_page_authentication.php');
}

$user_id = $_SESSION['user_id'];

$service_expert_row = getExpertUser($user_id);

?>

<section class=" login-reg job-form">
    <div class="container">
        <div class="row">
            <div class="login-main add-list">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['SERVICE-EXPERT-PROFILE-LABEL']; ?></span>
                <div class="log">
                    <form action="service_expert_insert.php" class="service_expert_form" id="service_expert_form"
                          name="service_expert_form"
                          method="post" enctype="multipart/form-data">
                        <input type="hidden" id="cover_image_old"
                               value="<?php echo $service_expert_row['cover_image']; ?>"
                               name="cover_image_old"
                               class="validate">
                        <input type="hidden" id="root_path"
                               value="<?php echo $slash; ?>"
                               name="root_path"
                               class="validate">
                        <input type="hidden" id="profile_image_old"
                               value="<?php echo $service_expert_row['profile_image']; ?>"
                               name="profile_image_old"
                               class="validate">
                        <input type="hidden" id="id_proof_old"
                               value="<?php echo $service_expert_row['id_proof']; ?>"
                               name="id_proof_old"
                               class="validate">
                        <div class="inn">
                            <div class="col-md-12">
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['NAME']; ?>*</label>
                                    <input type="text" name="profile_name"
                                           value="<?php echo $service_expert_row['profile_name'] != NULL ? $service_expert_row['profile_name'] : $user_details_row['first_name']; ?>"
                                           class="form-control" readonly="readonly">
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['CITY']; ?></label>
                                    <select onChange="getExpertArea(this.value);" class="chosen-select" name="city_id">
                                        <option value=""><?php echo $BIZBOOK['SERVICE-EXPERT-SELECT-CITY-LABEL']; ?></option>
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
                                    <label
                                        class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-START-TIME-LABEL']; ?></label>
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
                                    <label
                                        class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-CLOSE-TIME-LABEL']; ?></label>
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
                                    <label class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-PROFILE-IMAGE-LABEL']; ?></label>
                                    <div class="fil-img-uplo">
                                        <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                        <input type="file" name="profile_image" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-WORK-PROFESSION-LABEL']; ?></label>
                                    <select onChange="getExpertSubCategory(this.value);" class="chosen-select"
                                            name="category_id">
                                        <option value=""><?php echo $BIZBOOK['SERVICE-EXPERT-SELECT-WORK-PROFESSION-LABEL']; ?></option>
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
                                    <label class="tit"><?php echo $BIZBOOK['JOB-YEARS-OF-EXPERIENCE-LABEL']; ?></label>
                                    <input type="text" onkeypress="return isNumber(event)" name="years_of_experience"
                                           value="<?php echo $service_expert_row['years_of_experience']; ?>"
                                           class="form-control">
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-BASE-FARE-LABEL']; ?></label>
                                    <input type="text" name="base_fare" onkeypress="return isNumber(event)"
                                           value="<?php echo $service_expert_row['base_fare']; ?>" class="form-control">
                                </div>
                                <div class="form-group">
                                    <label
                                        class="tit"><?php echo $BIZBOOK['JOB-INTERVIEW-PROFILE-COVER-IMAGE-LABEL']; ?></label>
                                    <div class="fil-img-uplo">
                                        <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                        <input type="file" name="cover_image" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group">
                                    <label
                                        class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-SERVICES-CAN-DO-LABEL']; ?></label>
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
                                    <label
                                        class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-SERVICES-AREAS-LABEL']; ?></label>
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
                                    <label
                                        class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-PAYMENT-ACCEPT-LABEL']; ?></label>
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
                                    <h5 data-toggle="collapse"
                                        data-target="#jb-expe"><?php echo $BIZBOOK['JOB-INTERVIEW-EXPERIENCE-DETAILS-LABEL']; ?></h5>
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
                                    <h5 data-toggle="collapse"
                                        data-target="#jb-edu"><?php echo $BIZBOOK['JOB-INTERVIEW-EDUCATIONAL-LABEL']; ?></h5>
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
                                    <h5 data-toggle="collapse"
                                        data-target="#jb-addi"><?php echo $BIZBOOK['JOB-INTERVIEW-ADDITIONAL-INFORMATION-LABEL']; ?></h5>
                                    <div id="jb-addi" class="collapse coll-box">
                                        <input type="text" name="additional_info_1"
                                               value="<?php echo $service_expert_row['additional_info_1']; ?>"
                                               class="form-control"
                                               placeholder="<?php echo $BIZBOOK['JOB_EXTRA_COURSES']; ?>">
                                        <hr>
                                        <input type="text" name="additional_info_2"
                                               value="<?php echo $service_expert_row['additional_info_2']; ?>"
                                               class="form-control"
                                               placeholder="<?php echo $BIZBOOK['JOB_TRAINING_DETAILS']; ?>">
                                        <hr>
                                        <input type="text" name="additional_info_3"
                                               value="<?php echo $service_expert_row['additional_info_3']; ?>"
                                               class="form-control"
                                               placeholder="<?php echo $BIZBOOK['JOB_OTHERS_1']; ?>">
                                        <hr>
                                        <input type="text" name="additional_info_4"
                                               value="<?php echo $service_expert_row['additional_info_4']; ?>"
                                               class="form-control"
                                               placeholder="<?php echo $BIZBOOK['JOB_OTHERS_2']; ?>">
                                    </div>
                                </div>
                            </div>
                            <div class="form-group col-md-6 serex-date">
                                <label class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-DATE-OF-BIRTH-LABEL']; ?></label>
                                <input type="text" name="date_of_birth"
                                       value="<?php echo $service_expert_row['date_of_birth']; ?>" class="form-control"
                                       id="dobfield">
                            </div>

                            <div class="form-group col-md-6 serex-time">
                                <label class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-ID-PROOF-LABEL']; ?></label>
                                <div class="fil-img-uplo">
                                    <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                    <input type="file" name="id_proof" accept="application/pdf,application/msword,
  application/vnd.openxmlformats-officedocument.wordprocessingml.document" class="form-control">
                                </div>
                            </div>

                            <div class="col-md-12">
                                <div class="form-group">
                                    <button name="service_expert_submit" class="blu-upp"><?php echo $BIZBOOK['SUBMIT_NOW']; ?></button>
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
            url: "expert_sub_category_process.php",
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
            url: "expert_area_process.php",
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