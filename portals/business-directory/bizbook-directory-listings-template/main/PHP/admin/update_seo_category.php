<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['seo-submit'])) {

        $category_id = $_POST['category_id'];
        $category_description = addslashes($_POST['category_description']);


        $category_seo_title = $_POST['category_seo_title'];
        $category_seo_keywords = $_POST['category_seo_keywords'];
        $category_seo_description = $_POST['category_seo_description'];

        $category_faq_1_ques = $_POST['category_faq_1_ques'];
        $category_faq_1_ans = $_POST['category_faq_1_ans'];

        $category_faq_2_ques = $_POST['category_faq_2_ques'];
        $category_faq_2_ans = $_POST['category_faq_2_ans'];

        $category_faq_3_ques = $_POST['category_faq_3_ques'];
        $category_faq_3_ans = $_POST['category_faq_3_ans'];

        $category_faq_4_ques = $_POST['category_faq_4_ques'];
        $category_faq_4_ans = $_POST['category_faq_4_ans'];

        $category_faq_5_ques = $_POST['category_faq_5_ques'];
        $category_faq_5_ans = $_POST['category_faq_5_ans'];

        $category_faq_6_ques = $_POST['category_faq_6_ques'];
        $category_faq_6_ans = $_POST['category_faq_6_ans'];

        $category_faq_7_ques = $_POST['category_faq_7_ques'];
        $category_faq_7_ans = $_POST['category_faq_7_ans'];

        $category_faq_8_ques = $_POST['category_faq_8_ques'];
        $category_faq_8_ans = $_POST['category_faq_8_ans'];

        $category_google_schema = $_POST['category_google_schema'];


        $sql = mysqli_query($conn,"UPDATE  " . TBL . "categories SET  category_seo_title='" . $category_seo_title. "'
        ,category_seo_keywords='" . $category_seo_keywords. "', category_seo_description='" . $category_seo_description . "'
        , category_faq_1_ques='" . $category_faq_1_ques. "', category_faq_1_ans='" . $category_faq_1_ans . "'
        , category_faq_2_ques='" . $category_faq_2_ques. "', category_faq_2_ans='" . $category_faq_2_ans . "'
        , category_faq_3_ques='" . $category_faq_3_ques. "', category_faq_3_ans='" . $category_faq_3_ans . "'
        , category_faq_4_ques='" . $category_faq_4_ques. "', category_faq_4_ans='" . $category_faq_4_ans . "'
        , category_faq_5_ques='" . $category_faq_5_ques. "', category_faq_5_ans='" . $category_faq_5_ans . "'
        , category_faq_6_ques='" . $category_faq_6_ques. "', category_faq_6_ans='" . $category_faq_6_ans . "'
        , category_faq_7_ques='" . $category_faq_7_ques. "', category_faq_7_ans='" . $category_faq_7_ans . "'
        , category_faq_8_ques='" . $category_faq_8_ques. "', category_faq_8_ans='" . $category_faq_8_ans . "'
        , category_description='" . $category_description. "', category_edit_cdt='$curDate'
        , category_google_schema='" . $category_google_schema . "'
        where category_id='" . $category_id . "'");


        if ($sql) {

            $_SESSION['status_msg'] = "Category SEO options has been Updated Successfully!!!";


            header('Location: seo-listing-options.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: seo-listing-options.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: seo-listing-options.php');
    exit;
}
?>