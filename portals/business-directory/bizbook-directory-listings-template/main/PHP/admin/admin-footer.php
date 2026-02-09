<?php
include "header.php";
?>

<?php if($admin_row['admin_footer_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Footer</span>
                <div class="ud-cen-s2 ud-pro-edit ad-all-txt-chan">
                    <h2>Footer CMS</h2>
                    <?php include "../page_level_message.php"; ?>
                    <form name="footer_form" id="footer_form" method="post" enctype="multipart/form-data" action="update_footer.php">

                    <table class="responsive-table bordered">
                        <thead>
								<tr>
                                    <th>Section</th>
									<th>Text</th>
									<th>Change</th>
								</tr>
							</thead>
							<tbody>
                            <?php
                            $row_f = getAllFooter();
                            $admin_sql_row = getAllSuperAdmin();
                                ?>
                                <input type="hidden" autocomplete="off" name="footer_id" value="<?php echo $row_f['footer_id']; ?>" id="footer_id" class="validate">
                            <input type="hidden" class="validate" id="header_logo_old" name="header_logo_old"
                                   value="<?php echo $row_f['header_logo']; ?>" required="required">
                            <input type="hidden" class="validate" id="admin_photo_old" name="admin_photo_old"
                                   value="<?php echo $admin_sql_row['admin_photo']; ?>" required="required">
                            <input type="hidden" class="validate" id="home_page_banner_old" name="home_page_banner_old"
                                   value="<?php echo $admin_sql_row['home_page_banner']; ?>" required="required">
                            <input type="hidden" class="validate" id="home_page_fav_icon_old" name="home_page_fav_icon_old"
                                   value="<?php echo $admin_sql_row['home_page_fav_icon']; ?>" required="required">
                                <tr>
                                    <td>Support</td>
                                    <td>Phone num:</td>
                                    <td colspan="3">
                                        <div class="form-group">
                                            <input type="text" class="form-control" name="footer_mobile" placeholder="Phone"
                                                   value="<?php echo $row_f['footer_mobile']; ?>">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Top category</td>
                                    <td>Category 1:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="top_category_1" class="form-control" id="top_category_1">
                                                <?php
                                                foreach (getAllCategories() as $row_1){
                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['top_category_1']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                    <td>Category 2:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="top_category_2" class="form-control" id="top_category_2">
                                                <?php
                                                foreach (getAllCategories() as $row_1){

                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['top_category_2']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Category 3:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="top_category_3" class="form-control" id="top_category_3">
                                                <?php
                                                foreach (getAllCategories() as $row_1){

                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['top_category_3']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                    <td>Category 4:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="top_category_4" class="form-control" id="top_category_4">
                                                <?php
                                                foreach (getAllCategories() as $row_1){
                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['top_category_4']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Category 5:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="top_category_5" class="form-control" id="top_category_5">
                                                <?php
                                                foreach (getAllCategories() as $row_1){
                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['top_category_5']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                    <td>Category 6:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="top_category_6" class="form-control" id="top_category_6">
                                                <?php
                                                foreach (getAllCategories() as $row_1){
                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['top_category_6']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Category 7:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="top_category_7" class="form-control" id="top_category_7">
                                                <?php
                                                foreach (getAllCategories() as $row_1){
                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['top_category_7']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                    <td>Category 8:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="top_category_8" class="form-control" id="top_category_8">
                                                <?php
                                                foreach (getAllCategories() as $row_1){
                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['top_category_8']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Trending category</td>
                                    <td>Category 1:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="trend_category_1" class="form-control" id="trend_category_1">
                                                <?php
                                                foreach (getAllCategories() as $row_1){

                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['trend_category_1']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                    <td>Category 2:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="trend_category_2" class="form-control" id="trend_category_2">
                                                <?php
                                                foreach (getAllCategories() as $row_1){

                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['trend_category_2']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Category 3:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="trend_category_3" class="form-control" id="trend_category_3">
                                                <?php
                                                foreach (getAllCategories() as $row_1){

                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['trend_category_3']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                    <td>Category 4:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="trend_category_4" class="form-control" id="trend_category_4">
                                                <?php
                                                foreach (getAllCategories() as $row_1){

                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['trend_category_4']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Category 5:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="trend_category_5" class="form-control" id="trend_category_5">
                                                <?php
                                                foreach (getAllCategories() as $row_1){

                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['trend_category_5']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                    <td>Category 6:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="trend_category_6" class="form-control" id="trend_category_6">
                                                <?php
                                                foreach (getAllCategories() as $row_1){

                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['trend_category_6']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Category 7:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="trend_category_7" class="form-control" id="trend_category_7">
                                                <?php
                                                foreach (getAllCategories() as $row_1){

                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['trend_category_7']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                    <td>Category 8:</td>
                                    <td>
                                        <div class="form-group">
                                            <select name="trend_category_8" class="form-control" id="trend_category_8">
                                                <?php
                                                foreach (getAllCategories() as $row_1){

                                                    ?>
                                                    <option <?php if($row_1['category_id']== $row_f['trend_category_8']){ echo "selected"; } ?>
                                                        value="<?php echo $row_1['category_id']; ?>"><?php echo $row_1['category_name']; ?></option>
                                                    <?php
                                                }
                                                ?>
                                            </select>
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Get in touch</td>
                                    <td>Address:</td>
                                    <td colspan="3">
                                        <div class="form-group">
                                            <input type="text" class="form-control" name="footer_address" value="<?php echo $row_f['footer_address']; ?>" required="required">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Mobile app</td>
                                    <td>Android:</td>
                                    <td colspan="3">
                                        <div class="form-group">
                                            <input type="text" name="mobile_app_andriod" value="<?php echo $row_f['mobile_app_andriod']; ?>" class="form-control"
                                                   placeholder="Playstore download link">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Apple:</td>
                                    <td colspan="3">
                                        <div class="form-group">
                                            <input type="text" name="mobile_app_ios" value="<?php echo $row_f['mobile_app_ios']; ?>" class="form-control"
                                                   placeholder="App store download link">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Social media</td>
                                    <td>Facebook:</td>
                                    <td colspan="3">
                                        <div class="form-group">
                                            <input type="text" name="footer_fb" value="<?php echo $row_f['footer_fb']; ?>" class="form-control" placeholder="Profile link">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Twitter:</td>
                                    <td colspan="3">
                                        <div class="form-group">
                                            <input type="text" class="form-control" name="footer_twitter" value="<?php echo $row_f['footer_twitter']; ?>" placeholder="Profile link">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Linkedin:</td>
                                    <td colspan="3">
                                        <div class="form-group">
                                            <input type="text" class="form-control" name="footer_linked_in" value="<?php echo $row_f['footer_linked_in']; ?>" placeholder="Profile link">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Youtube:</td>
                                    <td colspan="3">
                                        <div class="form-group">
                                            <input type="text" class="form-control" name="footer_youtube" value="<?php echo $row_f['footer_youtube']; ?>" placeholder="Profile link">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>WhatsApp:</td>
                                    <td colspan="3">
                                        <div class="form-group">
                                            <input type="text" name="footer_whatsapp" value="<?php echo $row_f['footer_whatsapp']; ?>" class="form-control"
                                                   placeholder="WhatsApp mobile number">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Help & Support</td>
                                    <td>Page name:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" name="footer_page_name_1" placeholder="Page name" value="<?php echo $row_f['footer_page_name_1']; ?>">
                                        </div>
                                    </td>
                                    <td>Page URL:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Page full url"
                                                   name="footer_page_url_1" value="<?php echo $row_f['footer_page_url_1']; ?>">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Page name:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" name="footer_page_name_2" placeholder="Page name" value="<?php echo $row_f['footer_page_name_2']; ?>">
                                        </div>
                                    </td>
                                    <td>Page URL:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Page full url"
                                                   name="footer_page_url_2" value="<?php echo $row_f['footer_page_url_2']; ?>">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Page name:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" name="footer_page_name_3" placeholder="Page name" value="<?php echo $row_f['footer_page_name_3']; ?>">
                                        </div>
                                    </td>
                                    <td>Page URL:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Page full url"
                                                   name="footer_page_url_3" value="<?php echo $row_f['footer_page_url_3']; ?>">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Page name:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" name="footer_page_name_4" placeholder="Page name" value="<?php echo $row_f['footer_page_name_4']; ?>">
                                        </div>
                                    </td>
                                    <td>Page URL:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Page full url"
                                                   name="footer_page_url_4" value="<?php echo $row_f['footer_page_url_4']; ?>">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Other countries</td>
                                    <td>Country name:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Country name" name="footer_country_name_1" value="<?php echo $row_f['footer_country_name_1']; ?>">
                                        </div>
                                    </td>
                                    <td>Country url:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Country page full url"
                                                   name="footer_country_url_1" value="<?php echo $row_f['footer_country_url_1']; ?>">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Country name:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Country name" name="footer_country_name_2" value="<?php echo $row_f['footer_country_name_2']; ?>">
                                        </div>
                                    </td>
                                    <td>Country url:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Country page full url"
                                                   name="footer_country_url_2" value="<?php echo $row_f['footer_country_url_2']; ?>">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Country name:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Country name" name="footer_country_name_3" value="<?php echo $row_f['footer_country_name_3']; ?>">
                                        </div>
                                    </td>
                                    <td>Country url:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Country page full url"
                                                   name="footer_country_url_3" value="<?php echo $row_f['footer_country_url_3']; ?>">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Country name:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Country name" name="footer_country_name_4" value="<?php echo $row_f['footer_country_name_4']; ?>">
                                        </div>
                                    </td>
                                    <td>Country url:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Country page full url"
                                                   name="footer_country_url_4" value="<?php echo $row_f['footer_country_url_4']; ?>">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Country name:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Country name" name="footer_country_name_5" value="<?php echo $row_f['footer_country_name_5']; ?>">
                                        </div>
                                    </td>
                                    <td>Country url:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Country page full url"
                                                   name="footer_country_url_5" value="<?php echo $row_f['footer_country_url_5']; ?>">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Country name:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Country name" name="footer_country_name_6" value="<?php echo $row_f['footer_country_name_6']; ?>">
                                        </div>
                                    </td>
                                    <td>Country url:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Country page full url"
                                                   name="footer_country_url_6" value="<?php echo $row_f['footer_country_url_6']; ?>">
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td>Country name:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Country name" name="footer_country_name_7" value="<?php echo $row_f['footer_country_name_7']; ?>">
                                        </div>
                                    </td>
                                    <td>Country url:</td>
                                    <td>
                                        <div class="form-group">
                                            <input class="form-control" placeholder="Country page full url"
                                                   name="footer_country_url_7" value="<?php echo $row_f['footer_country_url_7']; ?>">
                                        </div>
                                    </td>
                                </tr>
                            <tr>
                                <td>Copyright</td>
                                <td>Copyright year</td>
                                <td colspan="3">
                                    <div class="form-group">
                                        <input type="text" name="copyright_year" value="<?php echo $row_f['copyright_year']; ?>" class="form-control"
                                               placeholder="2017-2020">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td></td>
                                <td>Copyright Website</td>
                                <td colspan="3">
                                    <div class="form-group">
                                        <input type="text" name="copyright_website" value="<?php echo $row_f['copyright_website']; ?>" class="form-control"
                                               placeholder="RN53 Themes">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td></td>
                                <td>Copyright Website Link</td>
                                <td colspan="3">
                                    <div class="form-group">
                                        <input type="text" name="copyright_website_link" value="<?php echo $row_f['copyright_website_link']; ?>" class="form-control"
                                               placeholder="i.e https://google.com">
                                    </div>
                                </td>
                            </tr>

                                <tr>
                                    <td>
                                        <button type="submit" name="footer_submit" class="db-pro-bot-btn">Save changes</button>
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