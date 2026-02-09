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
        <span class="udb-inst"><?php echo $BIZBOOK['DB-INVOICE-INVOICES']; ?></span>
        <?php include('config/user_activation_checker.php'); ?>
        <div class="ud-cen-s2">
            <h2><?php echo $BIZBOOK['DB-INVOICE-PAYMENT-INVOICE']; ?></h2>
            <?php include "page_level_message.php"; ?>
            <table class="responsive-table bordered">
                <thead>
                <tr>
                    <th><?php echo $BIZBOOK['S_NO']; ?></th>
                    <th><?php echo $BIZBOOK['NAME']; ?></th>
                    <th><?php echo $BIZBOOK['DB-INVOICE-PAYMENT-DATE']; ?></th>
                    <th><?php echo $BIZBOOK['AMOUNT']; ?></th>
                    <th><?php echo $BIZBOOK['DOWNLOAD']; ?></th>
                </tr>
                </thead>
                <tbody>
                <?php
                $si = 1;
                $session_user_id = $_SESSION['user_id'];
                foreach (getAllUserTransaction($session_user_id) as $row) {

                    $transaction_plan_type_id = $row['plan_type_id'];
                    $transaction_user_plan_type = getPlanType($transaction_plan_type_id);
                    $user_details1 = getUser($row['user_id']);
                    ?>

                    <tr>
                        <td><?php echo $si; ?></td>
                        <td><?php echo $transaction_user_plan_type['plan_type_name'].' '.'Plan'; ?></td>
                        <td><?php echo dateFormatconverter($row['transaction_cdt']); ?></td>
                        <td><span class="db-list-rat"><?php echo $footer_row['currency_symbol'] . '' . $row['transaction_amount']; ?></span></td>
                        <?php
                        if($row['transaction_invoice'] != NULL || !empty($row['transaction_invoice'])) {
                            ?>
                            <td><a href="images/invoices/<?php echo $row['transaction_invoice']; ?>"
                                   download="<?php echo $user_details1['first_name']; ?>-Invoice-<?php echo strtotime($row['transaction_cdt']); ?>"
                                   class="db-invo-dwn"><?php echo $BIZBOOK['DB-INVOICE-DOWNLOAD-INVOICE']; ?></a></td>
                            <?php
                        }else {
                            ?>
                            <td><?php echo $BIZBOOK['DB-INVOICE-INVOICE-N_A']; ?></td>
                            <?php
                        }
                            ?>
                    </tr>
                    <?php
                    $si++;
                }
                ?>
                </tbody>
            </table>
        </div>
    </div>
<?php
include "dashboard_right_pane.php";
?>