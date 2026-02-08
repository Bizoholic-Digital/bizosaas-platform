<?php
include "header.php";
?>

<?php if($footer_row['admin_expert_show'] != 1 || $admin_row['admin_service_expert_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Expert City</span>
                <div class="ud-cen-s2 hcat-cho">
                    <h2>All Expert City</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <a href="expert-add-new-city.php" class="db-tit-btn">Add New Expert City</a>
                    <table class="responsive-table bordered" id="pg-resu">
							<thead>
								<tr>
									<th>No</th>
                                    <th>City Name</th>
									<th>Created date</th>
									<th>Edit</th>
									<th>Delete</th>
								</tr>
							</thead>
							<tbody>
                            <?php
                            $si = 1;
                            foreach (getAllExpertCities() as $row) {

                            $country_id = $row['country_id'];

                            ?>
                                <tr>
                                    <td><?php echo $si; ?></td>
                                    <td><b class="db-list-rat"><?php echo $row['country_name']; ?></b></td>
                                    <td><?php echo dateFormatconverter($row['country_cdt']); ?></td>
                                    <td><a href="expert-edit-city.php?row=<?php echo $row['country_id']; ?>" class="db-list-edit">Edit</a></td>
                                    <td><a href="expert-delete-city.php?row=<?php echo $row['country_id']; ?>" class="db-list-edit">Delete</a></td>
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