<?php
include "header.php";
?>

<?php if($footer_row['admin_coupon_show'] !=1 || $admin_row['admin_feedback_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <?php
            $coupon_row_code = $_GET['row'];
            $coupon_row = getCoupon($coupon_row_code);
            ?>
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Coupon used users</span>
                <div class="ud-cen-s2">
                    <h2><?php echo $coupon_row['coupon_name']; ?> - Coupon access users</h2>
                    <?php include "../page_level_message.php"; ?>
                    <a href="admin-add-new-coupons.php" class="db-tit-btn">Add new Coupons</a>
                    <table class="responsive-table bordered">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Name</th>
									<th>Email</th>
                                    <th>Phone</th>
									<th>View profile</th>
								</tr>
							</thead>
							<tbody>
                            <?php
                            $si = 1;
                            $coupon_use_members = $coupon_row['coupon_use_members'];
                            $array_new = explode(',',$coupon_use_members);

                            foreach ($array_new as $array1) {
                                $user_coupo_details_row = getUser($array1);
                                ?>
                                <tr>
                                    <td><?php echo $si; ?></td>
                                    <td><?php echo $user_coupo_details_row['first_name'];?>
                                        <span><?php echo dateFormatconverter($user_coupo_details_row['user_cdt']); ?></span>
                                    </td>
                                    <td><?php echo $user_coupo_details_row['email_id']; ?></td>
                                    <td><?php echo $user_coupo_details_row['mobile_number']; ?></td>
                                    <td><a href="<?php echo $PROFILE_URL.urlModifier($user_coupo_details_row['user_slug']); ?>" target="_blank"  class="db-list-edit">Profile</a></td>
                                </tr>
                                <?php
                            }
                            $si++;
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