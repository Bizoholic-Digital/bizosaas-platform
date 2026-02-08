<?php
include "header.php";
?>
<?php if ($admin_row['admin_invoice_options'] != 1) {
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
                            <span class="udb-inst">Send Invoice</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Send Invoice</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <form name="send_invoice_form" action="insert_send_invoice.php" enctype="multipart/form-data" id="send_invoice_form" method="post" class="cre-dup-form cre-dup-form-show">
                                        <ul>
                                            <li>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select name="user_code" id="user_code" class="form-control"
                                                                    required="required">
                                                                <option value="" disabled selected>Choose User</option>
                                                                <?php
                                                                foreach (getAllUser() as $ad_users_row) {
                                                                    ?>
                                                                    <option
                                                                        value="<?php echo $ad_users_row['user_code']; ?>"><?php echo $ad_users_row['first_name']; ?></option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                    </br>
                                                    </br>
                                                    </br>
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select name="plan_type_id" id="plan_type_id" class="form-control"
                                                                    required="required">
                                                                <option value="" disabled selected>Choose the plan</option>
                                                                <?php
                                                                foreach (getAllPlanType() as $plan_type_row) {
                                                                    ?>
                                                                    <option
                                                                        value="<?php echo $plan_type_row['plan_type_id']; ?>"><?php echo $plan_type_row['plan_type_name']; ?></option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                    </br>
                                                    </br>
                                                    </br>
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" name="transaction_amount" onkeypress="return isNumber(event)" required="required" class="form-control" placeholder="Invoice Amount *">
                                                        </div>
                                                    </div>
                                                    </br>
                                                    </br>
                                                    </br>
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label>Choose Invoice</label>
                                                            <input type="file" name="invoice_name" class="form-control" required="required">
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        </ul>
                                        <button type="submit" name="invoice_submit" class="btn btn-primary">Submit</button>
                                    </form>
                                    <div class="col-md-12">
                                        <a href="admin-invoice-create.php" class="skip">Go to Create Invoice >></a>
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
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>