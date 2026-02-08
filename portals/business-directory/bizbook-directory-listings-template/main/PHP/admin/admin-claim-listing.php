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
                <span class="udb-inst">All Claim Request listings</span>
                <div class="ud-cen-s2">
                    <h2>Claim Request details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <a href="admin-add-new-listings.php" class="db-tit-btn">Add new listing</a>
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Listing Name</th>
                            <th>Enquirer Name</th>
                            <th>Enquirer Mobile</th>
                            <th>Enquirer Email Id</th>
                            <th>Verification Image</th>
                            <th>Enquirer Message</th>
                            <th>Enquiry Date</th>
                            <th>Status</th>
                            <th>Approve</th>
                            <th>Delete</th>
                            <th>Preview</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php

                        $si = 1;
                        foreach (getAllClaimListings() as $claimrow) {

                            $user_id = $claimrow['user_id'];
                            $listing_id = $claimrow['listing_id'];

                            $listrow = getIdListing($listing_id);
                            $user_details_row = getUser($user_id);

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><img
                                        src="<?php if ($listrow['profile_image'] != NULL || !empty($listrow['profile_image'])) {
                                            echo "../images/listings/" . $listrow['profile_image'];
                                        } else {
                                            echo "../images/listings/hot4.jpg";
                                        } ?>"><?php echo $listrow['listing_name']; ?> <span><?php echo dateFormatconverter($listrow['listing_cdt']); ?></span></td>

                                <td><?php echo $claimrow['enquiry_name']; ?></td>
                                <td><?php echo $claimrow['enquiry_mobile']; ?></td>
                                <td><?php echo $claimrow['enquiry_email']; ?></td>
                                <td><img width="100px"
                                        src="<?php if ($claimrow['enquiry_image'] != NULL || !empty($claimrow['enquiry_image'])) {
                                            echo "../images/listings/" . $claimrow['enquiry_image'];
                                        } else {
                                            echo "../images/listings/hot4.jpg";
                                        } ?>"></td>
                                <td><?php echo $claimrow['enquiry_message']; ?></td>
                                <td><span class="db-list-rat"><?php  echo dateFormatconverter($claimrow['claim_cdt']); ?></span></td>
                                <td><span class="db-list-rat"><?php if($claimrow['claim_status'] == 1){ echo "Approved"; } else{ echo "Pending";} ?></span></td>
                                <?php if($claimrow['claim_status'] == 0){ ?>
                                <td><a href="approve-claim.php?approveclaimrequestapproveclaimrequestapproveclaimrequestapproveclaimrequestapproveclaimrequest=<?php echo $claimrow['enquiry_sender_id']; ?>&&listing_id=<?php echo $claimrow['listing_id']; ?>&&claim_id=<?php echo $claimrow['claim_listing_id']; ?>" class="db-list-edit">Approve</a></td>
                                <?php }else{ ?>
                                <td> - </td>
                                <?php } ?>
                                    <td><a href="trash-claim.php?trashclaimrequesttrashclaimrequesttrashclaimrequesttrashclaimrequesttrashclaimrequest=<?php echo $claimrow['claim_listing_id']; ?>&image=<?php echo $claimrow['enquiry_image']; ?>" class="db-list-edit">Delete</a></td>
                                <td><a href="../listing-details.php?code=<?php echo $listrow['listing_code']; ?>" class="db-list-edit" target="_blank">Preview</a></td>
                            </tr>
                            <?php
                            $si++;
                        }
                        ?>
                        </tbody>
                    </table>
                </div>

            </div>
            <div class="ad-pgnat">
                <ul class="pagination">
                    <li class="page-item"><a class="page-link" href="#">Previous</a></li>
                    <li class="page-item active"><a class="page-link" href="#">1</a></li>
                    <li class="page-item"><a class="page-link" href="#">2</a></li>
                    <li class="page-item"><a class="page-link" href="#">3</a></li>
                    <li class="page-item"><a class="page-link" href="#">Next</a></li>
                </ul>
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