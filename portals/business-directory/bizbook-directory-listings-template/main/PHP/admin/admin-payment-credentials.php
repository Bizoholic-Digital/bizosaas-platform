<?php
include "header.php";
?>

<?php if($admin_row['admin_payment_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Payment</span>
                <div class="ud-cen-s2">
                     <h2>Payment details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered" id="pg-resu">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Payment type</th>
                                    <th>Details</th>
                                    <th>Currency</th>
									<th>Edit</th>
                                    <th>Status</th>
								</tr>
							</thead>
                        <?php

                       $row_f = getAllFooter();
                        
                        ?>
							<tbody>
								<tr>
                                    <td>1</td>
                                    <td>Cash on delivery</td>
                                    <td><span class="db-list-rat">Free</span></td>
                                    <td><span class="db-list-rat"> - </span></td>
                                    <td><a href="admin-payment-credentials-edit.php?row=cod" class="db-list-edit">Edit</a></td>
                                    <td><span class="db-list-appro"><?php echo $row_f['admin_cod_status']; ?></span></td>
								</tr>
                                <tr>
                                    <td>2</td>
                                    <td>PayPal</td>
                                    <td><span class="db-list-rat"><?php echo $row_f['admin_paypal_id']; ?></span></td>
                                    <td><span class="db-list-rat"><?php echo $row_f['admin_paypal_currency_code']; ?></span></td>
                                    <td><a href="admin-payment-credentials-edit.php?row=paypal" class="db-list-edit">Edit</a></td>
                                    <td><span class="db-list-appro"><?php echo $row_f['admin_paypal_status']; ?></span></td>
								</tr>
                                <tr>
                                    <td>3</td>
                                    <td>Stripe</td>
                                    <td><span class="db-list-rat"><?php echo $row_f['admin_stripe_id']; ?></span></td>
                                    <td><span class="db-list-rat"><?php echo $row_f['admin_stripe_currency_code']; ?></span></td>
                                    <td><a href="admin-payment-credentials-edit.php?row=stripe" class="db-list-edit">Edit</a></td>
                                    <td><span class="db-list-appro"><?php echo $row_f['admin_stripe_status']; ?></span></td>
								</tr>
                                <tr>
                                    <td>4</td>
                                    <td>Razorpay</td>
                                    <td><span class="db-list-rat"><?php echo $row_f['admin_razor_pay_key_id']; ?></span></td>
                                    <td><span class="db-list-rat"><?php echo $row_f['admin_razor_pay_currency_code']; ?></span></td>
                                    <td><a href="admin-payment-credentials-edit.php?row=razor_pay" class="db-list-edit">Edit</a></td>
                                    <td><span class="db-list-appro"><?php echo $row_f['admin_razor_pay_status']; ?></span></td>
								</tr>
                                <tr>
                                    <td>5</td>
                                    <td>Paytm</td>
                                    <td><span class="db-list-rat"><?php echo $row_f['admin_paytm_merchant_id']; ?></span></td>
                                    <td><span class="db-list-rat"><?php echo "INR" ?></span></td>
                                    <td><a href="admin-payment-credentials-edit.php?row=paytm" class="db-list-edit">Edit</a></td>
                                    <td><span class="db-list-appro"><?php echo $row_f['admin_paytm_status']; ?></span></td>
								</tr>
                                <tr>
                                    <td>5</td>
                                    <td>Ozow</td>
                                    <td><span class="db-list-rat"><?php echo $row_f['admin_stripe_id']; ?></span></td>
                                    <td><a href="admin-payment-credentials-edit.php?row=stripe" class="db-list-edit">Edit</a></td>
                                    <td><span class="db-list-appro"><?php echo $row_f['admin_stripe_status']; ?></span></td>
								</tr>
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