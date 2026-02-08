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
				<span class="udb-inst">Expert Sub-Category(Work profession)</span>
                <div class="ud-cen-s2 hcat-cho">
                    <h2>All Expert Sub-Category</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <a href="expert-add-new-sub-category.php" class="db-tit-btn">Add New Expert Sub-Category</a>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Sub Category Name</th>
                            <th>Main Category Name</th>
                            <th>Created date</th>
                            <th>Edit</th>
                            <th>Delete</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si=1;

                        if(isset($_GET['cat'])){
                            $qry = getCategoryExpertSubCategories($_GET['cat']);
                        }else{
                            $qry = getAllExpertSubCategories();
                        }

                        foreach ($qry as $row) {

                            $sub_category_id = $row['sub_category_id'];
                            $category_id = $row['category_id'];

                            $cat_sql_row = getExpertCategory($category_id);

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><b class="db-list-rat"><?php echo $row['sub_category_name']; ?></b></td>
                                <td><b class="db-list-rat"><?php echo $cat_sql_row['category_name']; ?></b></td>
                                <td><?php echo dateFormatconverter($row['sub_category_cdt']); ?></td>
                                <td><a href="expert-edit-sub-category.php?row=<?php echo $row['sub_category_id']; ?>" class="db-list-edit">Edit</a></td>
                                <td><a href="expert-delete-sub-category.php?row=<?php echo $row['sub_category_id']; ?>" class="db-list-edit">Delete</a></td>
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