<?php
include "header.php";

include "home_page_inline_css.php";

include "home_page_top_section.php";
?>
<?php

if ($current_home_page != '2' && $current_home_page != '3'){

?>

<div class="ban-ql">
<div class="container">
            <div class="row">
                            <ul>
                                <?php
                                foreach (getAllHomePageTopSection() as $home_page_top_section_row) {
                                    ?>
                                    <li>
                                        <div>
                                            <img
                                                src="<?php echo $webpage_full_link; ?>images/icon/<?php echo $home_page_top_section_row['top_section_image']; ?>"
                                                alt="">
                                            <h4><?php echo $home_page_top_section_row['top_section_title']; ?></h4>
                                            <p><?php echo $home_page_top_section_row['top_section_description']; ?></p>
                                            <a href="<?php echo $home_page_top_section_row['top_section_link']; ?>"><?php echo $home_page_top_section_row['top_section_link_text']; ?></a>
                                        </div>
                                    </li>
                                    <?php
                                }
                                ?>

                            </ul>

                        </div>
                        </div>
                        </div>

<!-- START --> 
<section>
    <div class="str">
        <div class="container">
            <div class="row">
                <div class="home-tit">
                    <h2><span><?php echo $BIZBOOK['HOM-POP-TIT']; ?></span> <?php echo $BIZBOOK['HOM-POP-TIT1']; ?></h2>
                    <p><?php echo $BIZBOOK['HOM-POP-SUB-TIT']; ?></p>
                </div>
                <div class="land-pack">
                    <ul>
                        <?php
                        if ($current_home_page == '3' || $current_home_page == '4' || $current_home_page == '5' || $current_home_page == '6' || $current_home_page == '7' || $current_home_page == '8' || $current_home_page == '9' ) {

                            $all_cat_function = getAllCategoriesPos();

                        } else {
                            $all_cat_function = getAllTopCategories();
                        }

                        foreach ($all_cat_function as $toprow) {

                            $category_name = $toprow['category_name'];

                            if ($current_home_page == '3' || $current_home_page == '4' || $current_home_page == '5' || $current_home_page == '6' || $current_home_page == '7' || $current_home_page == '8' || $current_home_page == '9' ) {

                                $category_sql_row = getNameCategory($category_name);

                            } else {
                                $category_sql_row = getCategory($category_name);
                            }

                            ?>
                            <li>
                                <div class="land-pack-grid">
                                    <div class="land-pack-grid-img">
                                        <img src="images/services/<?php echo $toprow['category_image']; ?>" alt="">
                                    </div>
                                    <div class="land-pack-grid-text">
                                        <h4><?php echo $category_sql_row['category_name']; ?>
                                            <?php
                                            if ($current_home_page == '3' || $current_home_page == '4' || $current_home_page == '5' || $current_home_page == '6' || $current_home_page == '7' || $current_home_page == '8' || $current_home_page == '9' ) {
                                                ?>
                                                <span
                                                    class="dir-ho-cat"><?php echo $BIZBOOK['LISTINGS']; ?> <?php echo AddingZero_BeforeNumber(getCountCategoryListing($category_sql_row['category_id'])); ?></span>
                                                <?php
                                            } else {
                                                ?>
                                                <span
                                                    class="dir-ho-cat"><?php echo $BIZBOOK['SHOW_ALL']; ?> (<?php echo AddingZero_BeforeNumber(getCountCategoryListing($category_sql_row['category_id'])); ?>
                                                    )</span>
                                                <?php
                                            }
                                            ?>
                                        </h4>
                                    </div>
                                    <a href="<?php echo $ALL_LISTING_URL . urlModifier($category_sql_row['category_slug']); ?>"
                                       class="land-pack-grid-btn"><?php echo $BIZBOOK['VIEW_ALL_LISTINGS']; ?></a>
                                </div>
                            </li>
                            <?php
                        }
                        ?>
                    </ul>
                    <?php if ($current_home_page == '1' || $current_home_page == '2') { ?>
                    <a href="all-category" class="more"><?php echo $BIZBOOK['HOM-VI-ALL-SER']; ?></a>
                    <?php } ?>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->
<?php } ?>
<?php
include "home_page_mid_section.php"
?>

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
                            <span><?php echo $BIZBOOK['AD']; ?></span>

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
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/slick.js"></script>
<script src="js/custom.js"></script> 
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>
<?php
include "home_page_inline_js.php"
?>
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
                centerMode: false,
            }
        }]

    });
//test
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
    
    $('.multiple-items1').slick({
        infinite: true,
        slidesToShow: 3,
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