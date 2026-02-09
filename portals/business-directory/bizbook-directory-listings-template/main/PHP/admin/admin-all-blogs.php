<?php
include "header.php";
?>

<?php if($footer_row['admin_blog_show'] !=1 || $admin_row['admin_blog_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Blogs</span>
                <div class="ud-cen-s2">
                    <h2>Blog post details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div style="display: none" class="static-success-message log-suc"><p>Blog(s) has been Permanently Deleted!!! Please wait for automatic page refresh!! </p></div>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <a href="admin-add-new-blogs.php" class="db-tit-btn">Add new post</a>
                    <table class="responsive-table bordered" id="pg-resu">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Post Name</th>
                                    <th>Created by</th>
									<th>Views</th>
									<th>Edit</th>
									<th>Delete</th>
									<th>Preview</th>
                                    <th><input type="checkbox" class="checkall" id="checkall"><input type="button" style="display: none" class='multi-del-btn' id='delete_record' value='Delete' ></th>
                                </tr>
							</thead>
							<tbody>
                            <?php
                            $si =1;
                            foreach (getAllBlogs() as $blogrow) {
                                
                                $user_id = $blogrow['user_id'];

                                $blog_id = $blogrow['blog_id'];
                                
                                $user_details_row = getUser($user_id);

                            ?>
								<tr>
                                    <td><?php echo $si; ?></td>
                                    <td><?php echo $blogrow['blog_name']; ?> <span><?php  echo dateFormatconverter($blogrow['blog_cdt'])?></span></td>
                                    <td><a href="<?php echo $PROFILE_URL.urlModifier($user_details_row['user_slug']); ?>" class="db-list-ststus" target="_blank"><?php echo $user_details_row['first_name']; ?></a></td>
									<td><span class="db-list-rat"><?php  echo blog_pageview_count($blogrow['blog_id']); ?></span></td>
									<td><a href="admin-edit-blogs.php?row=<?php echo $blogrow['blog_id']; ?>" class="db-list-edit">Edit</a></td>
									<td><a href="admin-delete-blogs.php?row=<?php echo $blogrow['blog_id']; ?>" class="db-list-edit">Delete</a></td>
									<td><a href="<?php echo $BLOG_URL.urlModifier($blogrow['blog_slug']); ?>" class="db-list-edit" target="_blank">Preview</a></td>
                                    <td><input type='checkbox' class='delete_check' id='delcheck_<?php echo $blog_id; ?>' onclick='checkcheckbox();' value='<?php echo $blog_id; ?>'></td>
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
                { "bSortable": false, "aTargets": [ 7 ] }
            ]
        });
    });
</script>

<script>
    $('#delete_record').click(function(){

        var deleteids_arr = [];
        // Read all checked checkboxes
        $("input:checkbox[class=delete_check]:checked").each(function () {
            deleteids_arr.push($(this).val());
        });

        // Check checkbox checked or not
        if(deleteids_arr.length > 0){

            // Confirm alert
            var confirmdelete = confirm("Do you really want to Delete records?");
            if (confirmdelete == true) {
                $.ajax({
                    url: 'multiple_delete_users.php',
                    type: 'post',
                    data: {request: 5,deleteids_arr: deleteids_arr},
                    success: function(response){
                        $('.static-success-message').css("display", "block");
                        window.setTimeout(function(){location.reload()},3000)
                    }
                });
            }
        }
    });
</script>
</body>

</html>