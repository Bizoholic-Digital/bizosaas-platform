<?php
include "header.php";
?>

<?php if($admin_row['admin_ads_options'] != 1){
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Ad Request & Enquiry</span>
                <div class="ud-cen-s2 ad-table-inn">
                    <h2>Ad Request</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>User Name</th>
                            <th>Ad Position</th>
                            <th>Start date</th>
                            <th>End date</th>
                            <th>Image</th>
                            <th>Ad Days</th>
                            <th>Ad Cost</th>
                            <th>Status</th>
                            <th>Edit</th>
                            <th>Delete</th>
                            <th>Approve</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllInactiveAdsEnquiry() as $row) {

                            $all_ads_price_id = $row['all_ads_price_id'];

                            $user_id = $row['user_id'];

                            $user_details_row = getUser($user_id);
                            
                            $ads_price_details_row = getAdsPrice($all_ads_price_id);

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><a href="admin-user-full-details.php?row=<?php echo $user_details_row['user_id'];   ?>"><img src="../images/user/<?php echo $user_details_row['profile_image'];   ?>" alt=""><?php
                                     echo $user_details_row['first_name'];   ?><span>Join: <?php echo dateFormatconverter($user_details_row['user_cdt']);?></span></a></td>
                                <td><?php echo $ads_price_details_row['ad_price_name']; ?> (<?php echo $row['ad_cost_per_day']; ?><?php echo $footer_row['currency_symbol']; ?>/per day)</td>
                                <td><?php echo dateFormatconverter($row['ad_start_date']);?></td>
                                <td><?php echo dateFormatconverter($row['ad_end_date']);?></td>
                                <td><img src="../images/ads/<?php echo $row['ad_enquiry_photo']; ?>" alt=""></td>
                                <td><?php echo $row['ad_total_days']; ?></td>
                                <td><span class="db-list-rat"><?php echo $footer_row['currency_symbol']; ?><?php echo $row['ad_total_cost']; ?></span></td>
                                <td><a href="#!" class="db-list-appro"><?php echo $row['ad_enquiry_status']; ?></a></td>
                                <td><a href="admin-ads-edit.php?row=<?php echo $row['all_ads_enquiry_id']; ?>" class="db-list-edit">Edit</a></td>
                                <td><a href="admin-ads-delete.php?row=<?php echo $row['all_ads_enquiry_id']; ?>" class="db-list-edit">Delete</a></td>
                                <td><a href="admin-ads-approve.php?adsstatusadsstatusadsstatusadsstatusadsstatus=<?php echo $row['all_ads_enquiry_id']; ?>" class="db-list-appro">Approve this</a></td>
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