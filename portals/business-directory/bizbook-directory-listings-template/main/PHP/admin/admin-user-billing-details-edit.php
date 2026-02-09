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
                 <div class="ud-cen-s2 ud-pro-edit">
                    <h2>Billing details</h2>
                     <?php include "../page_level_message.php"; ?>
                     <?php
                     $user_id = $_GET['row'];
                     $user_details_row = getUser($user_id);
                     ?>
                    <table class="responsive-table bordered">
                        <form name="billing_form" id="billing_form" method="post"
                              action="update_billing.php">

                            <input type="hidden" name="user_id"
                                   class="form-control"
                                   value="<?php echo $user_id; ?>"
                                   placeholder="Country">
                            
							<tbody>
                                <tr>
                                    <td>Full name</td>
									<td>
                                        <div class="form-group">
                                          <input type="text" class="form-control" readonly="readonly" value="<?php echo $user_details_row['first_name']; ?>">
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>Country</td>
									<td>
                                        <div class="form-group">
                                          <input type="text" name="user_country"
                                                 class="form-control"
                                                 value="<?php echo $user_details_row['user_country']; ?>"
                                                 placeholder="Country">
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>State</td>
									<td>
                                        <div class="form-group">
                                          <input type="text" name="user_state"
                                                 class="form-control"
                                                 value="<?php echo $user_details_row['user_state']; ?>"
                                                 placeholder="State">
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>City</td>
									<td>
                                        <div class="form-group">
                                          <input type="text" name="user_city"
                                                 class="form-control"
                                                 value="<?php echo $user_details_row['user_city']; ?>"
                                                 placeholder="City *">
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>Village & Street details</td>
									<td>
                                        <div class="form-group">
                                          <input type="text" name="user_address"
                                                 class="form-control"
                                                 value="<?php echo $user_details_row['user_address']; ?>"
                                                 placeholder="Village & Street name">
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>Postcode/Zip</td>
									<td>
                                        <div class="form-group">
                                          <input type="text" name="user_zip_code"
                                                 onkeypress="return isNumber(event)"
                                                 class="form-control"
                                                 value="<?php echo $user_details_row['user_zip_code']; ?>"
                                                 placeholder="Postcode/ZIP">
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>Contact person</td>
									<td>
                                        <div class="form-group">
                                          <input type="text" class="form-control"
                                                 name="user_contact_name"
                                                 value="<?php echo $user_details_row['user_contact_name']; ?>"
                                                 placeholder="Contact person *">
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>Contact no</td>
									<td>
                                        <div class="form-group">
                                          <input type="text" class="form-control"
                                                 name="user_contact_mobile"
                                                 onkeypress="return isNumber(event)"
                                                 value="<?php echo $user_details_row['user_contact_mobile']; ?>"
                                                 placeholder="Contact number">
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>Contact email</td>
									<td>
                                        <div class="form-group">
                                          <input class="form-control"
                                                 name="user_contact_email"
                                                 value="<?php echo $user_details_row['user_contact_email']; ?>"
                                                 placeholder="Contact email">
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>
                                        <button type="submit" name="billing_submit" class="db-pro-bot-btn">Submit My Changes</button>
                                    </td>
									<td></td>
								</tr>
							</tbody>
                            </form>
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