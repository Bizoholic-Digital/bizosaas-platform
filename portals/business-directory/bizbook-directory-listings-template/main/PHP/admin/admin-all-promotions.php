<?php
include "header.php";
?>

<?php if($footer_row['admin_listing_show'] != 1 || $admin_row['admin_listing_options'] != 1){
    header("Location: profile.php");
}
?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">All Promotions</span>
                <div class="ud-cen-s2">
                    <h2>All Promotions details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Name</th>
                            <th>Type</th>
                            <th>User</th>
                            <th>Start date</th>
                            <th>End date</th>
                            <th>Duration</th>
                            <th>Status</th>
                            <th>Delete</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllPromoteEnquiry() as $row) {

                            $all_promote_price_id = $row['all_promote_price_id'];
                            $all_promote_enquiry_id = $row['all_promote_enquiry_id'];

                            $promote_type_value = $row['promote_type_value'];

                            $promote_type_id = $row['promote_type_id'];
                            $promote_type_id = $row['promote_type_id'];
                            
                            $user_id = $row['user_id'];

                            $user_details_row = getUser($user_id);

                            $promote_price_value = 1;

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
                                    $activate_url = "admin-promote-now.php?code=$seo_listing_code&&type=listing";
                                    $delete_url = "trash_promotion.php?trash=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV&&code=$all_promote_enquiry_id&&type=listing&&trashh=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV";
                                    ?>
                                    <td><img
                                            src="<?php if ($seo_details_row['profile_image'] != NULL || !empty($seo_details_row['profile_image'])) {
                                                echo "../images/listings/" . $seo_details_row['profile_image'];
                                            } else {
                                                echo "../images/listings/hot4.jpg";
                                            } ?>"><?php echo $seo_details_row['listing_name']; ?>
                                        <span><?php echo dateFormatconverter($seo_details_row['listing_cdt']); ?></span>
                                    </td>
                                    <td><span class="db-list-ststus">Listing</span></td>
                                    <?php
                                }elseif($promote_type_value == 2) {
                                    $seo_details_row = getEvent($promote_type_id);
                                    $activate_url = "admin-promote-now.php?code=$promote_type_id&&&&type=event";
                                    $delete_url = "trash_promotion.php?trash=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV&&code=$all_promote_enquiry_id&&type=event&&trashh=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV";
                                    ?>
                                    <td><img
                                            src="../images/events/<?php echo $seo_details_row['event_image']; ?>"><?php echo $seo_details_row['event_name']; ?>
                                        <span><?php echo dateFormatconverter($seo_details_row['event_cdt']); ?></span>
                                    </td>
                                    <td><span class="db-list-ststus">Events</span></td>
                                    <?php
                                }elseif($promote_type_value == 3) {
                                    $seo_details_row = getBlog($promote_type_id);
                                    $activate_url = "admin-promote-now.php?code=$promote_type_id&&&&type=blog";
                                    $delete_url = "trash_promotion.php?trash=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV&&code=$all_promote_enquiry_id&&type=blog&&trashh=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV";
                                    ?>
                                    <td><img
                                            src="../images/blogs/<?php echo $seo_details_row['blog_image']; ?>"><?php echo $seo_details_row['blog_name']; ?>
                                        <span><?php echo dateFormatconverter($seo_details_row['blog_cdt']); ?></span>
                                    </td>
                                    <td><span class="db-list-ststus">Blogs</span></td>
                                    <?php
                                }elseif($promote_type_value == 4) {
                                    $seo_details_row = getIdProduct($promote_type_id);
                                    $seo_product_code = $seo_details_row["product_code"];
                                    $activate_url = "admin-promote-now.php?code=$seo_product_code&&&&type=product";
                                    $delete_url = "trash_promotion.php?trash=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV&&code=$all_promote_enquiry_id&&type=product&&trashh=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV";
                                    ?>
                                    <td>
                                        <img
                                            src="<?php if ($seo_details_row['gallery_image'] != NULL || !empty($seo_details_row['gallery_image'])) {
                                                echo "../images/products/" . array_shift(explode(',', $seo_details_row['gallery_image']));
                                            } else {
                                                echo "../images/products/hot4.jpg";
                                            } ?>"><?php echo $seo_details_row['product_name']; ?>
                                        <span><?php echo dateFormatconverter($seo_details_row['product_cdt']); ?></span>
                                    </td>
                                    <td><span class="db-list-ststus">Products</span></td>
                                    <?php
                                }
                                ?>
                                <td><?php echo $user_details_row['first_name']; ?></td>

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
                                    if ($current_date > $start_date && $current_date > $end_date){ ?><a href="<?php echo $delete_url; ?>"> <span  style="background-color: #f33d45;" class="db-list-ststus"> Delete <?php }
                                            }

                                                                    ?>
                            </span></a></td>
                            </tr>
                            <?php
                            $si++;
                        }
                        ?>
                        </tbody>
                    </table>
                </div>

            </div>

        </div>
    </div>
</section>
<!-- END -->

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="../js/jquery.min.js"></script>
<script src="../js/popper.min.js"></script>
<script src="../js/bootstrap.min.js"></script>
<script src="../js/jquery-ui.js"></script>
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>