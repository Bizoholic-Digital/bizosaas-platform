<?php
include "header.php";
?>

<?php if($admin_row['admin_setting_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Settings</span>
                 <div class="ud-cen-s2 ud-pro-edit">
                    <h2>Admin details</h2>
                     <?php include "../page_level_message.php"; ?>
                     <form name="setting_form" id="setting_form" method="post" enctype="multipart/form-data" action="update_setting.php">
                     <table class="responsive-table bordered">
                        <?php
                            $row_f = getAllFooter();

                            $admin_sql_row = getAllSuperAdmin();
                            ?>
                            <input type="hidden" autocomplete="off" name="footer_id"
                                   value="<?php echo $row_f['footer_id']; ?>" id="footer_id" class="validate">
                         <input type="hidden" autocomplete="off" name="admin_password_old"
                                   value="<?php echo $admin_sql_row['admin_password']; ?>" id="admin_password_old" class="validate">
                            <input type="hidden" class="validate" id="admin_photo_old" name="admin_photo_old"
                                   value="<?php echo $admin_sql_row['admin_photo']; ?>" required="required">
                            <input type="hidden" class="validate" id="home_page_banner_old" name="home_page_banner_old"
                                value="<?php echo $row_f['home_page_banner']; ?>" required="required">
                            <input type="hidden" class="validate" id="home_page_fav_icon_old" name="home_page_fav_icon_old"
                                value="<?php echo $row_f['home_page_fav_icon']; ?>" required="required">

                            <tbody>
                            <tr>
                                <td>Website Name</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" name="website_address" value="<?php echo $row_f['website_address']; ?>" required="required" class="form-control" placeholder="RN53 Themes">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Admin Email [For All Mails] :</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" name="admin_primary_email" class="form-control" placeholder="Email"
                                               value="<?php echo $row_f['admin_primary_email']; ?>">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Currency Symbol</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" name="currency_symbol" required="required" value="<?php echo $row_f['currency_symbol']; ?>"
                                               placeholder="[ Note: Please make sure the currency code is correct ]">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Name</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" required="required" name="admin_name" value="<?php echo $admin_sql_row['admin_name']; ?>" placeholder="Name">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>User name</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" required="required" name="admin_email" value="<?php echo $admin_sql_row['admin_email']; ?>" placeholder="Enter user name">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>New Password</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" name="admin_password" autocomplete="off" value="" placeholder="Enter new password if you like to change">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Recovery Email [For Password reset] :</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" name="admin_recovery_email" class="form-control" placeholder="Enter your Email Id to enable admin password recovery"
                                               value="<?php echo $row_f['admin_recovery_email']; ?>">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Fav Icon</td>
                                <td>
                                    <div class="form-group">
                                        <input type="file" name="home_page_fav_icon" class="form-control" >
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>SEO Title</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" required="required" name="admin_seo_title" value="<?php echo $row_f['admin_seo_title']; ?>" placeholder="SEO Title for whole website">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>SEO Description</td>
                                <td>
                                    <div class="form-group">
                                        <textarea class="form-control" required="required" name="admin_seo_description"><?php echo $row_f['admin_seo_description']; ?></textarea>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>SEO Keywords</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" required="required" name="admin_seo_keywords" value="<?php echo $row_f['admin_seo_keywords']; ?>" placeholder="Enter SEO Keywords (i.e) Best Template in the world,Themes,User friendly">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Home page Banner</td>
                                <td>
                                    <div class="form-group">
                                        <input type="file" name="home_page_banner"  class="form-control" >
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Login using Google</td>
                                <td>
                                    <div class="form-group">
                                        <select name="admin_google_login" class="form-control" id="admin_google_login">

                                            <option <?php if($row_f['admin_google_login']== 1){ echo "selected"; } ?>
                                                value="1">Active</option>
                                            <option <?php if($row_f['admin_google_login']== 2){ echo "selected"; } ?>
                                                value="2">Inactive</option>

                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Login using Facebook</td>
                                <td>
                                    <div class="form-group">
                                        <select name="admin_facebook_login" class="form-control" id="admin_facebook_login">

                                            <option <?php if($row_f['admin_facebook_login']== 1){ echo "selected"; } ?>
                                                value="1">Active</option>
                                            <option <?php if($row_f['admin_facebook_login']== 2){ echo "selected"; } ?>
                                                value="2">Inactive</option>

                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Client ID [Login Using Google] </br></br> <a target="_blank" href="https://developers.google.com/identity/sign-in/web/sign-in">To Create New - Click Here</a></td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" required="required" name="admin_google_client_id" value="<?php echo $row_f['admin_google_client_id']; ?>" placeholder="Paste your Google Client Id">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>App Id [Login Using Facebook] </br></br> <a target="_blank" href="https://developers.facebook.com/apps/">To Create New - Click Here</a></td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" required="required" name="admin_facebook_app_id" value="<?php echo $row_f['admin_facebook_app_id']; ?>" placeholder="Paste your Facebook APP Id">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Google Geo Map API Key </br></br> <a target="_blank" href="https://developers.google.com/maps/documentation/geocoding/get-api-key">To Create New - Click Here</a></td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" required="required" name="admin_geo_map_api" value="<?php echo $row_f['admin_geo_map_api']; ?>" placeholder="Paste your Google Map Api Key">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Map View Default Latitude</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" required="required" name="admin_geo_default_latitude" value="<?php echo $row_f['admin_geo_default_latitude']; ?>" placeholder="Paste your Default Google Map Latitude">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Map View Default Longitude</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" required="required" name="admin_geo_default_longitude" value="<?php echo $row_f['admin_geo_default_longitude']; ?>" placeholder="Paste your Default Google Map Longitude">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Map View Default Zoom Size</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" required="required" name="admin_geo_default_zoom" value="<?php echo $row_f['admin_geo_default_zoom']; ?>" placeholder="Paste your Default Google Map Zoom Size">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Language</td>
                                <td>
                                    <div class="form-group">
                                        <select name="admin_language" class="form-control" id="admin_language">

                                                <option <?php if($row_f['admin_language']== 1){ echo "selected"; } ?>
                                                    value="1">English</option>
                                            <option <?php if($row_f['admin_language']== 2){ echo "selected"; } ?>
                                                value="2">Arabic</option>

                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Countries</td>
                                <td>
                                    <div class="form-group">
                                        <select name="admin_countries[]" multiple class="chosen-select form-control" id="admin_countries">

                                            <?php
                                            foreach (getAllCountries() as $countries_row) {
                                                ?>
                                                <option <?php $counArray = explode(',', $row_f['admin_countries']);
                                                foreach($counArray as $coun_Array){
                                                    if ($countries_row['country_id'] == $coun_Array) {
                                                        echo "selected";
                                                    }
                                                } ?>
                                                    value="<?php echo $countries_row['country_id']; ?>"><?php echo $countries_row['country_name']; ?></option>
                                                <?php
                                            }
                                            ?>

                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Profile picture</td>
                                <td>
                                    <div class="form-group">
                                        <input type="file" name="admin_photo"  class="form-control" >
                                    </div>
                                </td>
                            </tr>

<!--                            <tr>-->
<!--                                <td>Listing Module</td>-->
<!--                                <td>-->
<!--                                    <div class="custom-control custom-switch">-->
<!--                                        <input type="checkbox" class="share_button custom-control-input" name="admin_listing_show" id="admin_listing_show" --><?php //if($row_f['admin_listing_show'] == 1){ echo "checked"; } ?><!-->
<!--                                        <label class="custom-control-label" for="admin_listing_show"> Enable or Disable Listing related feature</label>-->
<!--                                    </div>-->
<!--                                </td>-->
<!--                            </tr>-->

                            <tr>
                                <td>Job Module</td>
                                <td>
                                    <div class="custom-control custom-switch">
                                        <input type="checkbox" class="share_button custom-control-input" name="admin_job_show" id="admin_job_show" <?php if($row_f['admin_job_show'] == 1){ echo "checked"; } ?>>
                                        <label class="custom-control-label" for="admin_job_show"> Enable or Disable Job related feature</label>
                                    </div>
                                </td>
                            </tr>

                            <tr>
                                <td>Service Expert Module</td>
                                <td>
                                    <div class="custom-control custom-switch">
                                        <input type="checkbox" class="share_button custom-control-input" name="admin_expert_show" id="admin_expert_show" <?php if($row_f['admin_expert_show'] == 1){ echo "checked"; } ?>>
                                        <label class="custom-control-label" for="admin_expert_show"> Enable or Disable Service Expert related feature</label>
                                    </div>
                                </td>
                            </tr>

                            <tr>
                                <td>Product Module</td>
                                <td>
                                    <div class="custom-control custom-switch">
                                        <input type="checkbox" class="share_button custom-control-input" name="admin_product_show" id="admin_product_show" <?php if($row_f['admin_product_show'] == 1){ echo "checked"; } ?>>
                                        <label class="custom-control-label" for="admin_product_show"> Enable or Disable Product related feature</label>
                                    </div>
                                </td>
                            </tr>

                            <tr>
                                <td>Blog Module</td>
                                <td>
                                    <div class="custom-control custom-switch">
                                        <input type="checkbox" class="share_button custom-control-input" name="admin_blog_show" id="admin_blog_show" <?php if($row_f['admin_blog_show'] == 1){ echo "checked"; } ?>>
                                        <label class="custom-control-label" for="admin_blog_show"> Enable or Disable Blog related feature</label>
                                    </div>
                                </td>
                            </tr>

                            <tr>
                                <td>Event Module</td>
                                <td>
                                    <div class="custom-control custom-switch">
                                        <input type="checkbox" class="share_button custom-control-input" name="admin_event_show" id="admin_event_show" <?php if($row_f['admin_event_show'] == 1){ echo "checked"; } ?>>
                                        <label class="custom-control-label" for="admin_event_show"> Enable or Disable Event related feature</label>
                                    </div>
                                </td>
                            </tr>

                            <tr>
                                <td>News Module</td>
                                <td>
                                    <div class="custom-control custom-switch">
                                        <input type="checkbox" class="share_button custom-control-input" name="admin_news_show" id="admin_news_show" <?php if($row_f['admin_news_show'] == 1){ echo "checked"; } ?>>
                                        <label class="custom-control-label" for="admin_news_show"> Enable or Disable News related feature</label>
                                    </div>
                                </td>
                            </tr>

                            <tr>
                                <td>Places Module</td>
                                <td>
                                    <div class="custom-control custom-switch">
                                        <input type="checkbox" class="share_button custom-control-input" name="admin_place_show" id="admin_place_show" <?php if($row_f['admin_place_show'] == 1){ echo "checked"; } ?>>
                                        <label class="custom-control-label" for="admin_place_show"> Enable or Disable Places related feature</label>
                                    </div>
                                </td>
                            </tr>

                            <tr>
                                <td>Discount & Coupon Module</td>
                                <td>
                                    <div class="custom-control custom-switch">
                                        <input type="checkbox" class="share_button custom-control-input" name="admin_coupon_show" id="admin_coupon_show" <?php if($row_f['admin_coupon_show'] == 1){ echo "checked"; } ?>>
                                        <label class="custom-control-label" for="admin_coupon_show"> Enable or Disable Coupons related feature</label>
                                    </div>
                                </td>
                            </tr>

                            <tr>
                                <td>
                                    <button type="submit" name="setting_submit" class="db-pro-bot-btn">Submit Changes</button>
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
<script src="../js/select-opt.js"></script>
    <script src="js/admin-custom.js"></script>

</body>

</html>