<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */


if(file_exists('config/info.php'))
{
    include('config/info.php');
}

if(isset($_GET['code'])){

    $all_promote_enquiry_id = $_GET['code'];

    $sql = "SELECT * FROM " . TBL . "all_promote_enquiry where all_promote_enquiry_id = '" . $all_promote_enquiry_id . "'";
    $rs = mysqli_query($conn, $sql);
    $row = mysqli_fetch_array($rs);

    $promote_type_value = $row['promote_type_value'];

    $promote_type_id = $row['promote_type_id'];

    $all_promote_price = mysqli_query($conn, "SELECT * FROM  " . TBL . "all_promote_price where all_promote_price_id='" . $all_promote_enquiry_id . "'");
    $all_promote_price_row = mysqli_fetch_array($all_promote_price);

    $display_position = 101;  //Position Id


    $listing_qry =
        "DELETE  FROM " . TBL . "all_promote_enquiry where all_promote_enquiry_id='" . $all_promote_enquiry_id . "'";

    $listing_res = mysqli_query($conn, $listing_qry);


    if ($listing_res) {

        if ($promote_type_value == 1) {



                $lisupqry = "UPDATE  " . TBL . "listings SET display_position=100,start_date='0000-00-00',end_date='0000-00-00',payment=0
					  WHERE listing_id = $promote_type_id";

                $lisupres = mysqli_query($conn, $lisupqry);


        } elseif ($promote_type_value == 2) {

            if ($display_position > 100) {


                $lisupqry = "DELETE FROM  " . TBL . "top_events  where event_name = '$promote_type_id' AND display_position != 1";

                $lisupres = mysqli_query($conn, $lisupqry);

            } else {

                $lisupqry = "UPDATE  " . TBL . "events SET display_position=100,start_date='0000-00-00',end_date='0000-00-00',payment=0 WHERE event_id = $promote_type_id";

                $lisupres = mysqli_query($conn, $lisupqry);
            }

        } elseif ($promote_type_value == 3) {

            $lisupqry = "UPDATE  " . TBL . "blogs SET display_position=100,
    start_date='0000-00-00',end_date='0000-00-00',payment=0
					  WHERE blog_id = $promote_type_id";

            $lisupres = mysqli_query($conn, $lisupqry);

        } elseif ($promote_type_value == 4) {

            if ($display_position > 100) {


                $lisupqry = "DELETE FROM  " . TBL . "trend_categories  where category_name = '$promote_type_id' AND display_position != 1";

                $lisupres = mysqli_query($conn, $lisupqry);

            } else {

                $lisupqry = "UPDATE  " . TBL . "products SET display_position=100,
    start_date='0000-00-00',end_date='0000-00-00',payment=0
					  WHERE product_id = $promote_type_id";

                $lisupres = mysqli_query($conn, $lisupqry);
            }

        }


        $_SESSION['status_msg'] = "Expired Promotion has been Deleted Successfully!!!";


        header('Location: admin-all-promotions.php');

    } else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";


        header('Location:admin-all-promotions.php');

    }


}