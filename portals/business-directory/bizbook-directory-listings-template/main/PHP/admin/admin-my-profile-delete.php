<?php
include "header.php";
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">User Delete Details</span>
                <div class="ud-cen-s2 ud-pro-edit">
                    <h2>Delete Profile details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <?php
                    $path_id = $_GET['path'];
                    $user_id = $_GET['row'];

                    $user_details_row = getUser($user_id);

                    ?>
                    <form name="register_form" id="register_form" method="post" action="trash_user_profile.php" enctype="multipart/form-data" class="">

                        <input type="hidden" autocomplete="off" name="trap_box" id="trap_box" class="validate">
                        <input type="hidden" autocomplete="off" name="user_id" value="<?php echo $user_details_row['user_id']; ?>" id="user_id" class="validate">
                        <input type="hidden" autocomplete="off" name="path_id" value="<?php echo $path_id; ?>" id="path_id" class="validate">

                        <input type="hidden" autocomplete="off" name="mode_path" value="XeBaCk_MoDeX_PATHXHU" id="mode_path" class="validate">
                        <input type="hidden" value="<?php echo $user_details_row['profile_image']; ?>" autocomplete="off" name="profile_image_old" id="profile_image_old" required class="validate">

                        <table class="responsive-table bordered">
                            <tbody>
                            <tr>
                                <td>Name</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" readonly="readonly" value="<?php echo $user_details_row['first_name']; ?>" required="required" autocomplete="off" name="first_name" id="first_name" class="form-control">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Email id</td>
                                <td>
                                    <div class="form-group">
                                        <input type="email" readonly="readonly" value="<?php echo $user_details_row['email_id']; ?>"  required="required" autocomplete="off" name="email_id" id="email_id" class="form-control" >
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Profile password</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" readonly="readonly" autocomplete="off" required="required" value="<?php echo $user_details_row['password']; ?>" name="password" id="password" class="form-control" >
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Mobile number</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" readonly="readonly" value="<?php echo $user_details_row['mobile_number']; ?>" required="required" autocomplete="off" name="mobile_number" id="mobile_number" class="form-control">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>City</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" readonly="readonly" value="<?php echo $user_details_row['user_city']; ?>" class="form-control" name="user_address">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Facebook</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" readonly="readonly" value="<?php echo $user_details_row['user_facebook']; ?>" name="user_facebook" class="form-control" >
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Twitter</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" readonly="readonly" value="<?php echo $user_details_row['user_twitter']; ?>" name="user_twitter" class="form-control" >
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Youtube</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" readonly="readonly" value="<?php echo $user_details_row['user_youtube']; ?>" name="user_youtube" class="form-control" >
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Website</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" readonly="readonly"  value="<?php echo $user_details_row['user_website']; ?>" name="user_website" class="form-control" >
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <button type="submit" name="register_submit" class="db-pro-bot-btn">Delete User</button>
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