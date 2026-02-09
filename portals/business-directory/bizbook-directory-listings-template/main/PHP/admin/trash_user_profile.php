<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {

    if (isset($_POST['register_submit'])) {


        $path_id = $_POST['path_id'];
        $user_id = $_POST['user_id']; //Session User Code


        //Delete user from user table
        $sql =
            " DELETE FROM  " . TBL . "users  WHERE user_id='" . $user_id . "'";

        $sql_res = mysqli_query($conn,$sql);


        //Delete user listings from listing table

        $list =
            " DELETE FROM  " . TBL . "listings  WHERE user_id='" . $user_id . "'";

        $list_res = mysqli_query($conn,$list);

        //Delete user products from product table

        $product =
            " DELETE FROM  " . TBL . "products  WHERE user_id='" . $user_id . "'";

        $product_res = mysqli_query($conn,$product);


        //Delete user Events from events table

        $events =
            " DELETE FROM  " . TBL . "events  WHERE user_id='" . $user_id . "'";

        $events_res = mysqli_query($conn,$events);


        //Delete user Blogs from events table

        $blogs =
            " DELETE FROM  " . TBL . "blogs  WHERE user_id='" . $user_id . "'";

        $blogs_res = mysqli_query($conn,$blogs);

        


        if ($sql_res) {

            $_SESSION['status_msg'] = "User has been Permenantly Deleted!!!";

            if ($path_id == 1) {
                header('Location: admin-new-user-requests.php');
                exit;
            } elseif ($path_id == 2) {
                header('Location: admin-all-users.php');
                exit;
            } elseif ($path_id == 3) {
                header('Location: admin-all-users-general.php');
                exit;
            } elseif ($path_id == 4) {
                header('Location: admin-all-users-service-provider.php');
                exit;
            } elseif ($path_id == 5) {
                header('Location: admin-free-users.php');
                exit;
            } elseif ($path_id == 6) {
                header('Location: admin-standard-users.php');
                exit;
            } elseif ($path_id == 7) {
                header('Location: admin-premium-users.php');
                exit;
            } elseif ($path_id == 8) {
                header('Location: admin-premium-plus-users.php');
                exit;
            } else {
                header('Location: admin-all-users.php');
                exit;
            }

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            if ($path_id == 1) {
                header('Location: admin-new-user-requests.php');
                exit;
            } elseif ($path_id == 2) {
                header('Location: admin-all-users.php');
                exit;
            } elseif ($path_id == 3) {
                header('Location: admin-all-users-general.php');
                exit;
            } elseif ($path_id == 4) {
                header('Location: admin-all-users-service-provider.php');
                exit;
            } elseif ($path_id == 5) {
                header('Location: admin-free-users.php');
                exit;
            } elseif ($path_id == 6) {
                header('Location: admin-standard-users.php');
                exit;
            } elseif ($path_id == 7) {
                header('Location: admin-premium-users.php');
                exit;
            } elseif ($path_id == 8) {
                header('Location: admin-premium-plus-users.php');
                exit;
            } else {
                header('Location: admin-all-users.php');
                exit;
            }
        }

    }
    else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        if ($path_id == 1) {
            header('Location: admin-new-user-requests.php');
            exit;
        } elseif ($path_id == 2) {
            header('Location: admin-all-users.php');
            exit;
        } elseif ($path_id == 3) {
            header('Location: admin-all-users-general.php');
            exit;
        } elseif ($path_id == 4) {
            header('Location: admin-all-users-service-provider.php');
            exit;
        } elseif ($path_id == 5) {
            header('Location: admin-free-users.php');
            exit;
        } elseif ($path_id == 6) {
            header('Location: admin-standard-users.php');
            exit;
        } elseif ($path_id == 7) {
            header('Location: admin-premium-users.php');
            exit;
        } elseif ($path_id == 8) {
            header('Location: admin-premium-plus-users.php');
            exit;
        } else {
            header('Location: admin-all-users.php');
            exit;
        }
    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    if ($path_id == 1) {
        header('Location: admin-new-user-requests.php');
        exit;
    } elseif ($path_id == 2) {
        header('Location: admin-all-users.php');
        exit;
    } elseif ($path_id == 3) {
        header('Location: admin-all-users-general.php');
        exit;
    } elseif ($path_id == 4) {
        header('Location: admin-all-users-service-provider.php');
        exit;
    } elseif ($path_id == 5) {
        header('Location: admin-free-users.php');
        exit;
    } elseif ($path_id == 6) {
        header('Location: admin-standard-users.php');
        exit;
    } elseif ($path_id == 7) {
        header('Location: admin-premium-users.php');
        exit;
    } elseif ($path_id == 8) {
        header('Location: admin-premium-plus-users.php');
        exit;
    } else {
        header('Location: admin-all-users.php');
        exit;
    }
}
?>