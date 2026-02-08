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
				<span class="udb-inst">Expert Category(Work profession)</span>
                <div class="ud-cen-s2 hcat-cho">
                    <h2>All Expert Category</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <a href="expert-add-new-category.php" class="db-tit-btn">Add New Expert Category</a>
                    <table class="responsive-table bordered" id="pg-resu">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Category Name</th>
                                    <th>Category Image</th>
									<th>Created date</th>
									<th>Experts</th>
                                    <th>Sub Cate</th>
									<th>Edit</th>
                                    <th>View Sub-cate</th>
									<th>Delete</th>
								</tr>
							</thead>
							<tbody>
                            <?php
                            $si=1;
                            foreach (getAllActiveExpertCategoriesPos() as $row) {

                            $category_id = $row['category_id'];

                            $category_listing_count = getCountCategoryJob($category_id);

                            $category_sub_category_count = getCountJobSubCategoryCategory($category_id);

                            ?>
                                <tr>
                                    <td><?php echo $si; ?></td>
                                    <td><?php echo $row['category_name']; ?></td>
                                    <td><img src="../service-experts/images/services/<?php echo $row['category_image']; ?>" alt=""></td>
                                    <td><?php echo dateFormatconverter($row['category_cdt']); ?></td>
                                    <td><span class="db-list-ststus" data-toggle="tooltip"
                                             title="Total Service Experts in this category"><?php echo $category_listing_count; ?></span></td>
                                    <td><span class="db-list-ststus"><?php echo $category_sub_category_count; ?></span></td>
                                    <td><a href="expert-category-edit.php?row=<?php echo $row['category_id']; ?>" class="db-list-edit"><span class="material-icons">edit</span></a></td>
                                    <td><a href="expert-all-sub-category.php?cat=<?php echo $row['category_id']; ?>" class="db-list-edit cta-blu-sml"><span class="material-icons">remove_red_eye</span></a></td>
                                    <td><a href="expert-category-delete.php?row=<?php echo $row['category_id']; ?>" class="db-list-edit"><span class="material-icons">delete</span></a></td>
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

<!-- START -->
<section>
    <div class="pop-table">
        <!-- The Modal -->
        <div class="modal fade" id="expstatus">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="log-bor">&nbsp;</div>
                    <span class="udb-inst">AC Services - Sub-category</span>
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                    <div class="inn">
                    <table class="responsive-table bordered">
							<tbody>
                                <tr>
                                    <td>1</td>
                                    <td>AC Service</td>
                                </tr>
                                <tr>
                                    <td>2</td>
                                    <td>AC Board Problem</td>
                                </tr>
							</tbody>
						</table>
                    </div>
                </div>
            </div>
        </div>
        <!--- END --->   
    </div>
</section>
<!-- END -->
</body>

</html>