<?php
include "header.php";
?>

<?php if($admin_row['admin_listing_options'] != 1){
    header("Location: profile.php");
}
?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Popular Tags</span>
                <div class="ud-cen-s2">
                    <h2>Popular Tag details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <a href="footer-add-popular-tags.php" class="db-tit-btn">Add New Popular Tag</a>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Page</th>
                            <th>Edit</th>
                            <th>Delete</th>
                            <th>Preview</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si =1;
                        foreach (getAllPopularTags() as $row) {
                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $row['popular_tags_name']; ?> <span>Created: <?php  echo dateFormatconverter($row['popular_tags_cdt'])?></span></td>
                                <td><a href="footer-edit-popular-tags.php?row=<?php echo $row['popular_tags_id']; ?>" class="db-list-edit">Edit</a></td>
                                <td><a href="footer-delete-popular-tags.php?row=<?php echo $row['popular_tags_id']; ?>" class="db-list-edit">Delete</a></td>
                                <td><a href="<?php echo $row['popular_tags_link']; ?>" class="db-list-edit"
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
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>