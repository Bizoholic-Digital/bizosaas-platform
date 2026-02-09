<?php
include "header.php";
?>
<!-- START -->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?>">
    <div class="abou-pg commun-pg-main">
        <div class="about-ban comunity-ban">
            <h1><?php echo $BIZBOOK['COMMUNITY-PAGE-HEADING-LABEL']; ?></h1>
            <p><?php echo $BIZBOOK['COMMUNITY-PAGE-P-TAG']; ?></p>
            <input type="text" id="tail-se" placeholder="<?php echo $BIZBOOK['COMMUNITY-PAGE-PLACEHOLDER']; ?>">
        </div>
    </div>
    <div class="container">
        <div class="row">
            <div class="comity-all-user">
                <ul id="tail-re" class="community-wrapper">
                    <?php
                    $si = 1;
                    //                    foreach (getUserNotFollowingCommunity($_SESSION['user_id']) as $all_user_details_row) {
                    foreach (getAllCommunityUser() as $all_user_details_row) {

                        $all_user_id = $all_user_details_row['user_id'];

                        $all_list_count = getCountUserListing($all_user_id);

                        $all_event_count = getCountUserEvent($all_user_id);

                        $all_blog_count = getCountUserBlog($all_user_id);

                        $all_product_count = getCountUserProduct($all_user_id);

                        if (getCountReceiverChatLinks($all_user_id, $_SESSION['user_id']) > 0) {

                            foreach (getAllReceiverChatLinks($all_user_id, $_SESSION['user_id']) as $query) {

                                $chat_link_id = $query['chat_link_id'];
                            }

                        } elseif (getCountSenderChatLinks($all_user_id, $_SESSION['user_id']) > 0) {

                            foreach (getAllSenderChatLinks($all_user_id, $_SESSION['user_id']) as $query) {

                                $chat_link_id = $query['chat_link_id'];
                            }
                        }

                        ?>
                        <li class="community-item">
                            <div class="pro-fol-gr">
                                <div class="pro-ful-img">
                                    <img
                                        src="images/user/<?php if (($all_user_details_row['profile_image'] == NULL) || empty($all_user_details_row['profile_image'])) {
                                            echo $footer_row['user_default_image'];
                                        } else {
                                            echo $all_user_details_row['profile_image'];
                                        } ?>" alt="">
                                    <h4>
                                        <b><?php echo ucfirst(strtolower($all_user_details_row['first_name'])); ?></b><?php echo $all_user_details_row['user_city']; ?>
                                    </h4>
                                    <a href="<?php echo $PROFILE_URL . urlModifier($all_user_details_row['user_slug']); ?>"
                                       class="comm-viw-pro-btn" target="_blank"></a>
                                </div>
                                <div class="count-li">
                                    <span><b><?php echo $all_list_count; ?></b> <?php echo $BIZBOOK['LISTINGS']; ?></span>
                                    <span><b><?php echo $all_event_count; ?></b> <?php echo $BIZBOOK['EVENTS']; ?></span>
                                    <span><b><?php echo $all_blog_count; ?></b> <?php echo $BIZBOOK['BLOGS']; ?></span>
                                    <span><b><?php echo $all_product_count; ?></b> <?php echo $BIZBOOK['PRODUCTS']; ?></span>
                                </div>
                                <div class="pro-pg-msg">
                                    <span id="chat-box-div<?php echo $si; ?>" class="comm-msg-act-btn"><i
                                            class="material-icons">message</i> <?php echo $BIZBOOK['MESSAGE']; ?></span>
                                    <?php
                                    if ($_SESSION['user_id'] == NULL || empty($_SESSION['user_id'])) {
                                        ?>
                                        <a href="<?php echo $webpage_full_link; ?>login"><?php echo $BIZBOOK['FOLLOW']; ?></a>
                                        <?php
                                    } else {
                                        ?><span
                                        class="cta userfollow follow-content<?php echo $all_user_id ?>"
                                        data-item="<?php echo $all_user_id; ?>"
                                        data-num="<?php echo $_SESSION['user_id']; ?>"><?php if (getCountUserProfileFollowing($_SESSION['user_id'], $all_user_id) == 0) {
                                            echo $BIZBOOK['FOLLOW'];
                                        } else {
                                            echo $BIZBOOK['UN_FOLLOW'];
                                        } ?></span>
                                        <?php
                                    }
                                    ?>
                                </div>
                            </div>
                        </li>
                        <!--- CHAT CONVERSATION BOX START --->
                        <div class="msg-op msg-op-conve" id="msg-op-conve<?php echo $si; ?>">
                            <span class="comm-msg-pop-clo" id="comm-msg-pop-clo<?php echo $si; ?>"><i
                                    class="material-icons">close</i></span>

                            <div class="inn">
                                <form name="new_chat_form" id="new_chat_form<?php echo $si; ?>" method="post">
                                    <div class="s1">
                                        <img
                                            src="images/user/<?php if (($user_details_row['profile_image'] == NULL) || empty($user_details_row['profile_image'])) {
                                                echo $footer_row['user_default_image'];
                                            } else {
                                                echo $user_details_row['profile_image'];
                                            } ?>" alt="">
                                        <h4><?php echo $BIZBOOK['HI']; ?>
                                            , <?php echo $user_details_row['first_name']; ?></h4>
                                        <input type="hidden" id="chat_from_user" name="chat_from_user"
                                               value="<?php echo $_SESSION['user_id']; ?>">
                                        <input type="hidden" name="chat_to_user" value="<?php echo $all_user_id; ?>">
                                        <select disabled="disabled" class="chosen-select"
                                                data-id="<?php echo $_SESSION['user_id']; ?>" id="chat_to_user234"
                                                name="chat_to_user234">
                                            <option value=""><?php echo $BIZBOOK['CHOOSE_A_USER']; ?></option>
                                            <?php
                                            foreach (getAllServiceUserExceptUserIdWithoutLimit($_SESSION['user_id']) as $except_user_row) {

                                                ?>
                                                <option <?php if ($all_user_id == $except_user_row['user_id']) {
                                                    echo "selected";
                                                } ?>
                                                    value="<?php echo $except_user_row['user_id']; ?>"><?php echo $except_user_row['first_name']; ?></option>
                                                <?php
                                            }
                                            ?>
                                        </select>
                                    </div>
                                    <div class="s2 chat-box-messages">
                                        <?php

                                        if (getCountChatLinkIdChats($chat_link_id) > 0) {


                                            foreach (getAllChatLinkIdChats($chat_link_id) as $chat_row) {

                                                ?>
                                                <div class="chat-con">
                                                    <div
                                                        class="<?php if ($_SESSION['user_id'] == $chat_row['chat_user_id']) { ?>chat-rhs<?php } else { ?> chat-lhs<?php } ?>">
                                                        <?php echo stripslashes($chat_row['chat_message']); ?>
                                                    </div>
                                                </div>

                                                <?php
                                            }

                                        } else {
                                            ?>
                                            <span><?php echo $BIZBOOK['COMMUNITY-PAGE-START-A-NEW-CHAT']; ?></span>
                                            <?php
                                        }
                                        ?>
                                    </div>
                                    <div class="s3">
                                        <textarea name="chat_message" id="chat_message"
                                                  placeholder="<?php echo $BIZBOOK['DB-MESSAGES-PLACEHOLDER']; ?>"
                                                  required=""></textarea>
                                        <button id="chat_send<?php echo $si; ?>" name="chat_send"
                                                type="submit"><?php echo $BIZBOOK['SEND']; ?> <i class="material-icons">send</i>
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </div>
                        <!--- END --->
                        <?php
                        $si++;
                    }
                    ?>


                </ul>
            </div>
        </div>
    </div>
</section>
<!--END-->
<div id="community-pagination-container"></div>
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
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>
<script src="js/jquery.simplePagination.min.js"></script>
<script>
    var items = $(".community-wrapper .community-item");
    var numItems = items.length;
    var perPage = 18;

    items.slice(perPage).hide();

    $('#community-pagination-container').pagination({
        items: numItems,
        itemsOnPage: perPage,
        prevText: "&laquo;",
        nextText: "&raquo;",
        onPageClick: function (pageNumber) {
            var showFrom = perPage * (pageNumber - 1);
            var showTo = showFrom + perPage;
            items.hide().slice(showFrom, showTo).show();
            $("html, body").animate({scrollTop: 0}, "fast");
            return false;
        }
    });
</script>
<script>
    $("#tail-se").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#tail-re li").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
</script>
<?php
$si = 1;
foreach (getAllJob() as $all_user_details_row) {

    ?>
    <script>
        $(document).ready(function () {
            $("#chat-box-div<?php echo $si; ?>").on('click', function () {
                $("#msg-op-conve<?php echo $si; ?>").addClass("msg-sho-act");
                setTimeout(function () {
                    var d = $(".chat-box-messages");
                    d.scrollTop(d[0].scrollHeight);
                }, 1);
            });
            $("#comm-msg-pop-clo<?php echo $si; ?>").on('click', function () {
                $("#msg-op-conve<?php echo $si; ?>").removeClass("msg-sho-act");
            });

        });

    </script>
    <script>

        //
        <!--Message New Chat Form Ajax Call And Validation starts-->

        $("#chat_send<?php echo $si; ?>").click(function () {
            $("#new_chat_form<?php echo $si; ?>").validate({
                rules: {
                    chat_to_user: {required: true},
                    chat_message: {required: true}

                },
                messages: {

                    chat_to_user: {required: "Choose User"},
                    chat_message: {required: "Type Something.."}
                },

                submitHandler: function (form) { // for demo
                    //form.submit();
                    $.ajax({
                        type: "POST",
                        data: $("#new_chat_form<?php echo $si; ?>").serialize(),
                        url: "chat_submit.php",
                        cache: true,
                        success: function (data) {
                            var success = $.parseJSON(data);
                            if (data != null) {
                                updateChat<?php echo $si; ?>(success.sender23, success.receiver);
                                $('input[type="text"],textarea').val('');
                            } else {
                                $('input[type="text"],textarea').val('');
                            }

                        }

                    })
                }
            });
        });
        <!--Message New Chat Form Ajax Call And Validation ends-->

        // Update Chat Box function starts

        function updateChat<?php echo $si; ?>(sender, receiver) {
            var sender_checklist = "&sender_id=" + sender;
            var receiver_checklist = "&receiver_id=" + receiver;
            var main_string = sender_checklist + receiver_checklist;
            main_string = main_string.substring(1, main_string.length);

            $.ajax({
                type: "POST",
                url: 'filter_chat.php',
                data: main_string,
                cache: false,
                success: function (html) {
                    //alert(html);
                    $(".chat-box-messages").html(html);
                    $(".chat-box-messages").css("opacity", 1);
                    setTimeout(function () {
                        var d = $(".chat-box-messages");
                        d.scrollTop(d[0].scrollHeight);
                    }, 1);
                    // $("#loaderID").css("opacity",0);
                }
            });
        }

        // Update Chat Box function Ends


    </script>
    <?php
    $si++;
}
?>
</body>

</html>