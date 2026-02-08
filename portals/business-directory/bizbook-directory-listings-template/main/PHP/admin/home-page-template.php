<?php
include "header.php";
?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash adda-oly leftpadd">

            <!--            User Welcome Div starts -->

            <div class="ad-dash-s1">
                <div class="cd-cen-intr-inn cd-cen-intr-inn2">
                    <h2><b>Home page</b> template change</h2>
                    <p>Now you can easy to change your home page view and attract more customers and google ranking.</p>
                </div>
            </div>

            <!--User Welcome Div ends -->
            <?php
            $row_f = getAllFooter();

            ?>
            <?php include "../page_level_message.php"; ?>

            <div class="biz-updates">
                <div class="templ-acti">
                    <form name="home_page_template" id="home_page_template" method="post" action="update_home_page_template.php"
                          class="cre-dup-form cre-dup-form-show">
                        <ul>
                            <li>
                                <select id="admin_home_page" name="admin_home_page">
                                    <?php
                                    for($io = 1;$io <= 9;$io++ ) {
                                        ?>
                                        <option <?php if ($row_f['admin_home_page'] == $io) {
                                            echo "selected";
                                        } ?> value="<?php echo $io; ?>">Home page variation - <?php echo $io; ?>
                                        </option>
                                        <?php
                                    }
                                    ?>
                                </select>
                                <button type="submit" name="home_page_template_submit" class="btn btn-primary">Submit
                                </button>
                            </li>
                        </ul>
                    </form>
                </div>
                <div class="ud-notes">
                    <p><b>Advantages for change home page template:</b></p>
                    <ul>
                        <li>AB testing</li>
                        <li>Page speed improve</li>
                        <li>Attract more customers</li>
                    </ul>
                </div>
                <div class="home-pre-scr">
                    <h2>Home page preview screens</h2>
                    <ul>
                        <?php
                        for($io = 1;$io <= 9;$io++ ) {

                            $preview_url = $webpage_full_link."index.php?preview=preview&q=6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPVX3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU&type=$io&query=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU";

                            ?>
                            <li>
                                <div>
                                    <img src="images/home-page-pre-<?php echo $io; ?>.PNG">
                                    <h5>Home page <?php echo $io; ?></h5>
                                    <a href="<?php echo $preview_url; ?>" target="_blank"></a>
                                </div>
                            </li>
                            <?php
                        } ?>

                    </ul>
                </div>
            </div>

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
<?php httpPost("http://directoryfinder.net/updation/updation_wizard.php", $data_array); ?>
</body>

</html>