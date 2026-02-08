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
            <section class="login-reg">
                <div class="container">
                    <div class="row">
                        <div class="login-main add-list posr">
                            <div class="log-bor">&nbsp;</div>
                            <span class="udb-inst">Website logo</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Website Logo</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <form name="logo_form" id="logo_form" method="post" action="update_logo.php"
                                          enctype="multipart/form-data" class="">
                                        <?php
                                        $row_f = getAllFooter();

                                        ?>
                                        <input type="hidden" autocomplete="off" name="footer_id"
                                               value="<?php echo $row_f['footer_id']; ?>" id="footer_id"
                                               class="validate">
                                        <input type="hidden" class="validate" id="header_logo_old"
                                               name="header_logo_old"
                                               value="<?php echo $row_f['header_logo']; ?>" required="required">

                                        <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="file" name="header_logo"
                                                                   accept="image/*,.jpg,.jpeg,.png"
                                                                   class="form-control">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" name="header_logo_width" autocomplete="off"
                                                                   value="<?php echo $row_f['header_logo_width']; ?>"
                                                                   class="form-control"
                                                                   placeholder="Logo width in px(ex: 100px)">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" name="header_logo_height" autocomplete="off"
                                                                   value="<?php echo $row_f['header_logo_height']; ?>"
                                                                   class="form-control"
                                                                   placeholder="Logo height in px(ex: 50px)">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                            </li>
                                        </ul>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <button type="submit" name="logo_form_submit" class="btn btn-primary">
                                                    Update
                                                </button>
                                            </div>
                                        </div>
                                        <!--FILED END-->
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