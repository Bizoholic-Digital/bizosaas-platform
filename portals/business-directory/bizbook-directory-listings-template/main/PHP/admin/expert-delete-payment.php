<?php
include "header.php";
?>

<?php if ($footer_row['admin_expert_show'] != 1 || $admin_row['admin_service_expert_options'] != 1) {
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <section class="login-reg">
                <div class="container">
                    <div class="row">
                        <div class="login-main add-list add-ncate">
                            <div class="log-bor">&nbsp;</div>
                            <span class="udb-inst">Delete This Expert Payment</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Delete This Expert Payment</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $payment_id = $_GET['row'];
                                    $row = getExpertPayments($payment_id);
                                    ?>
                                    <form name="category_form" id="category_form" method="post"
                                          action="trash_expert_payment.php" class="cre-dup-form cre-dup-form-show"
                                          enctype="multipart/form-data">
                                        <input type="hidden" class="validate" id="payment_id" name="payment_id" value="<?php echo $row['payment_id']; ?>" required="required">

                                        <ul>
                                            <li>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" id="payment_name" name="payment_name" readonly="readonly"
                                                                   value="<?php echo $row['payment_name']; ?>"   class="form-control" placeholder="Payment name *"
                                                                   required>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        </ul>
                                        <button type="submit" name="payment_submit" class="btn btn-primary">Delete
                                        </button>
                                    </form>
                                    <div class="col-md-12">
                                        <a href="expert-payment-accept.php" class="skip">Go to All Expert Payments >></a>
                                    </div>

                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

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
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
</body>

</html>