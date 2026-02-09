<?php
include "header.php";
?>
<?php if ($footer_row['admin_coupon_show'] != 1){
    header("Location: profile.php");
}
?>
<?php if($admin_row['admin_feedback_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Coupons and deals</span>
                <div class="ud-cen-s2">
                    <h2>All Coupons details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <a href="admin-add-new-coupons.php" class="db-tit-btn">Add new Coupons</a>
                    <table class="responsive-table bordered">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Coupon Name</th>
									<th>Coupon Code</th>
                                    <th>Created by</th>
                                    <th>Expiry date</th>
									<th>Views</th>
									<th>Viewers list</th>
                                    <th>Edit</th>
									<th>Delete</th>
								</tr>
							</thead>
							<tbody>
                            <?php
                            $si = 1;
                            foreach (getAllActiveCoupons() as $couponrow) {

                            $user_id = $couponrow['coupon_user_id'];

                            $user_details_row = getUser($user_id);

                            ?>
								<tr>
                                    <td><?php echo $si; ?></td>
                                    <td><?php echo $couponrow['coupon_name']; ?><span><?php echo dateFormatconverter($couponrow['coupon_cdt']); ?></span></td>
                                    <td><?php echo $couponrow['coupon_code']; ?></td>
                                    <td><a href="<?php echo $PROFILE_URL.urlModifier($user_details_row['user_slug']); ?>" class="db-list-ststus" target="_blank"><?php echo $user_details_row['first_name']; ?></a></td>
                                    <td><?php echo dateFormatconverter($couponrow['coupon_end_date']); ?></td>
                                    <td><span class="db-list-rat"><?php echo coupon_pageview_count($couponrow['coupon_id']); ?></span></td>
                                    <td><a href="admin-coupons-viewers.php?row=<?php echo $couponrow['coupon_id']; ?>" class="db-list-edit">View</a></td>
                                    <td><a href="admin-edit-coupons.php?row=<?php echo $couponrow['coupon_id']; ?>" class="db-list-edit">Edit</a></td>
                                    <td><a href="admin-delete-coupons.php?row=<?php echo $couponrow['coupon_id']; ?>" class="db-list-edit">Delete</a></td>
								</tr>
                                <?php
                                $si++;
                            }
                            ?>

							</tbody>
						</table>
                </div>

            </div>
                <div class="ad-pgnat">
                    <ul class="pagination">
                      <li class="page-item"><a class="page-link" href="#">Previous</a></li>
                      <li class="page-item active"><a class="page-link" href="#">1</a></li>
                      <li class="page-item"><a class="page-link" href="#">2</a></li>
                      <li class="page-item"><a class="page-link" href="#">3</a></li>
                      <li class="page-item"><a class="page-link" href="#">Next</a></li>
                    </ul>
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