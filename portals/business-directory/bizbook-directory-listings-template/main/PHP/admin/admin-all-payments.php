<?php
include "header.php";
?>

<?php if($admin_row['admin_payment_options'] != 1){
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">All Payments</span>
                <div class="ud-cen-s2">
                    <h2>All Payments</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>User</th>
                            <th>Plan</th>
                            <th>Payment Amount</th>
                            <th>Payment Mode</th>
                            <th>Payment Date</th>
                            <th>Invoice</th>
                            <th>Create Invoice</th>
                            <th>Delete</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllTransaction() as $row) {

                            $transaction_plan_type_id = $row['plan_type_id'];
                            $transaction_user_plan_type = getPlanType($transaction_plan_type_id);
                            $user_details1 = getUser($row['user_id']);

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><img src="../images/user/<?php if(($user_details1['profile_image'] == NULL) || empty($user_details1['profile_image'])){  echo $footer_row['user_default_image'];}else{ echo $user_details1['profile_image']; } ?>" alt=""><?php echo $user_details1['first_name']; ?><span><?php echo $user_details1['email_id']; ?></span><span>Join:<?php echo dateFormatconverter($user_details1['user_cdt']); ?></span>
                                </td>
                                <td><?php echo $transaction_user_plan_type['plan_type_name'].' '.'Plan'; ?></td>
                                <td><?php echo $row['transaction_amount'].' '.$row['transaction_currency'];?></td>
                                <td><?php echo $row['transaction_mode'];?></td>
                                <td><?php echo dateFormatconverter($row['transaction_cdt']);?></td>
                                <?php
                                if($row['transaction_invoice'] != NULL || !empty($row['transaction_invoice'])) {
                                    ?>
                                    <td><a href="../images/invoices/<?php echo $row['transaction_invoice']; ?>"
                                           download="<?php echo $user_details1['first_name']; ?>-Invoice-<?php echo strtotime($row['transaction_cdt']); ?>"
                                           class="db-invo-dwn">Download Invoice</a></td>
                                    <td><a href="#" class="db-list-rat"> N/A </a></td>
                                    <?php
                                }else {
                                    ?>
                                    <td>N/A</td>
                                    <td><a href="admin-invoice-create.php" class="db-list-rat">Send</a></td>

                                    <?php
                                }
                                ?>
                                <td><a href="admin-all-payment-delete.php?row=<?php echo $row['transaction_id']; ?>&path=1" class="db-list-edit">Delete</a></td>
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