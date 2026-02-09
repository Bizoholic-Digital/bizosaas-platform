<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}
//To redirect the general type user to dashboard to avoid using this page

$user_details_row = getUser($_SESSION['user_id']);


?>
<!-- START -->
<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg">
    <div class="container">
        <div class="row">
            <div class="login-main add-list">
                <div class="log-bor">&nbsp;</div>
                <?php
                $transaction_code = $_GET['code'];
                $transaction_details_row = getTransaction($transaction_code); //Get Transaction details

                $transaction_plan_type_id = $transaction_details_row['plan_type_id'];

                $transaction_user_plan_type = getPlanType($transaction_plan_type_id);  //Get Plan Type details

                ?>
                <span class="steps"><?php echo $BIZBOOK['DB-INVOICE-YOUR-NEW-INVOICE']; ?></span>
                <div class="ud-cen-s2 add-list">
                    <div id="content2">
                        <div class="pdf-main">
                            <div class="inn">
                                <div class="head">
                                    <h2><?php echo $transaction_user_plan_type['plan_type_name'] . ' ' . 'Plan'; ?> - <?php echo $BIZBOOK['DB-INVOICE-INVOICE']; ?></h2>
                                </div>
                                <div class="con">
                                    <p><?php echo $BIZBOOK['DB-INVOICE-P-TAG']; ?></p>
                                    <table class="table table-hover">
                                        <tbody>
                                        <tr>
                                            <td><?php echo $BIZBOOK['USER']; ?></td>
                                            <td>:</td>
                                            <td><?php echo $user_details_row['user_contact_name']; ?></td>
                                        </tr>
                                        <tr>
                                            <td><?php echo $BIZBOOK['DB-INVOICE-PLAN-TYPE']; ?></td>
                                            <td>:</td>
                                            <td><?php echo $transaction_user_plan_type['plan_type_name'] . ' ' . 'Plan'; ?></td>
                                        </tr>
                                        <tr>
                                            <td><?php echo $BIZBOOK['DB-INVOICE-AMOUNT-PAID'];?></td>
                                            <td>:</td>
                                            <td><?php echo $footer_row['currency_symbol'] . '' . $transaction_details_row['transaction_amount']; ?></td>
                                        </tr>
                                        <tr>
                                            <td><?php echo $BIZBOOK['EMAIL_ID']; ?></td>
                                            <td>:</td>
                                            <td><?php echo $user_details_row['user_contact_email']; ?></td>
                                        </tr>
                                        <tr>
                                            <td><?php echo $BIZBOOK['DB-INVOICE-PAYMENT-TYPE']; ?></td>
                                            <td>:</td>
                                            <td><?php echo $BIZBOOK['CASH_ON_DELIVERY'];?></td>
                                        </tr>
                                        <tr>
                                            <td><?php echo $BIZBOOK['PROFILE'];?></td>
                                            <td>:</td>
                                            <td><?php echo $PROFILE_URL . urlModifier($user_details_row['user_slug']); ?></td>
                                        </tr>
                                        <tr>
                                            <td><?php echo $BIZBOOK['ADDRESS'];?></td>
                                            <td>:</td>
                                            <td><?php echo $user_details_row['user_address']; ?></td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="but">
                                    <p><?php echo $BIZBOOK['DB-INVOICE-P-TAG-BOTTOM']; ?></p>
                                </div>
                                <div class="foot">
                                    <p><?php echo $BIZBOOK['DB-INVOICE-FOOT-BOTTOM']; ?> <?php echo $footer_row['website_address']; ?></p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button class="btn-mpdf" id="downloadPDF"><?php echo $BIZBOOK['DB-INVOICE-CLICK-TO-DOWNLOAD-PDF']; ?></button>

                </div>
            </div>
        </div>
    </div>
</section>
<!--END PRICING DETAILS-->


<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="admin/js/dom-to-image.min.js"></script>
<script src="admin/js/jspdf.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<?php
if (isset($_GET['pord'])) {
    dbUpdateDropNew($conn);
}
?>
</body>

</html>