<?php
include "header.php";
?>
<style>
body{background-color:#e8ecf0}
.ind2-home{float:left;width:100%;background:url(images/ex2.jpg) no-repeat;position:relative;padding:80px 0 0;background-size:100%;background-position:0 50px}
.ind2-home:before{content:'';position:absolute;width:100%;height:100%;background:#56CCF2;background:-webkit-linear-gradient(to right,#2f80eddb,#27f19dd9);background:linear-gradient(to right,#2f80ede3,#27f19ddb);left:0;top:0;right:0;bottom:0}
.news-top-menu{position:absolute;top:-5px;left:0;right:0;z-index:10;background:#616161}
.news-hban-box .im img{height:400px}
.news-menu ul li a{color:#fff;font-size:12px;font-weight:500;border-bottom:2px solid #616161}
.news-menu ul li a.act{border-bottom:2px solid #2d344d;background:#434859}
.news-menu ul li a:hover{border-bottom:2px solid #323232;background:#575757}
    .land-pack-grid, .land-pack-grid-img img, .land-pack-grid-text{border-radius: 15px;}    
.hom-top{transition:all .5s ease;background:#000;    padding-bottom: 2px;}
.hom-head{background:#f4f4f4 url(images/bgIcons.png) repeat!important}
.top-ser,.ban-ql, .mob-app{display:none}
.dmact .top-ser{display:block}
.caro-home{margin-top:90px;float:left;width:100%}
.carousel-item:before{background:none}
.hom-head{padding:140px 0 70px;margin-bottom:0}
.ban-search{background:none;padding:0;border-radius:50px;    padding-bottom: 90px;}
.ban-search ul li.sr-cit{display:block;width:25%}
.ban-search ul li.sr-sea{width:54%;margin:0 1%}
.ban-search ul li.sr-btn{width:19%}
.ban-search ul li input{border-radius:5px}
.ban-search ul li input[type="submit"]{padding:5px;border-radius:5px;background:#2140d7}
.hom-head:before{background:#ffffff14}
.hom-head:after{display:none}
.ban-tit h1{font-weight:500;color:#fff;text-shadow:none}
.ban-tit h1 b{padding-bottom:15px;color:#fff;text-shadow:none}
.h2-ban-ql ul li div{border:1px solid #d9d9da;background:#fff}
.h2-ban-ql ul li div h5{font-weight:500;color:#383942}
.h2-ban-ql ul li div h5 span{font-weight:700}
.home-tit h2{font-weight:400;}
.home-tit h2 span{font-weight:700}
.h2-ban-ql ul li div:hover{background:#d3f0fb;box-shadow:0 14px 22px -13px #0b1017ba}
.land-pack-grid-text{position:relative;-webkit-transition:all .5s ease;-moz-transition:all .5s ease;-o-transition:all .5s ease;transition:all .5s ease;position:absolute;top:0;bottom:0;left:0;right:0;width:100%;height:100%;z-index:2;background:linear-gradient(to top,#000000c7,#00000008)}
.land-pack-grid-text h4{padding:15px;font-size:16px;font-weight:400;text-align:center;bottom:0;position:absolute;width:100%;text-align:center;color:#fff}
.land-pack-grid-text h4 .dir-ho-cat{color:#f6f7f9;font-size:11px;position:relative;width:100%;display:inline-block}
.land-pack-grid-img{background:#333}
.home-tit{padding-top:60px}
    .news-hom-ban-sli{margin-bottom: 30px;}    
.pri {padding: 75px 0 60px 0;background: #e8ecf0;}
.hom2-hom-ban{float:left;width:46%;background-size:cover;margin:0 2%;background:#e6f6fb;padding:30px 100px 30px 30px;border-radius:5px;position:relative;}
.hom2-hom-ban:hover a{background:#d6c607}
.hom2-hom-ban h2{font-weight:600;font-size:25px;padding-bottom:5px}
.hom2-hom-ban p{font-size:14px}
.hom2-hom-ban a{background:#21d78d;color:#fff;padding:10px 20px;border-radius:5px;display:inline-block;cursor:pointer;font-size:13px;font-weight:400}
.hom2-hom-ban p,.hom2-hom-ban h2,.hom2-hom-ban a{position:relative;color:#fff}
.hom2-hom-ban:before{content:'';position:absolute;width:100%;height:100%;left:0;top:0;right:0;bottom:0;z-index:0;opacity:.8;background:#24C6DC;border-radius:5px}
.hom2-hom-ban1:before{background-image:linear-gradient(140deg,#0c7ada 0%,#0761af 50%,#0f243e94 75%)}
.hom2-hom-ban2:before{background-image:linear-gradient(140deg,#768404 0%,#768404 50%,#0f243e94 75%)}
.hom2-hom-ban1{background-image:url(images/home2-hand.jpg)}
.hom2-hom-ban2{background-image:url(images/home2-work.jpg)}
.hom2-hom-ban-main{float:left;width:100%;padding-bottom:70px}
.hom2-cus-sli{float:left;width:100%}
.hom2-cus-sli ul li{float:left;width:25%;padding:12px 20px}
.testmo{width:100%;background:#fff;box-shadow:0 1px 7px -3px #161d2926;border-radius:5px;padding:30px;position:relative}
.testmo img{width:64px;height:64px;border-radius:50px;object-fit:cover;margin:-80px 0 0}
.testmo h4{font-size:14px;font-weight:600;margin-bottom:2px;font-family:'Poppins',sans-serif}
.testmo span{font-size:11px;font-weight:400;color:#727688}
.testmo span a{font-weight:500;color:#4caf50;display:block;font-size:12px}
.testmo p{color:#727688;font-size:12px;line-height:20px;margin:0;font-weight:400;height:58px;overflow:hidden;border-top:1px solid #f1eeee;padding-top:15px;margin-top:15px}
.testmo p:before{content:'format_quote';font-size:21px;margin:-25px 0 0;background:#fff}
.hom2-cus{background:#e8ecf0;padding-bottom:70px}
.testmo .rat{padding:2px 2px 2px 10px;display:inline-block;position:absolute;right:30px;top:52px}
.testmo .rat i{color:#FF9800;font-size:17px;width:12px}
.hom2-cus-sli ul{position:relative;overflow:hidden;padding:20px 20px 0}
.slick-arrow{width:50px;height:50px;border-radius:50px;background:#fff;border:1px solid #ededed;color:#ffffff03;position:absolute;z-index:9;top:38%}
.slick-arrow:before{content:'chevron_left';font-size:27px;top:4px;left:9px}
.slick-prev{left:14px}
.slick-next{right:14px}
.slick-next:before{content:'chevron_right';font-size:27px}
.hom4-prop-box{padding:0;background:#fff;box-shadow:0 1px 14px -4px #161d2926;border:1px solid #efefef}
.hom4-prop-box img{width:100%;border-radius:5px 5px 0 0;margin:0;height:185px}
.hom4-prop-box div{padding:25px}
.hom4-prop-box .rat{position:relative;top:initial;right:initial;padding:2px 2px 2px 0;display:block;margin:0;height:17px;left:-2px}
.hom4-fea{padding-bottom:40px}
.hom4-fea .hom2-cus-sli ul li{padding:12px 20px}
.hom4-fea .home-tit{margin-bottom: 0px;padding-top: 70px;}       
@media screen and (max-width:992px) {
.hom2-hom-ban{width:100%;margin:20px 0}
}
@media screen and (max-width:767px) {
.ban-tit h1 b{font-size:32px;line-height:38px}
    .ind2-home{padding-top: 120px;}
    .ban-search ul li{width:100% !important;margin:0 0 10px 0 !important;}
    .ban-tit{padding-bottom: 30px;}
}
@media screen and (max-width:550px) {
.hom-head .ban-search ul li{width:100%;margin:0 0 15px}
}
</style>

<!-- START -->
<section class="news-top-menu">
    <div class="container">
        <div class="row">
            <div class="news-menu">
                <ul>
                    <li><a href="index" class="act">Home</a></li>
                    <li><a href="all-category">All Services</a></li>
                    <li><a href="service-experts">Service Expert</a></li>
                    <li><a href="jobs">Jobs</a></li>
                    <li><a href="news">News</a></li>
                    <li><a href="all-products">Products</a></li>
                    <li><a href="events">Events</a></li>
                    <li><a href="coupons">Coupons</a></li>
                    <li><a href="blog-posts">Blogs</a></li>
                    <li><a href="community">Community</a></li>
                </ul>
            </div>
        </div>
    </div>
</section>
<!--END-->

<!-- START -->
<section>
    <div>
        <div class="container">
            <div class="row">
                <!--<div class="home-tit">
                    <h2><span>Top Services</span> Cras nulla nulla, pulvinar sit amet nunc at, lacinia viverra lectus. Fusce imperdiet ullamcorper metus eu fringilla.</h2>
                </div>-->
                <div class="home-tit">
                    <h2><span><?php echo $BIZBOOK['HOM-POP-TIT']; ?></span> <?php echo $BIZBOOK['HOM-POP-TIT1']; ?></h2>
                    <p><?php echo $BIZBOOK['HOM-POP-SUB-TIT']; ?></p>
                </div>
                <div class="land-pack">
                    <ul>
                        <?php
                        foreach (getAllCategories() as $category_sql_row) {
                            ?>
                            <li>
                                <div class="land-pack-grid">
                                    <div class="land-pack-grid-img">
                                        <img src="images/services/<?php echo $category_sql_row['category_image']; ?>" alt="">
                                    </div>
                                    <div class="land-pack-grid-text">
                                        <h4><?php echo $category_sql_row['category_name']; ?> 
                                            <span class="dir-ho-cat">Listings <?php echo AddingZero_BeforeNumber(getCountCategoryListing($category_sql_row['category_id'])); ?></span>
                                        </h4>
                                    </div>
                                    <a href="all-listing?category=<?php echo preg_replace('/\s+/', '-', strtolower($category_sql_row['category_name'])); ?>"
                                           class="land-pack-grid-btn">View all listings</a>
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
                    <h2><span><?php echo $BIZBOOK['HOM-BEST-TIT']; ?></span> <?php echo $BIZBOOK['HOM-BEST-TIT1']; ?>
                    </h2>
                    <p><?php echo $BIZBOOK['HOM-BEST-SUB-TIT']; ?></p>
                </div>
                
                <div class="hom2-cus-sli">
                        <ul class="multiple-items1">
                            <?php
                            $pop_bus = 1;
                            foreach (getAllFeaturedListing() as $row) {

                                $listing_id = $row['listing_id'];

                                $listing_sql_row = getIdListing($listing_id);
                                $featured_category_id = $listing_sql_row['category_id'];

                                $popular_business_category_sql_row = getCategory($featured_category_id);

                                // List Rating. for Rating of Star
                                foreach (getListingReview($listing_id) as $star_rating_row) {
                                    if ($star_rating_row["rate_cnt"] > 0) {
                                        $star_rate_times = $star_rating_row["rate_cnt"];
                                        $star_sum_rates = $star_rating_row["total_rate"];
                                        $star_rate_one = $star_sum_rates / $star_rate_times;
                                        //$star_rate_one = (($Star_rate_value)/5)*100;
                                        $star_rate_two = number_format($star_rate_one, 1);
                                        $star_rate = $star_rate_two;

                                    } else {
                                        $rate_times = 0;
                                        $rate_value = 0;
                                        $star_rate = 0;
                                    }
                                }

                                ?>
                                <li>
                                    <div class="testmo hom4-prop-box">
                                        <img
                                            src="<?php if ($listing_sql_row['profile_image'] != NULL || !empty($listing_sql_row['profile_image'])) {
                                                echo "images/listings/" . $listing_sql_row['profile_image'];
                                            } else {
                                                echo "images/listings/hot4.jpg";
                                            } ?>" alt="">
                                        <div>
                                            <h4>
                                                <a href="<?php echo $LISTING_URL . urlModifier($listing_sql_row['listing_slug']); ?>"><?php echo $listing_sql_row['listing_name']; ?></a>
                                            </h4>
                                            <?php if ($star_rate != 0) { ?>
                                                <label class="rat">
                                                    <?php
                                                    for ($i = 1; $i <= ceil($star_rate_two); $i++) {
                                                        ?>
                                                        <i class="material-icons">star</i>
                                                        <?php
                                                    }
                                                    $bal_star_rate = abs(ceil($star_rate_two) - 5);

                                                    for ($i = 1; $i <= $bal_star_rate; $i++) {
                                                        ?>
                                                        <i class="material-icons">star_border</i>
                                                        <?php
                                                    }
                                                    ?>
                                                </label>
                                            <?php } ?>
                                            <span><a
                                                    href="#"><?php echo $popular_business_category_sql_row['category_name']; ?></a></span>
                                        </div>
                                        <a href="<?php echo $LISTING_URL . urlModifier($listing_sql_row['listing_slug']); ?>"
                                           class="fclick"></a>
                                    </div>
                                </li>
                                <?php
                                $pop_bus++;
                            }
                            ?>
                        </ul>
                    </div>
                    
            </div>
        </div>
    </div>
</section>
<!-- END -->

<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> pri">
    <div class="container">
        <div class="row">
            <div class="tit">
                <h2>
                    <span><?php echo $BIZBOOK['CHOOSE_YOUR_PLAN']; ?></span></h2>
            </div>
            <div>
                <ul>
                    <?php
                    $si = 1;
                    foreach (getAllPlanType() as $plan_type_row) {
                        ?>
                        <li>
                            <div class="pri-box">
                                <div class="c2">
                                    <h4><?php echo $plan_type_row['plan_type_name']; ?> plan</h4>

                                    <?php if ($plan_type_row['plan_type_id'] == 1) { ?>
                                        <p><?php echo $BIZBOOK['PRICING_GETTING_STARTED']; ?></p>
                                    <?php } elseif ($plan_type_row['plan_type_id'] == 2) { ?>
                                        <p><?php echo $BIZBOOK['PRICING_PERFECT_SMALL_TEAMS']; ?></p>
                                    <?php } elseif ($plan_type_row['plan_type_id'] == 3) { ?>
                                        <p><?php echo $BIZBOOK['PRICING_BEST_VALUE_LARGE']; ?></p>
                                    <?php } else { ?>
                                        <p><?php echo $BIZBOOK['PRICING_MADE_ENTERPRISES']; ?></p>
                                        <?php
                                    } ?>

                                </div>
                                <div class="c3">
                                    <h2><span></span><?php if ($plan_type_row['plan_type_price'] == 0) {
                                            echo "FREE";
                                        } else {
                                            echo $footer_row['currency_symbol'] . '' . $plan_type_row['plan_type_price'];
                                        } ?></h2>
                                    <?php if ($plan_type_row['plan_type_id'] == 1) { ?>
                                        <p><?php echo $BIZBOOK['PRICING_SINGLE_USER']; ?></p>
                                    <?php } elseif ($plan_type_row['plan_type_id'] == 2) { ?>
                                        <p><?php echo $BIZBOOK['PRICING_STARTUP_BUSINESS']; ?></p>
                                    <?php } elseif ($plan_type_row['plan_type_id'] == 3) { ?>
                                        <p><?php echo $BIZBOOK['PRICING_MEDIUM_BUSINESS']; ?></p>
                                    <?php } else { ?>
                                        <p><?php echo $BIZBOOK['PRICING_MADE_ENTERPRISES']; ?></p>
                                        <?php
                                    } ?>

                                </div>
                                <div class="c5">
                                    <a href="<?php
                                    if (isset($_SESSION['user_id'])) {
                                        echo "db-plan-change";
                                    } else {
                                        echo "login";
                                    } ?>" class="cta1"><?php echo $BIZBOOK['PRICING_GET_START']; ?></a>
                                    <a href="pricing-details" class="cta2"  target="_blank">Know more</a>
                                </div>
                            </div>
                        </li>
                        <?php
                        $si++;
                    }
                    ?>
                </ul>
            </div>
        </div>
    </div>
</section>
<!--END PRICING DETAILS-->

<!-- START -->
<section class="news-hom-ban-sli">
      <div class="home-tit">
          <h2><span><?php echo $BIZBOOK['HOM-EVE-TIT']; ?></span> <?php echo $BIZBOOK['HOM-EVE-TIT1']; ?></h2>
        <p><?php echo $BIZBOOK['HOM-EVE-SUB-TIT']; ?></p>
      </div>
       
    <div class="news-hom-ban-sli-inn">
        <ul class="multiple-items2">
            <li>
                <div class="news-hban-box">
                    <div class="im">
                        <img src="images/events/11503pexels-photo-2608517.jpeg" alt="">
                    </div>
                    <div class="txt">
                        <span class="news-cate">Feb 12</span>
                        <h2>Tima is an American news magazine and news</h2>
                        <span class="news-date">Posted on: 12 June 2022</span>
                    </div>
                    <a href="#" class="fclick"></a>
                </div>
            </li>
            <li>
                <div class="news-hban-box">
                    <div class="im">
                        <img src="images/events/8248pexels-photo-170811.jpeg" alt="">
                    </div>
                    <div class="txt">
                        <span class="news-cate">Feb 12</span>
                        <h2>Tima is an American news magazine and news</h2>
                        <span class="news-date">Posted on: 12 June 2022</span>
                    </div>
                    <a href="#" class="fclick"></a>
                </div>
            </li>
            <li>
                <div class="news-hban-box">
                    <div class="im">
                        <img src="images/events/4321pexels-helena-lopes-697244.jpg" alt="">
                    </div>
                    <div class="txt">
                        <span class="news-cate">Feb 12</span>
                        <h2>Tima is an American news magazine and news</h2>
                        <span class="news-date">Posted on: 12 June 2022</span>
                    </div>
                    <a href="#" class="fclick"></a>
                </div>
            </li>
            <li>
                <div class="news-hban-box">
                    <div class="im">
                        <img src="images/events/20523pexels-evg-culture-1126993.jpg" alt="">
                    </div>
                    <div class="txt">
                        <span class="news-cate">Feb 12</span>
                        <h2>Tima is an American news magazine and news</h2>
                        <span class="news-date">Posted on: 12 June 2022</span>
                    </div>
                    <a href="#" class="fclick"></a>
                </div>
            </li>
            <li>
                <div class="news-hban-box">
                    <div class="im">
                        <img src="images/events/19158pexels-punlob-564107.jpg" alt="">
                    </div>
                    <div class="txt">
                        <span class="news-cate">Feb 12</span>
                        <h2>Tima is an American news magazine and news</h2>
                        <span class="news-date">Posted on: 12 June 2022</span>
                    </div>
                    <a href="#" class="fclick"></a>
                </div>
            </li>
            <li>
                <div class="news-hban-box">
                    <div class="im">
                        <img src="images/events/10084pexels-photo-414807.jpeg" alt="">
                    </div>
                    <div class="txt">
                        <span class="news-cate">Feb 12</span>
                        <h2>Tima is an American news magazine and news</h2>
                        <span class="news-date">Posted on: 12 June 2022</span>
                    </div>
                    <a href="#" class="fclick"></a>
                </div>
            </li>
        </ul>
    </div>
</section>
<!--END-->

<!-- START -->
<section>
    <div class="str hom2-cus">
        <div class="container">
            <div class="row">
                <div class="home-tit">
                    <h2><span>Our user reviews</span></h2>
                    <p><?php echo $BIZBOOK['HOM3-OW-TIT-SUB']; ?></p>
                </div>
                
                <div class="hom2-cus-sli">
                    <ul class="multiple-items">
                        <li>
                            <div class="testmo">
                                <img src="images/user/33654pexels-photo-91227.jpeg" alt="">
                                <h4>Claude D Dial</h4>
                                <span>Written a review to <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <p>Update your business details including services, about, contact details payment options and more.</p>
                            </div>
                        </li>
                        <li>
                            <div class="testmo">
                                <img src="images/user/33654pexels-photo-91227.jpeg" alt="">
                                <h4>Claude D Dial</h4>
                                <span>Written a review to <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <p>Update your business details including services, about, contact details payment options and more.</p>
                            </div>
                        </li>
                        <li>
                            <div class="testmo">
                                <img src="images/user/33654pexels-photo-91227.jpeg" alt="">
                                <h4>Claude D Dial</h4>
                                <span>Written a review to <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <p>Update your business details including services, about, contact details payment options and more.</p>
                            </div>
                        </li>
                        <li>
                            <div class="testmo">
                                <img src="images/user/33654pexels-photo-91227.jpeg" alt="">
                                <h4>Claude D Dial</h4>
                                <span>Written a review to <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <p>Update your business details including services, about, contact details payment options and more.</p>
                            </div>
                        </li>
                        <li>
                            <div class="testmo">
                                <img src="images/user/33654pexels-photo-91227.jpeg" alt="">
                                <h4>Claude D Dial</h4>
                                <span>Written a review to <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <p>Update your business details including services, about, contact details payment options and more.</p>
                            </div>
                        </li>
                        <li>
                            <div class="testmo">
                                <img src="images/user/33654pexels-photo-91227.jpeg" alt="">
                                <h4>Claude D Dial</h4>
                                <span>Written a review to <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <p>Update your business details including services, about, contact details payment options and more.</p>
                            </div>
                        </li>
                        <li>
                            <div class="testmo">
                                <img src="images/user/33654pexels-photo-91227.jpeg" alt="">
                                <h4>Claude D Dial</h4>
                                <span>Written a review to <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <p>Update your business details including services, about, contact details payment options and more.</p>
                            </div>
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
                                    <img src="images/icon/how1.png" alt="">
                                    <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-1']; ?></h4>
                                    <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-1']; ?></p>
                                </div>
                            </li>
                            <li>
                                <div>
                                    <span>2</span>
                                    <img src="images/icon/how2.png" alt="">
                                    <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-2']; ?></h4>
                                    <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-2']; ?></p>
                                </div>
                            </li>
                            <li>
                                <div>
                                    <span>3</span>
                                    <img src="images/icon/how3.png" alt="">
                                    <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-3']; ?></h4>
                                    <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-3']; ?></p>
                                </div>
                            </li>
                            <li>
                                <div>
                                    <span>4</span>
                                    <img src="images/icon/how4.png" alt="">
                                    <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-4']; ?></h4>
                                    <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-4']; ?></p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>

                

                <div class="mob-app">
                    <div class="lhs">
                        <img src="images/mobile.png" alt="">
                    </div>
                    <div class="rhs">
                        <h2><?php echo $BIZBOOK['HOM-APP-TIT']; ?><span><?php echo $BIZBOOK['HOM-APP-TIT-SUB']; ?></span></h2>
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
                        <a href="#"><img src="images/android.png" alt=""> </a>
                        <a href="#"><img src="images/apple.png" alt=""> </a>
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

                            <img src="images/ads/<?php if ($ad_enquiry_photo != NULL || !empty($ad_enquiry_photo)) {
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
        <img src="images/quote.png" alt="">
    </div>
</div>
<!-- END -->

<?php
include "footer.php";
?>

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script src="js/select-opt.js"></script>
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>
<script src="js/slick.js"></script>
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
$('.multiple-items, .multiple-items1').slick({
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
          centerMode: false,
        }
      }]

}); 
    
$('.multiple-items2').slick({
  infinite: true,
  slidesToShow: 5,
  slidesToScroll: 1,
    autoplay: true,
  autoplaySpeed: 3000,
    responsive: [{
        breakpoint: 992,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          centerMode: false,
        }
      }]

});     
</script>
</body>

</html>