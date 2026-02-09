<?php
include "header.php";
?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash adda-oly leftpadd">

            <!--            User Welcome Div starts -->

            <div class="ad-dash-s1">
                <div class="cd-cen-intr-inn cd-cen-intr-inn2">
                    <h2>Welcome to <b>Bizbook activation</b></h2>
                    <p>Easy to activate and enjoy our Bizbook template.</p>
                </div>
            </div>

            <!--User Welcome Div ends -->
            <?php include "../page_level_message.php"; ?>
            <div class="biz-updates">
                <div class="ud-notes">
                    <p><b>Notes:</b> Enter your purchase code to the below box and activate your Bizbook Directory
                        template. Once you use your purchase code for your domain means you can't use the same purchase
                        code to another domain. Your purchase code only for one domain not for multi-domain use.</p>
                </div>
                <div class="templ-acti">
                    <form name="activation_form" id="activation_form" action="update_activation.php" method="post"
                          class="cre-dup-form cre-dup-form-show">
                        <ul>
                            <li>
                                <input type="text" name="purchase_code" id="purchase_code" required="required" autocomplete="off"
                                       placeholder="Enter your purchase code.">
                                <button type="submit" name="code_activation_submit" class="btn btn-primary">Submit
                                </button>
                            </li>
                        </ul>
                    </form>
                </div>
                <div class="inn">
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th>Domain</th>
                            <th>Purchase code</th>
                            <th>Installation date</th>
                            <th>Activate date</th>
                            <th>Expiry date</th>
                            <th>Activation</th>
<!--                            <th>De-Activation</th>-->
                        </tr>
                        </thead>
                        <tbody>
                        <?php

                        $admin_sql_row = getAllSuperAdmin();

                        $activation_date = $admin_sql_row['activation_date'];
                        $activation_code = $admin_sql_row['activation_code'];
                        $expiry_date = $admin_sql_row['expiry_date'];
                        $activation_status = $admin_sql_row['activation_status'];

                        ?>
                        <tr>
                            <td><?php echo $webpage_full_link; ?></td>
                            <td><?php if($activation_code != ''){ echo $activation_code;}else { echo "N/A"; } ?></td>
                            <td><?php echo filedateFormatconverter();?></td>
                            <td><?php if($activation_date != '0000-00-00 00:00:00') { echo dateFormatconverter($activation_date); } else { echo 'N/A'; }?></td>
                            <td><?php if($expiry_date != '0000-00-00 00:00:00') { echo dateFormatconverter($expiry_date); } else { echo 'N/A'; }?></td>
                            <td><span class="btn-sml <?php if($activation_status == 1) { ?>btn-c-gre <?php }else{ ?>btn-c-red <?php } ?>"><?php if($activation_status == 1) { echo "Yes"; } else { echo "No"; }?></span></td>
<!--                            <td><span class="btn-sml btn-c-red">De-activate </span></td>-->
                        </tr>
                        </tbody>
                    </table>
                </div>
            </div>

        </div>
    </div>
</section>

<!-- END -->

<!-- END -->

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="../js/jquery.min.js"></script>
<script src="../js/popper.min.js"></script>
<script src="../js/bootstrap.min.js"></script>
<script src="../js/jquery-ui.js"></script>
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
<?php httpPost("http://directoryfinder.net/updation/updation_wizard.php", $data_array); ?>
</body>

</html>