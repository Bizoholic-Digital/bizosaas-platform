<?php
include "header.php";
?>

<?php if($admin_row['admin_sub_admin_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Add new Sub Admin</span>
                 <div class="ud-cen-s2 ud-pro-edit">
                    <h2>Sub admin details</h2>
                     <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered">
                        <form name="admin_sub_admin_form" action="insert_admin_sub_admin.php" method="post" enctype="multipart/form-data" >
                        <tbody>
								<tr>
                                    <td>Sub admin name</td>
									<td>
                                        <div class="form-group">
                                          <input type="text" name="admin_name" required="required" class="form-control" placeholder="Name">
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>User name</td>
									<td>
                                        <div class="form-group">
                                          <input type="text" name="admin_email" required="required" class="form-control" placeholder="Enter user name">
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>Password</td>
									<td>
                                        <div class="form-group">
                                          <input type="text" name="admin_password" required="required" class="form-control" placeholder="Enter password">
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>Profile picture</td>
									<td>
                                        <div class="form-group">
                                          <input type="file" name="admin_photo" class="form-control">
                                        </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>Credentials</td>
									<td>
                                        <div class="ad-sub-cre">
                                            <ul>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_user_options" id="sac1" checked="">
                                                        <label for="sac1">User options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_listing_options" id="sac2" checked="">
                                                        <label for="sac2">Listing options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_event_options" id="sac3" checked="">
                                                        <label for="sac3">Event options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_blog_options" id="sac4" checked="">
                                                        <label for="sac4">Blog post options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_product_options" id="sac24" checked="">
                                                        <label for="sac24">Product options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_jobs_options" id="sac27" checked="">
                                                        <label for="sac27">Job options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_service_expert_options" id="sac28" checked="">
                                                        <label for="sac28">Service Expert options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_news_options" id="sac29" checked="">
                                                        <label for="sac29">News & Magazine options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_seo_setting_options" id="sac30" checked="">
                                                        <label for="sac30">SEO Setting options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_appearance_options" id="sac31" checked="">
                                                        <label for="sac31">Appearance options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_category_options" id="sac5" checked="">
                                                        <label for="sac5">Listing Category options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_product_category_options" id="sac25" checked="">
                                                        <label for="sac25">Product Category options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_enquiry_options" id="sac6" checked="">
                                                        <label for="sac6">Enquiry & get quote options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_review_options" id="sac7" checked="">
                                                        <label for="sac7">Reviews options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_feedback_options" id="sac26" checked="">
                                                        <label for="sac26">Feedback options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_notification_options" id="sac8" checked="">
                                                        <label for="sac8">Send notification options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_ads_options" id="sac9" checked="">
                                                        <label for="sac9">Ads options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_home_options" id="sac10" checked="">
                                                        <label for="sac10">Home Page options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_country_options" id="sac11" checked="">
                                                        <label for="sac11">Country options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_city_options" id="sac12" checked="">
                                                        <label for="sac12">City options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_listing_filter_options" id="sac22" checked="">
                                                        <label for="sac22">Listing Filter options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_invoice_options" id="sac13" checked="">
                                                        <label for="sac13">Invoice options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_import_options" id="sac14" checked="">
                                                        <label for="sac14">Import & Export options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_sub_admin_options" id="sac15" checked="">
                                                        <label for="sac15">Sub Admin options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_text_options" id="sac16" checked="">
                                                        <label for="sac16">All Text Change options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_listing_price_options" id="sac17" checked="">
                                                        <label for="sac17">Listing Price options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_payment_options" id="sac18" checked="">
                                                        <label for="sac18">Admin Payment options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_setting_options" id="sac19" checked="">
                                                        <label for="sac19">Setting options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_footer_options" id="sac20" checked="">
                                                        <label for="sac20">Footer CMS options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_dummy_image_options" id="sac21" checked="">
                                                        <label for="sac21">Dummy images options</label>
                                                    </div>
                                                </li>
                                                <li>
                                                    <div class="chbox">
                                                        <input type="checkbox" name="admin_mail_template_options" id="sac23" checked="">
                                                        <label for="sac23">Mail Template options</label>
                                                    </div>
                                                </li>
                                            </ul>
                                         </div>
                                    </td>
								</tr>
                                <tr>
                                    <td>
                                        <button type="submit" name="sub_admin_submit" class="db-pro-bot-btn">Add User</button>
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