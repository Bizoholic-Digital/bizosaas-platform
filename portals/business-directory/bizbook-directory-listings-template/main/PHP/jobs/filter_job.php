<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if(file_exists('job-config-info.php'))
{
    include "job-config-info.php";
}

if (isset($_SESSION['user_id'])) {
    $session_user_id = $_SESSION['user_id'];
}
$user_details_row = getUser($session_user_id); //Fetch User data

//Pagination Code Starts Here
$numberOfPages = 8;
$limit = 15;
if (isset($_GET["page"])) {
    $page = $_GET["page"];
} else {
    $page = 1;
};
$start_from = ($page - 1) * $limit;

//Pagination Code Ends Here


$scheck = $_REQUEST['scheck'];
$cat_check = $_REQUEST['cat_check'];
$sub_cat_check = $_REQUEST['sub_cat_check'];
$job_salary = $_REQUEST['job_salary'];
$city_check = $_REQUEST['city_check'];
$job_type_check = $_REQUEST['job_type_check'];


$WHERE = array();
$inner = $w = '';

// Category Check starts
if (!empty($cat_check)) {
    if (strstr($cat_check, ',')) {
        $data2 = explode(',', $cat_check);
        $cat_array = array();
        foreach ($data2 as $c) {
            $cat_array[] = "FIND_IN_SET($c,t1.category_id)";

        }
        $WHERE[] = '(' . implode(' OR ', $cat_array) . ')';
    } else {
        $WHERE[] = '(FIND_IN_SET(' . $cat_check . ',t1.category_id))';

    }
}

// Category Check Ends


//Sub Category Check starts
if (!empty($sub_cat_check)) {
    if (strstr($sub_cat_check, ',')) {
        $data2 = explode(',', $sub_cat_check);
        $sub_cat_array = array();
        foreach ($data2 as $c) {
            $sub_cat_array[] = "FIND_IN_SET($c,t1.sub_category_id)";

        }
        $WHERE[] = '(' . implode(' OR ', $sub_cat_array) . ')';
    } else {
        $WHERE[] = '(FIND_IN_SET(' . $sub_cat_check . ',t1.sub_category_id))';

    }
}

//Sub Category Check Ends

//Price Check starts
if (!empty($job_salary)) {

    if (strstr($job_salary, ',')) {
        $data8 = explode(',', $job_salary);
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
            $cityarray[] = "t1.job_salary BETWEEN $start_price AND $end_price";

        }
        $WHERE[] = '(' . implode(' OR ', $cityarray) . ')';
    } else {

            if($job_salary == 1000){
                $start_price = 0;
                $end_price = 1000;
            }elseif($job_salary == 5000){
                $start_price = 1001;
                $end_price = 5000;
            }elseif($job_salary == 15000){
                $start_price = 5001;
                $end_price = 15000;
            }else{
                $start_price = 15000;
                $end_price = 1000000;
            }
        $WHERE[] = '(t1.job_salary BETWEEN ' . $start_price . ' AND ' . $end_price . ')';

    }

}

//Price Check Ends

//Job Type Check starts
if (!empty($job_type_check)) {
    if (strstr($job_type_check, ',')) {
        $data2 = explode(',', $job_type_check);
        $sub_cat_array = array();
        foreach ($data2 as $c) {
            $sub_cat_array[] = "FIND_IN_SET($c,t1.job_type)";

        }
        $WHERE[] = '(' . implode(' OR ', $sub_cat_array) . ')';
    } else {
        $WHERE[] = '(FIND_IN_SET(' . $job_type_check . ',t1.job_type))';

    }
}

//Job Type Check Ends

//Job Location Check starts
if (!empty($city_check)) {
    if (strstr($city_check, ',')) {
        $data56 = explode(',', $city_check);
        $sub_cat_array2 = array();
        foreach ($data56 as $c) {
            $sub_cat_array2[] = "FIND_IN_SET($c,t1.job_location)";

        }
        $WHERE[] = '(' . implode(' OR ', $sub_cat_array2) . ')';
    } else {
        $WHERE[] = '(FIND_IN_SET(' . $city_check . ',t1.job_location))';

    }
}

//Job Type Check Ends

if (!empty($price_range)) {
    $data3 = explode('-', $price_range);
    $WHERE[] = "(t1.product_rate between $data3[0] and $data3[1])";
}

if (!empty($scheck)) {
    if (strstr($scheck, ',')) {
        $data3 = explode(',', $scheck);
        $sarray = array();
        foreach ($data3 as $c) {
            $sarray[] = "t2.size_id = $c";
        }
        $WHERE[] = '(' . implode(' OR ', $sarray) . ')';
    } else {
        $WHERE[] = '(t2.size_id = ' . $scheck . ')';
    }

    $inner = 'INNER JOIN `product_size_quantity` AS t2 ON t1.product_id = t2.product_id';

}

if (!empty($category_id)) {
    if (strstr($category_id, ',')) {
        $data4 = explode(',', $category_id);
        $ctarray = array();
        foreach ($data4 as $ct) {
            $ctarray[] = "t1.product_category_id = $ct";
        }
        $WHERE[] = '(' . implode(' OR ', $ctarray) . ')';
    } else {
        $WHERE[] = '(t1.category_id = ' . $category_id . ')';
    }
}

$w = implode(' AND ', $WHERE);
if (!empty($w)) {
    $w = 'WHERE ' . $w;
    $q = 'AND ';
} else {
    $q = 'WHERE ';
}
$footer_row = getAllFooter();


$query = mysqli_query($conn, "SELECT DISTINCT  t1 . * FROM  " . TBL . "jobs  AS t1 $inner $w $q job_status= 'Active' ORDER BY job_id DESC ");
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
<div class="col-md-9 all-job-total">
    <?php

    $total_jobs = mysqli_num_rows($query);

    if (mysqli_num_rows($query) > 0) {

        ?>
        <div class="job-ser-cnt"><?php echo $BIZBOOK['JOB-SHOWING']; ?> <?php echo AddingZero_BeforeNumber($total_jobs); ?> <?php echo $BIZBOOK['JOBS_BRACKET']; ?></div>
        <div class="job-list">
            <ul>
                <?php
                while ($jobrow = mysqli_fetch_array($query)) {

                    $job_id = $jobrow['job_id'];
                    $job_user_id = $jobrow['user_id'];

                    $usersqlrow = getUser($job_user_id); // To Fetch particular User Data
                    $total_count_jobs_applied = getCountJobAppliedJob($job_id);
                    ?>
                    <li>
                        <div class="job-box">
                            <div class="job-box-img">
                                <img src="<?php echo $slash; ?>images/jobs/<?php echo $jobrow['company_logo']; ?>" alt="">
                            </div>
                            <div class="job-days">
                                <span class="day"><?php echo time_elapsed_string($jobrow['job_cdt']); ?></span>
                                <span class="apl"><?php echo $total_count_jobs_applied; ?> <?php echo $BIZBOOK['APPLICANTS']; ?></span>
                            </div>
                            <div class="job-box-con">
                                <h4><?php echo $jobrow['job_title']; ?></h4>
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
                                <span><?php echo $jobrow['job_role']; ?></span>
                                <span><?php echo AddingZero_BeforeNumber($jobrow['no_of_openings']); ?> <?php echo $BIZBOOK['JOB_OPENINGS']; ?></span>
                            </div>
                            <div class="job-box-apl">
                                <span class="job-box-cta"><?php echo $BIZBOOK['JOB_APPLY_NOW']; ?></span>
                                <span><?php echo $BIZBOOK['JOB_MORE_DETAILS']; ?></span>
                            </div>
                            <a href="<?php echo $JOB_URL . urlModifier($jobrow['job_slug']); ?>" class="job-full-cta"></a>
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
    margin-top: 5%;"><?php echo $BIZBOOK['JOBS_NO_JOBS_MESSAGE']; ?></span>
        <?php
    }
    ?>
</div>

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link ='<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url ='<?php echo $LOGIN_URL;?>';</script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>jobs/js/job_filter.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>