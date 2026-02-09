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
				<span class="udb-inst">Listing Filters</span>
                <div class="ud-cen-s2">
                    <h2>All Listing Filters</h2>
                    <?php include "../page_level_message.php"; ?>
                    <form name="all_filter_form" id="all_filter_form" method="post" action="update_all_filters.php" enctype="multipart/form-data">
                    <table class="responsive-table bordered">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Filter Name</th>
									<th colspan="2">Status</th>
								</tr>
							</thead>
							<tbody>
                            <?php
                            $si = 1;
                            foreach (getAllListingFilter() as $row) {

                                ?>
                                <tr>
                                    <td>1</td>
                                    <td>Search the service</td>
                                    <td colspan="2">
                                        <select name="service_filter" class=" form-control filt-sele">
                                            <option <?php if ($row['service_filter'] == "Active") {
                                                echo "selected";
                                            } ?> value="Active">Active
                                            </option>
                                            <option <?php if ($row['service_filter'] == "Inactive") {
                                                echo "selected";
                                            } ?> value="Inactive">Inactive
                                            </option>
                                        </select>
                                    </td>

                                </tr>

                                <tr>
                                    <td>2</td>
                                    <td>Categories filter</td>
                                    <td>
                                        <select name="category_filter" class=" form-control filt-sele">
                                            <option <?php if ($row['category_filter'] == "Active") {
                                                echo "selected";
                                            } ?> value="Active">Active
                                            </option>
                                            <option <?php if ($row['category_filter'] == "Inactive") {
                                                echo "selected";
                                            } ?> value="Inactive">Inactive
                                            </option>
                                        </select>
                                    </td>
                                    <td><a href="admin-filter-category.php" class="db-list-edit">Go to filter</a></td>
                                </tr>
                                <tr>
                                    <td>3</td>
                                    <td>Features filter</td>
                                    <td>
                                        <select name="feature_filter" class=" form-control filt-sele">
                                            <option <?php if ($row['feature_filter'] == "Active") {
                                                echo "selected";
                                            } ?> value="Active">Active
                                            </option>
                                            <option <?php if ($row['feature_filter'] == "Inactive") {
                                                echo "selected";
                                            } ?> value="Inactive">Inactive
                                            </option>
                                        </select>
                                    </td>
                                    <td><a href="admin-filter-features.php" class="db-list-edit">Go to filter</a></td>
                                </tr>
                                <tr>
                                    <td>4</td>
                                    <td>Rating filter</td>
                                    <td colspan="2">
                                        <select name="rating_filter" class=" form-control filt-sele">
                                            <option <?php if ($row['rating_filter'] == "Active") {
                                                echo "selected";
                                            } ?> value="Active">Active
                                            </option>
                                            <option <?php if ($row['rating_filter'] == "Inactive") {
                                                echo "selected";
                                            } ?> value="Inactive">Inactive
                                            </option>
                                        </select>
                                    </td>
                                </tr>
                                <tr>
                                    <td colspan="4">
                                        <button type="submit" name="all_filter_submit" class="db-pro-bot-btn">Save
                                            changes
                                        </button>
                                    </td>
                                </tr>
                                <?php
                            }
                            ?>
							</tbody>
						</table>
                    </form>
                    <div class="ud-notes">
                        <p><b>Notes:</b> Hi, here we show 6 types of filters in All Listing pages. If you don't want any filter means you can just change the <b>Status</b> like <b>Active or De-Active</b> once you change the status like <b>De-Active</b> means the filter can't show in All Listing</p>
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