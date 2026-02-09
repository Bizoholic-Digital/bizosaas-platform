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
                <span class="udb-inst">Job Sub Categories</span>
                <div class="ud-cen-s2 hcat-cho">
                    <h2>All Job Sub Categories</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <a href="admin-add-new-job-sub-category.php" class="db-tit-btn">Add new job sub category</a>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Sub Category Name</th>
                            <th>Main Category Name</th>
                            <th>Created date</th>
                            <th>Jobs</th>
                            <th>Edit</th>
                            <th>Delete</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si=1;

                        if(isset($_GET['cat'])){
                            $qry = getCategoryJobSubCategories($_GET['cat']);
                        }else{
                            $qry = getAllJobSubCategories();
                        }

                        foreach ($qry as $row) {

                            $sub_category_id = $row['sub_category_id'];
                            $category_id = $row['category_id'];

                            $category_listing_count = getCountSubCategoryJob($sub_category_id);

                            $cat_sql_row = getJobCategory($category_id);

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><b class="db-list-rat"><?php echo $row['sub_category_name']; ?></b></td>
                                <td><b class="db-list-rat"><?php echo $cat_sql_row['category_name']; ?></b></td>
                                <td><?php echo dateFormatconverter($row['sub_category_cdt']); ?></td>
                                <td><span class="db-list-ststus" data-toggle="tooltip"
                                          title="Total listings in this category"><?php echo $category_listing_count; ?></span></td>
                                <td><a href="admin-job-sub-category-edit.php?row=<?php echo $row['sub_category_id']; ?>" class="db-list-edit">Edit</a></td>
                                <td><a href="admin-job-sub-category-delete.php?row=<?php echo $row['sub_category_id']; ?>" class="db-list-edit">Delete</a></td>
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