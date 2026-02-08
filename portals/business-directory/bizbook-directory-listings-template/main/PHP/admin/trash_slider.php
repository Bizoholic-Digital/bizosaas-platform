<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['delete_slider_submit'])) {

        $slider_id = $_POST['slider_id'];
        $slider_photo_old = $_POST['slider_photo_old'];

        $ads_qry =
            "DELETE FROM  " . TBL . "slider  where slider_id='" . $slider_id . "'";


        $ads_res = mysqli_query($conn,$ads_qry);


        if ($ads_res) {

            unlink('../images/slider/'.$slider_photo_old);  //Delete the slider image

            $_SESSION['status_msg'] = "Slider has been Deleted Successfully!!!";


                header('Location: admin-slider-all.php');
                exit;



        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-slider-all.php');
            exit;
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-slider-all.php');
}