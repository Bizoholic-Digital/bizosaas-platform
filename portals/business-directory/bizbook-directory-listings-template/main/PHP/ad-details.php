<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

?>
<!-- START -->
<!--PRICING DETAILS-->
<section class="login-reg <?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?>">
    <div class="container">
        <div class="row">
            <div class="login-main add-list ad-table">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['AD-DETAILS']; ?></span>
                <div class="ad-table-inn ud-cen-s2">
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th><?php echo $BIZBOOK['S_NO']; ?></th>
                            <th><?php echo $BIZBOOK['AD-DETAILS-ADS-NAME']; ?></th>
                            <th><?php echo $BIZBOOK['AD-DETAILS-ADS-PREVIEW']; ?></th>
                            <th><?php echo $BIZBOOK['AD-DETAILS-ADS-SIZE']; ?></th>
                            <th><?php echo $BIZBOOK['AD-DETAILS-COST-DAY']; ?></th>
                            <th><?php echo $BIZBOOK['AD-DETAILS-START-ADS']; ?></th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllAdsPrice() as $row) {

                            $all_ads_price_id = $row['all_ads_price_id'];

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $row['ad_price_name']; ?></td>
                                <td>
                                    <img src="images/ads/<?php echo $row['ad_price_photo']; ?>" alt="">
                                </td>
                                <td><?php echo $row['ad_price_size']; ?></td>
                                <td><?php echo $row['ad_price_cost']; ?><?php echo $footer_row['currency_symbol']; ?></td>
                                <td><a href="post-your-ads" class="db-list-rat"><?php echo $BIZBOOK['AD-DETAILS-POST-YOUR-ADS']; ?></a></td>
                            </tr>
                            <?php
                            $si++;
                        }
                        ?>
                        </tbody>
                    </table>
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
</body>

</html>