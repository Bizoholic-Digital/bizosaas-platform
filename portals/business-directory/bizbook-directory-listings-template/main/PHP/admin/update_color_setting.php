<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['color_setting_submit'])) {

        $custom_css_id = 1;
        
        $home_search_btn_default = $_POST['home_search_btn_default'];
        $home_search_btn_hover = $_POST['home_search_btn_hover'];

        $home_banner_btn_default = $_POST['home_banner_btn_default'];
        $home_banner_btn_hover = $_POST['home_banner_btn_hover'];

        $home_view_all_btn_default = $_POST['home_view_all_btn_default'];
        $home_view_all_btn_hover = $_POST["home_view_all_btn_hover"];

        $common_help_support_btn_default = $_POST["common_help_support_btn_default"];
        $common_help_support_btn_hover = $_POST["common_help_support_btn_hover"];
        
        $home_submit_req_btn_default = $_POST["home_submit_req_btn_default"];
        $home_submit_req_btn_hover = $_POST["home_submit_req_btn_hover"];
        
        $common_blue_btn = $_POST["common_blue_btn"];
        $common_light_blue_btn = $_POST["common_light_blue_btn"];

        $common_red_btn = $_POST["common_red_btn"];
        $common_dark_red_btn = $_POST["common_dark_red_btn"];

        $common_yellow_bottom_band = $_POST["common_yellow_bottom_band"];
        $common_yellow_1_bottom_band = $_POST["common_yellow_1_bottom_band"];
        $common_yellow_2_btn = $_POST["common_yellow_2_btn"];
        
        $common_gray_color = $_POST["common_gray_color"];
        $common_green_color = $_POST["common_green_color"];
        $common_light_green_color = $_POST["common_light_green_color"];
        $job_blue_color = $_POST["job_blue_color"];
        $job_orange_color = $_POST["job_orange_color"];


        $sql = mysqli_query($conn, "UPDATE  " . TBL . "custom_css SET  home_search_btn_default='" . $home_search_btn_default . "'
        ,home_search_btn_hover='" . $home_search_btn_hover . "', home_banner_btn_default='" . $home_banner_btn_default . "'
        , home_banner_btn_hover='" . $home_banner_btn_hover . "', home_view_all_btn_default='" . $home_view_all_btn_default . "'
        , home_view_all_btn_hover='" . $home_view_all_btn_hover . "'
        , common_help_support_btn_default='" . $common_help_support_btn_default . "', common_help_support_btn_hover='" . $common_help_support_btn_hover . "'
        , home_submit_req_btn_default='" . $home_submit_req_btn_default . "', home_submit_req_btn_hover='" . $home_submit_req_btn_hover . "'
        , common_blue_btn='" . $common_blue_btn . "', common_light_blue_btn='" . $common_light_blue_btn . "'
        , common_red_btn='" . $common_red_btn . "', common_dark_red_btn='" . $common_dark_red_btn . "'
        , common_yellow_bottom_band='" . $common_yellow_bottom_band . "', common_yellow_1_bottom_band='" . $common_yellow_1_bottom_band . "'
        , common_yellow_2_btn='" . $common_yellow_2_btn . "', common_gray_color='" . $common_gray_color . "'
        , common_green_color='" . $common_green_color . "', common_light_green_color='" . $common_light_green_color . "'
        , job_blue_color='" . $job_blue_color . "', job_orange_color='" . $job_orange_color . "'
        where custom_css_id ='" . $custom_css_id . "'");

        if ($sql) {


            $_SESSION['status_msg'] = "Color Setting Data has been Updated Successfully!!!";

            header('Location: color-setting.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: color-setting.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: color-setting.php');
    exit;
}
?>