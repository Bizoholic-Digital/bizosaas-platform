<?php
include "header.php";
?>

<?php if ($admin_row['admin_appearance_options'] != 1) {
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Features Enable & Disable</span>
                <div class="ud-cen-s2">
                    <h2>Features Enable & Disable</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Features</th>
                            <th>Page</th>
                            <th>Status</th>
                        </tr>
                        </thead>
                        <?php

                        $row_f = getAllFooter();

                        ?>
                        <tbody>
                        <tr>
                            <td>1</td>
                            <td>Mobile App</td>
                            <td>Home page</td>
                            <td>
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="share_button custom-control-input" name="admin_mobile_app_feature" id="admin_mobile_app_feature" <?php if($row_f['admin_mobile_app_feature'] == 1){ echo "checked"; } ?>>
                                    <label class="custom-control-label" for="admin_mobile_app_feature">&nbsp;</label>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td>Get in touch(footer)</td>
                            <td>All page</td>
                            <td>
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="share_button custom-control-input" name="admin_get_in_touch_feature" id="admin_get_in_touch_feature" <?php if($row_f['admin_get_in_touch_feature'] == 1){ echo "checked"; } ?>>
                                    <label class="custom-control-label" for="admin_get_in_touch_feature">&nbsp;</label>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>3</td>
                            <td>Download Free Mobile Apps(footer)</td>
                            <td>All page</td>
                            <td>
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="share_button custom-control-input" name="admin_footer_mobile_app_feature" id="admin_footer_mobile_app_feature" <?php if($row_f['admin_footer_mobile_app_feature'] == 1){ echo "checked"; } ?>>
                                    <label class="custom-control-label" for="admin_footer_mobile_app_feature">&nbsp;</label>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td>4</td>
                            <td>Country list(footer)</td>
                            <td>All page</td>
                            <td>
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="share_button custom-control-input" name="admin_country_list_feature" id="admin_country_list_feature" <?php if($row_f['admin_country_list_feature'] == 1){ echo "checked"; } ?>>
                                    <label class="custom-control-label" for="admin_country_list_feature">&nbsp;</label>
                                </div>
                            </td>
                        </tr>
                        
                        </tbody>
                    </table>
                    <p class="ud-notes">Note: If you don't want any features you can disable now using this options.</p>
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