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
				<span class="udb-inst">Current running ads</span>
                <div class="ud-cen-s2">
                     <h2>Current Ads</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <table class="responsive-table bordered" id="pg-resu">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Ad Position</th>
                                    <th>Start Date</th>
                                    <th>End Date</th>
                                    <th>Payment cost</th>
                                    <th>Payment Date</th>
                                    <th>Send Invoice</th>
									<th>Edit</th>
                                    <th>Delete</th>
								</tr>
							</thead>
							<tbody>
                            <?php
                            $si = 1;
                            foreach (getAllActiveAdsEnquiry() as $row) {

                            $all_ads_price_id = $row['all_ads_price_id'];

                            $user_id = $row['user_id'];

                            $user_details_row = getUser($user_id);

                            $ads_price_details_row = getAdsPrice($all_ads_price_id);

                            ?>
								<tr>
                                    <td><?php echo $si; ?></td>
                                    <td><?php echo $ads_price_details_row['ad_price_name']; ?></td>
                                    <td><?php echo dateFormatconverter($row['ad_start_date']);?></td>
                                    <td><?php echo dateFormatconverter($row['ad_end_date']);?></td>
                                    <td><?php echo $footer_row['currency_symbol']; ?><?php echo $row['ad_total_cost']; ?></td>
                                    <td><?php echo dateFormatconverter($row['ad_enquiry_cdt']);?></td>
									<td><a href="admin-invoice-create.php" class="db-list-rat">Send</a></td>
                                    <td><a href="admin-ads-edit.php?row=<?php echo $row['all_ads_enquiry_id']; ?>&path=1" class="db-list-edit">Edit</a></td>
                                    <td><a href="admin-ads-delete.php?row=<?php echo $row['all_ads_enquiry_id']; ?>&path=1" class="db-list-edit">Delete</a></td>
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