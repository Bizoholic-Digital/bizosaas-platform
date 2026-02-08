<?php
include "header.php";
?>

<?php if($footer_row['admin_place_show'] !=1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Place Categories</span>
                <div class="ud-cen-s2 hcat-cho">
                    <h2>All Place Categories</h2>
                    <?php include "../page_level_message.php"; ?>
                    <a href="place-add-new-category.php" class="db-tit-btn">Add new Category</a>
                    <table class="responsive-table bordered" id="pg-resu">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Category Name</th>
									<th>Created date</th>
									<th>Place count</th>
									<th>Edit</th>
									<th>Delete</th>
								</tr>
							</thead>
							<tbody>
                            <?php
                            $si=1;
                            foreach (getAllPlaceCategoriesPos() as $row) {

                            $category_id = $row['category_id'];

                            $category_news_count = getCountCategoryNews($category_id);

                            ?>
                                <tr>
                                    <td><?php echo $si; ?></td>
                                    <td><b class="db-list-rat"><?php echo $row['category_name']; ?></b></td>
                                    <td><?php echo dateFormatconverter($row['category_cdt']); ?></td>
                                    <td><span class="db-list-ststus"><?php echo $category_news_count; ?></span></td>
                                    <td><a href="place-category-edit.php?row=<?php echo $row['category_id']; ?>" class="db-list-edit">Edit</a></td>
                                    <td><a href="place-category-delete.php?row=<?php echo $row['category_id']; ?>" class="db-list-edit">Delete</a></td>
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
    <script src="js/admin-custom.js"></script> <script src="http://harvesthq.github.io/chosen/chosen.jquery.js"></script>
</body>

</html>