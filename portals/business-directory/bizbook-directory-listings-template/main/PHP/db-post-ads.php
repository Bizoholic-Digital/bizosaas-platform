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
        <span class="udb-inst"><?php echo $BIZBOOK['AD-DETAILS-PAID-ADS']; ?></span>
        <?php include('config/user_activation_checker.php'); ?>
        <div class="ud-cen-s2">
            <h2><?php echo $BIZBOOK['AD-DETAILS-BANNER-ADS']; ?></h2>
            <?php include "page_level_message.php"; ?>
            <a href="post-your-ads" class="db-tit-btn db-tit-btn-2-ads"><?php echo $BIZBOOK['AD-DETAILS-POST-YOUR-ADS']; ?></a>
            <a href="ad-details" class="db-tit-btn"><?php echo $BIZBOOK['AD-DETAILS-PRICING-OTHER-DETAILS']; ?></a>
            <table class="responsive-table bordered">
                <thead>
                <tr>
                    <th><?php echo $BIZBOOK['S_NO']; ?></th>
                    <th><?php echo $BIZBOOK['AD-DETAILS-ADS-POSITION']; ?></th>
                    <th><?php echo $BIZBOOK['COUPON-START-DATE-PLACEHOLDER']; ?></th>
                    <th><?php echo $BIZBOOK['COUPON-END-DATE-PLACEHOLDER']; ?></th>
                    <th><?php echo $BIZBOOK['DURATION']; ?></th>
                    <th><?php echo $BIZBOOK['STATUS']; ?></th>
                    <th><?php echo $BIZBOOK['VIEWS']; ?></th>
                    <th><?php echo $BIZBOOK['CLICKS']; ?></th>
                </tr>
                </thead>
                <tbody>
                <?php
                $si = 1;
                $session_user_id = $_SESSION['user_id'];
                foreach (getAllUserAdsEnquiry($session_user_id) as $row) {

                    $all_ads_price_id = $row['all_ads_price_id'];

                    $user_id = $row['user_id'];

                    $user_details_row = getUser($user_id);

                    $ads_price_details_row = getAdsPrice($all_ads_price_id);

                    ?>
                    <tr>
                        <td><?php echo $si; ?></td>
                        <td><?php echo $ads_price_details_row['ad_price_name']; ?></td>
                        <td><?php echo dateFormatconverter($row['ad_start_date']);?></td>
                        <td><?php echo dateFormatconverter($row['ad_end_date']);?></td>
                        <td><?php echo $row['ad_total_days']; ?> <?php echo $BIZBOOK['DAYS']; ?></td>
                        <td><span class="db-list-ststus"><?php echo $row['ad_enquiry_status']; ?></span></td>
                        <td><span class="db-list-rat">1k</span></td>
                        <td><span class="db-list-rat">642</span></td>
                    </tr>
                    <?php
                    $si++;
                }
                ?>
                </tbody>
            </table>
            <div class="ud-notes">
                <p><?php echo $BIZBOOK['DB-PAYMENTS-FOOTER-NOTES'];?>: <?php echo $BIZBOOK['DB-PAYMENTS-FOOTER-NOTES-MESSAGE'];?></p>
            </div>
        </div>
    </div>
<?php
include "dashboard_right_pane.php";
?>