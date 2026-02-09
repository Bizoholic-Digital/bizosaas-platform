<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

include "dashboard_left_pane.php";

if (file_exists('config/general_user_authentication.php')) {
    include('config/general_user_authentication.php');
}

if (file_exists('config/coupon_page_authentication.php')) {
    include('config/coupon_page_authentication.php');
}

?>
    <!--CENTER SECTION-->
    <div class="ud-main">
   <div class="ud-main-inn ud-no-rhs">
    <div class="ud-cen">
        <div class="log-bor">&nbsp;</div>
        <span class="udb-inst"><?php echo $BIZBOOK['COUPONS']; ?></span>
        <?php include('config/user_activation_checker.php'); ?>
        <div class="ud-cen-s2">
            <?php include "page_level_message.php"; ?>
            <h2><?php echo $BIZBOOK['COUPONS']; ?></h2>
            <a href="add-coupons" class="db-tit-btn"><?php echo $BIZBOOK['COUPON-ADD-NEW-COUPON']; ?></a>
            <ul class="nav nav-tabs">
                <li class="nav-item">
                    <a class="nav-link active" data-toggle="tab" href="#coupon"><?php echo $BIZBOOK['COUPON-ALL-COUPON-DETAILS']; ?></a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-toggle="tab" href="#couponacc"><?php echo $BIZBOOK['COUPON-COUPON-USED-MEMBERS']; ?></a>
                </li>
            </ul>
            <div class="tab-content">
                <div id="coupon" class="container tab-pane active">
                    <div class="db-coupons">
                        <ul>
                            <?php
                            $si = 1;
                            foreach (getAllUserCoupons($_SESSION['user_id']) as $couponrow) {

                                $user_id = $couponrow['coupon_user_id'];

                                $user_coupo_details_row = getUser($user_id);

                                ?>
                                <li>
                                    <div class="db-coup-lhs">
                                        <div class="coup-box">
                                            <div class="coup-box-1">
                                                <div class="s1">
                                                    <div class="lhs">
                                                        <img
                                                            src="images/user/<?php echo $couponrow['coupon_photo']; ?>">
                                                    </div>
                                                    <div class="rhs">
                                                        <h4><?php echo $couponrow['coupon_name']; ?></h4>
                                                    </div>
                                                </div>
                                                <div class="s2">
                                                    <div class="lhs">
                                                        <span><?php echo $BIZBOOK['COUPON-EXPIRES']; ?></span>
                                                        <h6><?php echo dateFormatconverter($couponrow['coupon_end_date']); ?></h6>
                                                        <a href="coupons"><?php echo $BIZBOOK['COUPON-TERMS-CONDITION-APPLY']; ?></a>
                                                    </div>
                                                    <div class="rhs">
                                                        <a href="coupons"><span class="get-coup-btn get-coup-act"><?php echo $BIZBOOK['COUPON-GET-COUPON']; ?></span></a>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="db-coup-rhs">
                                        <h5>
                                            <b><?php echo AddingZero_BeforeNumber(coupon_pageview_count($couponrow['coupon_id'])); ?></b>
                                            <span><?php echo $BIZBOOK['COUPON-MEMBER-ACCESS-THIS-COUPON']; ?></span>
                                        </h5>
                                        <ol>
                                            <li><b><?php echo $BIZBOOK['COUPON-START-DATE-PLACEHOLDER']; ?>:</b> <?php echo dateFormatconverter($couponrow['coupon_start_date']); ?>
                                            </li>
                                            <li><b><?php echo $BIZBOOK['COUPON-EXPIRY-DATE-PLACEHOLDER']; ?>:</b> <?php echo dateFormatconverter($couponrow['coupon_end_date']); ?>
                                            </li>
                                            <li><b><?php echo $BIZBOOK['COUPON-COUPON-CODE-PLACEHOLDER']; ?>:</b> <?php echo $couponrow['coupon_code']; ?></li>
                                            <li>
                                                <a href="edit-coupon?YLYLLE=OOYXZLEAFUK35ATJWJJSFMFJGVPWOVGYMFMFJ188WOVGYMFUKEX82JWJJS&&FMFJGVPWERFGVPWOVGYMFMFJ188WOVGYMFUKEX8=<?php echo $couponrow['coupon_id']; ?>&&JSFMFJG=VPWOVGYMFMFJ188WOVGYMFUKEXMFMFJ177"><?php echo $BIZBOOK['EDIT']; ?></a>
                                                <a href="delete-coupon?YLYLLE=OOYXZLEAFUK35ATJWJJSFMFJGVPWOVGYMFMFJ188WOVGYMFUKEX82JWJJS&&FMFJGVPWERFGVPWOVGYMFMFJ188WOVGYMFUKEX8=<?php echo $couponrow['coupon_id']; ?>&&JSFMFJG=VPWOVGYMFMFJ188WOVGYMFUKEXMFMFJ145"><?php echo $BIZBOOK['DELETE']; ?></a>
                                            </li>
                                        </ol>
                                    </div>
                                </li>
                                <?php
                                $si++;
                            }
                            ?>
                        </ul>
                    </div>
                </div>
                <div id="couponacc" class="container tab-pane fade">
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th><?php echo $BIZBOOK['S_NO']; ?></th>
                            <th><?php echo $BIZBOOK['NAME']; ?></th>
                            <th><?php echo $BIZBOOK['EMAIL']; ?></th>
                            <th><?php echo $BIZBOOK['PHONE']; ?></th>
                            <th><?php echo $BIZBOOK['COUPON-COUPON-NAME-PLACEHOLDER']; ?></th>
                            <th><?php echo $BIZBOOK['PROFILE']; ?></th>
                            <th><?php echo $BIZBOOK['DELETE']; ?></th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllUserCouponsUsed($_SESSION['user_id']) as $coupon_used_row) {

                            $user_id = $coupon_used_row['coupon_user_id'];
                            $coupon_use_members = $coupon_used_row['coupon_use_members'];
                            $coupon_name = $coupon_used_row['coupon_name'];

                            $user_coupo_details_row = getUser($coupon_use_members);

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $user_coupo_details_row['first_name'];?>
                                    <span><?php echo dateFormatconverter($user_coupo_details_row['user_cdt']); ?></span>
                                </td>
                                <td><?php echo $user_coupo_details_row['email_id']; ?></td>
                                <td><?php echo $user_coupo_details_row['mobile_number']; ?></td>
                                <td><?php echo $coupon_name;?></td>
                                <td><a href="<?php echo $PROFILE_URL.urlModifier($user_coupo_details_row['user_slug']); ?>" target="_blank" class="db-list-edit"><?php echo $BIZBOOK['VIEW']; ?></a></td>
                                <td><a href="" class="db-list-edit"><?php echo $BIZBOOK['DELETE']; ?></a></td>
                            </tr>
                            <?php
                            $si++;
                        }
                        ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    <!--RIGHT SECTION-->
<?php
include "dashboard_right_pane.php";
?>