<?php
include "header.php";
?>
<!-- START -->
<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg user-type">
    <div class="container">
        <div class="row">
            <div class="user-tcon">
                <div class="user-tc-img">
                    <img src="images/user-type.png" alt="">
                </div>
                <div class="user-tc-diff">
                    <ul>
                        <li>
                            <div class="pri-box">
                                <div class="c6">
                                    <img src="images/icon/service.png" alt="">
                                    <h4><?php echo $BIZBOOK['pg_utype_tit1']; ?></h4>
                                </div>
                                <div class="c4">
                                    <ol>
                                        <li><?php echo $BIZBOOK['pg_utype_sp1']; ?></li>
                                        <li><?php echo $BIZBOOK['pg_utype_sp2']; ?></li>
                                        <li><?php echo $BIZBOOK['pg_utype_sp3']; ?></li>
                                        <li><?php echo $BIZBOOK['pg_utype_sp4']; ?></li>
                                        <li><?php echo $BIZBOOK['pg_utype_sp5']; ?></li>
                                        <li><?php echo $BIZBOOK['pg_utype_sp6']; ?></li>
                                        <li><?php echo $BIZBOOK['pg_utype_sp7']; ?></li>
                                        <li><?php echo $BIZBOOK['pg_utype_sp8']; ?></li>
                                    </ol>
                                </div>
                                <div class="c5">
                                    <a href="login"><?php echo $BIZBOOK['pg_utype_start']; ?></a>
                                </div>
                            </div>
                        </li>
                        <li>
                            <div class="pri-box">
                                <div class="c6">
                                    <img src="images/icon/general.png" alt="">
                                    <h4><?php echo $BIZBOOK['pg_utype_tit2']; ?></h4>
                                </div>
                                <div class="c4">
                                    <ol>
                                        <li><?php echo $BIZBOOK['pg_utype_gp1']; ?></li>
                                        <li><?php echo $BIZBOOK['pg_utype_gp2']; ?></li>
                                        <li><?php echo $BIZBOOK['pg_utype_gp3']; ?></li>
                                        <li><?php echo $BIZBOOK['pg_utype_gp4']; ?></li>
                                        <li><?php echo $BIZBOOK['pg_utype_gp5']; ?></li>
                                        <li class="no"><?php echo $BIZBOOK['pg_utype_gp6']; ?></li>
                                        <li class="no"><?php echo $BIZBOOK['pg_utype_gp7']; ?></li>
                                        <li class="no"><?php echo $BIZBOOK['pg_utype_gp8']; ?></li>
                                    </ol>
                                </div>
                                <div class="c5">
                                    <a href="login"><?php echo $BIZBOOK['pg_utype_start']; ?></a>
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>
<!--END PRICING DETAILS-->


<section>
    <div class="pop-ups pop-quo">
        <!-- The Modal -->
        <div class="modal fade" id="quote">
            <div class="modal-dialog">
                <div class="modal-content">
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                    <!-- Modal Header -->
                    <div class="quote-pop">
                        <h4><?php echo $BIZBOOK['LEAD-GET-QUOTE']; ?></h4>
                        <form>
                            <div class="form-group">
                                <input type="text" class="form-control" placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>" required>
                            </div>
                            <div class="form-group">
                                <input type="email" class="form-control" placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>"
                                       pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>" required>
                            </div>
                            <div class="form-group">
                                <input type="text" class="form-control" placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>"
                                       pattern="[7-9]{1}[0-9]{9}"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>" required>
                            </div>
                            <div class="form-group">
                                <textarea class="form-control" rows="3"
                                          placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
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