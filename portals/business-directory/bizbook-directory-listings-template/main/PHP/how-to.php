<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

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
                <span class="udb-inst">How tos</span>
                <div class="log log-1">
                    <div class="login">
                        <h4><?php echo $BIZBOOK['pg_howto_tit']; ?></h4>
                        <p><?php echo $BIZBOOK['pg_howto_sub_tit']; ?></p>
                        <div class="col-md-12">
                            <div class="how-to-coll">
                                <ul>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_howto_q1']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_howto_a1']; ?></p>
                                        </div>
                                    </li>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_howto_q2']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_howto_a2']; ?></p>
                                        </div>
                                    </li>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_howto_q3']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_howto_a3']; ?></p>
                                        </div>
                                    </li>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_howto_q4']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_howto_a4']; ?></p>
                                        </div>
                                    </li>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_howto_q5']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_howto_a5']; ?></p>
                                        </div>
                                    </li>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_howto_q6']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_howto_a6']; ?></p>
                                        </div>
                                    </li>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_howto_q7']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_howto_a7']; ?></p>
                                        </div>
                                    </li>
                                    <li>
                                        <h4><?php echo $BIZBOOK['pg_howto_q8']; ?></h4>
                                        <div>
                                            <p><?php echo $BIZBOOK['pg_howto_a8']; ?></p>
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
</body>

</html>