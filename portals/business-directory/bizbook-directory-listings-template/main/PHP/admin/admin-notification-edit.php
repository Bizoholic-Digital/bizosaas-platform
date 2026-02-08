<?php
include "header.php";
?>

<?php if($admin_row['admin_notification_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                 <section class="login-reg">
		<div class="container">
			<div class="row">
                <div class="login-main add-list posr">
                     <div class="log-bor">&nbsp;</div>
                    <span class="udb-inst">Edit notification</span>
                    <div class="log log-1">
                        <div class="login">
                            <h4>Edit this Notification</h4>
                            <?php include "../page_level_message.php"; ?>
                            <?php
                            $notification_id = $_GET['id'];
                            $notifications_row = getNotification($notification_id);

                            ?>
                            <form name="notification_form" id="notification_form" method="post" action="update_notification.php" enctype="multipart/form-data" class="">

                                <input type="hidden" autocomplete="off" name="notification_id" value="<?php echo $notifications_row['notification_id']; ?>" id="notification_id" class="validate">

                                <ul>
										<li>
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <select id="notification_user" name="notification_user" required="required" class="form-control">
                                                    <option value="">Choose user</option>
                                                    <option <?php if($notifications_row['notification_user'] == 100){ echo "selected"; } ?> value="100">All Users</option>
                                                    <option <?php if($notifications_row['notification_user'] == 101){ echo "selected"; } ?> value="101">All Service Providers</option>
                                                    <option <?php if($notifications_row['notification_user'] == 102){ echo "selected"; } ?> value="102">All General Users</option>
                                                    <?php
                                                    foreach (getAllPlanType() as $plan_type_row) {
                                                        ?>
                                                        <option <?php if($plan_type_row['plan_type_id']== $notifications_row['notification_user']){ echo "selected"; } ?>
                                                            value="<?php echo $plan_type_row['plan_type_id'];?>"><?php echo "All ".$plan_type_row['plan_type_name']." Users";?></option>
                                                        <?php
                                                    }
                                                    ?>
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                     <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" id="notification_title" value="<?php echo $notifications_row['notification_title']; ?>" name="notification_title" required="required" class="form-control" placeholder="Notification title *">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" id="notification_message" value="<?php echo $notifications_row['notification_message']; ?>" name="notification_message" required="required" class="form-control" placeholder="Short description *">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" id="notification_link" value="<?php echo $notifications_row['notification_link']; ?>" name="notification_link" required="required" class="form-control" placeholder="Page link *">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
									</li>
									</ul>
									<!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <button type="submit" name="notification_submit" class="btn btn-primary">Update Changes</button>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                            </form>
                            <div class="col-md-12">
                                <a href="admin-notification-all.php" class="skip">Go to all notifications >></a>
                            </div>
                        </div>
                    </div>
                </div>
			</div>
		</div>
	</section>

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