<?php
include "header.php";
?>

<?php if($admin_row['admin_listing_price_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Pricing details</span>
                <div class="ud-cen-s2">
                     <h2>Pricing Plans</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered" id="pg-resu">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Plan name</th>
                                    <th>Price</th>
                                    <th>Status</th>
									<th>Edit</th>

								</tr>
							</thead>
							<tbody>
                            <?php
                            $si = 1;
                            foreach (getAllPlanType() as $plan_type_row) {
                                ?>
                                <tr>
                                    <td><?php echo $si; ?></td>
                                    <td><?php echo $plan_type_row['plan_type_name']; ?></td>
                                    <td><span class="db-list-rat"><?php if($plan_type_row['plan_type_price'] == 0){
                                                echo "Free";
                                            }else{
                                                echo $footer_row['currency_symbol'].''.$plan_type_row['plan_type_price'];
                                            }  ?></span></td>
                                    <td><span class="db-list-appro">Active</span></td>
                                    <td><a href="admin-price-edit.php?row=<?php echo $plan_type_row['plan_type_id']; ?>" class="db-list-edit">Edit</a></td>

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