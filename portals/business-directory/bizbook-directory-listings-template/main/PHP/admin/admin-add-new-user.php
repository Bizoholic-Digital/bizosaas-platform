<?php
include "header.php";
?>

<?php if($admin_row['admin_user_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Add new user</span>
                 <div class="ud-cen-s2 ud-pro-edit">
                    <h2>User details</h2>
                     <?php include "../page_level_message.php"; ?>
                     <form name="register_form" id="register_form" method="post" action="../register_update.php" enctype="multipart/form-data" class="">
                         
                         <input type="hidden" autocomplete="off" name="trap_box" id="trap_box" class="validate">
                         <input type="hidden" autocomplete="off" name="mode_path" value="XeBaCk_MoDeX_PATHXHU" id="mode_path" class="validate">

                         <table class="responsive-table bordered">
							<tbody>
								<tr>
                                    <td>Name</td>
									<td>
                                        <div class="form-group">
                                          <input type="text" required="required" autocomplete="off" name="first_name" id="first_name" class="form-control">
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>Email id</td>
                                    <td>
                                        <div class="form-group">
                                            <input type="email" required="required" autocomplete="off" name="email_id" id="email_id" class="form-control" >
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Pofile password</td>
                                    <td>
                                        <div class="form-group">
                                            <input type="text" autocomplete="off" required="required" name="password" id="password" class="form-control" >
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Mobile number</td>
                                    <td>
                                        <div class="form-group">
                                            <input type="text" required="required" autocomplete="off" name="mobile_number" id="mobile_number" class="form-control">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Profile picture</td>
                                    <td>
                                        <div class="form-group">
                                            <input type="file" name="profile_image" class="form-control">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Address</td>
                                    <td>
                                        <div class="form-group">
                                            <input type="text" class="form-control" name="user_address">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>User type</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="user_type" required="required" id="user_type" class="chosen-select form-control ca-check-plan">
                                                <option value="">User type</option>
                                                <option value="General">General user</option>
                                                <option value="Service provider">Service provider</option>
                                            </select>
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>User Plan</td>
									<td>
                                        <div class="form-group">
                                            <select name="user_plan" id="user_plan" class="form-control">
                                                <option value="" disabled="disabled" selected="selected">Choose your plan</option>
                                                <?php
                                                foreach (getAllPlanType() as $plan_type_row) {
                                                    ?>
                                                    <option value="<?php echo $plan_type_row['plan_type_id']; ?>"><?php echo $plan_type_row['plan_type_name']; if($plan_type_row['plan_type_price'] != 0){ echo ' - '.$plan_type_row['plan_type_price'].'/year';} ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>Facebook</td>
									<td>
                                        <div class="form-group">
                                          <input type="text" name="user_facebook" class="form-control" >
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>Twitter</td>
                                    <td>
                                        <div class="form-group">
                                          <input type="text" name="user_twitter" class="form-control" >
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>Youtube</td>
                                    <td>
                                        <div class="form-group">
                                          <input type="text" name="user_youtube" class="form-control" >
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>Website</td>
                                    <td>
                                        <div class="form-group">
                                          <input type="text"  name="user_website" class="form-control" >
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>
                                        <button type="submit" name="register_submit" class="db-pro-bot-btn">Add User</button>
                                    </td>
									<td></td>
								</tr>
							</tbody>
						</table>
                     </form>
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