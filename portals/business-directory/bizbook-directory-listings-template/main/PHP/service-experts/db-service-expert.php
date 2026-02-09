<?php
include "expert-config-info.php";
include "../header.php";

if (file_exists('../config/user_authentication.php')) {
    include('../config/user_authentication.php');
}
include "../dashboard_left_pane.php";

//To redirect the general type user to dashboard to avoid using this page

if (file_exists('../config/general_user_authentication.php')) {
    include('../config/general_user_authentication.php');
}

if (file_exists('../config/expert_page_authentication.php')) {
    include('../config/expert_page_authentication.php');
}

$user_id = $_SESSION['user_id'];

$service_expert_row = getExpertUser($user_id);

?>
    <!--CENTER SECTION-->
    <div class="ud-main">
   <div class="ud-main-inn ud-no-rhs">
    <div class="ud-cen">
        <div class="log-bor">&nbsp;</div>
        <span class="udb-inst"><?php echo $BIZBOOK['SERVICE-EXPERT-ALL-SERVICE-EXPERT-LEADS']; ?></span>
        <?php
        if ($user_details_row['user_status'] == 'Inactive') {
            ?>
            <div class="log-error use-act-err"><p><?php echo $BIZBOOK['USER_NOT_ACTIVATED_MESSAGE']; ?></p></div>
            <?php
        }
        ?>
        <div class="ud-cen-s2">
            <?php include "../page_level_message.php"; ?>
            <div class="ad-int-sear">
                <input type="text" id="myInput" placeholder="Search this page..">
            </div>
            <a href="#" class="db-tit-btn cta-db-exp-avail" data-toggle="modal"
               data-target="#expstatus"><?php echo $BIZBOOK['SERVICE-EXPERT-UPDATE-MY-AVAILABILITY']; ?></a>
            <table class="responsive-table bordered" id="myTable">
                <thead>
                <tr>
                    <th><?php echo $BIZBOOK['S_NO']; ?></th>
                    <th><?php echo $BIZBOOK['SERVICE-EXPERT-LEAD-DETAILS']; ?></th>
                    <th><?php echo $BIZBOOK['ENQUIRY_DETAILS']; ?></th>
                    <th><?php echo $BIZBOOK['MESSAGE']; ?></th>
                    <th><?php echo $BIZBOOK['RATING']; ?></th>
                    <th><?php echo $BIZBOOK['SERVICE-EXPERT-MANAGE']; ?></th>
                    <th><?php echo $BIZBOOK['STATUS']; ?></th>
                    <th><?php echo $BIZBOOK['DELETE']; ?></th>
                </tr>
                </thead>
                <tbody>
                <?php

                $si = 1;
                foreach (getUserExpertEnquiries($_SESSION['user_id']) as $service_expert_enquiry_row) {

                    $expert_id = $service_expert_enquiry_row['expert_id'];

                    $enquiry_id = $service_expert_enquiry_row['enquiry_id'];

                    $enquiry_sender_id = $service_expert_enquiry_row['enquiry_sender_id'];

                    $sender_user_row = getUser($enquiry_sender_id);

                    $rating_row = getEnquiryExpertExpertReviews($enquiry_id,$expert_id);

                    $rating = number_format(($rating_row['expert_rating']), 1);

                    ?>
                    <tr>
                        <td><?php echo $si; ?></td>
                        <td><img src="<?php echo $slash; ?>images/user/<?php if (($sender_user_row['profile_image'] == NULL) || empty($sender_user_row['profile_image'])) {
                                echo $footer_row['user_default_image'];
                            } else {
                                echo $sender_user_row['profile_image'];
                            } ?>"><?php echo $service_expert_enquiry_row['enquiry_name']; ?>
                            <span><?php echo $BIZBOOK['DATE']; ?>
                                : <?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_cdt']); ?></span></td>
                        <td>
                        <span><b><?php echo $BIZBOOK['PHONE']; ?>
                                : </b><?php echo $service_expert_enquiry_row['enquiry_mobile']; ?></span><br>
                        <span><b><?php echo $BIZBOOK['EMAIL_ID']; ?>
                                : </b><?php echo $service_expert_enquiry_row['enquiry_email']; ?></span><br>
                        <span><b><?php echo $BIZBOOK['LOCATION']; ?>
                                : </b><?php echo $service_expert_enquiry_row['enquiry_location']; ?></span><br>
                        <span><b><?php echo $BIZBOOK['DATE']; ?>
                                : </b><?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></span><br>
                        <span><b><?php echo $BIZBOOK['TIME']; ?>
                                : </b><?php echo $service_expert_enquiry_row['appointment_time']; ?></span>
                        </td>
                        <td><?php echo $service_expert_enquiry_row['enquiry_message']; ?></td>
                        <td><span class="db-list-rat"><?php if($rating == '0.0'){ echo '-'; }else{ echo $rating; } ?></span></td>
                        <td><a href="#" class="db-list-edit cta-blu-sml" data-toggle="modal"
                               data-target="#expfrm<?php echo $enquiry_id; ?>"><?php echo $BIZBOOK['SERVICE-EXPERT-MANAGE']; ?></a>
                        </td>
                        <td><span class="db-list-rat"><?php
                                $enquiry_status = $service_expert_enquiry_row['enquiry_status'];
                                if ($enquiry_status == 100) {
                                    echo $BIZBOOK['SERVICE-EXPERT-CANCEL-LABEL'];
                                } elseif ($enquiry_status == 200) {
                                    echo $BIZBOOK['SERVICE-EXPERT-NEW-LABEL'];
                                } elseif ($enquiry_status == 300) {
                                    echo $BIZBOOK['SERVICE-EXPERT-ON-THE-WAY-LABEL'];
                                } elseif ($enquiry_status == 400) {
                                    echo $BIZBOOK['SERVICE-EXPERT-PENDING-LABEL'];
                                } elseif ($enquiry_status == 500) {
                                    echo $BIZBOOK['SERVICE-EXPERT-DONE-LABEL'];
                                }
                                ?></span></td>
                        <td><a href="<?php echo $slash; ?>service-experts/expert_enquiry_trash.php?messageenquirymessageenquirymessageenquirymessageenquiry=<?php echo $enquiry_id; ?>&&return-url=<?php echo $slash; ?>service-experts/db-service-expert" class="db-list-edit"><span class="material-icons">delete</span></a></td>
                    </tr>
                    <section>
                        <div style="padding-bottom: 0!important;" class="pop-ups pop-quo job-form exp-pop-form">
                            <!-- The Modal -->
                            <div class="modal fade" id="expfrm<?php echo $enquiry_id; ?>">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="log-bor">&nbsp;</div>
                                        <span class="udb-inst"><?php echo $BIZBOOK['SERVICE-EXPERT-MANAGE-LEAD']; ?></span>
                                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                                        <!-- Modal Header -->
                                        <div class="quote-pop">
                                            <div id="expert_manage_lead_success<?php echo $enquiry_id; ?>" class="log" style="display: none;">
                                                <p><?php echo $BIZBOOK['SERVICE-EXPERT-ENQUIRY-STATUS-SUCCESS-MESSAGE']; ?></p>
                                            </div>
                                            <div id="expert_manage_lead_fail<?php echo $enquiry_id; ?>" class="log" style="display: none;">
                                                <p><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></p>
                                            </div>
                                            <form method="post" name="expert_manage_lead_form" id="expert_manage_lead_form<?php echo $enquiry_id; ?>">
                                                <input type="hidden" class="form-control" name="enquiry_id"
                                                       value="<?php echo $enquiry_id; ?>" required>
                                                <input type="hidden" class="form-control" name="expert_user_id"
                                                       value="<?php echo $expert_id; ?>" required>
                                                <div class="form-group">
                                                    <label
                                                        class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-PREFERRED-DATE']; ?></label>
                                                    <input type="text" class="form-control" name="appointment_date"
                                                           value="<?php echo $service_expert_enquiry_row['appointment_date']; ?>"
                                                           id="expredate<?php echo $enquiry_id; ?>">
                                                </div>
                                                <div class="form-group">
                                                    <label
                                                        class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-APPROX-ARRIVE-TIME-LABEL']; ?></label>
                                                    <select class="chosen-select" id="appointment_time"
                                                            name="appointment_time">
                                                        <?php
                                                        $time = '4:00'; // start
                                                        for ($i = 0; $i <= 19; $i++) {
                                                            $prev = date('g:i a', strtotime($time)); // format the start time
                                                            $next = strtotime('+60mins', strtotime($time)); // add 60 mins
                                                            $time = date('g:i A', $next); // format the next time
                                                            ?>
                                                            <option <?php if ($service_expert_enquiry_row['appointment_time'] == $time) {
                                                                echo "selected";
                                                            } ?> value="<?php echo $time; ?>"><?php echo $time; ?></option>
                                                            <?php
                                                        }
                                                        ?>
                                                    </select>
                                                </div>
                                                <div class="form-group">
                                                    <label
                                                        class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-SERVICE-STATUS']; ?></label>
                                                    <select class="chosen-select" name="enquiry_status" id="enquiry_status">
                                                        <option value="500" <?php if ($enquiry_status == 500) {
                                                            echo "selected";
                                                        } ?>><?php echo $BIZBOOK['SERVICE-EXPERT-DONE-LABEL']; ?></option>
                                                        <option value="300" <?php if ($enquiry_status == 300) {
                                                            echo "selected";
                                                        } ?>><?php echo $BIZBOOK['SERVICE-EXPERT-ON-THE-WAY-LABEL']; ?></option>
                                                        <option value="400" <?php if ($enquiry_status == 400) {
                                                            echo "selected";
                                                        } ?>><?php echo $BIZBOOK['SERVICE-EXPERT-PENDING-LABEL']; ?></option>
                                                        <option value="100" <?php if ($enquiry_status == 100) {
                                                            echo "selected";
                                                        } ?>><?php echo $BIZBOOK['SERVICE-EXPERT-CANCEL-LABEL']; ?></option>
                                                        <option value="200" <?php if ($enquiry_status == 200) {
                                                            echo "selected";
                                                        } ?>><?php echo $BIZBOOK['SERVICE-EXPERT-NEW-LABEL']; ?></option>
                                                    </select>
                                                </div>
                                                <button type="submit" id="expert_manage_lead_submit<?php echo $enquiry_id; ?>"
                                                        name="expert_manage_lead_submit"
                                                        class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!--- END --->
                        </div>
                    </section>
                    <?php
                    $si++;
                }
                ?>
                </tbody>
            </table>
        </div>
    </div>
    <!-- START -->
    <section>
        <div style="padding-bottom: 0!important;" class="pop-ups pop-quo job-form exp-pop-form">
            <!-- The Modal -->
            <div class="modal fade" id="expstatus">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="log-bor">&nbsp;</div>
                        <span class="udb-inst"><?php echo $BIZBOOK['SERVICE-EXPERT-AVAILABILITY']; ?></span>
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <!-- Modal Header -->
                        <div class="quote-pop">
                            <div
                                class="ser-exp-wel ser-exp-wel1"><?php echo $BIZBOOK['SERVICE-EXPERT-AVAILABILITY-INFO-DIV']; ?></div>
                            <div id="expert_availability_success" class="log" style="display: none;">
                                <p><?php echo $BIZBOOK['EXPERT_PROFILE_AVAILABILITY_SUCCESS_MESSAGE']; ?></p>
                            </div>
                            <div id="expert_availability_fail" class="log" style="display: none;">
                                <p><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></p>
                            </div>
                            <form method="post" name="expert_availability_form" id="expert_availability_form">
                                <input type="hidden" class="form-control" name="expert_id"
                                       value="<?php echo $service_expert_row['expert_id']; ?>">
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-CHOOSE-AVAILABILITY']; ?></label>
                                    <select class="chosen-select" id="expert_availability_status"
                                            name="expert_availability_status">
                                        <option <?php if ($service_expert_row['expert_availability_status'] == 0) {
                                            echo "selected";
                                        } ?>
                                            value="0"><?php echo $BIZBOOK['SERVICE-EXPERT-AVAILABILITY-READY-TO-WORK-LABEL']; ?></option>
                                        <option <?php if ($service_expert_row['expert_availability_status'] == 1) {
                                            echo "selected";
                                        } ?>
                                            value="1"><?php echo $BIZBOOK['SERVICE-EXPERT-BUSY-ON-OTHER-CUSTOMER-LABEL']; ?></option>
                                        <option <?php if ($service_expert_row['expert_availability_status'] == 2) {
                                            echo "selected";
                                        } ?> value="2"><?php echo $BIZBOOK['SERVICE-EXPERT-END-TODAY-LABEL']; ?></option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-START-TIME-LABEL']; ?></label>
                                    <select class="chosen-select" name="available_time_start">
                                        <?php
                                        $time = '4:00'; // start
                                        for ($i = 0; $i <= 19; $i++) {
                                            $prev = date('g:i a', strtotime($time)); // format the start time
                                            $next = strtotime('+60mins', strtotime($time)); // add 60 mins
                                            $time = date('g:i A', $next); // format the next time
                                            ?>
                                            <option <?php if ($service_expert_row['available_time_start'] == $time) {
                                                echo "selected";
                                            } ?> value="<?php echo $time; ?>"><?php echo $time; ?></option>
                                            <?php
                                        }
                                        ?>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label class="tit"><?php echo $BIZBOOK['SERVICE-EXPERT-CLOSE-TIME-LABEL']; ?></label>
                                    <select class="chosen-select" name="available_time_end">
                                        <?php
                                        $time = '5:00'; // start
                                        for ($i = 0; $i <= 18; $i++) {
                                            $prev = date('g:i a', strtotime($time)); // format the start time
                                            $next = strtotime('+60mins', strtotime($time)); // add 60 mins
                                            $time = date('g:i A', $next); // format the next time
                                            ?>
                                            <option <?php if ($service_expert_row['available_time_end'] == $time) {
                                                echo "selected";
                                            } ?> value="<?php echo $time; ?>"><?php echo $time; ?></option>
                                            <?php
                                        }
                                        ?>
                                    </select>
                                </div>
                                <button type="submit" id="expert_availability_submit" name="expert_availability_submit"
                                        class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!--- END --->
    </section>
    <!-- END -->
<?php
include "../dashboard_right_pane.php";
?>

    <script>

        $(document).ready(function () {
            $("#myInput").on("keyup", function () {
                var value = $(this).val().toLowerCase();
                $("#myTable tr").filter(function () {
                    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
                });
            });
        });
    </script>

<?php

$si = 1;
foreach (getUserExpertEnquiries($_SESSION['user_id']) as $service_expert_enquiry_loop_row) {

    $enquiry_id_new = $service_expert_enquiry_loop_row['enquiry_id'];
    ?>
    <script>
        $(function () {
            $("#expredate<?php echo $enquiry_id_new; ?>").datepicker();
        });
    </script>
    <script>

        //
        <!--Expert Service Manage Lead Form Ajax Call And Validation starts-->

        $("#expert_manage_lead_submit<?php echo $enquiry_id_new; ?>").click(function () {
            $("#expert_manage_lead_form<?php echo $enquiry_id_new; ?>").validate({
                rules: {
                    appointment_date: {required: true},
                    enquiry_status: {required: true},
                    appointment_time: {required: true}

                },
                messages: {
                    appointment_date: {required: "Date is Required"},
                    enquiry_status: {required: "Status is Required"},
                    appointment_time: {required: "Time is Required"}
                },

                submitHandler: function (form) { // for demo
                    //form.submit();

                    if (webpage_full_link != null) {
                        var link = webpage_full_link + 'service-experts/expert_manage_lead_update.php';
                    } else {
                        var link = 'service-experts/expert_manage_lead_update.php';
                    }

                    $.ajax({
                        type: "POST",
                        data: $("#expert_manage_lead_form<?php echo $enquiry_id_new; ?>").serialize(),
                        url: link,
                        cache: true,
                        success: function (html) {
                            // alert(html);
                            if (html == 500500) {
                                $("#expert_manage_lead_fail<?php echo $enquiry_id_new; ?>").show();
                                $("#expert_manage_lead_form<?php echo $enquiry_id_new; ?>")[0].reset();
                            } else {
                                if (html == 403403) {
                                    $("#expert_manage_lead_fail<?php echo $enquiry_id_new; ?>").show();
                                    $("#expert_manage_lead_form<?php echo $enquiry_id_new; ?>")[0].reset();
                                } else {
                                    $("#expert_manage_lead_success<?php echo $enquiry_id_new; ?>").show();
                                    $("#expert_manage_lead_form<?php echo $enquiry_id_new; ?>")[0].reset();
                                    window.location.reload();
                                }
                            }

                        }

                    })
                }
            });
        });
        <!--Expert Service Manage Lead Form Ajax Call And Validation ends-->
    </script>
    <?php
}
?>