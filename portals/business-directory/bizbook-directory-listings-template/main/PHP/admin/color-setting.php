<?php
include "header.php";
?>

<?php if ($admin_row['admin_appearance_options'] != 1) {
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Theme color settings</span>
                <div class="ud-cen-s2 color-set">
                    <h2>Color options</h2>
                    <?php include "../page_level_message.php"; ?>
                    <form name="color_setting_form" id="color_setting_form" method="post" enctype="multipart/form-data" action="update_color_setting.php" >
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Page name</th>
                            <th>Element</th>
                            <th>Default color</th>
                            <th>Hover color</th>
                        </tr>
                        </thead>
                        <?php

                        $color_setting_row = getAllCustomCss();

                        ?>
                        <tbody>
                        <tr>
                            <td>1</td>
                            <td>Home</td>
                            <td>Search (button)</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['home_search_btn_default']; ?>">
                                  <input type="text" name="home_search_btn_default" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['home_search_btn_default']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['home_search_btn_hover']; ?>">
                                  <input type="text" name="home_search_btn_hover" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['home_search_btn_hover']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td>Home</td>
                            <td>Banner "Explore now" (button)</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['home_banner_btn_default']; ?>">
                                  <input type="text" name="home_banner_btn_default" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['home_banner_btn_default']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['home_banner_btn_hover']; ?>">
                                  <input type="text" name="home_banner_btn_hover" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['home_banner_btn_hover']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                            <tr>
                            <td>3</td>
                            <td>Home</td>
                            <td>"View all services" (button)</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['home_view_all_btn_default']; ?>">
                                  <input type="text" name="home_view_all_btn_default" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['home_view_all_btn_default']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['home_view_all_btn_hover']; ?>">
                                  <input type="text" name="home_view_all_btn_hover" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['home_view_all_btn_hover']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                            <tr>
                            <td>4</td>
                            <td>Common</td>
                            <td>"Help & Support" (button)</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['common_help_support_btn_default']; ?>">
                                  <input type="text" name="common_help_support_btn_default" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['common_help_support_btn_default']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['common_help_support_btn_hover']; ?>">
                                  <input type="text" name="common_help_support_btn_hover" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['common_help_support_btn_hover']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                           <tr>
                            <td>5</td>
                            <td>Home</td>
                            <td>"Submit Requirements" (button)</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['home_submit_req_btn_default']; ?>">
                                  <input type="text" name="home_submit_req_btn_default" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['home_submit_req_btn_default']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['home_submit_req_btn_hover']; ?>">
                                  <input type="text" name="home_submit_req_btn_hover" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['home_submit_req_btn_hover']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                           <tr>
                            <td>6</td>
                            <td>Common</td>
                            <td>Blue color(button)</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['common_blue_btn']; ?>">
                                  <input type="text" name="common_blue_btn" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['common_blue_btn']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                           <tr>
                            <td>7</td>
                            <td>Common</td>
                            <td>Blue light color(button)</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['common_light_blue_btn']; ?>">
                                  <input type="text" name="common_light_blue_btn" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['common_light_blue_btn']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                           <tr>
                            <td>8</td>
                            <td>Common</td>
                            <td>Red color(button)</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['common_red_btn']; ?>">
                                  <input type="text" name="common_red_btn" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['common_red_btn']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                           <tr>
                            <td>9</td>
                            <td>Common</td>
                            <td>Red dark color(button)</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['common_dark_red_btn']; ?>">
                                  <input type="text" name="common_dark_red_btn" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['common_dark_red_btn']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                           <tr>
                            <td>10</td>
                            <td>Common</td>
                            <td>Yellow color(bottom band)</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['common_yellow_bottom_band']; ?>">
                                  <input type="text" name="common_yellow_bottom_band" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['common_yellow_bottom_band']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                           <tr>
                            <td>11</td>
                            <td>Common</td>
                            <td>Yellow-1 color(bottom band)</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['common_yellow_1_bottom_band']; ?>">
                                  <input type="text" name="common_yellow_1_bottom_band" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['common_yellow_1_bottom_band']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                          <tr>
                            <td>12</td>
                            <td>Common</td>
                            <td>Yellow-2 color(button)</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['common_yellow_2_btn']; ?>">
                                  <input type="text" name="common_yellow_2_btn" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['common_yellow_2_btn']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                           <tr>
                            <td>13</td>
                            <td>Common</td>
                            <td>Gray color</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['common_gray_color']; ?>">
                                  <input type="text" name="common_gray_color" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['common_gray_color']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                           <tr>
                            <td>14</td>
                            <td>Common</td>
                            <td>Green color</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['common_green_color']; ?>">
                                  <input type="text" name="common_green_color" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['common_green_color']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                           <tr>
                            <td>15</td>
                            <td>Common</td>
                            <td>Green light color</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['common_light_green_color']; ?>">
                                  <input type="text" name="common_light_green_color" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['common_light_green_color']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                           <tr>
                            <td>16</td>
                            <td>Job</td>
                            <td>Blue color</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['job_blue_color']; ?>">
                                  <input type="text" name="job_blue_color" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['job_blue_color']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                           <tr>
                            <td>17</td>
                            <td>Job</td>
                            <td>Orange color</td>
                            <td>
                                <div class="form-group">
                                  <input type="color" class="form-control clr-pan" value="<?php echo $color_setting_row['job_orange_color']; ?>">
                                  <input type="text" name="job_orange_color" class="form-control clr-cod" placeholder="color code" value="<?php echo $color_setting_row['job_orange_color']; ?>" minlength="7" maxlength="7" required>
                                </div>
                            </td>
                        </tr>
                            <tr>
                                <td colspan="2">
                                    <button type="submit" name="color_setting_submit" class="db-pro-bot-btn">Submit Changes</button>
                                    <button type="reset" name="color_setting_reset" class="db-pro-bot-btn db-pro-bot-grey-btn">Reset Changes</button>
                                </td>
                                <td colspan="3">&nbsp;</td>
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
<script src="js/admin-custom.js"></script>
<script>
$(document).ready(function(){
    $('.clr-pan').on('input', function() {
        $(this).siblings('.clr-cod').val(this.value);
    });
    $('.clr-cod').on('input', function() {
      $(this).siblings('.clr-pan').val(this.value);
    });
});
</script>
</body>

</html>