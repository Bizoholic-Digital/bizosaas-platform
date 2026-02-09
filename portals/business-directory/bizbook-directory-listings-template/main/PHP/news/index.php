<?php
include "news-config-info.php";
include "../header.php";

if (file_exists('../config/news_page_authentication.php')) {
    include('../config/news_page_authentication.php');
}
?>
<style>
    .hom-head .container {
        display: none
    }

    .hom-top {
        transition: all .5s ease;
        background: #000;
        box-shadow: none
    }

    .hom-head {
        background: none !important;
        padding: 0;
        margin: 0
    }

    .hom-head .hom-top .container {
        display: block
    }

    .hom-top {
        background: #292c2e;
    }
</style>
<!-- START -->
<section class="news-top-menu">
    <div class="container">
        <div class="row">
            <div class="news-menu">
                <ul>
                    <li><a href="<?php echo $slash ?>news" class="<?php if ($current_news_page == "news/index.php") {
                            echo 'act';
                        } ?>"><?php echo $BIZBOOK['HOME']; ?></a></li>
                    <?php
                    foreach (getAllNewsCategoriesPos() as $news_category_row) {
                        ?>
                        <li><a href="<?php echo $ALL_NEWS_URL . urlModifier($news_category_row['category_slug']); ?>"
                               class=""><?php echo $news_category_row['category_name']; ?></a></li>
                        <?php
                    }
                    ?>
                </ul>
            </div>
        </div>
    </div>
</section>
<!--END-->

<!-- START -->
<section class="news-hom-ban">
    <div class="news-hom-ban-inn">
        <h1><b><?php echo $BIZBOOK['NEWS-HOMEPAGE-BANNER-H1-TEXT-1']; ?></b> <?php echo $BIZBOOK['NEWS-HOMEPAGE-BANNER-H1-TEXT-2']; ?></h1>
        <p><?php echo $BIZBOOK['NEWS-HOMEPAGE-BANNER-P-TEXT']; ?></p>
    </div>
</section>
<!--END-->

<!-- START -->
<section class="news-hom-top">
    <div class="news-hom-top-inn">
        <div class="container">
            <div class="row">
                <div class="news-hom-ban-ads">
                    <?php
                    $ad_position_id = 7;   //Ad position on News Home Page Top
                    $get_ad_row = getAds($ad_position_id);
                    $ad_enquiry_photo = $get_ad_row['ad_enquiry_photo'];
                    ?>
                    <a href="<?php echo stripslashes($get_ad_row['ad_link']); ?>"><img src="<?php echo $slash; ?>images/ads/<?php if ($ad_enquiry_photo != NULL || !empty($ad_enquiry_photo)) {
                            echo $ad_enquiry_photo;
                        } else {
                            echo "ads1.png";
                        } ?>" alt=""></a>
                </div>
                <div class="news-com-tit">
                    <h2><?php echo $BIZBOOK['NEWS-TRENDINGS']; ?></h2>
                </div>
                <?php
                $news_si = 1;
                foreach (getAllNewsTrending() as $home_page_trending_row) {

                $home_page_trending_news_id = $home_page_trending_row['news_id'];

                $home_page_trending_news_trending_id = $home_page_trending_row['trending_news_id'];

                $home_page_trending_news_sql_row = getIdNews($home_page_trending_news_id);

                $home_page_trending_category_id = $home_page_trending_news_sql_row['category_id'];

                $home_page_trending_category_row = getNewsCategory($home_page_trending_category_id);

                $home_page_trending_category_name = $home_page_trending_category_row['category_name'];

                ?>
                <?php
                if ($news_si == 1 || $news_si == 4){
                ?>
                <div class="col-md-3">
                    <?php
                    }if ($news_si == 3){
                    ?>
                    <div class="col-md-6">
                        <?php
                        }
                        ?>

                        <div class="news-home-box <?php if ($news_si == 3) {
                            echo "news-home-box-big";
                        } ?>">
                            <div class="im">
                                <img src="<?php echo $slash; ?>/news/images/news/<?php echo $home_page_trending_news_sql_row['news_image']; ?>"
                                     alt="">
                            </div>
                            <div class="txt">
                                <span class="news-cate"><?php echo $home_page_trending_category_name; ?></span>
                                <h2><?php echo stripslashes($home_page_trending_news_sql_row['news_title']); ?></h2>
                            <span
                                class="news-date"><?php echo dateFormatconverter($home_page_trending_news_sql_row['news_cdt']); ?></span>
                            </div>
                            <a href="<?php echo $NEWS_DETAIL_URL . urlModifier($home_page_trending_news_sql_row['news_slug']); ?>" class="fclick"></a>
                        </div>
                        <?php
                        if ($news_si == 2 || $news_si == 3 || $news_si == 6){
                        ?>
                    </div>
                <?php
                }
                ?>
                    <?php
                    $news_si++;
                    }
                    ?>
                </div>
            </div>
        </div>
</section>
<!--END-->

<!-- START -->
<section class="news-hom-ban-sli">
    <div class="news-hom-ban-sli-inn">
        <ul class="multiple-items1">
            <?php
            foreach (getAllNewsSlider() as $home_page_slider_row) {

                $home_page_slider_news_id = $home_page_slider_row['news_id'];

                $home_page_slider_news_slider_id = $home_page_slider_row['news_slider_id'];

                $home_page_slider_news_sql_row = getIdNews($home_page_slider_news_id);

                $home_page_slider_category_id = $home_page_slider_news_sql_row['category_id'];

                $home_page_slider_category_row = getNewsCategory($home_page_slider_category_id);

                $home_page_slider_category_name = $home_page_slider_category_row['category_name'];

                ?>
                <li>
                    <div class="news-hban-box">
                        <div class="im">
                            <img
                                src="<?php echo $slash; ?>/news/images/news/<?php echo $home_page_slider_news_sql_row['news_image']; ?>"
                                alt="">
                        </div>
                        <div class="txt">
                            <span class="news-cate"><?php echo $home_page_slider_category_name; ?></span>
                            <h2><?php echo stripslashes($home_page_slider_news_sql_row['news_title']); ?></h2>
                            <span
                                class="news-date"><?php echo dateFormatconverter($home_page_slider_news_sql_row['news_cdt']); ?></span>
                        </div>
                        <a href="<?php echo $NEWS_DETAIL_URL . urlModifier($home_page_slider_news_sql_row['news_slug']); ?>"
                           class="fclick"></a>
                    </div>
                </li>
                <?php
            }
            ?>
        </ul>
    </div>
</section>
<!--END-->

<!-- START -->
<section class="news-hom-big">
    <div class="container">
        <div class="row">

            <div class="col-md-8">
                <div class="news-com-tit">
                    <h2><?php echo $BIZBOOK['NEWS-LATEST-POPULAR']; ?></h2>
                </div>
                <?php
                $latest_news_si = 1;
                foreach (getAllTopViewsPremiumActiveNews() as $latest_newsrow) {

                    $latest_news_id = $latest_newsrow['news_id'];

                    $latest_news_category_id = $latest_newsrow['category_id'];

                    $latset_news_category_row = getNewsCategory($latest_news_category_id);

                    $latest_news_category_name = $latset_news_category_row['category_name'];

                    ?>
                    <!--BIG POST START-->
                    <div class="news-home-box <?php if($latest_news_si != 1 && $latest_news_si != 2 ){ ?>news-home-box1 <?php } ?>">
                        <div class="im">
                            <img src="<?php echo $slash; ?>/news/images/news/<?php echo $latest_newsrow['news_image']; ?>"
                                 alt="">
                        </div>
                        <div class="txt">
                            <span class="news-cate"><?php echo $latest_news_category_name; ?></span>
                            <h2><?php echo stripslashes($latest_newsrow['news_title']); ?></h2>
                            <p><?php
                                if (strlen($latest_newsrow['news_description']) >= 100) {
                                    $pos = strpos($latest_newsrow['news_description'], ' ', 100);
                                    echo substr(stripslashes($latest_newsrow['news_description']), 0, $pos).'...';
                                }else{
                                    echo stripslashes($latest_newsrow['news_description']);
                                }

                                ?></p>
                            <span class="news-date"><?php echo dateFormatconverter($latest_newsrow['news_cdt']); ?></span>
                            <span class="news-views"><?php echo AddingZero_BeforeNumber(news_detail_pageview_count($latest_newsrow['news_id'])); ?> <?php echo $BIZBOOK['VIEWS']; ?></span>
                        </div>
                        <a href="<?php echo $NEWS_DETAIL_URL . urlModifier($latest_newsrow['news_slug']); ?>" class="fclick"></a>
                    </div>
                    <!--END BIG POST START-->
                    <?php
                    $latest_news_si++;
                }
                ?>
            </div>
            <div class="col-md-4">
                <div class="news-com-rhs">
                    <?php if(getCountNewsSocialMediaActive() >= 1){ ?>
                    <!-- SOCIAL MEDIA START-->
                    <div class="news-soci">
                        <h4><?php echo $BIZBOOK['SOCIAL_MEDIA']; ?></h4>
                        <ul>
                            <?php foreach (getAllNewsSocialMediaActive() as $home_social_media_row) { ?>
                            <li><a target="_blank" href="<?php echo $home_social_media_row['social_media_link']; ?>" class="<?php if($home_social_media_row['social_media_id'] == 1){ echo "sm-fb-big"; }
                                elseif($home_social_media_row['social_media_id'] == 2){ echo "sm-tw-big"; }
                                elseif($home_social_media_row['social_media_id'] == 3){ echo "sm-li-big"; }
                                elseif($home_social_media_row['social_media_id'] == 4){ echo "sm-yt-big"; }
                                ?>"><b><?php echo $home_social_media_row['social_media_count']; ?></b> <?php if($home_social_media_row['social_media_id'] == 1){ echo $BIZBOOK['FACEBOOK']; }
                                    elseif($home_social_media_row['social_media_id'] == 2){ echo $BIZBOOK['TWITTER']; }
                                    elseif($home_social_media_row['social_media_id'] == 3){ echo $BIZBOOK['LINKEDIN']; }
                                    elseif($home_social_media_row['social_media_id'] == 4){ echo $BIZBOOK['YOUTUBE']; }
                                    ?></a></li>
                            <?php } ?>
                        </ul>
                    </div>
                    <!-- SOCIAL MEDIA END-->
                    <?php } ?>
                    <!-- ADS START-->
                    <div class="news-rhs-cate">
                        <h4><?php echo $BIZBOOK['HOM-EXP-TIT1']; ?></h4>
                        <ul>
                            <?php
                            foreach (getAllNewsCategoriesPos() as $news_right_side_category_row) {

                                $count_news_per_category = getCountCategoryNews($news_right_side_category_row['category_id']);
                                ?>
                                <li><a href="<?php echo $ALL_NEWS_URL . urlModifier($news_right_side_category_row['category_slug']); ?>"><span><?php echo $count_news_per_category; ?></span><b><?php echo $news_right_side_category_row['category_name']; ?></b></a></li>
                                <?php
                            }
                            ?>
                        </ul>
                    </div>
                    <!-- ADS END-->
                    <!--TOP POSTS-->
                    <div class="hot-page2-hom-pre news-rhs-trends">
                        <h4><?php echo $BIZBOOK['TRENDING_POSTS']; ?></h4>
                        <ul>
                            <?php
                            $news_si = 1;
                            foreach (getAllNewsTrending() as $right_section_trending_row) {

                                $right_section_trending_news_id = $right_section_trending_row['news_id'];

                                $right_section_trending_news_sql_row = getIdNews($right_section_trending_news_id);

                                ?>
                                <li>
                                    <div class="hot-page2-hom-pre-1">
                                        <img src="<?php echo $slash; ?>/news/images/news/<?php echo $right_section_trending_news_sql_row['news_image']; ?>"
                                             alt="">
                                    </div>
                                    <div class="hot-page2-hom-pre-2">
                                        <h5><?php echo stripslashes($right_section_trending_news_sql_row['news_title']); ?></h5>
                                        <span class="news-date"><?php echo dateFormatconverter($right_section_trending_news_sql_row['news_cdt']); ?></span>
                                    </div>
                                    <a href="<?php echo $NEWS_DETAIL_URL . urlModifier($right_section_trending_news_sql_row['news_slug']); ?>" class="fclick"></a>
                                </li>
                                <?php
                            }
                            ?>
                        </ul>
                    </div>
                    <!--TOP POSTS-->
                    <!-- ADS START-->
                    <?php
                    $ad_position_id_1 = 8;   //Ad position on News Detail Page -1
                    $get_ad_row_1 = getAds($ad_position_id_1);
                    $ad_enquiry_photo_1 = $get_ad_row_1['ad_enquiry_photo'];
                    ?>
                    <div class="news-rhs-ads-ban">
                        <div class="ban-ati-com">
                            <a href="<?php echo stripslashes($get_ad_row_1['ad_link']); ?>"><span><?php echo $BIZBOOK['AD']; ?></span><img
                                    src="<?php echo $slash; ?>images/ads/<?php if ($ad_enquiry_photo_1 != NULL || !empty($ad_enquiry_photo_1)) {
                                        echo $ad_enquiry_photo_1;
                                    } else {
                                        echo "ads2.jpg";
                                    } ?>"></a>
                        </div>
                    </div>
                    <!-- ADS END-->
                    <?php
                    $ad_position_id_2 = 9;   //Ad position on News Detail Page -2
                    $get_ad_row_2 = getAds($ad_position_id_2);
                    $ad_enquiry_photo_2 = $get_ad_row_2['ad_enquiry_photo'];
                    ?>
                    <!-- ADS START-->
                    <div class="news-rhs-ads-ban">
                        <div class="ban-ati-com">
                            <a href="<?php echo stripslashes($get_ad_row_2['ad_link']); ?>"><span><?php echo $BIZBOOK['AD']; ?></span><img
                                    src="<?php echo $slash; ?>images/ads/<?php if ($ad_enquiry_photo_2 != NULL || !empty($ad_enquiry_photo_2)) {
                                        echo $ad_enquiry_photo_2;
                                    } else {
                                        echo "ads1.jpg";
                                    } ?>"></a>
                        </div>
                    </div>
                    <!-- ADS END-->
                    <!-- SUBSCRIBE START-->
                    <div class="news-subsc">
                        <div class="ud-rhs-poin1">
                            <div class="log-bor">&nbsp;</div>
                            <img src="https://cdn-icons-png.flaticon.com/512/6349/6349282.png"
                                 alt="">
                            <h5><?php echo $BIZBOOK['NEWS-SUBSCRIBE']; ?> <b><?php echo $BIZBOOK['NEWS-NEWSLETTER']; ?></b></h5>
                            <p><?php echo $BIZBOOK['NEWS-NEWSLETTER-P-TAG']; ?></p>
                        </div>
                        <div id="news_newsletter_success" class="log" style="display: none;">
                            <p><?php echo $BIZBOOK['NEWS_NEWSLETTER_SUBSCRIPTION_SUCCESSFUL_MESSAGE']; ?></p>
                        </div>
                        <div id="news_newsletter_fail" class="log" style="display: none;">
                            <p><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></p>
                        </div>
                        <form name="news_newsletter_subscribe_form" id="news_newsletter_subscribe_form">
                            <ul>
                                <li><input type="text" name="news_newsletter_subscribe_name" placeholder="<?php echo $BIZBOOK['LEAD-EMAIL-PLACEHOLDER']; ?>" class="form-control" required>
                                </li>
                                <li><input type="submit" id="news_newsletter_subscribe_submit" name="news_newsletter_subscribe_submit" class="form-control"></li>
                            </ul>
                        </form>
                    </div>
                    <!-- SUBSCRIBE END-->
                </div>
            </div>
        </div>
    </div>
</section>
<!--END-->


<!-- START -->
<section class="news-hom-all-lat">
    <div class="news-hom-all-lat-inn">
        <div class="container">
            <div class="row">
                <div class="news-com-tit">
                    <h2><?php echo $BIZBOOK['NEWS-LATEST-POST']; ?></h2>
                </div>
                <?php
                foreach (getAllNews() as $latest_news_row) {

                    $latest_news_category_id = $latest_news_row['category_id'];

                    $latest_news_category_row = getNewsCategory($latest_news_category_id);

                    $latest_news_category_name = $latest_news_category_row['category_name'];

                    ?>
                    <div class="col-md-4">
                        <div class="news-home-box">
                            <div class="im">
                                <img
                                    src="<?php echo $slash; ?>/news/images/news/<?php echo $latest_news_row['news_image']; ?>"
                                    alt="">
                            </div>
                            <div class="txt">
                                <span class="news-cate"><?php echo $latest_news_category_name; ?></span>
                                <h2><?php echo stripslashes($latest_news_row['news_title']); ?></h2>
                                <span class="news-date"><?php echo dateFormatconverter($latest_news_row['news_cdt']); ?></span>
                                <span class="news-views"><?php echo AddingZero_BeforeNumber(news_detail_pageview_count($latest_news_row['news_id'])); ?> <?php echo $BIZBOOK['VIEWS']; ?></span>
                            </div>
                            <a href="<?php echo $NEWS_DETAIL_URL . urlModifier($latest_news_row['news_slug']); ?>" class="fclick"></a>
                        </div>
                    </div>
                    <?php
                }
                ?>
            </div>
        </div>
    </div>
</section>
<!--END-->


<?php
include "../footer.php";
?>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="<?php echo $slash; ?>js/slick.js"></script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>
<script>
    $('.multiple-items1').slick({
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
                centerMode: false
            }
        }]

    });
</script>

</body>

</html>