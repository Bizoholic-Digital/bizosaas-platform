<?php
include "header.php";
?>

<?php if ($admin_row['admin_seo_setting_options'] != 1) {
    header("Location: profile.php");
}
?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Listing Category</span>
                <div class="ud-cen-s2">
                    <h2>Listing category details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Category</th>
                            <th>SEO score</th>
                            <th>Last edit</th>
                            <th>views</th>
                            <th>Edit</th>
                            <th>Preview</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllCategories() as $row) {

                            $cat_id = $row['category_id'];

                            $percentage = round(getCategorySeoScore($cat_id));

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $row['category_name']; ?></td>
                                <td>
                                    <div class="progress">
                                        <div class="progress-bar bg-success progress-bar-striped"
                                             style="width:<?php echo $percentage; ?>%">
                                            <?php echo $percentage; ?>%
                                        </div>
                                    </div>
                                </td>
                                <td><?php echo dateFormatconverter($row['category_edit_cdt']); ?></td>
                                <td><?php echo category_pageview_count($row['category_id']); ?></td>
                                <td><a href="seo-listing-options-edit.php?row=<?php echo $row['category_id']; ?>"
                                       class="db-list-edit">Edit</a></td>
                                <td>
                                    <a href="<?php echo $ALL_LISTING_URL . urlModifier($row['category_name']); ?>"
                                       class="db-list-edit"
                                       target="_blank">Preview</a>
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
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
</body>

</html>