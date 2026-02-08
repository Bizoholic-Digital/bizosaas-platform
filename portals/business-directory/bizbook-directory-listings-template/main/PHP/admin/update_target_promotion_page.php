<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {


    if (isset($_POST['target_submit'])) {


        $page_id = $_POST["page_id"];

        $page_name = $_POST["page_name"];

        $page_seo_title = $_POST["page_seo_title"];
        $page_seo_keyword = addslashes($_POST["page_seo_keyword"]);
        $page_seo_description = addslashes($_POST["page_seo_description"]);
        $page_seo_schema = addslashes($_POST["page_seo_schema"]);

        $page_type = 1;

        $page_listings123 = $_POST["page_listings"];

        $prefix3 = '';
        foreach ($page_listings123 as $fruit3)
        {
            $page_listings .= $prefix3 .  $fruit3 ;
            $prefix3 = ',';
        }

        function checkPageSlug($link,$page_id, $counter=1){
            global $conn;
            $newLink = $link;
            do{
                $checkLink = mysqli_query($conn, "SELECT page_id FROM " . TBL . "pages WHERE page_slug = '$newLink' AND page_id != '$page_id' AND page_type = 1");
                if(mysqli_num_rows($checkLink) > 0){
                    $newLink = $link.''.$counter;
                    $counter++;
                } else {
                    break;
                }
            } while(1);

            return $newLink;
        }


        $page_name1 = trim(preg_replace('/[^A-Za-z0-9]/', ' ', $page_name));
        $page_slug = checkPageSlug($page_name1,$page_id);


        $sql = mysqli_query($conn,"UPDATE  " . TBL . "pages SET  page_name='" . $page_name. "'
        , page_seo_title ='" . $page_seo_title . "'
        , page_seo_keyword ='" . $page_seo_keyword. "', page_seo_description='" . $page_seo_description . "'
        , page_seo_schema='" . $page_seo_schema. "', page_type='" . $page_type . "'
        , page_last_edit='" . $curDate . "', page_slug='" . $page_slug . "'
        , page_listings='" . $page_listings . "'
        where page_id='" . $page_id . "'");


        if ($sql) {

            $_SESSION['status_msg'] = "Target Promotion Page has been Updated Successfully!!!";


            header('Location: seo-target-promotion-all-pages.php');
            exit;

        } else {

            $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

            header('Location: seo-target-promotion-all-pages.php');
            exit;
        }

    }
} else {

    $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

    header('Location: seo-target-promotion-all-pages.php');
    exit;
}
?>