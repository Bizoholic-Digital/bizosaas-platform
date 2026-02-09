<?php
include "header.php";
?>

<?php if($admin_row['admin_home_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Feature events</span>
                <div class="ud-cen-s2">
                    <h2>Feature event details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered">
							<thead>
								<tr>
									<th>No</th>
                                    <th>Event Name</th>
                                    <th>Created by</th>
									<th>Clicks</th>
                                    <th>Views</th>
									<th>Change</th>
									<th>Preview</th>
								</tr>
							</thead>
							<tbody>
                            <?php
                            $si = 1;
                            foreach (getAllTopEvents() as $row) {

                                $event_id = $row['event_id'];
                                $event_name = $row['event_name'];
                                
                                $event_sql_row = getEvent($event_name);

                                $user_id = $event_sql_row['user_id'];

                                $user_details_row = getUser($user_id);

                                ?>
                                <tr>
                                    <td><?php echo $si; ?></td>
                                    <td><?php echo $event_sql_row['event_name']; ?> <span>Event Date: <?php echo dateFormatconverter($event_sql_row['event_start_date']); ?></span></td>
                                    <td><a href="<?php echo $PROFILE_URL.urlModifier($user_details_row['user_slug']); ?>" class="db-list-ststus" target="_blank"><?php echo $user_details_row['first_name']; ?></a></td>
                                    <td><span class="db-list-rat">76</span></td>
                                    <td><span class="db-list-rat">76</span></td>
                                    <td><a href="admin-home-feature-events-edit.php?row=<?php echo $event_id; ?>" class="db-list-edit"
                                           data-toggle="tooltip" title="Click to change the event and position">Change
                                            event</a></td>
                                    <td><a href="<?php echo $EVENT_URL.urlModifier($event_sql_row['event_slug']); ?>" class="db-list-edit" target="_blank">Preview</a>
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
<?php
if (isset($_GET['ledname_1'])) {
    trashFolder($_GET['ledname_1']);
}
?>
</body>

</html>