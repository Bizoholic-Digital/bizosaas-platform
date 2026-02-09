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
                 <section class="login-reg">
		<div class="container">
			<div class="row">
                <div class="login-main add-list add-ncate">
                     <div class="log-bor">&nbsp;</div>
                    <span class="udb-inst">Change event and position</span>
                    <div class="log log-1">
                        <div class="login">
                            <h4>Choose event</h4>
                            <?php include "../page_level_message.php"; ?>
                            
                            <?php
                            $event_id = $_GET['row'];
                            $row = getTopEvent($event_id);
                            ?>

                            <form class="cre-dup-form cre-dup-form-show" name="event_form" id="event_form" method="post" action="update_home_feature_events.php" enctype="multipart/form-data">

                                <input type="hidden" class="validate" id="event_id" name="event_id" value="<?php echo $row['event_id']; ?>" required="required">
                                <input type="hidden" class="validate" id="event_name_old" name="event_name_old" value="<?php echo $row['event_name']; ?>" required="required">
                                <input type="hidden" class="validate" id="event_image_old" name="event_image_old" value="<?php echo $row['event_image']; ?>" required="required">

                                <form >
                                 <ul>
                                     <li>
                                         <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <select name="event_name" class="form-control" id="event_name">

                                                        <?php
                                                        foreach (getAllActiveEvents() as $li_row) {
                                                            ?>
                                                            <option
                                                                value="<?php echo $li_row['event_id']; ?>" <?php if ($li_row['event_id'] == $row['event_name']) {
                                                                echo "selected";
                                                            } ?> ><?php echo $li_row['event_name']; ?>
                                                            </option>
                                                            <?php
                                                        }
                                                        ?>
                                                    </select>
                                                </div>
                                            </div>
                                        </div>
                                         <div class="row">
                                            <div class="col-md-12">
                                                 <div class="form-group">
                                                  <select class="form-control" name="event_pos_id">
                                                      <?php
                                                      for($i=1;$i<=8;$i++) {

                                                          ?>
                                                          <option <?php if($i == $row['event_pos_id']){ echo "selected";} ?> value="<?php echo $i; ?>"><?php echo $i; ?></option>
                                                          <?php
                                                      }
                                                      ?>
                                                  </select>
                                                </div>
                                            </div>
                                        </div>
                                     </li>
                                 </ul>
                                <button type="submit" name="top_event_submit" class="btn btn-primary">Update changes</button>
                            </form>
                            <div class="col-md-12">
                                    <a href="admin-home-feature-events.php" class="skip">Go to Feature Events >></a>
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