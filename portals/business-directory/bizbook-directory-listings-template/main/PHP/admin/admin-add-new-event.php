<?php
include "header.php";
?>

<?php if($footer_row['admin_event_show'] !=1 || $admin_row['admin_event_options'] != 1){
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
                    <span class="udb-inst">new event</span>
                    <div class="log log-1">
                        <div class="login">
                            <h4>Create Event</h4>
                            <?php include "../page_level_message.php"; ?>
                             <form  name="event_form" id="event_form" method="post" action="insert_event.php" enctype="multipart/form-data">
									<ul>
										<li>
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">

                                                <select name="user_id" required="required" class="chosen-select form-control" id="user_id">
                                                    <option value="">Choose a user</option>
                                                    <?php
                                                    foreach (getAllUser() as $row) {
                                                        ?>
                                                        <option value="<?php echo $row['user_id']; ?>"><?php echo $row['first_name']; ?></option>
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
                                              <input type="text" name="event_name" required="required" class="form-control" placeholder="Event name *">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                              <input type="text" name="event_address" required="required" class="form-control" placeholder="Address *">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                              <input type="date" name="event_start_date" required="required" class="form-control" placeholder="Date *">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                              <input type="text" name="event_time" required="required" class="form-control" placeholder="Time *">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                  <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea class="form-control" required="required" id="event_description" name="event_description" placeholder="Event details"></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea class="form-control" name="event_map" placeholder="Google map location"></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
									<!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <label>Choose banner image</label>
                                              <input type="file" name="event_image" required="required" class="form-control">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                              <input type="text" name="event_contact_name" required="required" class="form-control" placeholder="Contact person *">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                              <input type="text" name="event_mobile" required="required" class="form-control" placeholder="Contact phone number *">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                            <!--FILED START-->
                                            <div class="row">
                                                <div class="col-md-6">
                                                    <div class="form-group">
                                                        <input  type="email" name="event_email" required="required" class="form-control"
                                                                placeholder="Contact Email Id *">
                                                    </div>
                                                </div>
                                                <div class="col-md-6">
                                                    <div class="form-group">
                                                        <input type="text" name="event_website" class="form-control"
                                                               placeholder="Event Website">
                                                    </div>
                                                </div>
                                            </div>
                                            <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div>
                                                <div class="chbox">
                                                    <input type="checkbox" id="isenquiry" name="isenquiry" checked="">
                                                    <label for="isenquiry">Enquiry or Registration form enable</label>
                                                  </div>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->    
									</li>
									</ul>
									<!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <button type="submit" name="event_submit" class="btn btn-primary">Submit</button>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                            </form>
                            <div class="col-md-12">
                                <a href="profile.php" class="skip">Go to user dashboard >></a>
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
    <script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
<script src="ckeditor/ckeditor.js"></script>
<script>
    CKEDITOR.replace('event_description');
</script>
</body>

</html>