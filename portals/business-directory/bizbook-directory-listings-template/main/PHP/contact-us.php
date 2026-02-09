<?php
include "header.php";
?>
<!-- START -->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> con-us-map">
    <iframe
        src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d12566588.694179254!2d-89.26650700000002!3d39.739318!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x880b2d386f6e2619%3A0x7f15825064115956!2sIllinois%2C%20USA!5e0!3m2!1sen!2sin!4v1584780817502!5m2!1sen!2sin"
        allowfullscreen="" aria-hidden="false" tabindex="0"></iframe>
</section>
<!--END-->

<!-- START -->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> con-us-loc">
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <div class="tit">
                    <h2><?php echo $BIZBOOK['pg_contus_tit']; ?></h2>
                    <p><?php echo $BIZBOOK['pg_contus_tit_sub']; ?></p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="con-pg-addr ">
                    <h4><?php echo $BIZBOOK['pg_contus_addre']; ?></h4>
                    <h5><?php echo $BIZBOOK['pg_contus_cont1']; ?></h5>
                    <p><?php echo $BIZBOOK['pg_contus_cont1_addr']; ?></p>
                    <h5><?php echo $BIZBOOK['pg_contus_cont2']; ?></h5>
                    <p><?php echo $BIZBOOK['pg_contus_cont2_addr']; ?></p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="con-pg-info">
                    <h4><?php echo $BIZBOOK['pg_contus_coninfo']; ?></h4>
                    <ul>
                        <li class="ic-pho"><?php echo $BIZBOOK['pg_contus_sup_pho']; ?></li>
                        <li class="ic-pho"><?php echo $BIZBOOK['pg_contus_enqu']; ?></li>
                        <li class="ic-eml"><?php echo $BIZBOOK['pg_contus_email1']; ?></li>
                        <li class="ic-eml"><?php echo $BIZBOOK['pg_contus_email2']; ?></li>
                    </ul>
                </div>
            </div>
            <div class="col-md-4">
                <div class="con-pg-soc">
                    <h4><?php echo $BIZBOOK['pg_contus_web_tit']; ?></h4>
                    <ul>
                        <li class="ic-man-web"><a href="<?php echo $BIZBOOK['pg_contus_web_link']; ?>" target="_blank"><?php echo $BIZBOOK['pg_contus_web']; ?></a></li>
                        <li class="ic-man-fb"><a href="<?php echo $BIZBOOK['pg_contus_fb_link']; ?>" target="_blank"><?php echo $BIZBOOK['pg_contus_fb']; ?></a></li>
                        <li class="ic-man-tw"><a href="<?php echo $BIZBOOK['pg_contus_twi_link']; ?>" target="_blank"><?php echo $BIZBOOK['pg_contus_twi']; ?></a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>
<!--END-->
<?php
include "footer.php";
?>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>
</body>

</html>