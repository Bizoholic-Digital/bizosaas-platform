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
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Social media share options</span>
                <div class="ud-cen-s2">
                    <h2>Share options</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Social media</th>
                            <th>Status</th>
                        </tr>
                        </thead>
                        <?php

                        $row_f = getAllFooter();

                        ?>
                        <tbody>
                        <tr>
                            <td>1</td>
                            <td>Facebook</td>
                            <td>
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="share_button custom-control-input" name="admin_share_facebook" id="admin_share_facebook" <?php if($row_f['admin_share_facebook'] == 1){ echo "checked"; } ?>>
                                    <label class="custom-control-label" for="admin_share_facebook">&nbsp;</label>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td>Twitter</td>
                            <td>
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="share_button custom-control-input" name="admin_share_twitter" id="admin_share_twitter" <?php if($row_f['admin_share_twitter'] == 1){ echo "checked"; } ?>>
                                    <label class="custom-control-label" for="admin_share_twitter">&nbsp;</label>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td>WhatsApp</td>
                            <td>
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="share_button custom-control-input" name="admin_share_whatsapp" id="admin_share_whatsapp" <?php if($row_f['admin_share_whatsapp'] == 1){ echo "checked"; } ?>>
                                    <label class="custom-control-label" for="admin_share_whatsapp">&nbsp;</label>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>4</td>
                            <td>LinkedIn</td>
                            <td>
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="share_button custom-control-input" name="admin_share_linkedin" id="admin_share_linkedin" <?php if($row_f['admin_share_linkedin'] == 1){ echo "checked"; } ?>>
                                    <label class="custom-control-label" for="admin_share_linkedin">&nbsp;</label>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>5</td>
                            <td>Pinterest</td>
                            <td>
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="share_button custom-control-input" name="admin_share_pinterest" id="admin_share_pinterest" <?php if($row_f['admin_share_pinterest'] == 1){ echo "checked"; }?>>
                                    <label class="custom-control-label" for="admin_share_pinterest">&nbsp;</label>
                                </div>
                            </td>
                        </tr>
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
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
<script>
    $('.share_button').click(function() {
        var idd = $(this).attr('id');  //-->this will alert id of checked checkbox.
        if(this.checked) {
            var new1 = 1;
        }else{
            var new1 = 0;
        }
        var main_string = idd+new1;
            $.ajax({
                type: "POST",
                url: 'update_social_share.php',
                data: { idd: idd, value1: new1 }, //--> send data of checked checkbox on other page
                success: function(data) {
                    //alert(data);
                },
                error: function() {
                    alert('it broke');
                }
            });

        
    });
</script>
</body>

</html>