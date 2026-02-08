<?php
include "header.php";
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">User Billing Details</span>
                 <div class="ud-cen-s2 ud-sp">
                    <h2>Billing profile details</h2>
                     <?php include "../page_level_message.php"; ?>
                     <?php
                     $user_id = $_GET['row'];
                     $user_details_row = getUser($user_id);
                     ?>
                    <a href="admin-user-billing-details-edit.php?row=<?php echo $user_id; ?>" class="db-tit-btn">Edit this billing</a>
                    <table class="responsive-table bordered">
							<tbody>
                                <tr>
                                    <td>Full name</td>
									<td><?php echo $user_details_row['first_name']; ?></td>
								</tr>
                                <tr>
                                    <td>Country</td>
									<td><?php echo $user_details_row['user_country']; ?></td>
								</tr>
                                <tr>
                                    <td>State</td>
									<td><?php echo $user_details_row['user_state']; ?></td>
								</tr>
                                <tr>
                                    <td>City</td>
									<td><?php echo $user_details_row['user_city']; ?></td>
								</tr>
                                <tr>
                                    <td>Village & Street details</td>
									<td><?php echo $user_details_row['user_address']; ?></td>
								</tr>
                                <tr>
                                    <td>Postcode/Zip</td>
									<td><?php echo $user_details_row['user_zip_code']; ?></td>
								</tr>
                                <tr>
                                    <td>Contact person</td>
									<td><?php echo $user_details_row['user_contact_name']; ?></td>
								</tr>
                                <tr>
                                    <td>Contact no</td>
									<td><?php echo $user_details_row['user_contact_mobile']; ?></td>
								</tr>
                                <tr>
                                    <td>Contact email</td>
									<td><?php echo $user_details_row['user_contact_email']; ?></td>
								</tr>
							</tbody>
						</table>
                     
                     <div class="ud-notes">
                         <p><b>Notes about this user:</b> <span contenteditable="true">Click here to write short notes or conversation with this user.(Ex: I spoke him to discuss about advantage of Premium Plan on April 12th 2020.)</span></p>
                    </div>
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