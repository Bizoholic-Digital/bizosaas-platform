<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['service_expert_submit'])) {

        $expert_id = $_POST["expert_id"];

        $profile_image_old = $_POST["profile_image_old"];
        $cover_image_old = $_POST["cover_image_old"];
        $id_proof_old = $_POST["id_proof_old"];

        $expert_qry =
            " DELETE FROM  " . TBL . "experts WHERE expert_id='" . $expert_id . "'";


        $expert_res = mysqli_query($conn,$expert_qry);


        if ($expert_res) {
            unlink('../service-experts/images/services/'.$profile_image_old);  //Delete the profile image
            unlink('../service-experts/images/services/'.$cover_image_old);  //Delete the Cover image
            unlink('../service-experts/images/services/'.$id_proof_old);  //Delete the Id Proof image


            //Query to delete the page view starts

            $page_view_qry = "DELETE FROM  " . TBL . "page_views where expert_id='" . $expert_id . "'";

            $page_view_res = mysqli_query($conn,$page_view_qry);

            //Query to delete the page view ends


            $_SESSION['status_msg'] = "Service Expert has been Permanently Deleted!!!";
            header('Location: expert-users.php');
        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: expert-delete-profile.php?code=' . $expert_id);
        }

        //    Experts Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: expert-users.php');
}