<?php
include "header.php";
?>

<?php if ($footer_row['admin_listing_show'] != 1 || $admin_row['admin_listing_options'] != 1) {
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">All Trash listings</span>
                <div class="ud-cen-s2">
                    <h2>Listing details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div style="display: none" class="static-success-message log-suc"><p>Listing(s) has been Permanently
                            Deleted!!! Please wait for automatic page refresh!! </p></div>
                    <a href="admin-add-new-listings.php" class="db-tit-btn">Add new listing</a>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Listing Name</th>
                            <th>Created Date</th>
                            <th>Deleted Date</th>
                            <th>Created by</th>
                            <th>Edit</th>
                            <th>Restore</th>
                            <th>Delete</th>
                            <th>Preview</th>
                            <th><input type="checkbox" class="checkall" id="checkall"><input type="button"
                                                                                             style="display: none"
                                                                                             class='multi-del-btn'
                                                                                             id='delete_record'
                                                                                             value='Delete'></th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php

                        $si = 1;
                        foreach (getAllTrashListing() as $listrow) {

                            $user_id = $listrow['user_id'];

                            $reviewlisting_id = $listrow['listing_id'];

                            $user_details_row = getUser($user_id);

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><img
                                        src="<?php if ($listrow['profile_image'] != NULL || !empty($listrow['profile_image'])) {
                                            echo "../images/listings/" . $listrow['profile_image'];
                                        } else {
                                            echo "../images/listings/hot4.jpg";
                                        } ?>"><?php echo $listrow['listing_name']; ?>
                                    <span><?php echo dateFormatconverter($listrow['listing_cdt']); ?></span></td>
                                <td><span
                                        class="db-list-rat"><?php echo dateFormatconverter($listrow['listing_cdt']); ?></span>
                                </td>
                                <td><span
                                        class="db-list-rat"><?php echo dateFormatconverter($listrow['listing_delete_cdt']); ?></span>
                                </td>
                                <td><a href="<?php echo $PROFILE_URL . urlModifier($user_details_row['user_slug']); ?>"
                                       class="db-list-ststus"
                                       target="_blank"><?php echo $user_details_row['first_name']; ?></a></td>
                                <td><a href="admin-edit-listings.php?code=<?php echo $listrow['listing_code']; ?>"
                                       class="db-list-edit">Edit</a></td>
                                <td>
                                    <a href="admin-delete-listings.php?code=<?php echo $listrow['listing_code']; ?>&path=restore"
                                       class="db-list-edit">Restore</a></td>
                                <td>
                                    <a href="admin-delete-listings.php?code=<?php echo $listrow['listing_code']; ?>&path=trash"
                                       class="db-list-edit">Delete Permanently</a></td>
                                <td><a href="<?php echo $LISTING_URL . urlModifier($listrow['listing_slug']); ?>"
                                       class="db-list-edit" target="_blank">Preview</a></td>
                                <td><input type='checkbox' class='delete_check'
                                           id='delcheck_<?php echo $reviewlisting_id; ?>' onclick='checkcheckbox();'
                                           value='<?php echo $reviewlisting_id; ?>'></td>
                            </tr>
                            <?php
                            $si++;
                        }
                        ?>
                        </tbody>
                    </table>
                </div>

            </div>
            <div class="ad-pgnat">
                <ul class="pagination">
                    <li class="page-item"><a class="page-link" href="#">Previous</a></li>
                    <li class="page-item active"><a class="page-link" href="#">1</a></li>
                    <li class="page-item"><a class="page-link" href="#">2</a></li>
                    <li class="page-item"><a class="page-link" href="#">3</a></li>
                    <li class="page-item"><a class="page-link" href="#">Next</a></li>
                </ul>
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
<script src="../js/select-opt.js"></script>
<script src="../js/select-opt.js"></script>
<script src="https://code.jquery.com/jquery-3.3.1.js"></script>
<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap4.min.js"></script>
<script src="js/admin-custom.js"></script>
<script>
    $(document).ready(function () {
        $('#pg-resu').DataTable({
            "columnDefs": [
                {"bSortable": false, "aTargets": [9]}
            ]
        });
    });
</script>

<script>
    $('#delete_record').click(function () {

        var deleteids_arr = [];
        // Read all checked checkboxes
        $("input:checkbox[class=delete_check]:checked").each(function () {
            deleteids_arr.push($(this).val());
        });

        // Check checkbox checked or not
        if (deleteids_arr.length > 0) {

            // Confirm alert
            var confirmdelete = confirm("Do you really want to Delete records?");
            if (confirmdelete == true) {
                $.ajax({
                    url: 'multiple_delete_users.php',
                    type: 'post',
                    data: {request: 3, deleteids_arr: deleteids_arr},
                    success: function (response) {
                        $('.static-success-message').css("display", "block");
                        window.setTimeout(function () {
                            location.reload()
                        }, 3000)
                    }
                });
            }
        }
    });
</script>
</body>

</html>