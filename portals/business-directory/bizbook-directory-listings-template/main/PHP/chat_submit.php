<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

//    Chat Insert Part Starts

    $chat_from_user = $_POST["chat_from_user"];
    $chat_to_user = $_POST["chat_to_user"];
    $chat_message = addslashes($_POST["chat_message"]);

    $chat_link_status = "Active";

    if (getCountReceiverChatLinks($chat_to_user, $chat_from_user) > 0) {

        foreach (getAllReceiverChatLinks($chat_to_user, $chat_from_user) as $query) {

            $chat_link_id = $query['chat_link_id']; //Chat Link Id
        }

    } elseif (getCountSenderChatLinks($chat_to_user, $chat_from_user) > 0) {

        foreach (getAllSenderChatLinks($chat_to_user, $chat_from_user) as $query) {

            $chat_link_id = $query['chat_link_id']; //Chat Link Id
        }

    } else {

           //New Chat Link Insert starts

        $chat_links_qry = "INSERT INTO " . TBL . "chat_links 
					(sender_id,receiver_id,chat_link_status,chat_link_udt,chat_link_cdt) 
					VALUES 
					('$chat_from_user','$chat_to_user','$chat_link_status', '$curDate', '$curDate')";

        $chat_links_res = mysqli_query($conn, $chat_links_qry);

        $chat_link_id = mysqli_insert_id($conn); //Chat Link Id

        //New Chat Link Insert Ends
    }

   //New Chat Insert starts

    $chat_qry = "INSERT INTO " . TBL . "chats 
					(chat_link_id,chat_user_id,chat_message,chat_status,chat_cdt) 
					VALUES 
					('$chat_link_id','$chat_from_user','$chat_message', '$chat_link_status', '$curDate')";

    $chat_res = mysqli_query($conn, $chat_qry);

    //New Chat Insert ends


    //Update Chat Link Update Date starts

    $chattt_link_qry = "UPDATE  " . TBL . "chat_links  SET chat_link_udt ='" . $curDate . "' where chat_link_id='" . $chat_link_id . "'";

    $chattt_link_res = mysqli_query($conn,$chattt_link_qry);

    //Update Chat Link Update Date ends

    if ($chat_res) {

        echo json_encode( array("sender23"=>$chat_from_user, "receiver"=>$chat_to_user));

    } else {
        echo '';
    }
} else {

    header('Location: index');
    exit;
}

//    Chat Insert Part Ends

