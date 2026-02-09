<?php
include "header.php";
?>

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
                            <span class="udb-inst">Points Settings</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Points Settings</h4>
                                    <?php
                                    $row_f = getAllFooter();
                                    ?>
                                    <?php include "../page_level_message.php"; ?>
                                    <form name="point_setting_form" id="point_setting_form" method="post" action="update_point_setting.php" enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                                        <ul>

                                            <li>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label>Cost Per Point :</label>
                                                            <input type="text" autocomplete="off" onkeypress="return isNumber(event)" value="<?php echo $row_f['cost_per_point']; ?>" name="cost_per_point" id="cost_per_point" class="form-control" placeholder="Cost per Point *" required>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        </ul>
                                        <button type="submit" name="cost_per_point_submit" class="btn btn-primary">Submit</button>
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