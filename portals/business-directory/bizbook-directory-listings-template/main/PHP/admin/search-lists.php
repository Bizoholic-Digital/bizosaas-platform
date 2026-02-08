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
                <span class="udb-inst">Search lists</span>
                <div class="ud-cen-s2">
                    <h2>Initial search lists</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Search query</th>
                            <th>Search link</th>
                            <th>Edit</th>
                            <th>Delete</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllSearch() as $row) {
                        ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $row['search_title']; ?></td>
                                <td><a href="<?php echo $row['search_list_link']; ?>" class="db-list-edit" target="_blank">Preview</a>
                                </td>
                                <td><a href="search-lists-edit.php?row=<?php echo $row['search_list_id']; ?>" class="db-list-edit">Edit</a></td>
                                <td><a href="search-lists-delete.php?row=<?php echo $row['search_list_id']; ?>" class="db-list-edit">Delete</a></td>
                            </tr>
                            <?php
                            $si++;
                        }
                        ?>
                        </tbody>
                    </table>
                </div>
                <div class="ud-notes">
                    <p><b>Notes:</b> When user <b>click on search box</b> your <b>custom search list shows</b> then user <b>start typing</b> means results shows depends on <b>user type text</b>.</p>
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