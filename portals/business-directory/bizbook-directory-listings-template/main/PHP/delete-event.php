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
                <span class="steps"><?php echo $BIZBOOK['DELETE_EVENT']; ?></span>
                <div class="log">
                    <div class="login add-list-off">
                        <?php
                        $event_codea = $_GET['code'];
                        $events_a_row = getEvent($event_codea);
                        ?>
                        <h4><?php echo $BIZBOOK['DELETE_THIS_EVENT']; ?></h4>
                        <form action="event_delete.php" class="event_delete_form" id="event_delete_form"
                              name="event_delete_form"
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
                                                <input type="text" name="event_name" readonly="readonly"
                                                       class="form-control"
                                                       value="<?php echo $events_a_row['event_name']; ?>"
                                                       placeholder="<?php echo $BIZBOOK['EVENT_NAME']; ?>*">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <input type="text" name="event_address" readonly="readonly"
                                                       class="form-control"
                                                       value="<?php echo $events_a_row['event_address']; ?>"
                                                       placeholder="<?php echo $BIZBOOK['ADDRESS']; ?>*">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="date" name="event_start_date" readonly="readonly"
                                                       class="form-control"
                                                       value="<?php echo $events_a_row['event_start_date']; ?>"
                                                       placeholder="<?php echo $BIZBOOK['DATE']; ?>*">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="event_time" readonly="readonly"
                                                       class="form-control"
                                                       value="<?php echo $events_a_row['event_time']; ?>"
                                                       placeholder="<?php echo $BIZBOOK['TIME']; ?>*">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea class="form-control" readonly="readonly"
                                                          name="event_description"
                                                          placeholder="<?php echo $BIZBOOK['EVENT_DETAILS']; ?>"><?php echo $events_a_row['event_description'] ?></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div class="form-group">
                                                <textarea class="form-control" readonly="readonly" name="event_map"
                                                          placeholder="<?php echo $BIZBOOK['GOOGLE_MAP_LOCATION']; ?>"><?php echo $events_a_row['event_map']; ?></textarea>
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->
                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="event_contact_name" readonly="readonly"
                                                       class="form-control"
                                                       value="<?php echo $events_a_row['event_contact_name']; ?>"
                                                       placeholder="<?php echo $BIZBOOK['CONTACT_PERSON']; ?>*">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="event_mobile" readonly="readonly"
                                                       class="form-control"
                                                       value="<?php echo $events_a_row['event_mobile']; ?>"
                                                       placeholder="<?php echo $BIZBOOK['CONTACT_PHONE_NUMBER']; ?>*">
                                            </div>
                                        </div>
                                    </div>
                                    <!--FILED END-->

                                    <!--FILED START-->
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="email" name="event_email" readonly="readonly"
                                                       class="form-control"
                                                       value="<?php echo $events_a_row['event_email']; ?>"
                                                       placeholder="<?php echo $BIZBOOK['CONTACT_EMAIL_ID']; ?>*">
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-group">
                                                <input type="text" name="event_website" class="form-control"
                                                       readonly="readonly"
                                                       value="<?php echo $events_a_row['event_website']; ?>"
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
                                                    <input type="checkbox" disabled="disabled" id="isenquiry"
                                                           name="isenquiry"
                                                           <?php if ($events_a_row['isenquiry'] == 1){ ?>checked="" <?php } ?>>
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
                                            class="btn btn-primary"><?php echo $BIZBOOK['DELETE_EVENT']; ?></button>
                                </div>
                                <!--                                        <div class="col-md-6">-->
                                <!--                                            <button type="submit" class="btn btn-primary">Preview</button>-->
                                <!--                                        </div>-->
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
</body>

</html>