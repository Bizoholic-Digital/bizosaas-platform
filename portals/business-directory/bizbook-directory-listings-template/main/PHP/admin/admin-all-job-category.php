<?php
include "header.php";
?>

<?php if($footer_row['admin_job_show'] != 1 || $admin_row['admin_jobs_options'] != 1){
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Job Category</span>
                <div class="ud-cen-s2 hcat-cho">
                    <h2>All Job Category</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <a href="admin-add-new-job-category.php" class="db-tit-btn">Add new job category</a>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Category Name</th>
                            <th>Created date</th>
                            <th>Job</th>
                            <th>Sub Cate</th>
                            <th>Edit</th>
                            <th>View Sub Cate</th>
                            <th>Delete</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si=1;
                        foreach (getAllJobCategories() as $row) {

                            $category_id = $row['category_id'];

                            $category_listing_count = getCountCategoryJob($category_id);

                            $category_sub_category_count = getCountJobSubCategoryCategory($category_id);

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><b class="db-list-rat"><?php echo $row['category_name']; ?></b></td>
                                <td><?php echo dateFormatconverter($row['category_cdt']); ?></td>
                                <td><span class="db-list-ststus" data-toggle="tooltip"
                                          title="Total Jobs in this category"><?php echo $category_listing_count; ?></span></td>
                                <td><span class="db-list-ststus"><?php echo $category_sub_category_count; ?></span></td>
                                <td><a href="admin-job-category-edit.php?row=<?php echo $row['category_id']; ?>" class="db-list-edit">Edit</a></td>
                                <td><a href="admin-all-job-sub-category.php?cat=<?php echo $row['category_id']; ?>" class="db-list-edit">View</a></td>
                                <td><a href="admin-job-category-delete.php?row=<?php echo $row['category_id']; ?>" class="db-list-edit">Delete</a></td>
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
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
</body>

</html>