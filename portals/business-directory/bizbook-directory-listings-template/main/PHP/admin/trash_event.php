<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['event_submit'])) {

        $event_id = $_POST["event_id"];

        $event_image_old = $_POST["event_image_old"];

        $event_qry =
            "DELETE FROM  " . TBL . "events  where event_id='" . $event_id . "'";


        $event_res = mysqli_query($conn,$event_qry);


        if ($event_res) {

            unlink('../images/events/'.$event_image_old);  //Delete the Event image

            //Query to delete the page view starts

            $page_view_qry = "DELETE FROM  " . TBL . "page_views where event_id='" . $event_id . "'";

            $page_view_res = mysqli_query($conn,$page_view_qry);

            //Query to delete the page view ends                                    

            $_SESSION['status_msg'] = "Event has been Deleted Successfully!!!";

            header('Location: admin-event.php');

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-event.php');
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-event.php');
}