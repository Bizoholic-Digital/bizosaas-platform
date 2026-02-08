<?php
include "header.php";
?>

<?php if ($footer_row['admin_place_show'] !=1) {
    header("Location: profile.php");
}
?>
<style>
    .ud-cen-s2 table tr td img{width: 36px;height: 36px;border-radius: 50%;object-fit: cover;float: left;margin-right: 15px;}
    .ud-cen-s2 table tr td:nth-child(4){width: 250px;}
</style>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">place request</span>
                <div class="ud-cen-s2">
                    <!-- TAB START -->

                    <!-- Tab panes -->
                    <div class="tab-content">
                        <!-- TODAY LEADS -->
                        <div id="home" class="tab-pane active"><br>
                            <h2>New place request</h2>
                            <?php include "../page_level_message.php"; ?>
                            <table class="responsive-table bordered">
                                <thead>
                                <tr style="">
                                    <th>No</th>
                                    <th>Place name</th>
                                    <th>Address</th>
                                    <th>Descriptions</th>
                                    <th>Image</th>
                                    <th>User details</th>
                                    <th>Delete</th>
                                </tr>
                                </thead>
                                <tbody>
                                <?php
                                $si = 1;
                                foreach (getAllPlaceRequest() as $row) {

                                $place_request_id = $row['place_request_id'];

                                ?>
                                    <tr>
                                        <td><?php echo $si; ?></td>
                                        <td><?php echo $row['place_name']; ?></td>
                                        <td><?php echo stripslashes($row['place_address']); ?></td>
                                        <td><?php echo stripslashes($row['place_description']); ?></td>
                                        <td><img src="../places/images/<?php echo $row['place_image']; ?>" alt=""></td>
                                        <td>Name: <?php echo $row['enquiry_name']; ?> <br> Email: <?php echo $row['enquiry_email']; ?> <br> Phone: <?php echo $row['enquiry_mobile']; ?></td>
                                        <td><a href="trash_place_request.php?placerequestplacerequestplacerequestplacerequestplacerequestplacerequestplacerequestplacerequest=<?php echo $place_request_id; ?>" class="db-list-edit">Delete</a></td>
                                    </tr>
                                    <?php
                                    $si++;
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                        <!-- END TODAY LEADS -->

                        <!-- TAB END -->
                    </div>

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
<script src="http://harvesthq.github.io/chosen/chosen.jquery.js"></script>
</body>

</html>