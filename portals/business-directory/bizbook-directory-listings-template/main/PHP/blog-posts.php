<?php
include "header.php";

if($footer_row['admin_blog_show'] != 1) {
    header("Location: ".$webpage_full_link."dashboard");
}

?>
<!-- START -->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> blog-head">
    <div class="container">
        <div class="blog-head-inn">
            <h1><?php echo $BIZBOOK['BLOG_POSTS']; ?></h1>
            <p><?php echo $BIZBOOK['BLOG-POST-HEAD']; ?></p>
        </div>
        <div class="ban-search">
            <form>
                <ul>
                    <li class="sr-sea">
                        <input type="text" id="blog-search" class="autocomplete" placeholder="<?php echo $BIZBOOK['BLOG-POST-SEARCH-LABEL']; ?>">
                    </li>
                </ul>
            </form>
        </div>
        <div class="blog-sli">
            <ul class="multiple-items1">
                <?php
                $si = 1;
                foreach (getAllTopViewsPremiumActiveBlogs() as $top_blog_row) {

                    $top_user_id = $top_blog_row['user_id'];

                    $top_user_details_row = getUser($top_user_id);

                    ?>
                    <li>
                        <div class="blog-sli-box">
                            <div class="lhs">
                                <img src="images/blogs/<?php echo $top_blog_row['blog_image']; ?>" alt="">
                            </div>

                            <div class="rhs">
                                <span class="hig"><?php echo $BIZBOOK['BLOG_TOP_POSTS']; ?></span>
                                <h4><?php echo $top_blog_row['blog_name']; ?></h4>
                                <div class="sli-desc">
                                <p><?php echo stripslashes($top_blog_row['blog_description'])?></p>
                                </div>
                                <div class="auth">
                                    <img src="<?php echo $slash; ?>images/user/<?php if (($top_user_details_row['profile_image'] == NULL) || empty($top_user_details_row['profile_image'])) {
                                        echo $footer_row['user_default_image'];
                                    } else {
                                        echo $top_user_details_row['profile_image'];
                                    } ?>" alt="">
                                    <b><?php echo $BIZBOOK['HOM3-OW-POSTED-BY']; ?></b><br>
                                    <h6><?php echo $top_blog_row['first_name']; ?></h6>
                                </div>
                            </div>
                            <a href="<?php echo $BLOG_URL . urlModifier($top_blog_row['blog_slug']); ?>"
                               class="fclick"></a>
                        </div>
                    </li>
                    <?php
                }
                ?>
            </ul>
        </div>
    </div>
</section>
<!--END-->

<!-- START -->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> blog-body">
    <div class="container">
        <div class="us-ppg-com us-ppg-blog">
            <ul id="intseres" class="blog-wrapper">
                <?php
                $si = 1;
                foreach (getAllActiveBlogs() as $blogrow) {

                    $user_id = $blogrow['user_id'];

                    $user_details_row = getUser($user_id);

                    ?>
                    <li class="blog-item">
                        <div class="pro-eve-box">
                            <div>
                                <img src="images/blogs/<?php echo $blogrow['blog_image']; ?>" alt="">
                            </div>
                            <div>
                                <h2><?php echo $blogrow['blog_name']; ?></h2>
                                <span class="ic-time"><?php echo dateFormatconverter($blogrow['blog_cdt']); ?></span>
                                <span class="ic-view"><?php echo blog_pageview_count($blogrow['blog_id']); ?></span>
                            </div>
                            <a href="<?php echo $BLOG_URL . urlModifier($blogrow['blog_slug']); ?>" class="fclick">
                                &nbsp;</a>
                        </div>
                    </li>
                    <?php
                }
                ?>
            </ul>
        </div>

    </div>
</section>
<!--END-->

<section>
    <div class="pop-ups pop-quo">
        <!-- The Modal -->
        <div class="modal fade" id="quote">
            <div class="modal-dialog">
                <div class="modal-content">
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                    <!-- Modal Header -->
                    <div class="quote-pop">
                        <h4><?php echo $BIZBOOK['LEAD-GET-QUOTE']; ?></h4>
                        <form>
                            <div class="form-group">
                                <input type="text" class="form-control" placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>" required>
                            </div>
                            <div class="form-group">
                                <input type="email" class="form-control" placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>"
                                       pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>" required>
                            </div>
                            <div class="form-group">
                                <input type="text" class="form-control" placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>"
                                       pattern="[7-9]{1}[0-9]{9}"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>" required>
                            </div>
                            <div class="form-group">
                                <textarea class="form-control" rows="3"
                                          placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
                        </form>
                    </div>
                    <div class="log-bor">&nbsp;</div>
                </div>
            </div>
        </div>
    </div>
</section>
<div id="blog-pagination-container"></div>
<?php
include "footer.php";
?>

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/slick.js"></script>
<script src="js/custom.js"></script>
<script src="js/jquery.simplePagination.min.js"></script>
<script>
    var items = $(".blog-wrapper .blog-item");
    var numItems = items.length;
    var perPage = 12;

    items.slice(perPage).hide();

    $('#blog-pagination-container').pagination({
        items: numItems,
        itemsOnPage: perPage,
        prevText: "&laquo;",
        nextText: "&raquo;",
        onPageClick: function (pageNumber) {
            var showFrom = perPage * (pageNumber - 1);
            var showTo = showFrom + perPage;
            items.hide().slice(showFrom, showTo).show();
            $("html, body").animate({ scrollTop: 0 }, "fast");
            return false;
        }
    });
    $('.multiple-items1').slick({
        infinite: true,
        slidesToShow: 1,
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