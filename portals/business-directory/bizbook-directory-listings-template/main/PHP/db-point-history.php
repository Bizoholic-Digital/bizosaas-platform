<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

include "dashboard_left_pane.php";

if (file_exists('config/general_user_authentication.php')) {
    include('config/general_user_authentication.php');
}

delBuyPoints();

?>
    <!--CENTER SECTION-->
    <div class="ud-main">
   <div class="ud-main-inn ud-no-rhs">
    <div class="ud-cen">
        <div class="log-bor">&nbsp;</div>
        <span class="udb-inst"><?php echo $BIZBOOK['POINTS_HISTORY']; ?></span>
        <?php include('config/user_activation_checker.php'); ?>
        <div class="ud-cen-s2">
            <h2><?php echo $BIZBOOK['POINTS_HISTORY']; ?></h2>
            <?php include "page_level_message.php"; ?>
            <a href="buy-points" class="db-tit-btn"><?php echo $BIZBOOK['BUY_MORE_POINTS'];?></a>
            <table class="responsive-table bordered">
                <thead>
                <tr>
                    <th><?php echo $BIZBOOK['S_NO']; ?></th>
                    <th><?php echo $BIZBOOK['PURCHASE_DATE'];?></th>
                    <th><?php echo $BIZBOOK['POINTS'];?></th>
                    <th><?php echo $BIZBOOK['TOTAL_COST'];?></th>
                    <th><?php echo $BIZBOOK['DELETE'];?></th>

                </tr>
                </thead>
                <tbody>
                <?php
                $si = 1;
                $session_user_id = $_SESSION['user_id'];

                foreach (getUserPointsEnquiry($session_user_id) as $row) {

                    $all_points_enquiry_id = $row['all_points_enquiry_id'];

                    $delete_url = "points_enquiry_trash?trash=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV&&code=$all_points_enquiry_id&&type=listing&&trashh=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV";

                    ?>
                    <tr>
                        <td><?php echo $si; ?></td>
                        <td><?php echo dateFormatconverter($row['all_points_cdt']); ?></td>
                        <td><?php echo $row['new_points']; ?></td>
                        <td><?php echo $footer_row['currency_symbol'] . $row['total_cost']; ?></td>
                        <td>
                            <a href="<?php echo $delete_url; ?>">
                                <span style="background-color: #f33d45;" class="db-list-ststus"> <?php echo $BIZBOOK['DELETE'];?> </span>
                            </a>
                        </td>
                    </tr>
                    <?php
                    $si++;
                }
                ?>

                </tbody>
            </table>
        </div>
    </div>
    <!--RIGHT SECTION-->
<?php
include "dashboard_right_pane.php";
?>