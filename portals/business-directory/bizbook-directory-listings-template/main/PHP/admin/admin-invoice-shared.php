<?php
include "header.php";
?>
<?php if ($admin_row['admin_invoice_options'] != 1) {
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Sent Invoices</span>
                <div class="ud-cen-s2">
                    <h2>Your shared Invoices</h2>
                    <?php include "../page_level_message.php"; ?>
                    <a href="admin-invoice-create.php" class="db-tit-btn">Create new invoice</a>
                    <table class="responsive-table bordered">
							<thead>
								<tr>
									<th>No</th>
                                    <th>User Name</th>
									<th>Plan type</th>
                                    <th>Amount</th>
									<th>Delete</th>
                                    <th>Download Invoice</th>
								</tr>
							</thead>
							<tbody>
                            <?php
                            $si = 1;
                            $session_user_id = $_SESSION['user_id'];
                            foreach (getAllTransaction() as $row) {

                            $transaction_plan_type_id = $row['plan_type_id'];
                            $transaction_user_plan_type = getPlanType($transaction_plan_type_id);
                            $user_details_row = getUser($row['user_id']);

                            ?>
								<tr>
                                    <td><?php echo $si; ?></td>
                                    <td><img src="../images/user/<?php if(($user_details_row['profile_image'] == NULL) || empty($user_details_row['profile_image'])){  echo $footer_row['user_default_image'];}else{ echo $user_details_row['profile_image']; } ?>" alt=""><?php echo $user_details_row['first_name']; ?> <span>Send on: <?php echo dateFormatconverter($row['transaction_cdt']); ?></span></td>
									<td><span class="db-list-rat"><?php echo $transaction_user_plan_type['plan_type_name']; ?></span></td>
                                    <td><span class="db-list-rat"><?php echo $footer_row['currency_symbol'] . '' . $row['transaction_amount']; ?></span></td>
									<td><span class="db-list-edit">Delete</span></td>
                                    <td><a href="../images/invoices/<?php echo $row['transaction_invoice']; ?>" download="<?php echo $user_details_row['first_name']; ?>-Invoice-<?php echo strtotime($row['transaction_cdt']); ?>" class="db-list-edit">Download</a></td>
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