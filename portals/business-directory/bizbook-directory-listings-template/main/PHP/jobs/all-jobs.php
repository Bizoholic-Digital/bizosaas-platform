<?php
include "job-config-info.php";
include "../header.php";

if (isset($_SESSION['user_id'])) {
    $session_user_id = $_SESSION['user_id'];
}

if($footer_row['admin_job_show'] != 1) {
    header("Location: ".$webpage_full_link."dashboard");
}

if (isset($_GET['category'])) {


    $category_search_slug1 = str_replace('-', ' ', $_GET['category']);

    $category_search_slug = str_replace('.php', '', $category_search_slug1);

    $cat_search_row = getSlugJobCategory($category_search_slug);  //Fetch Category Id using category name

    $category_id = $cat_search_row['category_id'];

    $category_slug = $cat_search_row['category_slug'];

    $category_search_name = $cat_search_row['category_name'];

    $category_search_query = "AND FIND_IN_SET($category_id, category_id)";


}

if (isset($_GET['sub_cat']) && !empty($_GET['sub_cat'])) {
    //Sub category process From GET

    $subcategory_id = $_GET['sub_cat'];

    if (strstr($subcategory_id, ',')) {
        $data2 = explode(',', $subcategory_id);
        $sub_cat_array = array();
        foreach ($data2 as $c) {
            $sub_cat_array[] = "FIND_IN_SET($c,sub_category_id)";

        }
        $sub_category_search_query = 'AND (' . implode(' OR ', $sub_cat_array) . ')';
    } else {
        $sub_category_search_query = 'AND (FIND_IN_SET(' . $subcategory_id . ',sub_category_id))';

    }
}


//Salary Check starts
if (isset($_REQUEST['job_salary']) && !empty($_REQUEST['job_salary'])) {

    $get_job_salary = $_REQUEST['job_salary'];

    if (strstr($get_job_salary, ',')) {
        $data8 = explode(',', $get_job_salary);
        $cityarray = array();
        foreach ($data8 as $ci) {
            if($ci == 1000){
                $start_price = 0;
                $end_price = 1000;
            }elseif($ci == 5000){
                $start_price = 1001;
                $end_price = 5000;
            }elseif($ci == 15000){
                $start_price = 5001;
                $end_price = 15000;
            }else{
                $start_price = 15000;
                $end_price = 1000000;
            }
            $cityarray[] = "job_salary BETWEEN $start_price AND $end_price";

        }
        $salary_search_query = 'AND (' . implode(' OR ', $cityarray) . ')';
    } else {

        if($get_job_salary == 1000){
            $start_price = 0;
            $end_price = 1000;
        }elseif($get_job_salary == 5000){
            $start_price = 1001;
            $end_price = 5000;
        }elseif($get_job_salary == 15000){
            $start_price = 5001;
            $end_price = 15000;
        }else{
            $start_price = 15000;
            $end_price = 1000000;
        }
        $salary_search_query = 'AND (job_salary BETWEEN ' . $start_price . ' AND ' . $end_price . ')';

    }

}

//Salary Check Ends

//Job Type Check starts
if (isset($_REQUEST['job_type']) && !empty($_REQUEST['job_type'])) {

     $get_job_type = $_REQUEST['job_type'];

    if (strstr($get_job_type, ',')) {
        $data2 = explode(',', $get_job_type);
        $sub_cat_array = array();
        foreach ($data2 as $c) {
            $sub_cat_array[] = "FIND_IN_SET($c,job_type)";

        }
        $job_type_search_query = 'AND (' . implode(' OR ', $sub_cat_array) . ')';
    } else {
        $job_type_search_query = 'AND (FIND_IN_SET(' . $get_job_type . ',job_type))';

    }
}

//Job Type Check Ends

//Job Location Check starts
if (isset($_REQUEST['city']) && !empty($_REQUEST['city'])) {

    $get_city = $_REQUEST['city'];

    if (strstr($get_city, ',')) {
        $data56 = explode(',', $get_city);
        $sub_cat_array2 = array();
        foreach ($data56 as $c) {
            $sub_cat_array2[] = "FIND_IN_SET($c,job_location)";

        }
        $job_location_search_query = 'AND (' . implode(' OR ', $sub_cat_array2) . ')';
    } else {
        $job_location_search_query = 'AND (FIND_IN_SET(' . $get_city . ',job_location))';

    }
}

//Job Type Check Ends


?>
<style>
    .hom2-cus-sli ul {
        position: relative;
        overflow: hidden;
        padding: 20px 20px 0
    }

    .slick-arrow {
        width: 50px;
        height: 50px;
        border-radius: 50px;
        background: #fff;
        border: 1px solid #ededed;
        color: #ffffff03;
        position: absolute;
        z-index: 9;
        top: 38%
    }

    .slick-arrow:before {
        content: 'chevron_left';
        font-size: 27px;
        top: 4px;
        left: 9px
    }

    .slick-prev {
        left: 14px
    }

    .slick-next {
        right: 14px
    }

    .slick-next:before {
        content: 'chevron_right';
        font-size: 27px
    }
</style>


<!-- START -->
<section>
    <div class="all-listing all-jobs m">
        <!--FILTER ON MOBILE VIEW-->
        <div class="fil-mob fil-mob-act">
            <h4>Listing filters <i class="material-icons">filter_list</i></h4>
        </div>
        <div class="container">
            <div class="row">
                <div class="col-md-3 fil-mob-view">
                    <!--- START --->
                    <div class="filt-com">
                        <div class="job-alert">
                            <h5><?php echo $BIZBOOK['JOB-PROFILE-H1']; ?></h5>
                            <p><?php echo $BIZBOOK['JOB-PROFILE-P']; ?></p>
                            <a href="<?php echo $slash; ?>login"><?php echo $BIZBOOK['JOB-PROFILE-A']; ?></a>
                        </div>
                    </div>
                    <!--- END --->
                    <!--- START --->
                    <div class="filt-com lhs-cate">
                        <h4><?php echo $BIZBOOK['ALL-LISTING-CATEGORIES']; ?></h4>
                        <div class="form-group">
                            <select onChange="jobSubcategoryFilter(this.value);"
                                    name="cat_check" id="cat_check" class="cat_check chosen-select ">
                                <option value=""><?php echo $BIZBOOK['SELECT_CATEGORY']; ?></option>
                                <?php
                                foreach (getAllActiveJobCategoriesPos() as $categories_row) {
                                    ?>
                                    <option <?php if ($category_slug === $categories_row['category_slug']) {
                                        echo 'selected';
                                    } ?>
                                        value="<?php echo urlModifier($categories_row['category_slug']); ?>"><?php echo $categories_row['category_name']; ?></option>
                                    <?php
                                }
                                ?>
                            </select>
                        </div>
                    </div>
                    <!--- END --->
                    <!--- START --->
                    <div class="sub_cat_section filt-com lhs-sub">
                        <h4><?php echo $BIZBOOK['ALL-LISTING-SUB-CATEGORY']; ?></h4>
                        <ul>
                            <?php
                            if (isset($_GET['category'])) {
                                $sub_category_qry = getCategoryJobSubCategories($category_id);
                            } else {
                                $sub_category_qry = getAllJobSubCategories();
                            }
                            foreach ($sub_category_qry as $sub_category_row) { ?>
                                <li>
                                    <div class="chbox">
                                        <input type="checkbox" class="sub_cat_check" name="sub_cat_check"
                                               value="<?php echo $sub_category_row['sub_category_id']; ?>"
                                            <?php
                                            $subcategory_id_new = explode(',',$subcategory_id);
                                            if (in_array($sub_category_row['sub_category_id'], $subcategory_id_new)) {
                                                    echo "checked";
                                                }?>
                                               id="<?php echo $sub_category_row['sub_category_name']; ?>"/>
                                        <label
                                            for="<?php echo $sub_category_row['sub_category_name']; ?>"><?php echo $sub_category_row['sub_category_name']; ?></label>
                                    </div>
                                </li>
                                <?php
                            }
                            ?>
                        </ul>
                    </div>
                    <!--- END --->

                    <!--- START --->
                    <div class="filt-com lhs-sub">
                        <h4><?php echo $BIZBOOK['JOB-TYPE-LABEL']; ?></h4>
                        <ul>
                            <li>
                                <div class="chbox">
                                    <input type="checkbox" name="job_type" <?php
                                    $get_job_type_check_new = explode(',',$get_job_type);
                                    if (in_array(1, $get_job_type_check_new)) {
                                        echo 'checked';
                                    } ?> value="1" class="job_type" id="j1">
                                    <label for="j1"><?php echo $BIZBOOK['JOB-PERMANENT']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="chbox">
                                    <input type="checkbox" name="job_type" <?php
                                    $get_job_type_check_new = explode(',',$get_job_type);
                                    if (in_array(2, $get_job_type_check_new)) {
                                        echo 'checked';
                                    } ?> value="2" class="job_type" id="j2">
                                    <label for="j2"><?php echo $BIZBOOK['JOB-CONTRACT']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="chbox">
                                    <input type="checkbox" name="job_type" <?php
                                    $get_job_type_check_new = explode(',',$get_job_type);
                                    if (in_array(3, $get_job_type_check_new)) {
                                        echo 'checked';
                                    } ?> value="3" class="job_type" id="j3">
                                    <label for="j3"><?php echo $BIZBOOK['JOB-PART-TIME']; ?></label>
                                </div>
                            </li>
                            <li>
                                <div class="chbox">
                                    <input type="checkbox" name="job_type" <?php
                                    $get_job_type_check_new = explode(',',$get_job_type);
                                    if (in_array(4, $get_job_type_check_new)) {
                                        echo 'checked';
                                    } ?> value="4" class="job_type" id="j4">
                                    <label for="j4"><?php echo $BIZBOOK['JOB-FREELANCE']; ?></label>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <!--- END --->
                    <!--- START --->
                    <div class="filt-com lhs-sub">
                        <h4><?php echo $BIZBOOK['JOB-LOCATION-LABEL']; ?></h4>
                        <ul>
                            <?php
                            $job_location_qry = getAllJobGroupByCity();

                            foreach ($job_location_qry as $job_location_row) {

                                $job_location = $job_location_row['job_location'];

                                $job_city_row = getJobCity($job_location);

                                ?>
                                <li>
                                    <div class="chbox">
                                        <input type="checkbox" name="city_check" <?php
                                        $get_city_new = explode(',',$get_city);
                                        if (in_array($job_city_row['city_id'], $get_city_new)) {
                                            echo 'checked';
                                        } ?> class="city_check" value="<?php echo $job_city_row['city_id']; ?>" id="city_check<?php echo $job_city_row['city_id']; ?>">
                                        <label for="city_check<?php echo $job_city_row['city_id']; ?>"><?php echo $job_city_row['city_name']; ?></label>
                                    </div>
                                </li>
                                <?php
                            }
                            ?>
                        </ul>
                    </div>
                    <!--- END --->
                    <!--- START --->
                    <div class="filt-com lhs-sub">
                        <h4><?php echo $BIZBOOK['JOB-SALARY-LABEL']; ?></h4>
                        <ul>
                            <li>
                                <div class="chbox">
                                    <input type="checkbox" name="job_salary" <?php
                                    $get_job_salary_new = explode(',',$get_job_salary);
                                    if (in_array(1000, $get_job_salary_new)) {
                                        echo 'checked';
                                    } ?> value="1000" class="job_salary" id="sal1">
                                    <label for="sal1"><?php echo $footer_row['currency_symbol']; ?> 0 - 1000</label>
                                </div>
                            </li>
                            <li>
                                <div class="chbox">
                                    <input type="checkbox" name="job_salary" <?php
                                    $get_job_salary_new = explode(',',$get_job_salary);
                                    if (in_array(5000, $get_job_salary_new)) {
                                        echo 'checked';
                                    } ?> value="5000" class="job_salary" id="sal2">
                                    <label for="sal2"><?php echo $footer_row['currency_symbol']; ?> 1000 - 5000</label>
                                </div>
                            </li>
                            <li>
                                <div class="chbox">
                                    <input type="checkbox" name="job_salary" <?php
                                    $get_job_salary_new = explode(',',$get_job_salary);
                                    if (in_array(15000, $get_job_salary_new)) {
                                        echo 'checked';
                                    } ?> value="15000" class="job_salary" id="sal3">
                                    <label for="sal3"><?php echo $footer_row['currency_symbol']; ?> 5000 - 15000</label>
                                </div>
                            </li>
                            <li>
                                <div class="chbox">
                                    <input type="checkbox" name="job_salary" <?php
                                    $get_job_salary_new = explode(',',$get_job_salary);
                                    if (in_array(15001, $get_job_salary_new)) {
                                        echo 'checked';
                                    } ?> value="15001" class="job_salary" id="sal4">
                                    <label for="sal4"><?php echo $footer_row['currency_symbol']; ?> 15000 - above</label>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <!--- END --->
                </div>
                <?php
                $jobsql = "SELECT *  FROM " . TBL . "jobs  WHERE job_status= 'Active' $category_search_query $sub_category_search_query $salary_search_query $job_type_search_query $job_location_search_query ORDER BY job_id DESC";

                $jobrs = mysqli_query($conn, $jobsql);
                $total_jobs = mysqli_num_rows($jobrs);

                ?>
                <div class="col-md-9 all-job-total">
                    <?php

                    if (mysqli_num_rows($jobrs) > 0) {
                        ?>
                        <div
                            class="job-ser-cnt"><?php echo $BIZBOOK['JOB-SHOWING']; ?> <?php echo AddingZero_BeforeNumber($total_jobs); ?> <?php echo $BIZBOOK['JOBS_BRACKET']; ?></div>
                        <div class="job-list">
                            <ul>
                                <?php
                                while ($jobrow = mysqli_fetch_array($jobrs)) {

                                    $job_id = $jobrow['job_id'];
                                    $job_user_id = $jobrow['user_id'];

                                    $usersqlrow = getUser($job_user_id); // To Fetch particular User Data
                                    $total_count_jobs_applied = getCountJobAppliedJob($job_id);
                                    ?>
                                    <li>
                                        <div class="job-box">
                                            <div class="job-box-img">
                                                <img
                                                    src="<?php echo $slash; ?>jobs/images/jobs/<?php echo $jobrow['company_logo']; ?>"
                                                    alt="">
                                            </div>
                                            <div class="job-days">
                                                <span
                                                    class="day"><?php echo time_elapsed_string($jobrow['job_cdt']); ?></span>
                                                <span
                                                    class="apl"><?php echo $total_count_jobs_applied; ?> <?php echo $BIZBOOK['APPLICANTS']; ?></span>
                                            </div>
                                            <div class="job-box-con">
                                                <h4><?php echo $jobrow['job_title']; ?></h4>
                                                <span><?php echo $jobrow['job_role']; ?></span>
                                            <span><?php
                                                $job_type = $jobrow['job_type'];
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
                                                <span><?php echo AddingZero_BeforeNumber($jobrow['no_of_openings']); ?> <?php echo $BIZBOOK['JOB_OPENINGS']; ?></span>
                                            </div>
                                            <div class="job-box-apl">
                                                <span
                                                    class="job-box-cta"><?php echo $BIZBOOK['JOB_APPLY_NOW']; ?></span>
                                                <span><?php echo $BIZBOOK['JOB_MORE_DETAILS']; ?></span>
                                            </div>
                                            <a href="<?php echo $JOB_URL . urlModifier($jobrow['job_slug']); ?>"
                                               class="job-full-cta"></a>
                                        </div>
                                    </li>
                                    <?php
                                }
                                ?>
                            </ul>
                        </div>
                        <?php
                    }else {
                        ?>
                        <span style="    font-size: 21px;
    color: #bfbfbf;
    letter-spacing: 1px;
    /* background: #525252; */
    text-shadow: 0px 0px 2px #fff;
    text-transform: uppercase;
    text-align: center!important;
    margin-top: 5%;"><?php echo $BIZBOOK['JOBS_NO_JOBS_MESSAGE']; ?></span>
                        <?php
                    }
                    ?>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->


<?php
include "../footer.php";
?>


<!--  Quick View box starts  -->
<!-- START -->
<section>

</section>
<!-- END -->
<!--  Quick View box ends  -->

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script src="<?php echo $slash; ?>js/select-opt.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>jobs/js/job_filter.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>

<!--on page scroll load data ends-->
<script>
    function jobSubcategoryFilter(val) {
        $(".sub_cat_section").css("opacity", 0);
        $.ajax({
            type: "POST",
            url: "<?php echo $slash; ?>jobs/job_sub_category_filter.php",
            data: 'category_id=' + val,
            success: function (data) {
                if (data == null) {
                    $(".sub_cat_section").remove();
                } else {
                    $(".sub_cat_section").html(data);
                    $(".sub_cat_section").css("opacity", 1);
                }

            }
        });
    }
</script>

</body>

</html>