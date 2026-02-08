<?php
//database configuration
if (file_exists('config/info.php')) {
    include('config/info.php');
}
session_start();

if (isset($_REQUEST['scheck']) && isset($_REQUEST['cat_check']) && isset($_REQUEST['sub_cat_check']) && isset($_REQUEST['feature_check']) && isset($_REQUEST['city_check']) && isset($_REQUEST['rating_check'])) {
    $_SESSION['scheck'] = $_REQUEST['scheck'];
    $_SESSION['cat_check'] = $_REQUEST['cat_check'];
    $_SESSION['sub_cat_check'] = $_REQUEST['sub_cat_check'];
    $_SESSION['feature_check'] = $_REQUEST['feature_check'];
    $_SESSION['city_check'] = $_REQUEST['city_check'];
    $_SESSION['rating_check'] = $_REQUEST['rating_check'];
}

$scheck = $_SESSION['scheck'];
$cat_check = $_SESSION['cat_check'];
$sub_cat_check = $_SESSION['sub_cat_check'];
$feature_check = $_SESSION['feature_check'];
$city_check = $_SESSION['city_check'];
$rating_check = $_SESSION['rating_check'];


if ($scheck == NULL && $cat_check == NULL && $sub_cat_check == NULL && $feature_check == NULL && $city_check == NULL && $rating_check == NULL) {
    $sql = getAllListing();
} else {

    $WHERE = array();
    $inner = $w = '';

// Category Check starts
    if (!empty($cat_check)) {
        if (strstr($cat_check, ',')) {
            $data2 = explode(',', $cat_check);
            $cat_array = array();
            foreach ($data2 as $c) {
//            $cat_array[] = "t1.category_id = $c";
                $cat_array[] = "FIND_IN_SET($c,t1.category_id)";

            }
            $WHERE[] = '(' . implode(' OR ', $cat_array) . ')';
        } else {
//        $WHERE[] = '(t1.category_id = ' . $cat_check . ')';
            $WHERE[] = '(FIND_IN_SET(' . $cat_check . ',t1.category_id))';

        }
    }

// Category Check Ends


//Sub Category Check starts
    if (!empty($sub_cat_check)) {
        if (strstr($sub_cat_check, ',')) {
            $data2 = explode(',', $sub_cat_check);
            $sub_cat_array = array();
            foreach ($data2 as $c) {
//            $sub_cat_array[] = "t1.sub_category_id = $c";
                $sub_cat_array[] = "FIND_IN_SET($c,t1.sub_category_id)";

            }
            $WHERE[] = '(' . implode(' OR ', $sub_cat_array) . ')';
        } else {
//        $WHERE[] = '(t1.category_id = ' . $sub_cat_check . ')';
            $WHERE[] = '(FIND_IN_SET(' . $sub_cat_check . ',t1.sub_category_id))';

        }
    }

//Sub Category Check Ends

//City Check starts
    if (!empty($city_check)) {

        if (strstr($city_check, ',')) {
            $data8 = explode(',', $city_check);
            $cityarray = array();
            foreach ($data8 as $ci) {
                $cityarray[] = "FIND_IN_SET($ci,t1.city_id)";

            }
            $WHERE[] = '(' . implode(' OR ', $cityarray) . ')';
        } else {
//        $WHERE[] = '(t1.category_id = ' . $cat_check . ')';
            $WHERE[] = '(FIND_IN_SET(' . $city_check . ',t1.city_id))';

        }

    }

//City Check Ends


//Rating Check Starts

    if (!empty($rating_check)) {
        if (strstr($rating_check, ',')) {
            $data3 = explode(',', $rating_check);
            $rate_array = array();
            foreach ($data3 as $c) {
                $rate_array[] = "t2.price_rating = $c";
            }
            $WHERE[] = '(' . implode(' OR ', $rate_array) . ')';
        } else {
            $WHERE[] = '(t2.price_rating = ' . $rating_check . ')';
        }

        $inner = "INNER JOIN `" . TBL . "reviews` AS t2 ON t1.listing_id = t2.listing_id";

    }

//Rating Check Ends

    if (!empty($price_range)) {
        $data3 = explode('-', $price_range);
        $WHERE[] = "(t1.product_rate between $data3[0] and $data3[1])";
    }

//if(!empty($bcheck)) {
//    if(strstr($bcheck,',')) {
//        $data1 = explode(',',$bcheck);
//        $barray = array();
//        foreach($data1 as $c) {
//            $barray[] = "t1.Brand = $c";
//        }
//        $WHERE[] = '('.implode(' OR ',$barray).')';
//    } else {
//        $WHERE[] = '(t1.Brand = '.$bcheck.')';
//    }
//}


    if (!empty($scheck)) {
        if (strstr($scheck, ',')) {
            $data3 = explode(',', $scheck);
            $sarray = array();
            foreach ($data3 as $c) {
                $sarray[] = "t2.size_id = $c";
            }
            $WHERE[] = '(' . implode(' OR ', $sarray) . ')';
        } else {
            $WHERE[] = '(t2.size_id = ' . $scheck . ')';
        }

        $inner = 'INNER JOIN `product_size_quantity` AS t2 ON t1.product_id = t2.product_id';

    }

    if (!empty($category_id)) {
        if (strstr($category_id, ',')) {
            $data4 = explode(',', $category_id);
            $ctarray = array();
            foreach ($data4 as $ct) {
                $ctarray[] = "t1.product_category_id = $ct";
            }
            $WHERE[] = '(' . implode(' OR ', $ctarray) . ')';
        } else {
            $WHERE[] = '(t1.product_category_id = ' . $category_id . ')';
        }
    }

    $w = implode(' AND ', $WHERE);
    if (!empty($w)) {
        $w = 'WHERE ' . $w;
        $q = 'AND ';
    } else {
        $q = 'WHERE ';
    }

    $sql = mysqli_query($conn, "SELECT DISTINCT  t1 . * FROM  " . TBL . "listings  AS t1 $inner $w $q listing_status= 'Active' AND listing_is_delete != '2' ORDER BY listing_id DESC ");

}
function parseToXML($htmlStr)
{
    $xmlStr = str_replace('<', '&lt;', $htmlStr);
    $xmlStr = str_replace('>', '&gt;', $xmlStr);
    $xmlStr = str_replace('"', '&quot;', $xmlStr);
    $xmlStr = str_replace("'", '&#39;', $xmlStr);
    $xmlStr = str_replace("&", '&amp;', $xmlStr);
    return $xmlStr;
}

header("Content-type: text/xml");
if(mysqli_num_rows($sql) <= 0){
    echo 1;
}else {

// Start XML file, echo parent node
    echo "<?xml version='1.0' ?>";
    echo '<markers>';
    $ind = 0;
    $flag = 0;

    while ($row = mysqli_fetch_array($sql)) {

        // Add to XML document node
        echo '<marker ';
        echo 'id="' . $row['listing_id'] . '" ';
        echo 'code="' . $row['listing_code'] . '" ';
        echo 'name="' . parseToXML($row['listing_name']) . '" ';
        echo 'slug="' . parseToXML($row['listing_slug']) . '" ';
        echo 'address="' . parseToXML($row['listing_address']) . '" ';
        echo 'lat="' . $row['listing_lat'] . '" ';
        echo 'lng="' . $row['listing_lng'] . '" ';
        echo 'type="' . $row['listing_type'] . '" ';
        echo 'image="' . $row['profile_image'] . '" ';
        echo '/>';
        $ind = $ind + 1;
    }

// End XML file
    echo '</markers>';
}
?>