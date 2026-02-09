<?php
include "header.php";
?>
<!-- START -->
<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg">
    <div class="container">
        <div class="row">
            <div class="login-main add-list posr">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst"><?php echo $BIZBOOK['pg_faq_head']; ?></span>
                <div class="log log-1">
                    <div class="login">
                        <h4><?php echo $BIZBOOK['pg_faq_tit']; ?></h4>
                        <p><?php echo $BIZBOOK['pg_faq_sub_tit']; ?></p>
                        <div class="col-md-12">
                            <div class="how-to-coll">
                                <ul>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_faq_q1']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_faq_a1']; ?></p>
                                        </div>
                                    </li>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_faq_q2']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_faq_a2']; ?></p>
                                        </div>
                                    </li>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_faq_q3']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_faq_a3']; ?></p>
                                        </div>
                                    </li>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_faq_q4']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_faq_a4']; ?></p>
                                        </div>
                                    </li>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_faq_q5']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_faq_a5']; ?></p>
                                        </div>
                                    </li>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_faq_q6']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_faq_a6']; ?></p>
                                        </div>
                                    </li>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_faq_q7']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_faq_a7']; ?></p>
                                        </div>
                                    </li>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_faq_q8']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_faq_a8']; ?></p>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="col-md-12">
                            <a href="dashboard" class="skip"><?php echo $BIZBOOK['GO_TO_USER_DASHBOARD']; ?> &gt;&gt;</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!--END PRICING DETAILS-->
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