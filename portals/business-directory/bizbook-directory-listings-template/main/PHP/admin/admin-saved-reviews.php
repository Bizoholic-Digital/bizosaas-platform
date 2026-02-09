<?php
include "header.php";
?>

<?php if($footer_row['admin_listing_show'] != 1 || $admin_row['admin_review_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Saved Reviews</span>
                <div class="ud-cen-s2">
                     <h2>Saved Reviews Details</h2>
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
									<th>City</th>
									<th>Message</th>
									<th>Ratings</th>
                                    <th>Listing name</th>
									<th>Delete</th>
                                    <th>Save</th>
								</tr>
							</thead>
							<tbody>
                            <?php
                            $si = 1;
                            foreach (getAllSavedReviews() as $reviewrow) {

                            $review_list_id = $reviewrow['listing_id'];
                            $listing_user_id = $reviewrow['listing_user_id'];
                            $rrating = $reviewrow['price_rating'];
                                
                            $rev_listrs = getAllListingUserListing($listing_user_id,$review_list_id);

                            $rrating_save = $reviewrow['review_save'];

                            ?>
                                <tr>
                                    <td><?php echo $si; ?></td>
                                    <td><?php echo $reviewrow['review_name']; ?> <span><?php echo dateFormatconverter($reviewrow['review_cdt']); ?></span></td>
                                    <td><?php echo $reviewrow['review_email']; ?></td>
                                    <td><?php echo $reviewrow['review_mobile']; ?></td>
                                    <td><?php echo $reviewrow['review_city']; ?></td>
                                    <td><?php echo $reviewrow['review_message']; ?></td>

                                    <td>
                                        <label class="rat">
                                            <?php
                                            for ($i = 1; $i <= $rrating; $i++) {
                                                ?>
                                                <i class="material-icons">star</i>
                                                <?php
                                            }
                                            ?>
                                        </label>
                                    </td>
                                    <td><?php echo $rev_listrs['listing_name']; ?></td>
                                    <td><a href="../review_trash.php?reviewreviewreviewreviewreviewreview=<?php echo $reviewrow['review_id']; ?>" class="db-list-edit">Delete</a></td>
                                    <td><a href="review_saved_update.php?reviewreviewreviewreviewreviewreview=<?php echo $reviewrow['review_id']; ?>&&status=<?php echo $rrating_save; ?>&&path=saved"><span class="enq-sav" data-toggle="tooltip" title="Click to save this review"><i class="material-icons  <?php if($rrating_save == 1){echo "sav-act"; } ?>">favorite</i></span></a></td>
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