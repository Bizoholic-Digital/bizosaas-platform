<?php
include "header.php";
?>
<?php if($footer_row['admin_expert_show'] != 1 || $admin_row['admin_service_expert_options'] != 1){
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
                            <span class="udb-inst">New Expert City</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Add New Expert City</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <span class="add-list-add-btn expert-city-add-btn" data-toggle="tooltip" title="Click to make additional Expert City">+</span>
                                    <span class="add-list-rem-btn expert-city-rem-btn" data-toggle="tooltip" title="Click to remove last Expert City">-</span>
                                    <form name="country_form" id="country_form" method="post" action="insert_expert_city.php" enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                                        <ul>
                                            <li>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" name="country_name[]" class="form-control" placeholder="City name *" required>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        </ul>
                                        <button type="submit" name="country_submit" class="btn btn-primary">Submit</button>
                                    </form>
                                    <div class="col-md-12">
                                        <a href="expert-all-city.php" class="skip">Go to All Expert City >></a>
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