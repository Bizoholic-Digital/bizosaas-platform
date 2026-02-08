<?php
include "header.php";
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">User Full Details</span>
                <div class="ud-cen-s2 ud-sp">
                    <h2>Profile details</h2> <?php include "../page_level_message.php"; ?>
                    <?php
                    $path_id = $_GET['path'];
                    $user_id = $_GET['row'];

                    $user_details_row = getUser($user_id);

                    $user_plan = $user_details_row['user_plan'];

                    $plan_type_row = getPlanType($user_plan);


                    ?>
                    <a href="admin-my-profile-edit.php?row=<?php echo $user_id; ?>" class="db-tit-btn">Edit this
                        profile</a>
                    <table class="responsive-table bordered">
                        <tbody>
                        <tr>
                            <td>Name</td>
                            <td><?php echo $user_details_row['first_name']; ?></td>
                        </tr>
                        <tr>
                            <td>Plan type</td>
                            <td><span class="db-list-rat"><?php if ($user_plan == 0) {
                                        echo "Free";
                                    } else {
                                        echo $plan_type_row['plan_type_name'];
                                    } ?></span></td>
                        </tr>
                        <tr>
                            <td>Plan Start on</td>
                            <td><span class="db-list-ststus"><?php // if ($user_details_row['payment_status'] == 'Paid') {
                                        echo dateFormatconverter($user_details_row['user_cdt']);
                                    //} else { echo "N/A"; } ?></span></td>
                        </tr>
                        <?php
                        //To calculate the expiry date from user created date starts

                        $start_date_timestamp = strtotime($user_details_row['user_cdt']);
                        $plan_type_duration = $plan_type_row['plan_type_duration'];

                        $expiry_date_timestamp = strtotime("+$plan_type_duration months", $start_date_timestamp);

                        $expiry_date = date("Y-m-d h:i:s", $expiry_date_timestamp);

                        //To calculate the expiry date from user created date ends
                        ?>
                        <tr>
                            <td>Plan Expiry on</td>
                            <td><span class="db-list-ststus"><?php //if ($user_details_row['payment_status'] == 'Paid')
                                   // {
                                        echo dateFormatconverter($expiry_date);
                                    //} else { echo "N/A"; } ?></span></td>
                        </tr>
                        <tr>
                            <td>Payment Status</td>
                            <td><span class="db-list-rat"><?php if ($user_details_row['payment_status'] == 'Paid') {
                                        echo "PAID";
                                    }elseif ($user_details_row['payment_status'] == 'COD') {
                                        echo "COD Initiated / Pending";
                                    } elseif ($user_plan_type['plan_type_price'] == 0) {
                                        echo "N/A";
                                    } else {
                                        echo "PENDING";
                                    } ?></span></td>
                        </tr>
                        <tr>
                            <td><?php if ($user_details_row['payment_status'] == 'Paid' || $user_plan_type['plan_type_price'] == 0) { ?>Amount paid <?php }else{ echo "Amount To be paid";}?></td>
                            <td><span class="db-list-rat"><?php if ($user_plan_type['plan_type_price'] == 0) {
                                        echo "FREE";
                                    } else {
                                        echo $footer_row['currency_symbol'] . '' . $user_plan_type['plan_type_price'];
                                    } ?></span></td>
                        </tr>
                        <tr>
                            <td>User Type</td>
                            <td><?php echo $user_details_row['user_type']; ?></td>
                        </tr>
                        <tr>
                            <td>Email id</td>
                            <td><?php echo $user_details_row['email_id']; ?></td>
                        </tr>
                        <tr>
                            <td>Profile password</td>
                            <td><?php echo "*******"; ?></td>
                        </tr>
                        <tr>
                            <td>Mobile number</td>
                            <td><?php echo $user_details_row['mobile_number']; ?></td>
                        </tr>
                        <tr>
                            <td>Profile picture</td>
                            <td><img
                                    src="../images/user/<?php if (($user_details_row['profile_image'] == NULL) || empty($user_details_row['profile_image'])) {
                                        echo "1.jpg";
                                    } else {
                                        echo $user_details_row['profile_image'];
                                    } ?>" alt=""></td>
                        </tr>
                        <tr>
                            <td>Cover Photo</td>
                            <td><img
                                    src="<?php if (($user_details_row['cover_image'] == NULL) || empty($user_details_row['cover_image'])) {
                                        echo "../images/home4.jpg";
                                    } else {
                                        echo "../images/user/".$user_details_row['cover_image'];
                                    } ?>" alt=""></td>
                        </tr>
                        <tr>
                            <td>Id Proof</td>
                            <td><?php if (($user_details_row['profile_id_proof'] == NULL) || empty($user_details_row['profile_id_proof'])) {
                                    echo "N/A";
                                }else{ ?>
                                <img src=" <?php echo "../images/user/".$user_details_row['profile_id_proof']; ?>" alt="">
                                <?php } ?>
                            </td>
                        </tr>
                        <tr>
                            <td>Address</td>
                            <td><?php echo $user_details_row['user_address']; ?></td>
                        </tr>
                        <tr>
                            <td>Join date</td>
                            <td><?php echo dateFormatconverter($user_details_row['user_cdt']); ?></td>
                        </tr>
                        <tr>
                            <td>Verified</td>
                            <td><?php if ($user_details_row['user_status'] == "Active") {
                                    echo "Yes";
                                } else {
                                    echo "No";
                                } ?></td>
                        </tr>
                        <tr>
                            <td>Profile link</td>
                            <td><a href="<?php echo $PROFILE_URL.urlModifier($user_details_row['user_slug']); ?>"
                                   target="_blank"><?php echo $PROFILE_URL.urlModifier($user_details_row['user_slug']); ?></a></td>
                        </tr>
                        <tr>
                            <td>Listings</td>
                            <td><span class="db-list-rat"><?php echo getCountUserListing($user_details_row['user_id']); ?></span></td>
                        </tr>
                        <tr>
                            <td>Blog posts</td>
                            <td><span class="db-list-rat"><?php echo getCountUserBlog($user_details_row['user_id']); ?></span></td>
                        </tr>
                        <tr>
                            <td>Events</td>
                            <td><span class="db-list-rat"><?php echo getCountUserEvent($user_details_row['user_id']); ?></span></td>
                        </tr>
                        <tr>
                            <td>Followers</td>
                            <td><span class="db-list-rat"><?php
                                    if($user_details_row['user_followers'] != NULL) {
                                        $user_followers_array = explode(",", $user_details_row['user_followers']);
                                        echo count($user_followers_array);
                                    }else{ echo 0;}
                                    ?></span></td>
                        </tr>
                        <tr>
                            <td>Facebook</td>
                            <td><?php echo $user_details_row['user_facebook']; ?></td>
                        </tr>
                        <tr>
                            <td>Twitter</td>
                            <td><?php echo $user_details_row['user_twitter']; ?></td>
                        </tr>
                        <tr>
                            <td>Youtube</td>
                            <td><?php echo $user_details_row['user_youtube']; ?></td>
                        </tr>
                        <tr>
                            <td>Website</td>
                            <td><?php echo $user_details_row['user_website']; ?></td>
                        </tr>
                        <tr>
                            <td>Source to join</td>
                            <td><?php if($user_details_row['register_mode'] == "Direct" || $user_details_row['register_mode'] == "" ){ echo "Website"; }else{ echo $user_details_row['register_mode']; } ?></td>
                        </tr>
                        <tr>
                            <td>
                                <a href="admin-my-profile-edit.php?row=<?php echo $user_id; ?>"
                                   class="db-pro-bot-btn">Edit my profile</a>
                            </td>
                            <td></td>
                        </tr>
                        </tbody>
                    </table>

                    <div class="ud-notes">
                        <p><b>Notes about this user:</b> <span contenteditable="true">Click here to write short notes or conversation with this user.(Ex: I spoke him to discuss about advantage of Premium Plan on April 12th 2020.)</span>
                        </p>
                    </div>
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