<?php
include "header.php";
?>

<?php if($footer_row['admin_news_show'] !=1 || $admin_row['admin_news_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">All News & Magazines</span>
                <div class="ud-cen-s2">
                    <h2>News & Magazines</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div style="display: none" class="static-success-message log-suc"><p>News/Magazine(s) has been Permanently Deleted!!! Please wait for automatic page refresh!! </p></div>
                    <a href="news-add-new.php" class="db-tit-btn">Add new news</a>
                    <table class="responsive-table bordered" id="pg-resu">
							<thead>
								<tr>
									<th>No</th>
                                    <th>News</th>
                                    <th>Category</th>
									<th>Published</th>
									<th>Views</th>
									<th>Edit</th>
									<th>Delete</th>
									<th>Preview</th>
                                    <th><input type="checkbox" class="checkall" id="checkall"><input type="button" style="display: none" class='multi-del-btn' id='delete_record' value='Delete' ></th>
                                </tr>
							</thead>
							<tbody>
                            <?php
                            $si = 1;
                            foreach (getAllNews() as $newsrow) {

                            $news_id = $newsrow['news_id'];

                            $category_id = $newsrow['category_id'];

                            $category_row = getNewsCategory($category_id);

                            ?>
								<tr>
                                    <td><?php echo $si; ?></td>
                                    <td><?php echo stripslashes($newsrow['news_title']); ?></td>
                                    <td><span class="db-list-ststus"><?php echo $category_row['category_name']; ?></span></td>
                                    <td><?php echo dateFormatconverter($newsrow['news_cdt']); ?></td>
                                    <td><span class="db-list-rat"><?php echo AddingZero_BeforeNumber(news_detail_pageview_count($newsrow['news_id'])); ?></span></td>
                                    <td><a href="news-edit.php?code=<?php echo $news_id; ?>" class="db-list-edit">Edit</a></td>
                                    <td><a href="news-delete.php?code=<?php echo $news_id; ?>" class="db-list-edit">Delete</a></td>
                                    <td><a target="_blank" href="<?php echo $NEWS_DETAIL_URL . urlModifier($newsrow['news_slug']); ?>" class="db-list-edit">Preview</a></td>
                                    <td><input type="checkbox" class="delete_check" id="delcheck_49" onclick="checkcheckbox();"></td>
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
<script src="http://harvesthq.github.io/chosen/chosen.jquery.js"></script>
<script src="http://harvesthq.github.io/chosen/chosen.jquery.js"></script>
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
                    data: {request: 8,deleteids_arr: deleteids_arr},
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