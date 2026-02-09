<?php
include "header.php";
?>
<?php if ($admin_row['admin_payment_options'] != 1) {
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
                            <span class="udb-inst">Delete This Payment</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Delete Payment</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $transaction_row_code = $_GET['row'];
                                    $transaction_row = getIdTransaction($transaction_row_code);

                                    $transaction_plan_type_id = $transaction_row['plan_type_id'];
                                    $transaction_user_plan_type = getPlanType($transaction_plan_type_id);

                                    ?>
                                    <form name="transaction_form" id="transaction_form" method="post" enctype="multipart/form-data"
                                          action="trash_all_payment.php"  class="cre-dup-form cre-dup-form-show">
                                        <input type="hidden" id="transaction_id" value="<?php echo $transaction_row['transaction_id']; ?>"
                                               name="transaction_id" class="validate">

                                        <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select name="transaction_user_id" required="required" disabled="disabled"
                                                                    class="form-control" id="transaction_user_id">
                                                                <option value="">Choose a user *</option>
                                                                <?php
                                                                foreach (getAllUser() as $row) {

                                                                    ?>
                                                                    <option <?php if($transaction_row['user_id']== $row['user_id']){ echo "selected"; } ?>
                                                                        value="<?php echo $row['user_id']; ?>"><?php echo $row['first_name']; ?></option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" class="form-control" name="transaction_name" readonly
                                                                   value="<?php echo $transaction_user_plan_type['plan_type_name'].' '.'Plan'; ?>" placeholder="transaction name" required>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" class="form-control" name="transaction_code" readonly
                                                                   value="<?php echo $transaction_row['transaction_amount'].' '.$transaction_row['transaction_currency'];?>" placeholder="Offer code" required>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" class="form-control" name="transaction_link" readonly
                                                                   value="<?php echo $transaction_row['transaction_mode'];?>" placeholder="Website link(if online offer)">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" class="form-control" name="transaction_link" readonly
                                                                   value="<?php echo 'Payment Date : '. dateFormatconverter($transaction_row['transaction_cdt']);?>" placeholder="Website link(if online offer)">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->

                                            </li>
                                        </ul>
                                        <button type="submit" name="transaction_submit" class="btn btn-primary">Delete
                                        </button>
                                    </form>

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