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
                            <span class="udb-inst">Delete event</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Delete this Event</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $event_codea = $_GET['row'];
                                    $events_a_row = getEvent($event_codea);

                                    ?>
                                    <form action="trash_event.php" class="event_delete_form" id="event_delete_form" name="event_delete_form"
                                          method="post" enctype="multipart/form-data">
                                        <input type="hidden" id="event_id" value="<?php echo $events_a_row['event_id']; ?>"
                                               name="event_id" class="validate">
                                        <input type="hidden" id="event_image_old"
                                               value="<?php echo $events_a_row['event_image']; ?>" name="event_image_old"
                                               class="validate">
                                        <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <select name="user_id" disabled="disabled" required="required" class="form-control" id="user_id">
                                                                <option value="">Choose a user</option>
                                                                <?php
                                                                foreach (getAllUser() as $row) {
                                                                    ?>
                                                                    <option <?php if($events_a_row['user_id']== $row['user_id']){ echo "selected"; } ?>
                                                                        value="<?php echo $row['user_id']; ?>"><?php echo $row['first_name']; ?></option>
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
                                                            <input type="text" name="event_name" required="required" readonly="readonly" class="form-control"
                                                                   value="<?php echo $events_a_row['event_name']; ?>" placeholder="Event name *">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" name="event_address" required="required" readonly="readonly" class="form-control"
                                                                   value="<?php echo $events_a_row['event_address']; ?>"  placeholder="Address *">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <input type="date" name="event_start_date" required="required" readonly="readonly" class="form-control"
                                                                   value="<?php echo $events_a_row['event_start_date']; ?>" placeholder="Date *">
                                                        </div>
                                                    </div>
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <input type="text" name="event_time" required="required" readonly="readonly" class="form-control"
                                                                   value="<?php echo $events_a_row['event_time']; ?>" placeholder="Time *">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <textarea class="form-control" required="required" readonly="readonly" name="event_description"
                                                                      placeholder="Event details"><?php echo $events_a_row['event_description']?></textarea>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <textarea class="form-control" name="event_map" readonly="readonly"
                                                                      placeholder="Google map location"><?php echo $events_a_row['event_map']; ?></textarea>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <input type="text" name="event_contact_name" required="required" readonly="readonly" class="form-control"
                                                                   value="<?php echo $events_a_row['event_contact_name']; ?>" placeholder="Contact person *">
                                                        </div>
                                                    </div>
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <input type="text" name="event_mobile" required="required" readonly="readonly" class="form-control"
                                                                   value="<?php echo $events_a_row['event_mobile']; ?>" placeholder="Contact phone number *">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->

                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <input type="email" name="event_email" required="required" readonly="readonly" class="form-control"
                                                                   value="<?php echo $events_a_row['event_email']; ?>" placeholder="Contact Email Id *">
                                                        </div>
                                                    </div>
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <input type="text" name="event_website" readonly="readonly" class="form-control"
                                                                   value="<?php echo $events_a_row['event_website']; ?>" placeholder="Event Website">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->

                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div>
                                                            <div class="chbox">
                                                                <input type="checkbox" id="isenquiry" disabled="disabled" name="isenquiry" <?php if($events_a_row['isenquiry'] == 1){ ?> checked="" <?php }?>>
                                                                <label for="isenquiry">Enquiry or Registration form
                                                                    enable</label>
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
                                                <button type="submit" name="event_submit" class="btn btn-primary">Delete</button>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                    </form>
                                    <div class="col-md-12">
                                        <a href="profile.php" class="skip">Go to user dashboard
                                            >></a>
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