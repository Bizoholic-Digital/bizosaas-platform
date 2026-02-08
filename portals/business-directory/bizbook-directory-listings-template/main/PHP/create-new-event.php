<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

if (file_exists('config/general_user_authentication.php')) {
    include('config/general_user_authentication.php');
}

if (file_exists('config/event_page_authentication.php')) {
    include('config/event_page_authentication.php');
}
//To check the event count with current plan starts

$plan_type_event_count = $user_plan_type['plan_type_event_count'];
$event_count_user = getCountUserEvent($_SESSION['user_id']);

if ($event_count_user >= $plan_type_event_count) {

    $_SESSION['status_msg'] = $BIZBOOK['EVENTS_LIMIT_EXCEED_MESSAGE'];

    header('Location: db-events');
    exit();
}
//To check the event count with current plan ends

?>
<!-- START -->
<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg">
    <div class="container">
        <div class="row">
            <div class="login-main add-list">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['ADD_NEW_EVENT']; ?></span>
                <div class="log">
                    <div class="login add-list-off">
                        <?php include "page_level_message.php"; ?>
                        <h4><?php echo $BIZBOOK['CREATE_EVENT']; ?></h4>
                        <form action="event_insert.php" class="event_form" id="event_form" name="event_form"
                              method="post" enctype="multipart/form-data">
                            <ul>
                                <li>
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" name="event_name" required="required"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['EVENT_NAME']; ?>*">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" name="event_address" required="required"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['ADDRESS']; ?>*">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="event_start_date" required="required"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['DATE']; ?>*" id="newdate">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="event_time" required="required"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['TIME']; ?>*">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea class="form-control" required="required"
                                                          name="event_description" id="event_description"
                                                          placeholder="<?php echo $BIZBOOK['EVENT_DETAILS']; ?>"></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea class="form-control" name="event_map"
                                                          placeholder="<?php echo $BIZBOOK['GOOGLE_MAP_LOCATION']; ?>"></textarea>
                                                <!-- INPUT TOOL TIP -->
                                                <div class="inp-ttip">
                                                    <b><?php echo $BIZBOOK['EVENT_IFRAME_FROM_GOOGLE']; ?></b><?php echo $BIZBOOK['EVENT_COPY_PASTE_IFRAME_FROM_GOOGLE']; ?></div>
                                                <!-- END INPUT TOOL TIP -->
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <label><?php echo $BIZBOOK['CHOOSE_BANNER_IMAGE']; ?></label>
                                               <div class="fil-img-uplo">
                                                    <span class="dumfil"><?php echo $BIZBOOK['UPLOAD_A_FILE'];  ?></span>
                                                    <input type="file" name="event_image" accept="image/*,.jpg,.jpeg,.png" class="form-control">
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="event_contact_name" required="required"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['CONTACT_PERSON']; ?>*">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="event_mobile" required="required"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['CONTACT_PHONE_NUMBER']; ?>*">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->

                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="email" name="event_email" required="required"
                                                       class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['CONTACT_EMAIL_ID']; ?>*">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="event_website" class="form-control"
                                                       placeholder="<?php echo $BIZBOOK['EVENT_WEBSITE']; ?>">
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
                                                    <label
                                                        for="isenquiry"><?php echo $BIZBOOK['ENQUIRY_BOX_ENABLE']; ?></label>
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
                                    <button type="submit" name="event_submit"
                                            class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
                                </div>
                                <div class="col-md-12">
                                    <a href="dashboard" class="skip"><?php echo $BIZBOOK['GO_TO_USER_DASHBOARD']; ?>
                                        >></a>
                                </div>
                            </div>
                            <!--FILED END-->
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!--END PRICING DETAILS-->


<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>
<script src="admin/ckeditor/ckeditor.js"></script>
<script>
    CKEDITOR.replace('event_description');
</script>
</body>

</html>