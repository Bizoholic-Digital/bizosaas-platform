<?php
include "header.php";

if($footer_row['admin_event_show'] != 1) {
    header("Location: ".$webpage_full_link."dashboard");
}

?>
<!-- START -->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> blog-head eve-head"> 
    <div class="container">
        <div class="blog-head-inn">
            <h1><?php echo $BIZBOOK['EVENTS']; ?></h1>
            <p><?php echo $BIZBOOK['EVENT_HEAD_MESSAGE']; ?></p>
        </div>
        <div class="ban-search">
            <form>
                <ul>
                    <li class="sr-sea">
                        <input type="text" id="event-search" class="autocomplete"
                               placeholder="<?php echo $BIZBOOK['EVENT_SEARCH_EVENT_PLACEHOLDER']; ?>">
                    </li>
                </ul>
            </form>
        </div>
        <div class="blog-sli">
            <ul class="multiple-items1">
                <?php
                $si = 1;
                foreach (getAllTopViewsPremiumActiveEvents() as $top_event_row) {

                    $top_user_id = $top_event_row['user_id'];

                    $top_user_details_row = getUser($top_user_id);

                    ?>
                    <li>
                        <div class="blog-sli-box">
                            <div class="lhs">
                                <img src="images/events/<?php echo $top_event_row['event_image']; ?>" alt="">
                                <span class="eve-date-sli"><?php echo dateDayFormatconverter($top_event_row['event_start_date']); ?> <b><?php echo dateMonthFormatconverter($top_event_row['event_start_date']); ?></b></span>
                            </div>

                            <div class="rhs">
                                <span class="hig"><?php echo $BIZBOOK['EVENT_TOP_EVENTS']; ?></span>
                                <h4><?php echo $top_event_row['event_name']; ?></h4>
                                <div class="sli-desc">
                                    <p><?php echo stripslashes($top_event_row['event_description']) ?></p>
                                </div>
                                <div class="auth">
                                    <img src="images/user/<?php if (($top_user_details_row['profile_image'] == NULL) || empty($top_user_details_row['profile_image'])) {
                                        echo "1.jpg";
                                    } else {
                                        echo $top_user_details_row['profile_image'];
                                    } ?>" alt="">
                                    <b><?php echo $BIZBOOK['EVENT_HOSTED_BY']; ?></b><br>
                                    <h6><?php echo $top_user_details_row['first_name']; ?></h6>
                                </div>
                            </div>
                            <a href="<?php echo $EVENT_URL . urlModifier($top_event_row['event_slug']); ?>"
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
} ?> event-body">
    <div class="container">
        <div class="us-ppg-com">
            <ul id="intseres" class="events-wrapper">
                <?php
                $si = 1;
                foreach (getAllActiveEvents() as $eventrow) {

                    $user_id = $eventrow['user_id'];

                    $user_details_row = getUser($user_id);

                    ?>
                    <li class="events-item">
                        <div class="eve-box">
                            <div>
                                <a href="<?php echo $EVENT_URL . urlModifier($eventrow['event_slug']); ?>">
                                    <img src="images/events/<?php echo $eventrow['event_image']; ?>" alt="">
                                    <span><?php echo dateMonthFormatconverter($eventrow['event_start_date']); ?>
                                        <b><?php echo dateDayFormatconverter($eventrow['event_start_date']); ?></b></span>
                                </a>
                            </div>
                            <div>
                                <h4>
                                    <a href="<?php echo $EVENT_URL . urlModifier($eventrow['event_slug']); ?>"><?php echo $eventrow['event_name']; ?></a>
                                </h4>
                                    <span
                                        class="addr"><?php echo $eventrow['event_address']; ?></span>
                                <span class="pho"><?php echo $eventrow['event_mobile']; ?></span>
                            </div>
                            <div>
                                <div class="auth">
                                    <img
                                        src="images/user/<?php if (($user_details_row['profile_image'] == NULL) || empty($user_details_row['profile_image'])) {
                                            echo "1.jpg";
                                        } else {
                                            echo $user_details_row['profile_image'];
                                        } ?>" alt="">
                                    <b><?php echo $BIZBOOK['EVENT_HOSTED_BY']; ?></b><br>
                                    <h4><?php echo $user_details_row['first_name']; ?></h4>
                                    <a target="_blank"
                                       href="<?php echo $PROFILE_URL . urlModifier($user_details_row['user_slug']); ?>"
                                       class="fclick"></a>
                                </div>
                            </div>
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
<div id="event-pagination-container"></div>
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
    var items = $(".events-wrapper .events-item");
    var numItems = items.length;
    var perPage = 9;

    items.slice(perPage).hide();

    $('#event-pagination-container').pagination({
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