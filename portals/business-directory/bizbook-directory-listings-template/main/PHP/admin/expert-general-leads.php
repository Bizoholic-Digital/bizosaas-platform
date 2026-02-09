<?php
include "header.php";
?>

<?php if ($footer_row['admin_expert_show'] != 1 || $admin_row['admin_service_expert_options'] != 1) {
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Service general leads</span>
                <div class="ud-cen-s2">
                    <h2>General leads - <?php echo AddingZero_BeforeNumber(getAllCountExpertGeneralEnquiries()); ?></h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered">
                        <thead>
                        <tr style="">
                            <th>No</th>
                            <th>Lead details</th>
                            <th>Service</th>
                            <th>Details</th>
                            <th>Message</th>
                            <th>Assign to</th>
                            <th>Delete</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllExpertGeneralEnquiries() as $service_expert_enquiry_row) {

                            $enquiry_id = $service_expert_enquiry_row['enquiry_id'];

                            $enquiry_sender_id = $service_expert_enquiry_row['enquiry_sender_id'];

                            $sender_user_row = getUser($enquiry_sender_id);

                            $expert_id = $service_expert_enquiry_row['expert_id'];

                            $expert_profile_row = getIdExpert($expert_id); //To get Expert Profile Details

                            $expert_profile_category_id = $service_expert_enquiry_row['enquiry_category']; //Enquiry Category Id

                            $expert_profile_category_row = getExpertCategory($expert_profile_category_id);

                            $expert_category_name = $expert_profile_category_row['category_name']; // Enquired Category Name

                            //Ratings Starts

                            foreach (getExpertReview($expert_id) as $star_rating_row) {
                                if ($star_rating_row["rate_cnt"] > 0) {
                                    $star_rate_times = $star_rating_row["rate_cnt"];
                                    $star_sum_rates = $star_rating_row["total_rate"];
                                    $star_rate_one = $star_sum_rates / $star_rate_times;
                                    $star_rate_two = number_format($star_rate_one, 1);
                                    $star_rate = floatval($star_rate_two);

                                } else {
                                    $rate_times = 0;
                                    $rate_value = 0;
                                    $star_rate = 0;
                                }
                            }

                            //Ratings Ends

                            ?>
                            <tr style="">
                                <td><?php echo $si; ?></td>
                                <td><img
                                        src="../images/user/<?php if (($sender_user_row['profile_image'] == NULL) || empty($sender_user_row['profile_image'])) {
                                            echo $footer_row['user_default_image'];
                                        } else {
                                            echo $sender_user_row['profile_image'];
                                        } ?>"><?php echo $service_expert_enquiry_row['enquiry_name']; ?>
                                    <span>Date: <?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_cdt']); ?></span>
                                </td>
                                <td><span class="db-list-ststus"><?php echo $expert_category_name; ?></span></td>
                                <td>
                                    <span><b>Phone: </b><?php echo $service_expert_enquiry_row['enquiry_mobile']; ?></span><br>
                                    <span><b>Email: </b><?php echo $service_expert_enquiry_row['enquiry_email']; ?></span><br>
                                    <span><b>Address: </b><?php echo $service_expert_enquiry_row['enquiry_location']; ?></span><br>
                                    <span><b>Preferred
                                            date: </b><?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></span><br>
                                    <span><b>Preferred
                                            time: </b><?php echo $service_expert_enquiry_row['appointment_time']; ?></span>
                                </td>
                                <td><?php echo $service_expert_enquiry_row['enquiry_message']; ?></td>
                                <td><a href="#" class="db-list-edit cta-blu-sml" data-toggle="modal"
                                       data-target="#expstatus<?php echo $enquiry_id; ?>">Assign to</a></td>
                                <td>
                                    <a href="trash_service_expert_enquiry.php?messageenquirymessageenquirymessageenquirymessageenquiry=<?php echo $enquiry_id; ?>&&path=1"
                                       class="db-list-edit"><span class="material-icons">delete</span></a></td>
                            </tr>
                            <?php
                            $si++;
                        }
                        ?>
                        </tbody>
                    </table>
                </div>

            </div>
            <div class="ad-pgnat">
                <ul class="pagination">
                    <li class="page-item"><a class="page-link" href="#">Previous</a></li>
                    <li class="page-item active"><a class="page-link" href="#">1</a></li>
                    <li class="page-item"><a class="page-link" href="#">2</a></li>
                    <li class="page-item"><a class="page-link" href="#">3</a></li>
                    <li class="page-item"><a class="page-link" href="#">Next</a></li>
                </ul>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<?php
$si = 1;
foreach (getAllExpertGeneralEnquiries() as $service_expert_enquiry_row) {

    $enquiry_id = $service_expert_enquiry_row['enquiry_id'];

    $enquiry_sender_id = $service_expert_enquiry_row['enquiry_sender_id'];

    $sender_user_row = getUser($enquiry_sender_id);

    $expert_id = $service_expert_enquiry_row['expert_id'];

    $expert_profile_row = getIdExpert($expert_id); //To get Expert Profile Details

    $expert_profile_category_id = $service_expert_enquiry_row['enquiry_category']; //Enquiry Category Id

    $expert_profile_category_row = getExpertCategory($expert_profile_category_id);

    $expert_category_name = $expert_profile_category_row['category_name']; // Enquired Category Name

//Ratings Starts

    foreach (getExpertReview($expert_id) as $star_rating_row) {
        if ($star_rating_row["rate_cnt"] > 0) {
            $star_rate_times = $star_rating_row["rate_cnt"];
            $star_sum_rates = $star_rating_row["total_rate"];
            $star_rate_one = $star_sum_rates / $star_rate_times;
            $star_rate_two = number_format($star_rate_one, 1);
            $star_rate = floatval($star_rate_two);

        } else {
            $rate_times = 0;
            $rate_value = 0;
            $star_rate = 0;
        }
    }

//Ratings Ends

    ?>
    <!-- START -->
    <section>
        <div class="pop-table job-form">
            <!-- The Modal -->
            <div class="modal fade" id="expstatus<?php echo $enquiry_id; ?>">
                <div class="modal-dialog modal-sm">
                    <div class="modal-content">
                        <div class="log-bor">&nbsp;</div>
                        <span class="udb-inst">Assign to</span>
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <div class="inn">
                            <div id="assign_service_expert_success<?php echo $enquiry_id; ?>" class="log" style="display: none;"><p>Service Provider Assigned Successfully!!!</p>
                            </div>
                            <div id="assign_service_expert_fail<?php echo $enquiry_id; ?>" class="log" style="display: none;"><p>Oops!! Something Went Wrong Try Later!!!</p>
                            </div>
                            <div id="assign_service_expert_same<?php echo $enquiry_id; ?>" class="log" style="display: none;"><p>You cannot assign same user with same enquirer!!</p>
                            </div>
                            <form name="assign_service_expert_form" id="assign_service_expert_form<?php echo $enquiry_id; ?>" method="post">
                                <input type="hidden" class="form-control"
                                       name="enquiry_id"
                                       value="<?php echo $enquiry_id; ?>"
                                       placeholder=""
                                       required>
                                <input type="hidden" class="form-control"
                                       name="enquiry_sender_id"
                                       value="<?php echo $enquiry_sender_id; ?>"
                                       placeholder=""
                                       required>
                                <div class="form-group col-md-12">
                                    <label class="tit">Assign to service expert</label>
                                    <select class="form-control" required="required" id="expert_id" name="expert_id">

                                        <option value="">Select Expert</option>
                                        <?php
                                        foreach (getAllExpertCategory($expert_profile_category_id) as $service_experts_row) {

                                            $expert_id = $service_experts_row['expert_id'];

                                            $profile_name = $service_experts_row['profile_name'];
                                            ?>
                                            <option value="<?php echo $expert_id; ?>"><?php echo $profile_name; ?></option>
                                            <?php
                                        }
                                        ?>
                                    </select>
                                </div>
                                <div class="form-group col-md-12">
                                    <button type="submit" name="assign_service_expert_submit" id="assign_service_expert_submit<?php echo $enquiry_id; ?>" class="btn btn-primary btn-block">Submit</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            <!--- END --->
        </div>
    </section>
    <!-- END -->
    <?php
    $si++;
}
?>


<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="../js/jquery.min.js"></script>
<script src="../js/popper.min.js"></script>
<script src="../js/bootstrap.min.js"></script>
<script src="../js/jquery-ui.js"></script>
<script src="../js/select-opt.js"></script>
<script src="../js/jquery.validate.min.js"></script>
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>

<?php
$si = 1;
foreach (getAllExpertGeneralEnquiries() as $service_expert_enquiry_row) {

    $enquiry_id = $service_expert_enquiry_row['enquiry_id'];?>
    <script>
        //        <!--Admin Assign Service provider to enquiry Form Ajax Call And Validation starts-->
        $("#assign_service_expert_submit<?php echo $enquiry_id; ?>").click(function () {
            $("#assign_service_expert_form<?php echo $enquiry_id; ?>").validate({
                rules: {
                    expert_id: {required: true}


                },
                messages: {
                    expert_id: {required: "Name is Required"}
                },

                submitHandler: function (form) { // for demo
                    //form.submit();


                    var link = 'update_assign_service_provider.php';


                    $.ajax({
                        type: "POST",
                        data: $("#assign_service_expert_form<?php echo $enquiry_id; ?>").serialize(),
                        url: link,
                        cache: true,
                        success: function (html) {
                            // alert(html);
                            if (html == 500500) {
                                $("#assign_service_expert_fail<?php echo $enquiry_id; ?>").show().delay(2000).fadeOut();
                                $("#assign_service_expert_form<?php echo $enquiry_id; ?>")[0].reset();
                            } else {
                                if (html == 403403) {
                                    $("#assign_service_expert_same<?php echo $enquiry_id; ?>").show().delay(2000).fadeOut();
                                    $("#assign_service_expert_form<?php echo $enquiry_id; ?>")[0].reset();
                                } else {
                                    $("#assign_service_expert_success<?php echo $enquiry_id; ?>").show().delay(2000).fadeOut();
                                    $("#assign_service_expert_form<?php echo $enquiry_id; ?>")[0].reset();
                                    setTimeout(function(){// wait for 5 secs(2)
                                        location.reload(); // then reload the page.(3)
                                    }, 3000);
                                }
                            }

                        }

                    })
                }
            });
        });
        <!--Admin Assign Service provider to enquiry Form Ajax Call And Validation ends-->
    </script>

    <?php
    $si++;
}
?>

</body>

</html>