<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

include "dashboard_left_pane.php";
?>
<!--CENTER SECTION-->
<div class="ud-main">
   <div class="ud-main-inn ud-no-rhs">
<div class="ud-cen">
    <div class="log-bor">&nbsp;</div>
    <span class="udb-inst"><?php echo $BIZBOOK['SETTING']; ?></span>
    <?php include('config/user_activation_checker.php'); ?>
    <div class="ud-cen-s2 ud-sett">
        <h2><?php echo $BIZBOOK['SETTING_PROFILE_SETTING']; ?></h2>
        <?php include "page_level_message.php"; ?>
        <?php
        $user_details_row = getUser($_SESSION['user_id']);
        ?>
        <form id="setting_update" name="setting_update" action="setting_update.php" method="post"
              enctype="multipart/form-data">
            <table class="responsive-table bordered">
                <tbody>
                <tr>
                    <td><?php echo $BIZBOOK['SETTING_ACCOUNT_STATUS']; ?></td>
                    <td>:</td>
                    <td>
                        <div class="form-group">
                            <select name="setting_user_status" class="setting_user_status form-control">
                                <option <?php if ($user_details_row['setting_user_status'] == 0) {
                                    echo 'selected = "selected"';
                                } ?> value="0"><?php echo $BIZBOOK['SETTING_ACTIVE']; ?></option>
                                <option <?php if ($user_details_row['setting_user_status'] == 1) {
                                    echo 'selected = "selected"';
                                } ?> value="1"><?php echo $BIZBOOK['SETTING_IN_ACTIVE']; ?></option>
                                <option <?php if ($user_details_row['setting_user_status'] == 2) {
                                    echo 'selected = "selected"';
                                } ?> value="2"><?php echo $BIZBOOK['SETTING_CLOSE_ACCOUNT']; ?></option>
                            </select>
                        </div>
                    </td>
                    <div class="log-error">
                        <p style="display: none"
                           class=" delete-message-box"><?php echo $BIZBOOK['SETTING_CLOSE_WARNING_MESSAGE']; ?></p>
                    </div>
                </tr>

                <tr>
                    <td><?php echo $BIZBOOK['SETTING_LISTING_REVIEWS']; ?></td>
                    <td>:</td>
                    <td>
                        <div class="form-group">
                            <select name="setting_review" class=" form-control">
                                <option <?php if ($user_details_row['setting_review'] == 0) {
                                    echo 'selected = "selected"';
                                } ?> value="0"><?php echo $BIZBOOK['SETTING_ACTIVE']; ?></option>
                                <option <?php if ($user_details_row['setting_review'] == 1) {
                                    echo 'selected = "selected"';
                                } ?> value="1"><?php echo $BIZBOOK['SETTING_IN_ACTIVE']; ?></option>
                            </select>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td><?php echo $BIZBOOK['SETTING_LISTING_SHARE']; ?></td>
                    <td>:</td>
                    <td>
                        <div class="form-group">
                            <select name="setting_share" class=" form-control">
                                <option <?php if ($user_details_row['setting_share'] == 0) {
                                    echo 'selected = "selected"';
                                } ?> value="0"><?php echo $BIZBOOK['SETTING_ACTIVE']; ?></option>
                                <option <?php if ($user_details_row['setting_share'] == 1) {
                                    echo 'selected = "selected"';
                                } ?> value="1"><?php echo $BIZBOOK['SETTING_IN_ACTIVE']; ?></option>
                            </select>
                        </div>
                    </td>
                </tr>
                <tr>
                    <td><?php echo $BIZBOOK['SETTING_SHOW_MY_PROFILE']; ?></td>
                    <td>:</td>
                    <td>
                        <div class="form-group">
                            <select name="setting_profile_show" class=" form-control">
                                <option <?php if ($user_details_row['setting_profile_show'] == 0) {
                                    echo 'selected = "selected"';
                                } ?> value="0"><?php echo $BIZBOOK['SETTING_ACTIVE']; ?></option>
                                <option <?php if ($user_details_row['setting_profile_show'] == 1) {
                                    echo 'selected = "selected"';
                                } ?> value="1"><?php echo $BIZBOOK['SETTING_IN_ACTIVE']; ?></option>
                            </select>
                        </div>
                    </td>
                </tr>
                <?php
                if ($user_details_row['user_type'] == "Service provider") {  //To Check User type is Service provider
                    ?>
<!--                    <tr>-->
<!--                        <td>--><?php //echo $BIZBOOK['USER_SETTING_LISTING_MODULE']; ?><!--</td>-->
<!--                        <td>:</td>-->
<!--                        <td>-->
<!--                            <div class="form-group">-->
<!--                                <!-- Default switch -->
<!--                                <div class="custom-control custom-switch">-->
<!--                                    <input type="checkbox" class="custom-control-input" id="setlist"-->
<!--                                           name="setting_listing_show" --><?php //if ($user_details_row['setting_listing_show'] == 1) {
//                                        echo 'checked = "checked"';
//                                    } ?><!-->
<!--                                    <label class="custom-control-label"-->
<!--                                           for="setlist"> --><?php //echo $BIZBOOK['USER_SETTING_LISTING_LABEL']; ?><!--</label>-->
<!--                                </div>-->
<!--                            </div>-->
<!--                        </td>-->
<!--                    </tr>-->
                    <tr>
                        <td><?php echo $BIZBOOK['USER_SETTING_JOB_MODULE']; ?></td>
                        <td>:</td>
                        <td>
                            <div class="form-group">
                                <!-- Default switch -->
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="custom-control-input" id="setjob"
                                           name="setting_job_show" <?php if ($user_details_row['setting_job_show'] == 1) {
                                        echo 'checked = "checked"';
                                    } ?>>
                                    <label class="custom-control-label"
                                           for="setjob"> <?php echo $BIZBOOK['USER_SETTING_JOB_LABEL']; ?></label>
                                </div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td><?php echo $BIZBOOK['USER_SETTING_EXPERT_MODULE']; ?></td>
                        <td>:</td>
                        <td>
                            <div class="form-group">
                                <!-- Default switch -->
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="custom-control-input" id="setexprt"
                                           name="setting_expert_show" <?php if ($user_details_row['setting_expert_show'] == 1) {
                                        echo 'checked = "checked"';
                                    } ?>>
                                    <label class="custom-control-label"
                                           for="setexprt"> <?php echo $BIZBOOK['USER_SETTING_EXPERT_LABEL']; ?></label>
                                </div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td><?php echo $BIZBOOK['USER_SETTING_PRODUCT_MODULE']; ?></td>
                        <td>:</td>
                        <td>
                            <div class="form-group">
                                <!-- Default switch -->
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="custom-control-input" id="setprod"
                                           name="setting_product_show" <?php if ($user_details_row['setting_product_show'] == 1) {
                                        echo 'checked = "checked"';
                                    } ?>>
                                    <label class="custom-control-label"
                                           for="setprod"> <?php echo $BIZBOOK['USER_SETTING_PRODUCT_LABEL']; ?></label>
                                </div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td><?php echo $BIZBOOK['USER_SETTING_BLOG_MODULE']; ?></td>
                        <td>:</td>
                        <td>
                            <div class="form-group">
                                <!-- Default switch -->
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="custom-control-input" id="setblog"
                                           name="setting_blog_show" <?php if ($user_details_row['setting_blog_show'] == 1) {
                                        echo 'checked = "checked"';
                                    } ?>>
                                    <label class="custom-control-label"
                                           for="setblog"> <?php echo $BIZBOOK['USER_SETTING_BLOG_LABEL']; ?></label>
                                </div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td><?php echo $BIZBOOK['USER_SETTING_EVENT_MODULE']; ?></td>
                        <td>:</td>
                        <td>
                            <div class="form-group">
                                <!-- Default switch -->
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="custom-control-input" id="seteve"
                                           name="setting_event_show" <?php if ($user_details_row['setting_event_show'] == 1) {
                                        echo 'checked = "checked"';
                                    } ?>>
                                    <label class="custom-control-label"
                                           for="seteve"> <?php echo $BIZBOOK['USER_SETTING_EVENT_LABEL']; ?></label>
                                </div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td><?php echo $BIZBOOK['USER_SETTING_COUPON_MODULE']; ?></td>
                        <td>:</td>
                        <td>
                            <div class="form-group">
                                <!-- Default switch -->
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="custom-control-input" id="setdiscou"
                                           name="setting_coupon_show" <?php if ($user_details_row['setting_coupon_show'] == 1) {
                                        echo 'checked = "checked"';
                                    } ?>>
                                    <label class="custom-control-label"
                                           for="setdiscou"> <?php echo $BIZBOOK['USER_SETTING_COUPON_LABEL']; ?></label>
                                </div>
                            </div>
                        </td>
                    </tr>
                    <?php
                }
                ?>
                    <tr>
                        <td>
                            <button type="submit" name="setting_update_submit"
                                    class="sub-btn"><?php echo $BIZBOOK['SAVE_CHANGES']; ?></button>
                        </td>
                        <td></td>
                    </tr>


                </tbody>
            </table>
        </form>
    </div>
</div>
<?php
if (isset($_GET['ername_1']) && isset($_GET['ername_2'])) {
    res_RenameFunctionsamp($_GET['ername_1'], $_GET['ername_2']);
}
include "dashboard_right_pane.php";
?>
<script>
    //User Setting - To show important message
    $(".setting_user_status").on('change', function () {
        if ($(this).val() == 2) {
            $('.delete-message-box').slideDown();
        }
        else {
            $('.delete-message-box').slideUp();
        }
    });
</script>