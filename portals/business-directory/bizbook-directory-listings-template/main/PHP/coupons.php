<?php
include "header.php";

if($footer_row['admin_coupon_show'] != 1) {
    header("Location: ".$webpage_full_link."dashboard");
}
?>
<!-- START -->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> coup-sec">


    <!--<div class="coup-sec1">
        <img src="images/coupon-bg.png">
    </div>-->

            <?php
            if(!isset($_SESSION['user_code']) && empty($_SESSION['user_code'])) {
                ?>

                <div class="plac-hom-ban coup-hom-ban">
        <div class="container">
            <div class="row">
                <div class="plac-hom-ban-inn">
                    <h1><?php echo $BIZBOOK['COUPON-HEADING-LABEL']; ?></h1>
                    <p><?php echo $BIZBOOK['COUPON-HEADING-P-LABEL']; ?></p>
                    <div class="coup-sec-log">
                    <h4><?php echo $BIZBOOK['COUPON-NO-LOGIN-HEADING-LABEL']; ?></h4>
                    <p><?php echo $BIZBOOK['COUPON-NO-LOGIN-P-LABEL']; ?></p>
                    <a href="<?php echo $LOGIN_URL; ?>"><?php echo $BIZBOOK['COUPON-NO-LOGIN-SIGN-IN-NOW']; ?></a>
                </div>
                </div>
            </div>
        </div>
    </div>


                <?php
            }else {
                ?>

     <div class="plac-hom-ban coup-hom-ban">
        <div class="container">
            <div class="row">
                <div class="plac-hom-ban-inn coup-sec2">
                    <h1><?php echo $BIZBOOK['COUPON-HEADING-LABEL']; ?></h1>
                    <p><?php echo $BIZBOOK['COUPON-HEADING-P-LABEL']; ?></p>
                    <div class="plac-hom-search">
                     <span><input type="text" id="tail-se" placeholder="<?php echo $BIZBOOK['COUPON-HEADING-PLACEHOLDER']; ?>"></span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="row">
                <div class="coup-sec3">
                    <ul id="tail-re">
                        <?php
                        foreach (getAllCurrentCoupons() as $couponrow) {

                            ?>
                            <li>
                                <div class="coup-box">
                                    <div class="coup-box-1">
                                        <div class="s1">
                                            <div class="lhs">
                                                <img src="images/user/<?php echo $couponrow['coupon_photo']; ?>">
                                            </div>
                                            <div class="rhs">
                                                <h4><?php echo $couponrow['coupon_name']; ?></h4>
                                            </div>
                                        </div>
                                        <div class="s2">
                                            <div class="lhs">
                                                <span><?php echo $BIZBOOK['COUPON-EXPIRES']; ?></span>
                                                <h6><?php echo dateFormatconverter($couponrow['coupon_end_date']); ?></h6>
                                                <a href="terms-of-use.php" target="_blank"><?php echo $BIZBOOK['COUPON-TERMS-CONDITION-APPLY']; ?></a>
                                            </div>
                                            <div class="rhs">
                                            <span data-id="<?php echo $couponrow['coupon_id']; ?>"
                                                  class="get-coup-btn get-coup-act"><?php echo $BIZBOOK['COUPON-GET-COUPON']; ?></span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="coup-box-2">
                                        <h4><?php echo $BIZBOOK['CONGRATULATIONS']; ?>!</h4>
                                        <p><?php echo $BIZBOOK['COUPON-HERE-CODE-FOR']; ?> <b><?php echo $couponrow['coupon_name']; ?></b></p>
                                        <i><?php echo $couponrow['coupon_code']; ?></i>
                                        <?php
                                        if ($couponrow['coupon_link'] != NULL) {
                                            ?>
                                            <a target="_blank"
                                               href="<?php echo $couponrow['coupon_link']; ?>"><?php echo $BIZBOOK['USER_WEBSITE']; ?></a>
                                            <?php
                                        }
                                        ?>
                                        <span class="coup-back"><?php echo $BIZBOOK['BACK']; ?></span>
                                    </div>
                                </div>
                            </li>
                            <?php
                        }
                        ?>
                    </ul>
                </div>
                <?php
            }
            ?>
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
<script>
    $(document).ready(function () {
        $(".get-coup-act").click(function () {
            $(this).parent().parent().parent().parent().addClass("act");

            var coupon_id = $(this).attr("data-id");
            $.ajax({
                type: 'POST',
                url: '<?php echo $slash; ?>coupon_view_process.php',
                cache: false,
                data: {coupon_id: coupon_id},
                success: function (response) {
                    return true;

                }
            });

        });
        $(".coup-back").click(function () {
            $(this).parent().parent().removeClass("act");
        });
        $("#tail-se").on("keyup", function () {
            var value = $(this).val().toLowerCase();
            $("#tail-re li").filter(function () {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
            });
        });
    });
</script>
</body>

</html>