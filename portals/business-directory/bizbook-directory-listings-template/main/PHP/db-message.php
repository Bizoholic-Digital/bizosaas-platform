<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

include "dashboard_left_pane.php";

?>
<!--CENTER SECTION-->
<div class="ud-cen">
    <div class="log-bor">&nbsp;</div>
    <span class="udb-inst"><?php echo $BIZBOOK['MESSAGE']; ?></span>
    <?php include('config/user_activation_checker.php'); ?>
    <div class="ud-cen-s2">
        <h2><?php echo $BIZBOOK['DB-MESSAGES-ALL-MESSAGES']; ?></h2>
        <?php include "page_level_message.php"; ?>
        <a href="#" class="db-tit-btn comm-msg-act-btn"><?php echo $BIZBOOK['DB-MESSAGES-SEND-MESSAGES']; ?></a>
        <div id="indox" class="container tab-pane active"><br>
            <div class="mess-dash">
                <div class="mess-tit">
                    <div class="s1"><?php echo $BIZBOOK['S_NO']; ?></div>
                    <div class="s2"><?php echo $BIZBOOK['USER']; ?></div>
                    <div class="s3"><?php echo $BIZBOOK['MESSAGE']; ?></div>
                </div>
                <div class="mess-bd">
                    <!--=== MAIL THREAD ===-->
                    <?php
                    $si = 1;
                    foreach (getAllGivenIdChatLinks($_SESSION['user_id']) as $except_user_row) {

                        if ($_SESSION['user_id'] == $except_user_row['receiver_id']) {
                            $other_user_id = $except_user_row['sender_id'];
                            $sender_id = $except_user_row['receiver_id'];
                        } elseif ($_SESSION['user_id'] == $except_user_row['sender_id']) {
                            $other_user_id = $except_user_row['receiver_id'];
                            $sender_id = $except_user_row['sender_id'];
                        }

                        $chat_link_id = $except_user_row['chat_link_id'];
                        $other_user_details = getUser($other_user_id);

                        foreach (getLastChatMessageLinkIdChats($chat_link_id) as $last_chat) {
                            $last_chat = $last_chat['chat_message'];
                        }

                        ?>
                        <div class="main">
                            <div class="se1" id="chat-box-div<?php echo $si; ?>">
                                <div class="s1"><?php echo $si; ?></div>
                                <div class="s2">
                                    <img
                                        src="images/user/<?php if (($other_user_details['profile_image'] == NULL) || empty($other_user_details['profile_image'])) {
                                            echo $footer_row['user_default_image'];
                                        } else {
                                            echo $other_user_details['profile_image'];
                                        } ?>"><?php echo $other_user_details['first_name']; ?>
                                    <span><?php echo dateFormatconverter($other_user_details['user_cdt']) ?></span>
                                </div>
                                <div class="s3"><?php echo stripslashes($last_chat); ?></div>
                            </div>
                        </div>


                        <!--- CHAT CONVERSATION BOX START --->
                        <div class="msg-op msg-op-conve" id="msg-op-conve<?php echo $si; ?>">
                            <span class="comm-msg-pop-clo2" id="comm-msg-pop-clo2<?php echo $si; ?>"><i
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
                                        <h4><?php echo $BIZBOOK['HI']; ?>, <?php echo $user_details_row['first_name']; ?></h4>
                                        <input type="hidden" id="chat_from_user" name="chat_from_user"
                                               value="<?php echo $_SESSION['user_id']; ?>">
                                        <input type="hidden" name="chat_to_user" value="<?php echo $other_user_id; ?>">
                                        <select disabled="disabled" class="chosen-select"
                                                data-id="<?php echo $_SESSION['user_id']; ?>" id="chat_to_user234"
                                                name="chat_to_user234">
                                            <option value=""><?php echo $BIZBOOK['CHOOSE_A_USER']; ?></option>
                                            <?php
                                            foreach (getAllServiceUserExceptUserIdWithoutLimit($_SESSION['user_id']) as $except_user_row) {

                                                ?>
                                                <option <?php if ($other_user_id == $except_user_row['user_id']) {
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
                                                  placeholder="<?php echo $BIZBOOK['DB-MESSAGES-PLACEHOLDER']; ?>" required=""></textarea>
                                        <button id="chat_send<?php echo $si; ?>" name="chat_send" type="submit"><?php echo $BIZBOOK['SEND']; ?> <i
                                                class="material-icons">send</i></button>
                                    </div>
                                </form>
                            </div>
                        </div>
                        <!--- END --->


                        <?php
                        $si++;
                    }
                    ?>
                    <!--=== END MAIL THREAD ===-->
                </div>
            </div>
        </div>
    </div>
</div>
<?php
include "dashboard_right_pane.php";
?>


<!--- CHAT NEW BOX START --->
<div class="msg-op msg-op-new">
    <span class="comm-msg-pop-clo1"><i class="material-icons">close</i></span>
    <div class="inn">
        <form name="new_chat_form" id="new_chat_form" method="post">
            <div class="s1">
                <img
                    src="images/user/<?php if (($user_details_row['profile_image'] == NULL) || empty($user_details_row['profile_image'])) {
                        echo $footer_row['user_default_image'];
                    } else {
                        echo $user_details_row['profile_image'];
                    } ?>" alt="">
                <h4>Hi, <?php echo $user_details_row['first_name']; ?></h4>
                <input type="hidden" id="chat_from_user" name="chat_from_user"
                       value="<?php echo $_SESSION['user_id']; ?>">
                <select class="chosen-select" data-id="<?php echo $_SESSION['user_id']; ?>" id="chat_to_user"
                        name="chat_to_user">
                    <option value=""><?php echo $BIZBOOK['CHOOSE_A_USER']; ?></option>
                    <?php
                    foreach (getAllServiceUserExceptUserIdWithoutLimit($_SESSION['user_id']) as $except_user_row) {

                        ?>
                        <option
                            value="<?php echo $except_user_row['user_id']; ?>"><?php echo $except_user_row['first_name']; ?></option>
                        <?php
                    }
                    ?>
                </select>
            </div>
            <div class="s2 chat-box-messages">
                <!-- FROM -->
                <div><?php echo $BIZBOOK['COMMUNITY-PAGE-START-A-NEW-CHAT']; ?></div>
            </div>
            <div class="s3">
                <textarea name="chat_message" id="chat_message" placeholder="<?php echo $BIZBOOK['DB-MESSAGES-PLACEHOLDER']; ?>"
                          required=""></textarea>
                <button id="chat_send" name="chat_send" type="submit"><?php echo $BIZBOOK['SEND']; ?> <i class="material-icons">send</i></button>
            </div>
        </form>
    </div>
</div>
<!--- END --->


<style>
    .ud-cen {
        width: 74%;
    }

    .ud-rhs {
        display: none;
    }

    @media screen and (max-width: 992px) {
        .ud-cen {
            width: 100%;
        }
    }
</style>
<script>
    $(document).ready(function () {
        $(".comm-msg-act-btn").on('click', function () {
            $(".msg-op-new").addClass("msg-sho-act");
        });
        $(".comm-msg-pop-clo1").on('click', function () {
            $(".msg-op-new").removeClass("msg-sho-act");
        });

    });
</script>
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
<script>

    //    
    <!--Message New Chat Form Ajax Call And Validation starts-->

    $("#chat_send").click(function () {

        $("#new_chat_form").validate({
            rules: {
                chat_to_user: {required: true},
                chat_message: {required: true}

            },
            messages: {

                chat_to_user: {required: "Choose User"},
                chat_message: {required: "Type Something.."}
            },

            submitHandler: function (form) { // for demo
                $.ajax({
                    type: "POST",
                    data: $("#new_chat_form").serialize(),
                    url: "chat_submit.php",
                    cache: true,
                    success: function (data) {
                        var success = $.parseJSON(data);
                        if (data != null) {
                            updateChat(success.sender23, success.receiver);
                            $("#home_slide_enq_success").show();
                            $('input[type="text"],textarea').val('');
                        } else {
                            if (data == 3) {
                                $("#home_slide_enq_same").show();
                                $('input[type="text"],textarea').val('');
                            } else {
                                $("#home_slide_enq_fail").show();
                                $('input[type="text"],textarea').val('');
                            }
                        }

                    }

                })
            }
        });
    });
    <!--Message New Chat Form Ajax Call And Validation ends-->

    // Update Chat Box function starts

    function updateChat(sender, receiver) {
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
$si = 1;
foreach (getAllGivenIdChatLinks($_SESSION['user_id']) as $except_user_row) {

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
            $("#comm-msg-pop-clo2<?php echo $si; ?>").on('click', function () {
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

        function updateChat <?php echo $si; ?>(sender, receiver) {
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
                }
            });
        }

        // Update Chat Box function Ends


    </script>
    <?php
    $si++;
}
?>