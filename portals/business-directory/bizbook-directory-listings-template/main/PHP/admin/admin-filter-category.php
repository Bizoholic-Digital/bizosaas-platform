<?php
include "header.php";
?>
<?php if($footer_row['admin_listing_show'] != 1 || $admin_row['admin_listing_filter_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Category Filters</span>
                <div class="ud-cen-s2">
                    <h2>All Category Filters</h2>
                    <?php include "../page_level_message.php"; ?>
                    <form name="category_filter_form" id="category_filter_form" method="post" action="update_category_filters.php" enctype="multipart/form-data">
                        <table class="responsive-table bordered">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Category Name</th>
									<th>Status</th>
                                    <th>Position</th>
								</tr>
							</thead>
							<tbody>
                            <?php
                            $si=1;
                            foreach (getAllCategoriesPos() as $row) {

                            $category_id = $row['category_id'];

                            ?>
                                <input type="hidden" class="form-control"
                                       name="category_id[]"
                                       value="<?php echo $row['category_id']; ?>">
								<tr>
                                    <td><?php echo $si; ?></td>
                                    <td><?php echo $row['category_name']; ?></td>
                                    <td>
                                        <select name="category_filter[]" class="chosen-select form-control filt-sele">
                                            <option <?php if($row['category_filter'] == 0 ){ echo "selected='selected'"; } ?> value="0" >Active</option>
                                            <option <?php if($row['category_filter'] == 1 ){ echo "selected='selected'"; } ?> value="1" >InActive</option>
                                        </select>
                                    </td>
                                    <td>
                                        <select name="category_filter_pos_id[]" class="chosen-select form-control filt-cpos">
                                            <?php for($sno = 1;$sno <=10;$sno++){ ?>
                                            <option <?php if($sno == $row['category_filter_pos_id'] ){ echo "selected='selected'"; } ?> value="<?php echo $sno; ?>"><?php echo $sno; ?></option>
                                            <?php } ?>
                                        </select>
                                    </td>
								</tr>
                                <?php
                                $si++;
                            }
                            ?>

                                <tr>
                                    <td colspan="4">
                                        <button type="submit" name="category_filter_submit" class="db-pro-bot-btn">Save changes</button>
                                    </td>
								</tr>
							</tbody>
						</table>
                        </form>
                    <div class="ud-notes">
                        <p><b>Notes:</b> Hi, Above all categories shows in All Listing page. If you want some of one category don't want to show means you change the <b>status</b> like <b>De-Active</b>. You can able to change <b>Category position</b></p>
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
    <script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>