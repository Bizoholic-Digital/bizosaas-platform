<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */


if (file_exists('config/info.php')) {
    include('config/info.php');
}

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

if (isset($_SESSION['user_id'])) {
    $session_user_id = $_SESSION['user_id'];
}
$user_details_row = getUser($session_user_id); //Fetch User data


$sender_id = $_REQUEST['sender_id'];
$receiver_id = $_REQUEST['receiver_id'];


?>

<div class="s2 chat-box-messages">

    <?php

    if (getCountReceiverChatLinks($receiver_id, $sender_id) > 0) {

        foreach (getAllReceiverChatLinks($receiver_id, $sender_id) as $query) {

            $chat_link_id = $query['chat_link_id'];
        }


        foreach (getAllChatLinkIdChats($chat_link_id) as $chat_row) {

            ?>
            <div class="chat-con">
                <div
                    class="<?php if ($chat_row['chat_user_id'] == $session_user_id) { ?>chat-rhs<?php } else { ?> chat-lhs<?php } ?>">
                    <?php echo stripslashes($chat_row['chat_message']); ?>
                </div>
            </div>

            <?php
        }

    } elseif (getCountSenderChatLinks($receiver_id, $sender_id) > 0) {

        foreach (getAllSenderChatLinks($receiver_id, $sender_id) as $query) {

            $chat_link_id = $query['chat_link_id'];
        }

        foreach (getAllChatLinkIdChats($chat_link_id) as $chat_row) {

            ?>
            <div class="chat-con">
                <div
                    class="<?php if ($chat_row['chat_user_id'] == $session_user_id) { ?>chat-rhs<?php } else { ?> chat-lhs<?php } ?>">
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

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<script src="js/listing_filter.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>