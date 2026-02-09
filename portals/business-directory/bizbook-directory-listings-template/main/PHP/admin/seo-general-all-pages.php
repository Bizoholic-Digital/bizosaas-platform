<?php
include "header.php";
?>

<?php if($admin_row['admin_seo_setting_options'] != 1){
    header("Location: profile.php");
}
?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">All Pages</span>
                <div class="ud-cen-s2">
                    <h2>General Promotion Pages</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <a href="seo-general-add-new-page.php" class="db-tit-btn">Add new page</a>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Page</th>
                            <th>Last edit</th>
                            <th>views</th>
                            <th>Edit</th>
                            <th>Delete</th>
                            <th>Preview</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllPagesType(2) as $row) {
                        ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $row['page_name']; ?> <span>Created: <?php echo dateFormatconverter($row['page_cdt']); ?></span></td>
                                <td><?php echo dateFormatconverter($row['page_last_edit']); ?></td>
                                <td><?php echo seopage_pageview_count($row['page_id']); ?></td>
                                <td><a href="seo-general-edit-page.php?row=<?php echo $row['page_id']; ?>" class="db-list-edit">Edit</a></td>
                                <td><a href="seo-general-delete-page.php?row=<?php echo $row['page_id']; ?>" class="db-list-edit">Delete</a></td>
                                <td><a href="<?php echo $GENERAL_PROMOTION_URL.urlModifier($row['page_slug']); ?>" class="db-list-edit" target="_blank">Preview</a>
                                </td>
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