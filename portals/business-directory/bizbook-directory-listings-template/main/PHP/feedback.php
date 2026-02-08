<?php
include "header.php";
?>
<!-- START -->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> fedback">
    <img src="images/admin-log-bg.jpg" alt="" class="fed">
    <div class="fed-box">
        <div class="lhs">
            <h3><?php echo $BIZBOOK['FEEDBACK-SEND-YOUR-FEEDBACK']; ?></h3>
            <?php include "page_level_message.php"; ?>
            <form name="feedback_form" id="feedback_form" method="post" action="feedback_submit.php"
                  enctype="multipart/form-data">
                <div class="form-group">
                    <input type="text" placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>" name="feedback_name" id="feedback_name" class="form-control"
                           required="required">
                </div>
                <div class="form-group">
                    <input type="email" class="form-control" placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>" required="required"
                           name="feedback_email"
                           pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                           title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>">
                </div>
                <div class="form-group">
                    <input type="text" onkeypress="return isNumber(event)" class="form-control" id="feedback_mobile"
                           name="feedback_mobile"
                           placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>" pattern="[7-9]{1}[0-9]{9}"
                           title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>" required="">
                </div>
                <div class="form-group">
                    <textarea name="feedback_message" id="feedback_message" required="required"
                              placeholder="<?php echo $BIZBOOK['LEAD-WRITE-YOUR-FEEDBACK-PLACEHOLDER']; ?>"></textarea>
                </div>
                <button type="submit" id="feedback_submit" name="feedback_submit"
                        class="btn btn-primary">
                    <?php echo $BIZBOOK['LEAD-SUBMIT-FEEDBACK']; ?>
                </button>
            </form>
        </div>
        <div class="rhs">
            <h2><?php echo $BIZBOOK['FEEDBACK-YOUR-FEEDBACK']; ?></h2>
            <p><?php echo $BIZBOOK['FEEDBACK-P-TAG-MESSAGE']; ?></p>
            <ul>
                <li><a href="#"><img src="images/icon/facebook.png" alt=""></a></li>
                <li><a href="#"><img src="images/icon/twitter.png" alt=""></a></li>
                <li><a href="#"><img src="images/icon/linkedin.png" alt=""></a></li>
                <li><a href="#"><img src="images/icon/whatsapp.png" alt=""></a></li>
            </ul>
            <h4><?php echo $BIZBOOK['FEEDBACK-WHY-SEND-FEEDBACK']; ?></h4>
            <p><?php echo $BIZBOOK['FEEDBACK-WHY-SEND-FEEDBACK-P-1']; ?></p>
            <p><?php echo $BIZBOOK['FEEDBACK-WHY-SEND-FEEDBACK-P-2']; ?></p>
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