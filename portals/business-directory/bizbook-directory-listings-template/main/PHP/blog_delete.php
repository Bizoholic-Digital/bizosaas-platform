<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['blog_submit'])) {

        $blog_id = $_POST["blog_id"];

        $blog_image_old = $_POST["blog_image_old"];

        $blog_qry =
            "DELETE FROM  " . TBL . "blogs where blog_id='" . $blog_id . "'";


        $blog_res = mysqli_query($conn,$blog_qry);


        if ($blog_res) {

            unlink('images/blogs/'.$blog_image_old);  //Delete the Blog image

            //Query to delete the page view starts

            $page_view_qry = "DELETE FROM  " . TBL . "page_views where blog_id='" . $blog_id . "'";

            $page_view_res = mysqli_query($conn,$page_view_qry);

            //Query to delete the page view ends  

            $_SESSION['status_msg'] = $BIZBOOK['BLOGS_DELETE_SUCCESSFUL_MESSAGE'];

            header('Location: db-blog-posts');

        } else {

            $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

            header('Location: db-blog-posts');
        }

        //    Listing Update Part Ends

    }
} else {

    $_SESSION['status_msg'] = $BIZBOOK['OOPS_SOMETHING_WENT_WRONG'];

    header('Location: dashboard');
}