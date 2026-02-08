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
                <span class="udb-inst">Delete Sub Admin</span>
                <div class="ud-cen-s2 ud-pro-edit">
                    <h2>Delete sub admin details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <?php
                    $admin_id = $_GET['row'];
                    $row = getAdmin($admin_id);
                    ?>
                    <table class="responsive-table bordered">
                        <form name="admin_sub_admin_form" action="trash_admin_sub_admin.php" method="post" enctype="multipart/form-data" >
                            <input type="hidden" class="validate" id="admin_id" name="admin_id" value="<?php echo $row['admin_id']; ?>" required="required">
                            <input type="hidden" class="validate" id="admin_photo_old" name="admin_photo_old" value="<?php echo $row['admin_photo']; ?>" required="required">

                            <tbody>
                            <tr>
                                <td>Sub admin name</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" readonly="readonly" name="admin_name" value="<?php echo $row['admin_name']; ?>"  required="required" class="form-control" placeholder="Name">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>User name</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" readonly="readonly" name="admin_email" value="<?php echo $row['admin_email']; ?>" required="required" class="form-control" placeholder="Enter user name">
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
                                                    <input type="checkbox" disabled="disabled" name="admin_user_options" id="sac1" <?php if($row['admin_user_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac1">User options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_listing_options" id="sac2" <?php if($row['admin_listing_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac2">Listing options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_event_options" id="sac3" <?php if($row['admin_event_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac3">Event options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_blog_options" id="sac4" <?php if($row['admin_blog_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac4">Blog post options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_product_options" id="sac24" <?php if($row['admin_product_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac24">Product options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_jobs_options" id="sac27" <?php if($row['admin_jobs_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac27">Job options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_service_expert_options" id="sac28" <?php if($row['admin_service_expert_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac28">Service Expert options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_news_options" id="sac29" <?php if($row['admin_news_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac29">News & Magazine options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_seo_setting_options" id="sac30" <?php if($row['admin_seo_setting_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac30">SEO Setting options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_appearance_options" id="sac31" <?php if($row['admin_appearance_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac31">Appearance options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_category_options" id="sac5" <?php if($row['admin_category_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac5">Listing Category options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_product_category_options" id="sac25" <?php if($row['admin_product_category_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac25">Product Category options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_enquiry_options" id="sac6"  <?php if($row['admin_enquiry_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac6">Enquiry & get quote options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_review_options" id="sac7" <?php if($row['admin_review_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac7">Reviews options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_feedback_options" id="sac26" <?php if($row['admin_feedback_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac26">Feedback options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_notification_options" id="sac8" <?php if($row['admin_notification_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac8">Send notification options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_ads_options" id="sac9" <?php if($row['admin_ads_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac9">Ads options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_home_options" id="sac10" <?php if($row['admin_home_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac10">Home Page options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_country_options" id="sac11" <?php if($row['admin_country_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac11">Country options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_city_options" id="sac12" <?php if($row['admin_city_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac12">City options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_listing_filter_options" id="sac22" <?php if($row['admin_listing_filter_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac22">Listing Filter options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_invoice_options" id="sac13" <?php if($row['admin_invoice_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac13">Invoice options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_import_options" id="sac14" <?php if($row['admin_import_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac14">Import & Export options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_sub_admin_options" id="sac15" <?php if($row['admin_sub_admin_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac15">Sub Admin options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_text_options" id="sac16" <?php if($row['admin_text_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac16">All Text Change options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_listing_price_options" id="sac17" <?php if($row['admin_listing_price_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac17">Listing Price options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_payment_options" id="sac18" <?php if($row['admin_payment_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac18">Admin Payment options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_setting_options" id="sac19" <?php if($row['admin_setting_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac19">Setting options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_footer_options" id="sac20" <?php if($row['admin_footer_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac20">Footer CMS options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_dummy_image_options" id="sac21" <?php if($row['admin_dummy_image_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac21">Dummy images options</label>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="chbox">
                                                    <input type="checkbox" disabled="disabled" name="admin_mail_template_options" id="sac23" <?php if($row['admin_mail_template_options'] == 1){ ?> checked="" <?php }?>>
                                                    <label for="sac23">Mail Template options</label>
                                                </div>
                                            </li>
                                        </ul>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <button type="submit" name="sub_admin_submit" class="db-pro-bot-btn">Delete</button>
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