<?php
include "header.php";
?>
<!-- START -->
<section class="<?php if($footer_row['admin_language']== 2){ echo "lg-arb";}?> abou-pg abou-pg1">
    <div class="about-ban">
        <h1><?php echo $BIZBOOK['pg_abo_ban_tit']; ?></h1>
        <p><?php echo $BIZBOOK['pg_abo_ban_sub_tit']; ?></p>
    </div>
    <div class="container">
        <div class="row">
            <div class="about-us">
                <p><?php echo $BIZBOOK['pg_abo_sec1']; ?></p>
                <p><?php echo $BIZBOOK['pg_abo_sec2']; ?></p>
            </div>
            <div class="how-wrks">
                <div class="home-tit">
                    <h2><span><?php echo $BIZBOOK['pg_abo_why_tit']; ?></span></h2>
                    <p><?php echo $BIZBOOK['pg_abo_why_sub']; ?></p>
                </div>
                <div class="how-wrks-inn">
                    <ul>
                        <li>
                            <div>
                                <img src="images/icon/how1.png" alt="">
                                <h4><?php echo $BIZBOOK['pg_abo_why_s1_tit']; ?></h4>
                                <p><?php echo $BIZBOOK['pg_abo_why_s1_sub']; ?></p>
                            </div>
                        </li>
                        <li>
                            <div>
                                <img src="images/icon/how2.png" alt="">
                                <h4><?php echo $BIZBOOK['pg_abo_why_s2_tit']; ?></h4>
                                <p><?php echo $BIZBOOK['pg_abo_why_s2_sub']; ?></p>
                            </div>
                        </li>
                        <li>
                            <div>
                                <img src="images/icon/how3.png" alt="">
                                <h4><?php echo $BIZBOOK['pg_abo_why_s3_tit']; ?></h4>
                                <p><?php echo $BIZBOOK['pg_abo_why_s3_sub']; ?></p>
                            </div>
                        </li>
                        <li>
                            <div>
                                <img src="images/icon/how4.png" alt="">
                                <h4><?php echo $BIZBOOK['pg_abo_why_s4_tit']; ?></h4>
                                <p><?php echo $BIZBOOK['pg_abo_why_s4_sub']; ?></p>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="how-wrks how-wrks-2">
                <div class="home-tit">
                    <h2><span><?php echo $BIZBOOK['pg_abo_team_tit']; ?></span></h2>
                    <p><?php echo $BIZBOOK['pg_abo_why_team_sub']; ?></p>
                </div>
                <div class="how-wrks-inn abo-memb">
                    <ul>
                        <li>
                            <div>
                                <img src="images/user/user2.jpg" alt="">
                                <h4><?php echo $BIZBOOK['pg_abo_tem_u1_nam']; ?></h4>
                                <p><?php echo $BIZBOOK['pg_abo_tem_u1_dec']; ?></p>
                            </div>
                        </li>
                        <li>
                            <div>
                                <img src="images/user/user1.jpg" alt="">
                                <h4><?php echo $BIZBOOK['pg_abo_tem_u2_nam']; ?></h4>
                                <p><?php echo $BIZBOOK['pg_abo_tem_u2_dec']; ?></p>
                            </div>
                        </li>
                        <li>
                            <div>
                                <img src="images/user/user3.jpg" alt="">
                                <h4><?php echo $BIZBOOK['pg_abo_tem_u3_nam']; ?></h4>
                                <p><?php echo $BIZBOOK['pg_abo_tem_u3_dec']; ?></p>
                            </div>
                        </li>
                        <li>
                            <div>
                                <img src="images/user/user4.jpg" alt="">
                                <h4><?php echo $BIZBOOK['pg_abo_tem_u4_nam']; ?></h4>
                                <p><?php echo $BIZBOOK['pg_abo_tem_u4_dec']; ?></p>
                            </div>
                        </li>
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
<script type="text/javascript">var webpage_full_link ='<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url ='<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>
</body>

</html>