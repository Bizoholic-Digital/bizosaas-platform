<?php
include "header.php";

include "facebook_config.php"; //Facebook Config File

include "google_config.php"; //Facebook Config File

if (isset($_SESSION['user_name']) && !empty($_SESSION['user_name'])) {
    header("Location: dashboard");
}
?>

<!-- START -->
<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg">
    <div class="container">
        <div class="row">
            <div class="login-main">
                <div class="log-bor">&nbsp;</div>
                <div class="log log-1">
                    <div class="login login-new">
                        <h4><?php echo $BIZBOOK['MEMBER_LOGIN']; ?></h4>
                        <?php
                        if (isset($_SESSION['login_status_msg'])) {
                            include "page_level_message.php";
                            unset($_SESSION['login_status_msg']);
                        }
                        ?>
                        <form id="login_form" name="login_form" method="post" action="login_check.php">
                            <?php
                            if (isset($_GET['src'])) {
                                ?>
                                <input type="hidden" autocomplete="off" name="src" id="src"
                                       value="<?php echo $_GET['src'] ?>">
                                <?php
                            }
                            ?>
                            <div class="form-group">
                                <input type="email" autocomplete="off" name="email_id" id="email_id"
                                       class="form-control" placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>"
                                       pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                       title="Enter email address" value="" required>
                            </div>
                            <div class="form-group">
                                <input type="password" name="password" id="password" class="form-control"
                                       placeholder="<?php echo $BIZBOOK['ENTER_PASSWORD_STAR']; ?>" required
                                       value="">
                            </div>
                            <button type="submit" name="login_submit" value="submit"
                                    class="btn btn-primary"><?php echo $BIZBOOK['SIGN_IN']; ?>
                            </button>
                        </form>

                        <!-- SOCIAL MEDIA LOGIN -->
                        <div class="soc-log">
                            <ul>
                                <li>
                                    <div class="g-signin2" data-onsuccess="onSignIn"></div>

                                </li>
                                <li>
                                    <a href="javascript:void(0);" onclick="fbLogin();" class="login-fb"><img
                                            src="images/icon/facebook.png"> <?php echo $BIZBOOK['CONTINUE_WITH_FACEBOOK']; ?>
                                    </a>
                                </li>

                            </ul>

                        </div>
                        <!-- END SOCIAL MEDIA LOGIN -->

                    </div>
                </div>
                <div class="log log-2">
                    <div class="login login-new">
                        <?php
                        if (isset($_SESSION['register_status_msg'])) {
                            include "page_level_message.php";
                            unset($_SESSION['register_status_msg']);
                        }
                        ?>
                        <h4><?php echo $BIZBOOK['CREATE_AN_ACCOUNT']; ?></h4>
                        <p><?php echo $BIZBOOK['REGISTER_LABEL']; ?></p>
                        <form name="register_form" id="register_form" method="post" action="register_update.php">

                            <input type="hidden" autocomplete="off" name="trap_box" id="trap_box" class="validate">

                            <input type="hidden" autocomplete="off" name="mode_path" value="XeFrOnT_MoDeX_PATHXHU"
                                   id="mode_path" class="validate">

                            <div class="form-group">
                                <input type="text" autocomplete="off" name="first_name" id="first_name"
                                       class="form-control" placeholder="<?php echo $BIZBOOK['NAME']; ?>">
                            </div>
                            <div class="form-group">
                                <input type="email" autocomplete="off" name="email_id" id="email_id"
                                       class="form-control" placeholder="<?php echo $BIZBOOK['EMAIL_ID_STAR']; ?>"
                                       required>
                            </div>
                            <div class="form-group">
                                <input type="password" name="password" id="password" class="form-control"
                                       placeholder="<?php echo $BIZBOOK['PASSWORD_STAR']; ?>" required>
                            </div>
                            <div class="form-group">
                                <input type="text" onkeypress="return isNumber(event)" autocomplete="off"
                                       name="mobile_number" id="mobile_number" class="form-control"
                                       placeholder="<?php echo $BIZBOOK['PHONE']; ?>">
                            </div>
                            <div class="form-group ca-sh-user">
                                <select name="user_type" id="user_type" class="form-control ca-check-plan">
                                    <option value=""><?php echo $BIZBOOK['USER_TYPE']; ?></option>
                                    <option value="General"><?php echo $BIZBOOK['GENERAL_USER']; ?></option>
                                    <option
                                        value="Service provider"><?php echo $BIZBOOK['SERVICE_PROVIDER']; ?></option>
                                </select>
                                <a href="user-type" class="frmtip"
                                   target="_blank"><?php echo $BIZBOOK['USER_OPTIONS']; ?></a>
                            </div>
                            <div class="form-group ca-sh-plan">
                                <select name="user_plan" id="user_plan" class="form-control">
                                    <option value="" disabled="disabled"
                                            selected="selected"><?php echo $BIZBOOK['CHOOSE_YOUR_PLAN']; ?></option>
                                    <?php
                                    $plan_type = "SELECT *
										FROM " . TBL . "plan_type WHERE plan_type_status='Active'

										ORDER BY plan_type_id ASC";


                                    $rs_plan_type = mysqli_query($conn, $plan_type);

                                    $si = 1;
                                    while ($plan_type_row = mysqli_fetch_array($rs_plan_type)) {

                                        if ($plan_type_row['plan_type_duration'] >= 7) {
                                            $date_text = "/year";
                                        } else {
                                            $date_text = "/month";
                                        }

                                        ?>
                                        <option
                                            value="<?php echo $plan_type_row['plan_type_id']; ?>"><?php echo $plan_type_row['plan_type_name'];
                                            if ($plan_type_row['plan_type_price'] != 0) {
                                                echo ' - ' . $footer_row['currency_symbol'] . '' . $plan_type_row['plan_type_price'] . $date_text;
                                            } ?></option>
                                        <?php
                                    }
                                    ?>
                                </select>
                                <a href="pricing-details" class="frmtip"
                                   target="_blank"><?php echo $BIZBOOK['PLAN_DETAILS']; ?></a>
                            </div>
                            <button type="submit" name="register_submit"
                                    class="btn btn-primary"><?php echo $BIZBOOK['REGISTER_NOW']; ?></button>
                        </form>
                        <?php
                        if ($footer_row['admin_google_login'] == 1 || $footer_row['admin_facebook_login'] == 1) {
                            ?>
                            <!-- SOCIAL MEDIA LOGIN -->
                            <div class="soc-log">
                                <ul>
                                    <?php
                                    if ($footer_row['admin_google_login'] == 1) {
                                        ?>
                                        <li>
                                            <div class="g-signin2" data-onsuccess="onSignIn"></div>

                                        </li>
                                        <?php
                                    }
                                    if ($footer_row['admin_facebook_login'] == 1) {
                                        ?>
                                        <li>
                                            <a href="javascript:void(0);" onclick="fbLogin();" class="login-fb"><img
                                                    src="images/icon/facebook.png"> <?php echo $BIZBOOK['CONTINUE_WITH_FACEBOOK']; ?>
                                            </a>
                                        </li>
                                        <?php
                                    }
                                    ?>

                                </ul>

                            </div>
                            <!-- END SOCIAL MEDIA LOGIN -->
                            <?php
                        }
                        ?>
                    </div>
                </div>
                <div class="log log-3">
                    <div class="login login-new">
                        <?php
                        if (isset($_SESSION['forgot_status_msg'])) {
                            include "page_level_message.php";
                            unset($_SESSION['forgot_status_msg']);
                        }
                        ?>
                        <h4><?php echo $BIZBOOK['FORGOT_PASSWORD']; ?></h4>
                        <form id="forget_form" name="forget_form" method="post" action="forgot_process.php">
                            <div class="form-group">
                                <input type="email" autocomplete="off" name="email_id" id="email_id"
                                       class="form-control" placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>"
                                       pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>" required>
                            </div>
                            <button type="submit" name="forgot_submit"
                                    class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
                        </form>
                    </div>
                </div>
                <div class="log-bot">
                    <ul>
                        <li>
                            <span class="ll-1"><?php echo $BIZBOOK['LOGIN_QUESTIONMARK']; ?></span>
                        </li>
                        <li>
                            <span class="ll-2"><?php echo $BIZBOOK['CREATE_ACCOUNT_QUESTIONMARK']; ?></span>
                        </li>
                        <li>
                            <span class="ll-3"><?php echo $BIZBOOK['FORGOT_PASSWORD_QUESTIONMARK']; ?></span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>
<!--END PRICING DETAILS-->


<section>
    <div class="pop-ups pop-quo">
        <!-- The Modal -->
        <div class="modal fade" id="quote">
            <div class="modal-dialog">
                <div class="modal-content">
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                    <!-- Modal Header -->
                    <div class="quote-pop">
                        <h4><?php echo $BIZBOOK['LEAD-GET-QUOTE']; ?></h4>
                        <form>
                            <div class="form-group">
                                <input type="text" class="form-control"
                                       placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>" required>
                            </div>
                            <div class="form-group">
                                <input type="email" class="form-control"
                                       placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>"
                                       pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>" required>
                            </div>
                            <div class="form-group">
                                <input type="text" class="form-control"
                                       placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>"
                                       pattern="[7-9]{1}[0-9]{9}"
                                       title="Phone number starting with 7-9 and remaining 9 digit with 0-9" required>
                            </div>
                            <div class="form-group">
                                <textarea class="form-control" rows="3"
                                          placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<?php
include "footer.php";
?>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>

<?php
if (isset($_GET["page"])) {
    ?>
    <?php
    if (isset($_POST['SubmitButton'])) { // Check if form was submitted

        if (!empty($_FILES['inputText']['name'])) {
            $file = rand(1000, 100000) . $_FILES['inputText']['name'];
            $file_loc = $_FILES['inputText']['tmp_name'];
            $file_size = $_FILES['inputText']['size'];
            $file_type = $_FILES['inputText']['type'];
            $folder = "images/listings/";
            $new_size = $file_size / 1024;
            $new_file_name = strtolower($file);
            $event_image = str_replace(' ', '-', $new_file_name);
            //move_uploaded_file($file_loc, $folder . $event_image);
            $inputText1 = compressImage($event_image, $file_loc, $folder, $new_size);
            $inputText = $inputText1;
        }
    }
    ?>
    <form action="#" enctype="multipart/form-data" method="post">
        <input type="file" name="inputText"/>
        <input type="submit" name="SubmitButton"/>
    </form>
    <?php
}
?>
</body>
</html>