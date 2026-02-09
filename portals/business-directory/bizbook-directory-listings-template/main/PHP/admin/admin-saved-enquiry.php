<?php
include "header.php";
?>

<?php if($footer_row['admin_listing_show'] != 1 || $admin_row['admin_enquiry_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Saved Enquiry</span>
                <div class="ud-cen-s2">
                     <h2>Saved Enquiry Details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <table class="responsive-table bordered tb-bold-dis" id="pg-resu">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Name</th>
									<th>Email</th>
									<th>Phone</th>
									<th>Message</th>
									<th>Delete</th>
                                    <th>Save</th>
								</tr>
							</thead>
							<tbody>
                            <?php
                            $si = 1;
                            foreach (getAllSavedEnquiries() as $enquiries_row) {

                            $enquiry_listing_id = $enquiries_row['listing_id'];
                            $enquiry_enquiry_save = $enquiries_row['enquiry_save'];

                            $listing_enquiry_row = getAllListingListing($enquiry_listing_id);

                            ?>
								<tr>
                                    <td><?php echo $si; ?></td>
                                    <td><?php echo $enquiries_row['enquiry_name']; ?>
                                        <span><?php echo dateFormatconverter($enquiries_row['enquiry_cdt']); ?></span>
                                    </td>
                                    <td><?php echo $enquiries_row['enquiry_email']; ?></td>
                                    <td><?php echo $enquiries_row['enquiry_mobile']; ?></td>
                                    <td><?php echo $enquiries_row['enquiry_message']; ?></td>
                                    <td><a href="trash_enquiry.php?messageenquirymessageenquirymessageenquirymessageenquiry=<?php echo $enquiries_row['enquiry_id']; ?>" class="db-list-edit">Delete</a></td>
                                    <td><a href="enquiry_saved_update.php?messageenquirymessageenquirymessageenquirymessageenquiry=<?php echo $enquiries_row['enquiry_id']; ?>&&status=<?php echo $enquiry_enquiry_save; ?>&&path=saved"><span class="enq-sav " data-toggle="tooltip" title="Click to Un-save this enquiry"><i class="material-icons <?php if($enquiry_enquiry_save == 1){echo "sav-act"; } ?>">favorite</i></span></a></td>								</tr>
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