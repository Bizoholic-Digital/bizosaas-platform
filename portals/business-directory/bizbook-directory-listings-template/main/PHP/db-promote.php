<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

include "dashboard_left_pane.php";

if (file_exists('config/general_user_authentication.php')) {
    include('config/general_user_authentication.php');
}

?>
    <!--CENTER SECTION-->
    <div class="ud-main">
   <div class="ud-main-inn ud-no-rhs">
    <div class="ud-cen">
        <div class="log-bor">&nbsp;</div>
        <span class="udb-inst"><?php echo $BIZBOOK['PROMOTE-LISTING-PROMOTIONS']; ?></span>
        <?php include('config/user_activation_checker.php'); ?>
        <div class="ud-cen-s2">
            <h2><?php echo $BIZBOOK['PROMOTE-PROMOTIONS']; ?></h2>
            <?php include "page_level_message.php"; ?>
            <a href="promote-business" class="db-tit-btn"><?php echo $BIZBOOK['PROMOTE-BUSINESS-START-NEW-PROMOTIONS']; ?></a>
            <table class="responsive-table bordered">
                <thead>
                <tr>
                    <th><?php echo $BIZBOOK['S_NO']; ?></th>
                    <th><?php echo $BIZBOOK['LISTING_NAME']; ?></th>
                    <th><?php echo $BIZBOOK['COUPON-START-DATE-PLACEHOLDER']; ?></th>
                    <th><?php echo $BIZBOOK['COUPON-END-DATE-PLACEHOLDER']; ?></th>
                    <th><?php echo $BIZBOOK['DURATION']; ?></th>
                    <th><?php echo $BIZBOOK['STATUS']; ?></th>
                    <th><?php echo $BIZBOOK['DELETE']; ?></th>
                </tr>
                </thead>
                <tbody>
                <?php
                $si = 1;
                $session_user_id = $_SESSION['user_id'];
                
                foreach (getAllUserPromoteEnquiry($session_user_id) as $row) {

                    $all_promote_price_id = $row['all_promote_price_id'];
                    $all_promote_enquiry_id = $row['all_promote_enquiry_id'];

                    $promote_type_value = $row['promote_type_value'];

                    $promote_type_id = $row['promote_type_id'];

                    $user_id = $row['user_id'];

                    $user_details_row = getUser($user_id);

                    $promote_price_value= 1;

                    $start_date = strtotime($row['promote_start_date']);
                    $end_date = strtotime($row['promote_end_date']);
                    $current_date = strtotime(date("Y-m-d"));

                    ?>
                    <tr>
                        <td><?php echo $si; ?></td>
                        <?php
                        if($promote_type_value == 1) {
                            $seo_details_row = getIdListing($promote_type_id);
                            $seo_listing_code = $seo_details_row["listing_code"];
                            $activate_url = "promote-business?code=$seo_listing_code&&type=listing";
                            $delete_url = "promotion_trash?trash=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV&&code=$all_promote_enquiry_id&&type=listing&&trashh=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV";
                            ?>
                            <td><img
                                    src="<?php if ($seo_details_row['profile_image'] != NULL || !empty($seo_details_row['profile_image'])) {
                                        echo "images/listings/" . $seo_details_row['profile_image'];
                                    } else {
                                        echo "images/listings/hot4.jpg";
                                    } ?>"><?php echo $seo_details_row['listing_name']; ?>
                                <span><?php echo dateFormatconverter($seo_details_row['listing_cdt']); ?></span>
                            </td>
                            <?php
                        }elseif($promote_type_value == 2) {
                            $seo_details_row = getEvent($promote_type_id);
                            $activate_url = "promote-business?code=$promote_type_id&&&&type=event";
                            $delete_url = "promotion_trash?trash=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV&&code=$all_promote_enquiry_id&&type=event&&trashh=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV";
                            ?>
                            <td><img
                                    src="images/events/<?php echo $seo_details_row['event_image']; ?>"><?php echo $seo_details_row['event_name']; ?>
                                <span><?php echo dateFormatconverter($seo_details_row['event_cdt']); ?></span>
                            </td>
                            <?php
                        }elseif($promote_type_value == 3) {
                            $seo_details_row = getBlog($promote_type_id);
                            $activate_url = "promote-business?code=$promote_type_id&&&&type=blog";
                            $delete_url = "promotion_trash?trash=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV&&code=$all_promote_enquiry_id&&type=blog&&trashh=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV";
                            ?>
                            <td><img
                                    src="images/blogs/<?php echo $seo_details_row['blog_image']; ?>"><?php echo $seo_details_row['blog_name']; ?>
                                <span><?php echo dateFormatconverter($seo_details_row['blog_cdt']); ?></span>
                            </td>
                            <?php
                        }elseif($promote_type_value == 4) {
                            $seo_details_row = getIdProduct($promote_type_id);
                            $seo_product_code = $seo_details_row["product_code"];
                            $activate_url = "promote-business?code=$seo_product_code&&&&type=product";
                            $delete_url = "promotion_trash?trash=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV&&code=$all_promote_enquiry_id&&type=product&&trashh=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV";
                            ?>
                            <td>
                                <img
                                    src="<?php if ($seo_details_row['gallery_image'] != NULL || !empty($seo_details_row['gallery_image'])) {
                                        echo "images/products/" . array_shift(explode(',', $seo_details_row['gallery_image']));
                                    } else {
                                        echo "images/products/hot4.jpg";
                                    } ?>"><?php echo $seo_details_row['product_name']; ?>
                                <span><?php echo dateFormatconverter($seo_details_row['product_cdt']); ?></span>
                            </td>
                            <?php
                        }
                        ?>
                        <td><?php echo dateFormatconverter($row['promote_start_date']);?></td>
                        <td><?php echo dateFormatconverter($row['promote_end_date']);?></td>
                        <td><?php echo $row['promote_total_days']; ?> Days</td>
                        <td><span class="db-list-ststus"><?php
                                if($promote_price_value == 1){

                                    if ($current_date > $start_date && $current_date > $end_date){ echo "Expired"; }else{ echo "Active"; }
                                }

                                ?>
                                    </span>
                            </br>
                            </br>
                            <?php
                            if($promote_price_value == 1){
                            if ($current_date > $start_date && $current_date > $end_date){ ?><a href="<?php echo $activate_url; ?>"> <span  style="background-color: #4caf50;" class="db-list-ststus"> Activate <?php }
                                    }

                                                            ?>
                            </span></a></td>
                        <td><?php
                            if($promote_price_value == 1){
                            if ($current_date > $start_date && $current_date > $end_date){ ?>
                            <a href="<?php echo $delete_url; ?>">
                                <span  style="background-color: #f33d45;" class="db-list-ststus"> <?php echo $BIZBOOK['DELETE']; ?> </span>
                                </a>
                                <?php
                            }else{
                                ?>
                                <span> - </span>
                                <?php
                            } }   ?>
                            </td>

                    </tr>
                    <?php
                    $si++;
                }
                ?>

                </tbody>
            </table>
        </div>
    </div>
    <!--RIGHT SECTION-->
<?php
include "dashboard_right_pane.php";
?>