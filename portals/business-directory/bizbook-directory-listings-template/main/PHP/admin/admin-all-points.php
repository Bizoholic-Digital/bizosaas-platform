<?php
include "header.php";
?>

<?php if($footer_row['admin_listing_show'] != 1 || $admin_row['admin_listing_options'] != 1){
    header("Location: profile.php");
}
?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">All Points History</span>
                <div class="ud-cen-s2">
                    <h2>All Points History details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>User</th>
                            <th>Purchase date</th>
                            <th>Points</th>
                            <th>Total Cost</th>
                            <th>Delete</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllPointsEnquiry() as $row) {

                            $user_id = $row['user_id'];
                            $all_points_enquiry_id = $row['all_points_enquiry_id'];

                            $user_details_row = getUser($user_id);

                            $delete_url = "trash_points_enquiry.php?trash=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV&&code=$all_points_enquiry_id&&type=listing&&trashh=X3BR1GX3E6S4PPLDNTXA6RVUN4UZZI30O6NC8AT40BQRIEKF67NSOE0PEPFU6RVUN4UZZI30O6NC8AT4X3BR1GX3E6S4PPLDNTXAFBQXCPEGZIP3UXDVYKPV";

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $user_details_row['first_name']; ?></td>
                                <td><?php echo dateFormatconverter($row['all_points_cdt']); ?></td>
                                <td><?php echo $row['new_points']; ?></td>
                                <td><?php echo $footer_row['currency_symbol'] . $row['total_cost']; ?></td>
                                <td>
                                    <a href="<?php echo $delete_url; ?>">
                                        <span style="background-color: #f33d45;" class="db-list-ststus"> Delete </span>
                                    </a>
                                </td>
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
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
</body>

</html>