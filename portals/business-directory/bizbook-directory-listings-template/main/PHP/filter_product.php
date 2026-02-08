<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */


if (file_exists('config/info.php')) {
    include('config/info.php');
}
if (isset($_SESSION['user_id'])) {
    $session_user_id = $_SESSION['user_id'];
}
$user_details_row = getUser($session_user_id); //Fetch User data

//Pagination Code Starts Here
$numberOfPages = 8;
$limit = 15;
if (isset($_GET["page"])) {
    $page = $_GET["page"];
} else {
    $page = 1;
};
$start_from = ($page - 1) * $limit;

//Pagination Code Ends Here


$scheck = $_REQUEST['scheck'];
$cat_check = $_REQUEST['cat_check'];
$sub_cat_check = $_REQUEST['sub_cat_check'];
$price_check = $_REQUEST['price_check'];
$city_check = $_REQUEST['city_check'];
$discount_check = $_REQUEST['discount_check'];


$WHERE = array();
$inner = $w = '';

// Category Check starts
if (!empty($cat_check)) {
    if (strstr($cat_check, ',')) {
        $data2 = explode(',', $cat_check);
        $cat_array = array();
        foreach ($data2 as $c) {
            $cat_array[] = "FIND_IN_SET($c,t1.category_id)";

        }
        $WHERE[] = '(' . implode(' OR ', $cat_array) . ')';
    } else {
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
            $sub_cat_array[] = "FIND_IN_SET($c,t1.sub_category_id)";

        }
        $WHERE[] = '(' . implode(' OR ', $sub_cat_array) . ')';
    } else {
        $WHERE[] = '(FIND_IN_SET(' . $sub_cat_check . ',t1.sub_category_id))';

    }
}

//Sub Category Check Ends

//Price Check starts
if (!empty($price_check)) {

    if (strstr($price_check, ',')) {
        $data8 = explode(',', $price_check);
        $cityarray = array();
        foreach ($data8 as $ci) {
            if($ci == 100){
                $start_price = 0;
                $end_price = 100;
            }elseif($ci == 250){
                $start_price = 101;
                $end_price = 250;
            }elseif($ci == 500){
                $start_price = 251;
                $end_price = 500;
            }elseif($ci == 1000){
                $start_price = 501;
                $end_price = 1000;
            }else{
                $start_price = 1001;
                $end_price = 100000;
            }
            $cityarray[] = "t1.product_price BETWEEN $start_price AND $end_price";

        }
        $WHERE[] = '(' . implode(' OR ', $cityarray) . ')';
    } else {

        if($price_check == 100){
            $start_price = 0;
            $end_price = 100;
        }elseif($price_check == 250){
            $start_price = 101;
            $end_price = 250;
        }elseif($price_check == 500){
            $start_price = 251;
            $end_price = 500;
        }elseif($price_check == 1000){
            $start_price = 501;
            $end_price = 1000;
        }else{
            $start_price = 1001;
            $end_price = 100000;
        }
        $WHERE[] = '(t1.product_price BETWEEN ' . $start_price . ' AND ' . $end_price . ')';

    }

}

//Price Check Ends

//Discount Check starts
if (!empty($discount_check)) {

    if (strstr($discount_check, ',')) {
        $data63 = explode(',', $discount_check);
        $discountarray = array();
        foreach ($data63 as $dis) {
            if($dis == 10){
                $start_discount = 0;
                $end_discount = 10;
            }elseif($dis == 25){
                $start_discount = 11;
                $end_discount = 25;
            }elseif($dis == 50){
                $start_discount = 26;
                $end_discount = 50;
            }elseif($dis == 70){
                $start_discount = 51;
                $end_discount = 70;
            }else{
                $start_discount = 100;
                $end_discount = 100000;
            }
            $discountarray[] = "t1.product_price_offer BETWEEN $start_discount AND  $end_discount";

        }
        $WHERE[] = '(' . implode(' OR ', $discountarray) . ')';
    } else {

        if($discount_check == 10){
            $start_discount = 0;
            $end_discount = 10;
        }elseif($discount_check == 25){
            $start_discount = 11;
            $end_discount = 25;
        }elseif($discount_check == 50){
            $start_discount = 26;
            $end_discount = 50;
        }elseif($discount_check == 70){
            $start_discount = 51;
            $end_discount = 70;
        }else{
            $start_discount = 100;
            $end_discount = 100000;
        }
//        $WHERE[] = '(t1.category_id = ' . $cat_check . ')';
        $WHERE[] = '(t1.product_price_offer BETWEEN ' . $start_discount . ' AND  ' . $end_discount . ')';

    }

}

//Price Check Ends


if (!empty($price_range)) {
    $data3 = explode('-', $price_range);
    $WHERE[] = "(t1.product_rate between $data3[0] and $data3[1])";
}

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
$footer_row = getAllFooter();

$query = mysqli_query($conn, "SELECT DISTINCT  t1 . * FROM  " . TBL . "products  AS t1 $inner $w $q product_status= 'Active' ORDER BY product_id DESC ");
?>

<div class="all-list-sh all-product-total">
    <ul class="products-wrapper">
        <?php
        if (mysqli_num_rows($query) > 0) {

            while ($productrow = mysqli_fetch_array($query)) {

                $product_id = $productrow['product_id'];
                $list_user_id = $productrow['user_id'];

                $usersqlrow = getUser($list_user_id); // To Fetch particular User Data

                ?>

                <li class="products-item">
                    <div class="all-pro-box">
                        <div class="all-pro-img">
                            <img src="<?php echo $webpage_full_link; ?><?php if ($productrow['gallery_image'] != NULL || !empty($productrow['gallery_image'])) {
                                echo "images/products/" . array_shift(explode(',', $productrow['gallery_image']));
                            } else {
                                echo "images/products/hot4.jpg";
                            } ?>">
                        </div>
                        <div class="all-pro-aut">
                            <div class="auth">
                                <?php
                                //To Check whether listing owner made profile is visible

                                $setting_profile_show = $usersqlrow['setting_profile_show'];
                                if ($setting_profile_show == 0) {

                                    ?>
                                    <img
                                        src="<?php echo $webpage_full_link; ?>images/user/<?php if (($usersqlrow['profile_image'] == NULL) || empty($usersqlrow['profile_image'])) {
                                            echo $footer_row['user_default_image'];
                                        } else {
                                            echo $usersqlrow['profile_image'];
                                        } ?>" alt="">
                                    <a target="_blank"
                                       href="<?php echo $PROFILE_URL.urlModifier($usersqlrow['user_slug']); ?>"
                                       class="fclick"></a>
                                    <?php
                                }
                                ?>
                            </div>
                        </div>
                        <div class="all-pro-txt">
                            <h4><?php echo $productrow['product_name']; ?></h4>
                                                <span class="pri"><b class="pro-off"><?php echo $footer_row['currency_symbol']; ?><?php echo $productrow['product_price']; ?></b>
                                                    <?php if ($productrow['product_price_offer'] != NULL) { ?>
                                                        <?php echo $productrow['product_price_offer']; ?>% off<?php } ?>
                                                </span>
                            <div class="links">
                                <?php if ($session_user_id != NULL || !empty($session_user_id)) {
                                    ?>
                                    <a href="#" data-toggle="modal"
                                        <?php
                                        if ($list_user_id != 1) { ?>
                                            data-target="#quote<?php echo $product_id ?>"
                                            <?php
                                        }
                                        ?>><?php echo $BIZBOOK['LEAD-GET-QUOTE']; ?></a>
                                    <?php
                                } else { ?>
                                    <?php
                                }
                                ?>

                            </div>
                        </div>
                        <a href="<?php echo $PRODUCT_URL.urlModifier($productrow['product_slug']); ?>" class="pro-view-full"></a>
                    </div>
                </li>


                <!--  Get Quote Pop up box starts  -->
                <section>
                    <div class="pop-ups pop-quo">
                        <!-- The Modal -->
                        <div class="modal fade" id="quote<?php echo $product_id ?>">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="log-bor">&nbsp;</div>
                                    <span class="udb-inst"><?php echo $BIZBOOK['LEAD-SEND-ENQUIRY']; ?></span>
                                    <button type="button" class="close"
                                            data-dismiss="modal">&times;</button>
                                    <!-- Modal Header -->
                                    <div class="quote-pop">
                                        <h4><?php echo $BIZBOOK['LEAD-GET-QUOTE']; ?></h4>
                                        <div id="enq_success" style="display: none;color: #000;"><?php echo $BIZBOOK['ENQUIRY_SUCCESSFUL_MESSAGE']; ?></div>
                                        <div id="enq_fail" style="display: none;color: #000;"><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></div>
                                        <form method="post" name="all_product_enquiry_form" class="all_product_enquiry_form">
                                            <input type="hidden" class="form-control" name="product_id"
                                                   value="<?php echo $product_id ?>"
                                                   placeholder=""
                                                   required>
                                            <input type="hidden" class="form-control"
                                                   name="product_user_id"
                                                   value="<?php echo $list_user_id; ?>" placeholder=""
                                                   required>
                                            <input type="hidden" class="form-control"
                                                   name="enquiry_sender_id"
                                                   value="<?php echo $session_user_id; ?>"
                                                   placeholder=""
                                                   required>
                                            <div class="form-group">
                                                <input type="text"  name="enquiry_name"
                                                       value="<?php echo $user_details_row['first_name'] ?>"
                                                       required="required" class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>">
                                            </div>
                                            <div class="form-group">
                                                <input type="email" class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>" 
                                                       value="<?php echo $user_details_row['email_id'] ?>"
                                                       name="enquiry_email"
                                                       pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                                       title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>" required>
                                            </div>
                                            <div class="form-group">
                                                <input type="text" class="form-control"
                                                       value="<?php echo $user_details_row['mobile_number'] ?>"
                                                       name="enquiry_mobile"
                                                       placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>"
                                                       pattern="[7-9]{1}[0-9]{9}"
                                                       title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>"
                                                       required>
                                            </div>
                                            <div class="form-group">
                                <textarea class="form-control" rows="3" name="enquiry_message"
                                          placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                                            </div>
                                            <input type="hidden" id="source">
                                            <button type="submit" id="all_product_enquiry_submit" name="enquiry_submit" class="all_product_enquiry_submit btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?>
                                            </button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
                <!--  Get Quote Pop up box ends  -->


                <?php
            }
        } else {
            ?>
            <span style="    font-size: 21px;
    color: #bfbfbf;
    letter-spacing: 1px;
    /* background: #525252; */
    text-shadow: 0px 0px 2px #fff;
    text-transform: uppercase;
    margin-top: 5%;"><?php echo $BIZBOOK['PRODUCTS_NO_PRODUCTS_MESSAGE']; ?></span>
            <?php
        }
        ?>

    </ul>
    <div id="product-pagination-container"></div>
</div>

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link ='<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url ='<?php echo $LOGIN_URL;?>';</script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>js/product_filter.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>
<script src="<?php echo $slash; ?>js/jquery.simplePagination.min.js"></script>
<script>
    function products_paginate() {
        var items = $(".products-wrapper .products-item");
        var numItems = items.length;
        var perPage = 20;

        items.slice(perPage).hide();

        $('#product-pagination-container').pagination({
            items: numItems,
            itemsOnPage: perPage,
            prevText: "&laquo;",
            nextText: "&raquo;",
            onPageClick: function (pageNumber) {
                var showFrom = perPage * (pageNumber - 1);
                var showTo = showFrom + perPage;
                items.hide().slice(showFrom, showTo).show();
            }
        });
        return true;
    }
</script>