<?php
include "expert-config-info.php";
include "../header.php";

if($footer_row['admin_expert_show'] != 1) {
    header("Location: ".$webpage_full_link."dashboard");
}

?>
<style>
.hom-head .container{display:none}
.hom-top{transition:all .5s ease;background:#3d05c6;box-shadow:none}
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
.home-tit h2{font-weight:400;}
.home-tit h2 span{font-weight:700;font-size:32px;color:#4a5e95;position:relative;z-index:2}
.home-tit h2 span:before{content:'';position:absolute;width:40%;height:6px;background:#ff83bc;bottom:1px;left:30%;z-index:-1;transform:skew(51deg,0deg)}
.home-tit p{color:#4e6d8d}
.all-jobs-ban{margin-bottom:0}
.job-sear ul li.sr-btn button{background:#8cc152}
.all-jobs-ban h1{font-size: 50px;color: #fff;text-shadow: 0 1px 3px #333333f7;}
.job-sear ul li.sr-sea {width: calc(100% - 50px);}    
.job-sear ul li.sr-sea:before{content:'people'}
.all-jobs-ban p{color: #fff;}
.all-jobs-ban{background:url(../images/ex2.jpg) #f3e5ff no-repeat;background-size:cover}
.all-jobs-ban:before{content: '';position: absolute;width: 100%;height: 100%;left: 0px;right: 0px;top: 0px;bottom: 0px;background:linear-gradient(to top,#292930fa -6%,#f6f7f605 125%)}
.h2-ban-ql ul li div:hover{background:#d3f0fb;box-shadow:0 14px 22px -13px #0b1017ba}
.land-pack-grid-text{position:relative;-webkit-transition:all .5s ease;-moz-transition:all .5s ease;-o-transition:all .5s ease;transition:all .5s ease;position:absolute;top:0;bottom:0;left:0;right:0;width:100%;height:100%;z-index:2;background:linear-gradient(to top,#000000c7,#00000008)}
.land-pack-grid-text h4{padding:15px;font-size:20px;font-weight:400;text-align:center;bottom:0;position:absolute;width:100%;text-align:center;color:#fff}
.land-pack-grid-text h4 .dir-ho-cat{color:#f6f7f9;font-size:11px;position:relative;width:100%;display:inline-block}
.land-pack-grid-img{background:#333}
.home-tit{margin-bottom:20px;padding-top:60px}
.hom2-hom-ban{float:left;width:46%;background-size:cover;margin:0 2%;background:#e6f6fb;padding:30px 100px 30px 30px;border-radius:5px;position:relative;}
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
.hom2-cus-sli{float:left;width:100%}
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
.hom4-fea{background:#fff;padding-bottom:40px;float:left;width:100%}
.str{float:left;width:100%}
.hom4-fea .hom2-cus-sli ul li{padding:12px 20px}
.hom4-fea .home-tit{margin-bottom:0;padding-top:70px}
@media screen and (max-width: 767px) {
.land-pack-grid-text h4{font-size:16px}
}
</style>


<!-- START -->
<section>
    <div class="all-jobs-ban">
        <div class="container">
            <div class="row">
                <div class="jtit">
                    <h1><?php echo $BIZBOOK['SERVICE-EXPERT-FIND-SERVICE-EXPERT-H1']; ?></h1>
                    <p><?php echo $BIZBOOK['SERVICE-EXPERT-FIND-SERVICE-EXPERT-P']; ?></p>
                </div>
                <br>
                <div class="job-sear">
                    <form name="expert_filter_form" id="expert_filter_form" class="expert_filter_form">
                        <ul>
                            <li class="sr-sea">
                                <select class="chosen-select" id="expert-select-search" name="expert-select-search">
                                    <?php
                                    foreach (getAllActiveExpertCategoriesPos() as $expert_search_categories_row) {

                                        $search_category_name = $expert_search_categories_row['category_name'];

                                        $search_category_id = $expert_search_categories_row['category_id'];
                                        ?>
                                        <option
                                            value="<?php echo $search_category_id; ?>"><?php echo $search_category_name; ?></option>
                                        <?php
                                    }
                                    ?>
                                </select>
                            </li>
                            <li class="sr-btn">
                                <button id="expert_filter_submit"><i class="material-icons">search</i></button>
                            </li>
                        </ul>
                    </form>
                </div>
                <div class="job-pop-tag">
                    <?php
                    foreach (getAllExpertCategoriesOrderByExpertsTableLimit(5) as $expert_trend_categories_row) {

                        $trend_category_name = $expert_trend_categories_row['category_name'];

                        $trend_category_id = $expert_trend_categories_row['category_id'];
                        ?>
                        <a href="<?php echo $ALL_EXPERTS_URL . urlModifier($expert_trend_categories_row['category_slug']); ?>"><?php echo $trend_category_name; ?></a>
                        <?php
                    }
                    ?>
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
                    <h2><span><?php echo $BIZBOOK['SERVICE-EXPERT-SECTION-2-H1']; ?></span></h2>
                    <p><?php echo $BIZBOOK['SERVICE-EXPERT-SECTION-2-P']; ?></p>
                </div>
                <div class="land-pack">
                    <ul>
                        <?php
                        foreach (getAllActiveExpertCategoriesPos() as $expert_categories_row) {

                            $category_name = $expert_categories_row['category_name'];

                            $category_id = $expert_categories_row['category_id'];

                            $total_experts_category = getCountCategoryExperts($category_id);
                            ?>
                            <li>
                                <div class="land-pack-grid">
                                    <div class="land-pack-grid-img">
                                        <img
                                            src="<?php echo $slash; ?>service-experts/images/services/<?php echo $expert_categories_row['category_image']; ?>"
                                            alt="">
                                    </div>
                                    <div class="land-pack-grid-text">
                                        <h4><?php echo $category_name; ?><span
                                                class="dir-ho-cat"><?php echo $BIZBOOK['SERVICE-EXPERTS-EXPERTS']; ?> <?php echo $total_experts_category; ?></span>
                                        </h4>
                                    </div>
                                    <a href="<?php echo $ALL_EXPERTS_URL . urlModifier($expert_categories_row['category_slug']); ?>"
                                       class="land-pack-grid-btn"><?php echo $BIZBOOK['SERVICE-EXPERT-VIEW-ALL']; ?></a>
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
                        <h2><?php echo $BIZBOOK['EXP-HOME-JOIN-EMP-TIT']; ?></h2>
                        <p><?php echo $BIZBOOK['EXP-HOME-JOIN-EMP-SUB-TIT']; ?></p>
                        <a href="<?php echo $slash; ?>login?login=register"><?php echo $BIZBOOK['EXP-HOME-JOIN-EMP-CTA']; ?></a>
                    </div>
                    <div class="hom2-hom-ban hom2-hom-ban2">
                        <h2><?php echo $BIZBOOK['EXP-HOME-JOIN-COMP-TIT']; ?></h2>
                        <p><?php echo $BIZBOOK['EXP-HOME-JOIN-COMP-SUB-TIT']; ?></p>
                        <a href="<?php echo $slash; ?>login?login=register"><?php echo $BIZBOOK['EXP-HOME-JOIN-COMP-CTA']; ?></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->
<!-- START -->
<section>
    <div class="str hom2-cus">
        <div class="container">
            <div class="row">
                <div class="home-tit">
                    <h2><span><?php echo $BIZBOOK['SERVICE-EXPERT-OUR-USER-REVIEWS']; ?></span></h2>
                    <p><?php echo $BIZBOOK['SERVICE-EXPERT-OUR-USER-REVIEWS-P']; ?></p>
                </div>

                <div class="hom2-cus-sli">
                    <ul class="multiple-items">
                        <?php
                        foreach (getAllExpertReviews() as $reviewsqlrow) {

                            $review_user_id = $reviewsqlrow['review_user_id'];

                            $review_expert_id = $reviewsqlrow['expert_id'];

                            $total_per_user_rating = round((($reviewsqlrow['expert_rating']) / 4), 1);

                            $revuser_details_row = getUser($review_user_id); // To Fetch particular User Data

                            $rev_expert_details_row = getIdExpert($review_expert_id); // To Fetch particular User Data

                            ?>
                            <li>
                                <div class="testmo">
                                    <img
                                        src="<?php echo $slash; ?>images/user/<?php if (($revuser_details_row['profile_image'] == NULL) || empty($revuser_details_row['profile_image'])) {
                                            echo $footer_row['user_default_image'];
                                        } else {
                                            echo $revuser_details_row['profile_image'];
                                        } ?>"
                                        alt="">
                                    <h4><?php echo $revuser_details_row['first_name']; ?></h4>
                                    <span><?php echo $BIZBOOK['SERVICE-EXPERT-WRITTEN-REVIEW-TO']; ?> <a href="#"><?php echo $rev_expert_details_row['profile_name']; ?></a></span>
                                    <label class="rat">
                                        <?php if ($reviewsqlrow['expert_rating'] == 1) { ?>
                                            <i class="material-icons">star</i>
                                            <i class="material-icons">star_border</i>
                                            <i class="material-icons">star_border</i>
                                            <i class="material-icons">star_border</i>
                                            <i class="material-icons">star_border</i>
                                        <?php } ?>
                                        <?php if ($reviewsqlrow['expert_rating'] == 2) { ?>
                                            <i class="material-icons">star</i>
                                            <i class="material-icons">star</i>
                                            <i class="material-icons">star_border</i>
                                            <i class="material-icons">star_border</i>
                                            <i class="material-icons">star_border</i>
                                        <?php } ?>
                                        <?php if ($reviewsqlrow['expert_rating'] == 3) { ?>
                                            <i class="material-icons">star</i>
                                            <i class="material-icons">star</i>
                                            <i class="material-icons">star</i>
                                            <i class="material-icons">star_border</i>
                                            <i class="material-icons">star_border</i>
                                        <?php } ?>
                                        <?php if ($reviewsqlrow['expert_rating'] == 4) { ?>
                                            <i class="material-icons">star</i>
                                            <i class="material-icons">star</i>
                                            <i class="material-icons">star</i>
                                            <i class="material-icons">star</i>
                                            <i class="material-icons">star_border</i>
                                        <?php } ?>
                                        <?php if ($reviewsqlrow['expert_rating'] == 5) { ?>
                                            <i class="material-icons">star</i>
                                            <i class="material-icons">star</i>
                                            <i class="material-icons">star</i>
                                            <i class="material-icons">star</i>
                                            <i class="material-icons">star</i>
                                        <?php } ?>
                                    </label>
                                    <p><?php echo stripslashes($reviewsqlrow['expert_message']); ?></p>
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

                            <img
                                src="<?php echo $slash; ?>images/ads/<?php if ($ad_enquiry_photo != NULL || !empty($ad_enquiry_photo)) {
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
    $('.multiple-items').slick({
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