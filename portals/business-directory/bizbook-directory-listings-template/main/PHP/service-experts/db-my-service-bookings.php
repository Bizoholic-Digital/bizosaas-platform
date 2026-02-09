<?php
include "expert-config-info.php";
include "../header.php";

if (file_exists('../config/user_authentication.php')) {
    include('../config/user_authentication.php');
}

if (file_exists('../config/expert_page_authentication.php')) {
    include('../config/expert_page_authentication.php');
}

include "../dashboard_left_pane.php";


$user_id = $_SESSION['user_id'];

$service_expert_row = getExpertUser($user_id);

?>
    <!--CENTER SECTION-->
    <div class="ud-main">
   <div class="ud-main-inn ud-no-rhs">
    <div class="ud-cen">
        <div class="log-bor">&nbsp;</div>
        <span class="udb-inst"><?php echo $BIZBOOK['MY_SERVICE_BOOKINGS']; ?></span>
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
            <table class="responsive-table bordered" id="myTable">
                <thead>
                <tr>
                    <th><?php echo $BIZBOOK['S_NO']; ?></th>
                    <th><?php echo $BIZBOOK['SERVICE-EXPERT-EXPERT-PROFILE']; ?></th>
                    <th><?php echo $BIZBOOK['SERVICE-EXPERT-ENQUIRER-NAME']; ?></th>
                    <th><?php echo $BIZBOOK['ENQUIRY_DETAILS']; ?></th>
                    <th><?php echo $BIZBOOK['MESSAGE']; ?></th>
                    <th><?php echo $BIZBOOK['STATUS']; ?></th>
                    <th><?php echo $BIZBOOK['SERVICE-EXPERT-MANAGE']; ?></th>
                    <th><?php echo $BIZBOOK['DELETE']; ?></th>
                </tr>
                </thead>
                <tbody>
                <?php

                $si = 1;
                foreach (getSenderUserExpertEnquiries($_SESSION['user_id']) as $service_expert_enquiry_row) {

                    $expert_id = $service_expert_enquiry_row['expert_id'];

                    $expert_row = getIdExpert($expert_id); // Expert Table Details

                    $enquiry_id = $service_expert_enquiry_row['enquiry_id'];

                    $enquiry_sender_id = $service_expert_enquiry_row['enquiry_sender_id']; // Enquiry Sender Details

                    $sender_user_row = getUser($enquiry_sender_id);

                    $expert_user_id = $service_expert_enquiry_row['expert_user_id']; // Expert User Table Details

                    $expert_user_row = getUser($expert_user_id);

                    ?>
                    <tr>
                        <td><?php echo $si; ?></td>
                        <td><a target="_blank" href="<?php echo $SERVICE_EXPERT_URL . urlModifier($expert_row['expert_slug']); ?>"><img src="<?php echo $slash; ?>images/user/<?php if (($expert_user_row['profile_image'] == NULL) || empty($expert_user_row['profile_image'])) {
                                echo $footer_row['user_default_image'];
                            } else {
                                echo $expert_user_row['profile_image'];
                            } ?>"><?php echo $expert_user_row['first_name']; ?></a>
                            <span><?php echo $BIZBOOK['DATE']; ?>
                                : <?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_cdt']); ?></span></td>
                        <td><?php echo $service_expert_enquiry_row['enquiry_name']; ?></td>
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
                        <td><a href="<?php echo $slash; ?>service-experts/service-confirmation?code=<?php echo $enquiry_id; ?>" class="db-list-edit"><?php echo $BIZBOOK['SERVICE-EXPERT-MANAGE']; ?></a></td>
                        <td><a href="<?php echo $slash; ?>service-experts/expert_enquiry_trash.php?messageenquirymessageenquirymessageenquirymessageenquiry=<?php echo $enquiry_id; ?>&&return-url=<?php echo $slash; ?>service-experts/db-my-service-bookings" class="db-list-edit"><span class="material-icons">delete</span></a></td>
                    </tr>
                    <?php
                    $si++;
                }
                ?>
                </tbody>
            </table>
        </div>
    </div>
<?php
include "../dashboard_right_pane.php";
?>

    <style>
        .ud-rhs {
            display: none;
        }

        .ud-cen {
            width: 77%;
            margin: 40px 0% 0px 2%;
        }

        @media screen and (max-width: 992px) {
            .ud-cen {
                width: 100%;
                margin: 20px 0% 0px 0%;
            }
        }
    </style>
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