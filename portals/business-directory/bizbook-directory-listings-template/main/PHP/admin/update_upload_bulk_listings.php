<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['upload_bulk_submit'])) {

        set_time_limit(0);
        ini_set('memory_limit', '1G');
        ini_set("auto_detect_line_endings", true);
        
        //validate whether uploaded file is a csv file
        $csvMimes = array('text/x-comma-separated-values', 'text/comma-separated-values', 'application/octet-stream', 'application/vnd.ms-excel', 'application/x-csv', 'text/x-csv', 'text/csv', 'application/csv', 'application/excel', 'application/vnd.msexcel', 'text/plain');
        if(!empty($_FILES['file']['name']) && in_array($_FILES['file']['type'],$csvMimes)) {
            if (is_uploaded_file($_FILES['file']['tmp_name'])) {

                //open uploaded csv file with read only mode
                $csvFile = fopen($_FILES['file']['tmp_name'], 'r');

                //skip first line
                fgetcsv($csvFile);

                //parse data from csv file line by line
                while (($line = fgetcsv($csvFile)) !== FALSE) {

                    $city_name = ucwords($line[4]);
                    $category_name = ucwords($line[0]);



                    //check whether city already exists in database with same city_name
                    $prevQuery = mysqli_query($conn,"SELECT city_id FROM " . TBL . "cities WHERE city_name = '" . $city_name . "'");
                    $prevResult = mysqli_fetch_array($prevQuery);

                    if (mysqli_num_rows($prevQuery) > 0) {
                        //update city data
                        $city_id = $prevResult['city_id'];
                    } else {
                        //insert city data into database
                        $insert_city = mysqli_query($conn,"INSERT INTO " . TBL . "cities (city_name, state_id) VALUES ('" . $city_name . "','" . $state_id . "')");
                        $city_id = mysqli_insert_id($conn);
                    }

                     //===============================================================

                    //check whether category already exists in database with same category_name
                    $catQuery = mysqli_query($conn,"SELECT category_id FROM " . TBL . "categories WHERE category_name = '" . $category_name . "'");
                    $catResult = mysqli_fetch_array($catQuery);

                    if (mysqli_num_rows($catQuery) > 0) {
                        //update category data
                        $category_id = $catResult['category_id'];
                    } else {
                        //insert category data into database
                        $insert_categoryy = mysqli_query($conn,"INSERT INTO " . TBL . "categories (category_name) VALUES ('" . $category_name . "')");
                        $category_id = mysqli_insert_id($conn);
                    }



                    $user_id = '1';
                    $listing_type_id = "1";
                    $listing_name = ucwords($line[2]);
                    $listing_address = $line[3];
                    $country_id = "38";
                    $state_id = "671";
                    $listing_mobile = $line[1];

                    // Listing Status
                    $listing_status = "Active";
                    // $listing_status = "Pending";
                    $payment_status = "Pending";

                    $listsql = "SELECT listing_id FROM " . TBL . "listings  WHERE listing_name= '$listing_name' AND listing_address = '$listing_address' AND listing_mobile = '$listing_mobile' AND city_id = '$city_id'";

                    $listrs = mysqli_query($conn,$listsql);

                    if (mysqli_num_rows($listrs) <= 0) {

                        $listing_qry = "INSERT INTO " . TBL . "listings 
					(user_id, listing_type_id, listing_name, listing_address, listing_mobile, country_id, state_id, city_id, category_id, listing_status
					, payment_status, listing_cdt) 
					VALUES 
					('$user_id', '$listing_type_id', '$listing_name', '$listing_address', '$listing_mobile', '$country_id', '$state_id', '$city_id', '$category_id', '$listing_status'
					, '$payment_status', '$curDate')";

                        $listing_res = mysqli_query($conn,$listing_qry);
                        $ListingID = mysqli_insert_id($conn);
                        $listlastID = $ListingID;

                        switch (strlen($ListingID)) {
                            case 1:
                                $ListingID = '00' . $ListingID;
                                break;
                            case 2:
                                $ListingID = '0' . $ListingID;
                                break;
                            default:
                                $ListingID = $ListingID;
                                break;
                        }

                        $ListCode = 'LIST' . $ListingID;

                        $lisupqry = "UPDATE " . TBL . "listings 
					  SET listing_code = '$ListCode' 
					  WHERE listing_id = $listlastID";

                        $lisupres = mysqli_query($conn,$lisupqry);
                    }


                }

                //close opened csv file
                fclose($csvFile);

                $_SESSION['status_msg'] = "New Bulk Listings Updated Successfully!!!";


                header('Location: admin-upload-bulk.php');
                exit;

            }else {

                $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

                header('Location: admin-upload-bulk.php');
                exit;
            }



        }else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-import.php');
            exit;
        }

        }else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: admin-import.php');
            exit;
        }

        }else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: admin-import.php');
    exit;
}
?>