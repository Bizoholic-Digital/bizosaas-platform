<?php
include "header.php";
?>

<?php if ($admin_row['admin_home_options'] != 1) {
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Home page popular business</span>
                <div class="ud-cen-s2 hcat-cho">
                    <h2>Home page popular business</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Listing Name</th>
                            <th>Edit</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;

                        foreach (getAllFeaturedListing() as $row) {

                            $listing_id = $row['listing_id'];

                            $listing_sql_row = getIdListing($listing_id);

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $listing_sql_row['listing_name']; ?></td>
                                <td><a href="admin-home-popular-business-edit.php?row=<?php echo $listing_id; ?>"
                                       class="db-list-edit">Edit</a></td>
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