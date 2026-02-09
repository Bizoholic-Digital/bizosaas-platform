<?php
include "news-config-info.php";
include "../header.php";

if (file_exists('../config/news_page_authentication.php')) {
    include('../config/news_page_authentication.php');
}

if (isset($_SESSION['user_id'])) {
    $session_user_id = $_SESSION['user_id'];
}

$user_details_row = getUser($session_user_id);

if (isset($_GET['category'])) {


    $category_search_slug1 = str_replace('-', ' ', $_GET['category']);

    $category_search_slug = str_replace('.php', '', $category_search_slug1);

    $cat_search_row = getSlugNewsCategory($category_search_slug);  //Fetch Category Id using category name

    $category_id = $cat_search_row['category_id'];

    $category_slug = $cat_search_row['category_slug'];

    $category_search_name = $cat_search_row['category_name'];

    $category_search_query = "AND FIND_IN_SET($category_id, T1.category_id)";


}
?>
<style>
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
                    <li><a href="<?php echo $slash ?>news" class=""><?php echo $BIZBOOK['HOME']; ?></a></li>
                    <?php
                    foreach (getAllNewsCategoriesPos() as $news_category_row) {
                        ?>
                        <li><a href="<?php echo $ALL_NEWS_URL . urlModifier($news_category_row['category_slug']); ?>" class="<?php if($category_search_name == $news_category_row['category_name']){ echo 'act'; } ?>"><?php echo $news_category_row['category_name']; ?></a></li>
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
        <h1><b><?php echo $BIZBOOK['NEWS-HOMEPAGE-BANNER-H1-TEXT-1']; ?></b> <?php echo $category_search_name; ?></h1>
        <p><?php echo $BIZBOOK['NEWS-HOMEPAGE-BANNER-P-TEXT-1']; ?> <b><?php echo $category_search_name; ?></b> <?php echo $BIZBOOK['NEWS-HOMEPAGE-BANNER-P-TEXT-2']; ?></p>
    </div>
</section>
<!--END-->

<!-- START -->
<section class="news-hom-big">
    <div class="container">
        <div class="row">

            <div class="col-md-8">
                <div class="all-list-bre news-bre">
                    <ul>
                        <li><a href="<?php echo $slash ?>news"><?php echo $BIZBOOK['NEWS_HOME']; ?></a></li>
                        <li><a href="#!"><?php echo $category_search_name; ?></a></li>
                    </ul>
                </div>
                <?php
                $newssql = "SELECT T1.*  FROM " . TBL . "news AS T1 WHERE T1.news_status= 'Active' $category_search_query ";

                $newsrs = mysqli_query($conn, $newssql);
                $total_news = mysqli_num_rows($newsrs);

                if (mysqli_num_rows($newsrs) > 0) {

                    while ($newsrow = mysqli_fetch_array($newsrs)) {

                        $news_id = $newsrow['news_id'];

                        $news_category_id = $newsrow['category_id'];

                        $news_category_row = getNewsCategory($news_category_id);

                        $news_category_name = $news_category_row['category_name'];

                        ?>
                        <!--BIG POST START-->
                        <div class="news-home-box news-home-box1">
                            <div class="im">
                                <img src="<?php echo $slash; ?>/news/images/news/<?php echo $newsrow['news_image']; ?>"
                                     alt="">
                            </div>
                            <div class="txt">
                                <span class="news-cate"><?php echo $news_category_name; ?></span>
                                <h2><?php echo stripslashes($newsrow['news_title']); ?></h2>
                                <p><?php
                                    if (strlen($newsrow['news_description']) >= 100) {
                                        $pos = strpos($newsrow['news_description'], ' ', 100);
                                        echo substr(stripslashes($newsrow['news_description']), 0, $pos).'...';
                                    }else{
                                        echo stripslashes($newsrow['news_description']);
                                    }

                                    ?></p>
                                <span class="news-date"><?php echo dateFormatconverter($newsrow['news_cdt']); ?></span>
                                <span
                                    class="news-views"><?php echo AddingZero_BeforeNumber(news_detail_pageview_count($newsrow['news_id'])); ?> <?php echo $BIZBOOK['VIEWS']; ?></span>
                            </div>
                            <a href="<?php echo $NEWS_DETAIL_URL . urlModifier($newsrow['news_slug']); ?>"
                               class="fclick"></a>
                        </div>
                        <!--END BIG POST START-->
                        <?php
                    }
                } else {
                    ?>
                    <span style="    font-size: 21px;
    color: #bfbfbf;
    letter-spacing: 1px;
    /* background: #525252; */
    text-shadow: 0px 0px 2px #fff;
    text-transform: uppercase;
    text-align: center!important;
    margin-top: 5%;"><?php echo $BIZBOOK['NEWS_NO_NEWS_MESSAGE']; ?></span>
                    <?php
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
                if (isset($_GET['category'])) {
                    $latest_news_query = getAllNewsCategory($category_id);
                }else{
                    $latest_news_query = getAllNews();
                }
                foreach ($latest_news_query as $latest_news_row) {

                    $latest_news_category_id = $latest_news_row['category_id'];

                    $latest_news_category_row = getNewsCategory($latest_news_category_id);

                    $latest_news_category_name = $latest_news_category_row['category_name'];

                    ?>
                    <div class="col-md-4">
                        <div class="news-home-box">
                            <div class="im">
                                <img src="<?php echo $slash; ?>/news/images/news/<?php echo $latest_news_row['news_image']; ?>"
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
<script src="<?php echo $slash; ?><?php echo $slash; ?>js/slick.js"></script>
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