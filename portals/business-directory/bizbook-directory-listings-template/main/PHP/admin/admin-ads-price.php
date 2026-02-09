<?php
include "header.php";
?>
<?php if($admin_row['admin_ads_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
                     <div class="log-bor">&nbsp;</div>
                    <span class="udb-inst">Ad details</span>
                    <div class="ud-cen-s2 ad-table-inn">
                    <h2>Ad Pricing and other details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered">
                        <thead>
                            <tr>
                                <th>No</th>
                                <th>Ads Name</th>
                                <th>Ads Preview</th>
                                <th>Ads Size</th>
                                <th>Cost P/Day</th>
                                <th>Status</th>
                                <th>Edit</th>
                            </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si =1;
                        foreach (getAllAdsPrice() as $row) {

                            $all_ads_price_id = $row['all_ads_price_id'];

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $row['ad_price_name']; ?></td>
                                <td>
                                    <img src="../images/ads/<?php echo $row['ad_price_photo']; ?>" alt="">
                                </td>
                                <td><?php echo $row['ad_price_size']; ?></td>
                                <td><?php echo $row['ad_price_cost']; ?><?php echo $footer_row['currency_symbol']; ?></td>
                                <td><span class="db-list-rat"><?php echo $row['ad_price_status']; ?></span></td>
                                <td><a href="admin-ads-price-edit.php?row=<?php echo $row['all_ads_price_id']; ?>" class="db-list-edit">Edit</a></td>
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