<?php
include "job-config-info.php";
include "../header.php";

if($footer_row['admin_job_show'] != 1) {
    header("Location: ".$webpage_full_link."dashboard");
}

?>
<style>
    .hom-head .container{display:none}
.hom-top{transition:all .5s ease;background:#000;box-shadow:none}
.hom-head{background:none!important;padding:0;margin:0}
.hom-head .hom-top .container{display:block}
.dmact .top-ser{display:block}
.hm3-auto-ban{background:url(images/automobile-bg.jpg) no-repeat;background-size:100%;background-position:center right;padding-top:55px}
.h2-ban-ql{display:table}
.hm3-auto-ban .rhs .hom-col-req .log-bor{display:block}
.caro-home{margin-top:90px;float:left;width:100%}
.carousel-item:before{background:none}
.ban-tit h1{font-weight:500;color:#fff;text-shadow:none}
.ban-tit h1 b{font-weight:700;font-size:42px;line-height:49px;padding-bottom:15px;color:#fff;text-shadow:none}
.h2-ban-ql ul li div{border:1px solid #d9d9da;background:#fff}
.h2-ban-ql ul li div h5{font-weight:500;color:#383942}
.h2-ban-ql ul li div h5 span{font-weight:700}
.home-tit h2{font-weight:400}
.home-tit h2 span{font-weight:700}
.h2-ban-ql ul li div:hover{background:#d3f0fb;box-shadow:0 14px 22px -13px #0b1017ba}
.land-pack-grid-text{position:relative;-webkit-transition:all .5s ease;-moz-transition:all .5s ease;-o-transition:all .5s ease;transition:all .5s ease;position:absolute;top:0;bottom:0;left:0;right:0;width:100%;height:100%;z-index:2;background:linear-gradient(to top,#000000c7,#00000008)}
.land-pack-grid-text h4{padding:15px;font-size:20px;font-weight:400;text-align:center;bottom:0;position:absolute;width:100%;text-align:center;color:#fff}
.land-pack-grid-text h4 .dir-ho-cat{color:#f6f7f9;font-size:11px;position:relative;width:100%;display:inline-block}
.land-pack-grid-img{background:#333}
.home-tit{padding-top:60px}
.hom2-hom-ban{float:left;width:46%;background-size:cover;margin:0 2%;background:#e6f6fb;padding:30px 100px 30px 30px;border-radius:5px;position:relative}
.hom2-hom-ban:hover a{background:#d6c607}
.hom2-hom-ban h2{font-weight:600;font-size:22px;padding-bottom:5px}
.hom2-hom-ban p{font-size:14px}
.hom2-hom-ban a{background:#21d78d;color:#fff;padding:10px 20px;border-radius:5px;display:inline-block;cursor:pointer;font-size:13px;font-weight:400}
.hom2-hom-ban p,.hom2-hom-ban h2,.hom2-hom-ban a{position:relative;color:#fff}
.hom2-hom-ban:before{content:'';position:absolute;width:100%;height:100%;left:0;top:0;right:0;bottom:0;z-index:0;opacity:.8;background:#24C6DC;border-radius:5px}
.hom2-hom-ban1:before{background-image:linear-gradient(140deg,#0c7ada 0%,#0761af 50%,#0f243e94 75%)}
.hom2-hom-ban2:before{background-image:linear-gradient(140deg,#768404 0%,#768404 50%,#0f243e94 75%)}
.hom2-hom-ban1{background-image:url(../images/home2-hand.jpg)}
.hom2-hom-ban2{background-image:url(../images/home2-work.jpg)}
.hom2-hom-ban-main{float:left;width:100%;padding-bottom:70px}
.hom2-cus-sli{float:left;width:100%;padding-top:0}
.hom2-cus-sli ul li{float:left;width:25%;padding:12px 20px}
.testmo{width:100%;background:#fff;box-shadow:0 1px 7px -3px #161d2926;border-radius:5px;padding:30px;position:relative}
.testmo img{width:64px;height:64px;border-radius:50px;object-fit:cover;margin:-80px 0 0}
.testmo h4{font-size:14px;font-weight:600;margin-bottom:2px;}
.testmo span{font-size:11px;font-weight:400;color:#727688}
.testmo span a{font-weight:500;color:#4caf50;display:block;font-size:12px}
.testmo p{color:#727688;font-size:12px;line-height:20px;margin:0;font-weight:400;height:58px;overflow:hidden;border-top:1px solid #f1eeee;padding-top:15px;margin-top:15px}
.testmo p:before{content:'format_quote';font-size:21px;margin:-25px 0 0;background:#fff}
.hom2-cus{background:#f7f8f9;padding-bottom:70px}
.testmo .rat{padding:2px 2px 2px 10px;display:inline-block;position:absolute;right:30px;top:50px}
.testmo .rat i{color:#FF9800;font-size:13px;width:7px}
.hom2-cus-sli ul{position:relative;overflow:hidden;padding:20px 20px 0}
.slick-arrow{width:50px;height:50px;border-radius:50px;background:#fff;border:1px solid #ededed;color:#ffffff03;position:absolute;z-index:9;top:38%}
.slick-arrow:before{content:'chevron_left';font-size:27px;top:4px;left:9px}
.slick-prev{left:14px}
.slick-next{right:14px}
.slick-next:before{content:'chevron_right';font-size:27px}
.hom4-prop-box{padding:0;background:#fff;box-shadow:0 1px 14px -4px #161d2926;border:1px solid #efefef}
.hom4-prop-box img{width:100%;border-radius:2px;margin:0;height:120px}
.hom4-prop-box div{padding:25px}
.hom4-prop-box .rat{position:relative;top:initial;right:initial;padding:2px 2px 2px 0;display:block;margin:0;height:17px;left:-2px}
.hom4-fea{background:#fff;padding-bottom:40px}
.hom4-fea .hom2-cus-sli ul li{padding:12px 20px}
.hom4-fea .home-tit{margin-bottom:0;padding-top:70px}
</style>

<!-- START -->
<section>
    <div class="all-jobs-ban">
        <div class="container">
            <div class="row">
                <div class="jtit">
                    <h1><?php echo $BIZBOOK['JOB-HEADER-H1']; ?></h1>
                    <p><?php echo $BIZBOOK['JOB-HEADER-P']; ?></p>
                </div>
                <br>
                <div class="job-sear">
                    <form name="job_filter_form" id="job_filter_form" class="job_filter_form">
                        <ul>
                            <li class="sr-sea">
                                <select class="chosen-select" id="job-select-search" name="serjobs">
                                    <?php
                                    foreach (getAllJobCategories() as $job_search_categories_row) {

                                    $search_category_name = $job_search_categories_row['category_name'];

                                    $search_category_id = $job_search_categories_row['category_id'];
                                    ?>
                                    <option value="<?php echo $search_category_id; ?>"><?php echo $search_category_name; ?></option>
                                        <?php
                                    }
                                    ?>
                                </select>
                            </li>
                            <li class="sr-loc">
                                <select class="chosen-select" id="job-select-city" name="serjobsloc">
                                    <?php
                                    $job_location_qry = getAllJobGroupByCity();

                                    foreach ($job_location_qry as $job_location_row) {

                                    $job_location = $job_location_row['job_location'];

                                    $job_city_row = getJobCity($job_location);

                                    ?>
                                    <option value="<?php echo $job_city_row['city_id']; ?>"><?php echo $job_city_row['city_name']; ?></option>
                                        <?php
                                    }
                                    ?>
                                </select>
                            </li>
                            <li class="sr-btn">
                                <button id="job_filter_submit"><i class="material-icons">search</i></button>
                            </li>
                        </ul>
                    </form>
                </div>
                <div class="job-pop-tag">
                    <?php
                    foreach (getAllJobCategoriesOrderByJobsTableLimit(5) as $job_trend_categories_row) {

                        $trend_category_name = $job_trend_categories_row['category_name'];

                        $trend_category_id = $job_trend_categories_row['category_id'];
                        ?>
                        <a href="<?php echo $ALL_JOBS_URL . urlModifier($job_trend_categories_row['category_slug']); ?>"><?php echo $trend_category_name; ?></a>
                        <?php
                    }
                    ?>
                </div>
                <div class="job-counts">
                    <ul>
                        <li>
                            <span class="count1"><?php echo AddingZero_BeforeNumber(getCountJob()); ?></span>
                            <h4><?php echo $BIZBOOK['JOB-POSTED']; ?></h4>
                        </li>
                        <li>
                            <span class="count1"><?php echo AddingZero_BeforeNumber(getCountJobCompanyName()); ?></span>
                            <h4><?php echo $BIZBOOK['JOB-COMPANIES']; ?></h4>
                        </li>
                        <li>
                            <span class="count1"><?php echo AddingZero_BeforeNumber(getCountJobProfile()); ?></span>
                            <h4><?php echo $BIZBOOK['JOB-EMPLOYEES']; ?></h4>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<!-- START -->
<section>
    <div class="jobs-cate">
        <div class="container">
            <div class="row">
                <div class="sub-tit">
                    <h2><?php echo $BIZBOOK['JOB-HEADER-H2']; ?></h2>
                    <p><?php echo $BIZBOOK['JOB-HEADER-P2']; ?></p>
                </div>
                <div class="job-cate-main">
                    <ul>
                        <?php
                        foreach (getAllJobCategoriesOrderByJobsTable() as $job_categories_row) {

                            $category_name = $job_categories_row['category_name'];

                            $category_id = $job_categories_row['category_id'];

                            $total_jobs_category = getCountCategoryJob($category_id);
                            ?>
                            <li>
                                <div>
                                    <h4><?php echo $category_name; ?></h4>
                                    <span><?php echo $total_jobs_category; ?> <?php echo $BIZBOOK['JOBS']; ?></span><a
                                        href="<?php echo $ALL_JOBS_URL . urlModifier($job_categories_row['category_slug']); ?>" class="fcli"></a>
                                </div>
                            </li>
                            <?php
                        }
                        ?>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<!-- START -->
<section>
    <div class="str hom2-cus hom4-fea">
        <div class="container">
            <div class="row">
                <div class="home-tit">
                    <h2><span><?php echo $BIZBOOK['JOB-HEADER-H3']; ?></span></h2>
                    <p><?php echo $BIZBOOK['JOB-HEADER-P3']; ?></p>
                </div>
                <div class="job-tre">
                    <ul>
                        <?php

                        foreach (getAllJobLimit(3) as $job_profile_row) {

                            $job_id = $job_profile_row['job_id'];

                            $total_count_jobs_applied = getCountJobAppliedJob($job_id);
                            ?>
                            <li>
                                <div class="inn">
                                    <div class="jbtre-img">
                                        <div class="jbtre-img1">
                                            <img src="<?php echo $slash; ?>jobs/images/jobs/<?php echo $job_profile_row['company_logo']; ?>"
                                                 alt="">
                                        </div>
                                        <div class="jbtre-img2">
                                            <h4><?php echo $job_profile_row['job_title']; ?></h4>
                                            <span><?php $job_location_row = getJobCity($job_profile_row['job_location']); echo $job_location_row['city_name']; ?></span>
                                            <div class="jbtre-days">
                                                <span><?php echo time_elapsed_string($job_profile_row['job_cdt']); ?></span>
                                                <span><?php echo $total_count_jobs_applied; ?> <?php echo $BIZBOOK['APPLICANTS']; ?></span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="jbtre-con">
                                        <span><?php
                                            $job_type = $job_profile_row['job_type'];
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
                                        <span><?php echo $job_profile_row['job_role']; ?></span>
                                        <span><?php echo AddingZero_BeforeNumber($job_profile_row['no_of_openings']); ?> <?php echo $BIZBOOK['JOB_OPENINGS']; ?></span>
                                    </div>
                                    <div class="jbtre-sale">
                                        <span><?php echo $BIZBOOK['JOB-SALARY-LABEL']; ?></span>
                                        <span class="empsal"><?php echo $job_profile_row['job_salary']; ?>K</span>
                                    </div>
                                    <div class="jbtre-apl">
                                        <span class="job-box-cta"><?php echo $BIZBOOK['JOB_APPLY_NOW']; ?></span>
                                        <span><?php echo $BIZBOOK['JOB_MORE_DETAILS']; ?></span>
                                    </div>
                                    <a href="<?php echo $JOB_URL . urlModifier($job_profile_row['job_slug']); ?>"
                                       class="job-full-cta"></a>
                                </div>
                            </li>
                            <?php
                        }
                        ?>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<!-- START -->
<section>
    <div class="str">
        <div class="container">
            <div class="row">
                <div class="home-tit">
                    <h2><span><?php echo $BIZBOOK['HOM3-OW-TIT']; ?></span></h2>
                    <p><?php echo $BIZBOOK['HOM3-OW-TIT-SUB']; ?></p>
                </div>
                <div class="hom2-hom-ban-main">
                   <div class="hom2-hom-ban hom2-hom-ban1">
                        <h2><?php echo $BIZBOOK['JOB-HOME-JOIN-EMP-TIT']; ?></h2>
                        <p><?php echo $BIZBOOK['JOB-HOME-JOIN-EMP-SUB-TIT']; ?></p>
                        <a href="<?php echo $slash; ?>login?login=register"><?php echo $BIZBOOK['JOB-HOME-JOIN-EMP-CTA']; ?></a>
                    </div>
                    <div class="hom2-hom-ban hom2-hom-ban2">
                        <h2><?php echo $BIZBOOK['JOB-HOME-JOIN-COMP-TIT']; ?></h2>
                        <p><?php echo $BIZBOOK['JOB-HOME-JOIN-COMP-SUB-TIT']; ?></p>
                        <a href="<?php echo $slash; ?>login?login=register"><?php echo $BIZBOOK['JOB-HOME-JOIN-COMP-CTA']; ?></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<!-- START -->
<section>
    <div class="str hom2-cus hom4-fea">
        <div class="container">
            <div class="row">
                <div class="home-tit">
                    <h2><span><?php echo $BIZBOOK['JOB-HEADER-H4']; ?></span></h2>
                    <p><?php echo $BIZBOOK['HOM-BEST-SUB-TIT']; ?></p>
                </div>

                <div class="hom2-cus-sli job-list">
                    <ul class="multiple-items1">
                        <?php
                        $si = 1;

                        foreach (getAllJobPopular() as $row) {

                            $job_name = $row['job_name'];

                            $job_popular_id = $row['job_popular_id'];

                            $job_sql_row = getIdJob($job_name);
                            $job_id = $job_sql_row['job_id'];
                            $total_count_jobs_applied = getCountJobAppliedJob($job_id);

                            ?>
                            <li>
                                <div class="job-box">
                                    <div class="job-box-img">
                                        <img src="<?php echo $slash; ?>jobs/images/jobs/<?php echo $job_sql_row['company_logo']; ?>" alt="">
                                    </div>
                                    <div class="job-days">
                                        <span class="day"><?php echo time_elapsed_string($job_sql_row['job_cdt']); ?></span>
                                        <span class="apl"><?php echo $total_count_jobs_applied; ?> <?php echo $BIZBOOK['APPLICANTS']; ?></span>
                                    </div>
                                    <div class="job-box-con">
                                        <h4><?php echo $job_sql_row['job_title']; ?></h4>
                                        <span><?php
                                            $job_type = $job_sql_row['job_type'];
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
                                        <span><?php echo $job_sql_row['job_role']; ?></span>
                                        <span><?php echo AddingZero_BeforeNumber($job_sql_row['no_of_openings']); ?> <?php echo $BIZBOOK['JOB_OPENINGS']; ?></span>
                                    </div>
                                    <div class="job-box-apl">
                                        <span class="job-box-cta"><?php echo $BIZBOOK['JOB_APPLY_NOW']; ?></span>
                                    </div>
                                    <a href="<?php echo $JOB_URL . urlModifier($job_sql_row['job_slug']); ?>" class="job-full-cta"></a>
                                </div>
                            </li>
                            <?php
                        }
                        ?>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->


<!-- START -->
<section>
    <div class="str count">
        <div class="container">
            <div class="row">

                <div class="how-wrks">
                    <div class="home-tit">
                        <h2><span><?php echo $BIZBOOK['HOM-HOW-TIT']; ?></span></h2>
                        <p><?php echo $BIZBOOK['HOM-HOW-SUB-TIT']; ?></p>
                    </div>
                    <div class="how-wrks-inn">
                        <ul>
                            <li>
                                <div>
                                    <span>1</span>
                                    <img src="<?php echo $slash; ?>images/icon/how1.png" alt="">
                                    <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-1']; ?></h4>
                                    <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-1']; ?></p>
                                </div>
                            </li>
                            <li>
                                <div>
                                    <span>2</span>
                                    <img src="<?php echo $slash; ?>images/icon/how2.png" alt="">
                                    <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-2']; ?></h4>
                                    <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-2']; ?></p>
                                </div>
                            </li>
                            <li>
                                <div>
                                    <span>3</span>
                                    <img src="<?php echo $slash; ?>images/icon/how3.png" alt="">
                                    <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-3']; ?></h4>
                                    <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-3']; ?></p>
                                </div>
                            </li>
                            <li>
                                <div>
                                    <span>4</span>
                                    <img src="<?php echo $slash; ?>images/icon/how4.png" alt="">
                                    <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-4']; ?></h4>
                                    <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-4']; ?></p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>


                <div class="mob-app">
                    <div class="lhs">
                        <img src="<?php echo $slash; ?>images/mobile.png" alt="">
                    </div>
                    <div class="rhs">
                        <h2><?php echo $BIZBOOK['HOM-APP-TIT']; ?>
                            <span><?php echo $BIZBOOK['HOM-APP-TIT-SUB']; ?></span></h2>
                        <ul>
                            <li><?php echo $BIZBOOK['HOM-APP-PO-1']; ?></li>
                            <li><?php echo $BIZBOOK['HOM-APP-PO-2']; ?></li>
                            <li><?php echo $BIZBOOK['HOM-APP-PO-3']; ?></li>
                            <li><?php echo $BIZBOOK['HOM-APP-PO-4']; ?></li>
                        </ul>
                        <span><?php echo $BIZBOOK['HOM-APP-SEND']; ?></span>
                        <form>
                            <ul>
                                <li>
                                    <input type="email" placeholder="Enter email id" required></li>
                                <li>
                                    <input type="submit" value="Get App Link"></li>
                            </ul>
                        </form>
                        <a href="#"><img src="<?php echo $slash; ?>images/android.png" alt=""> </a>
                        <a href="#"><img src="<?php echo $slash; ?>images/apple.png" alt=""> </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->


<!-- START -->
<section>
    <div class="hom-ads">
        <div class="container">
            <div class="row">
                <div class="filt-com lhs-ads">
                    <div class="ads-box">
                        <?php
                        $ad_position_id = 1;   //Ad position on home page bottom
                        $get_ad_row = getAds($ad_position_id);
                        $ad_enquiry_photo = $get_ad_row['ad_enquiry_photo'];
                        ?>
                        <a href="<?php echo stripslashes($get_ad_row['ad_link']); ?>">
                            <span>Ad</span>

                            <img src="<?php echo $slash; ?>images/ads/<?php if ($ad_enquiry_photo != NULL || !empty($ad_enquiry_photo)) {
                                echo $ad_enquiry_photo;
                            } else {
                                echo "ads2.jpg";
                            } ?>" alt="">
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<!-- START -->
<div class="ani-quo">
    <div class="ani-q1">
        <h4><?php echo $BIZBOOK['HOM-WHAT-LOOK-TIT']; ?></h4>
        <p><?php echo $BIZBOOK['HOM-WHAT-LOOK-SUB']; ?></p>
        <span><?php echo $BIZBOOK['HOM-WHAT-LOOK-CTA']; ?></span>
    </div>
    <div class="ani-q2">
        <img src="<?php echo $slash; ?>images/quote.png" alt="">
    </div>
</div>
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
<script src="<?php echo $slash; ?>js/select-opt.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="<?php echo $slash; ?>js/slick.js"></script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>
<script>
    $(window).scroll(function () {
        var scroll = $(window).scrollTop();
        if (scroll >= 250) {
            $(".hom-top").addClass("dmact");
        }
        else {
            $(".hom-top").removeClass("dmact");
        }
    });
    $('.multiple-items1').slick({
        infinite: true,
        slidesToShow: 4,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
        responsive: [{
            breakpoint: 992,
            settings: {
                slidesToShow: 1,
                slidesToScroll: 1,
                centerMode: false
            }
        }]

    });
</script>
</body>

</html>