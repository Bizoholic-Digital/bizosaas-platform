<?php
include "header.php";
?>

<?php if($footer_row['admin_expert_show'] != 1 || $admin_row['admin_service_expert_options'] != 1){
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Service expert leads</span>
                <div class="ud-cen-s2">
                    <!-- TAB START -->
                    <!-- Nav tabs -->
                      <ul class="nav nav-tabs" role="tablist">
                        <li class="nav-item">
                          <a class="nav-link active" data-toggle="tab" href="#lead-all">All leads</a>
                        </li>
                         <li class="nav-item">
                          <a class="nav-link" data-toggle="tab" href="#home">Today leads</a>
                        </li>
                        <li class="nav-item">
                          <a class="nav-link" data-toggle="tab" href="#lead-fini">Finished service</a>
                        </li>
                        <li class="nav-item">
                          <a class="nav-link" data-toggle="tab" href="#lead-pend">Pending service</a>
                        </li>
                          <li class="nav-item">
                          <a class="nav-link" data-toggle="tab" href="#lead-canc">Cancel service</a>
                        </li>
<!--                        <li class="nav-item">-->
<!--                          <a class="nav-link" data-toggle="tab" href="#lead-repo">Report service</a>-->
<!--                        </li>-->
                      </ul>
                    
                    <!-- Tab panes -->
                      <div class="tab-content">
                       <!-- ALL LEADS -->
                        <div id="lead-all" class="tab-pane active"><br>
                          <h2>All leads - <?php echo AddingZero_BeforeNumber(getAllCountExpertEnquiries()); ?></h2>
                            <?php include "../page_level_message.php"; ?>
                            <table class="responsive-table bordered">
                                    <thead>
                                        <tr style="">
                                            <th>No</th>
                                            <th>Lead details</th>
                                            <th>Details</th>
                                            <th>Message</th>
                                            <th>Delete</th>
                                            <th>Details</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                    <?php
                                    $si = 1;
                                    foreach (getAllExpertEnquiries() as $service_expert_enquiry_row) {

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
                                        <tr>
                                            <td><?php echo $si; ?></td>
                                            <td><img src="../images/user/<?php if (($sender_user_row['profile_image'] == NULL) || empty($sender_user_row['profile_image'])) {
                                                    echo $footer_row['user_default_image'];
                                                } else {
                                                    echo $sender_user_row['profile_image'];
                                                } ?>"><?php echo $service_expert_enquiry_row['enquiry_name']; ?>
                                                <span>Date: <?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_cdt']); ?></span></td>
                                            <td>
                                                <span><b>Phone: </b><?php echo $service_expert_enquiry_row['enquiry_mobile']; ?></span><br>
                                                <span><b>Email:  </b><?php echo $service_expert_enquiry_row['enquiry_email']; ?></span><br>
                                                <span><b>Address: </b><?php echo $service_expert_enquiry_row['enquiry_location']; ?></span><br>
                                                <span><b>Preferred date: </b><?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></span><br>
                                                <span><b>Preferred time: </b><?php echo $service_expert_enquiry_row['appointment_time']; ?></span>
                                            </td>
                                            <td><?php echo $service_expert_enquiry_row['enquiry_message']; ?></td>
                                            <td><a href="trash_service_expert_enquiry.php?messageenquirymessageenquirymessageenquirymessageenquiry=<?php echo $enquiry_id; ?>" class="db-list-edit"><span class="material-icons">delete</span></a></td>
                                            <td><a href="#" class="db-list-edit cta-blu-sml" data-toggle="modal" data-target="#expstatusall<?php echo $enquiry_id; ?>">Details</a></td>
                                        </tr>

                                        <?php
                                        $si++;
                                        }
                                        ?>
                                    </tbody>
                                </table>
                        <!-- END All LEADS -->
                      </div>
                        <!-- TODAY LEADS -->
                        <div id="home" class="tab-pane"><br>
                          <h2>Today leads - <?php echo AddingZero_BeforeNumber(getCountTodayExpertEnquiries()); ?></h2>
                            <?php include "../page_level_message.php"; ?>
                            <table class="responsive-table bordered">
                                <thead>
                                <tr style="">
                                    <th>No</th>
                                    <th>Lead details</th>
                                    <th>Details</th>
                                    <th>Message</th>
                                    <th>Delete</th>
                                    <th>Details</th>
                                </tr>
                                </thead>
                                <tbody>
                                <?php
                                $si = 1;
                                foreach (getAllTodayExpertEnquiries() as $service_expert_enquiry_today_row) {

                                    $enquiry_id = $service_expert_enquiry_today_row['enquiry_id'];

                                    $enquiry_sender_id = $service_expert_enquiry_today_row['enquiry_sender_id'];

                                    $sender_user_row = getUser($enquiry_sender_id);

                                    $expert_id = $service_expert_enquiry_today_row['expert_id'];

                                    $expert_profile_row = getIdExpert($expert_id); //To get Expert Profile Details

                                    $expert_profile_category_id = $service_expert_enquiry_today_row['enquiry_category']; //Enquiry Category Id

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
                                    <tr>
                                        <td><?php echo $si; ?></td>
                                        <td><img src="../images/user/<?php if (($sender_user_row['profile_image'] == NULL) || empty($sender_user_row['profile_image'])) {
                                                echo $footer_row['user_default_image'];
                                            } else {
                                                echo $sender_user_row['profile_image'];
                                            } ?>"><?php echo $service_expert_enquiry_today_row['enquiry_name']; ?>
                                            <span>Date: <?php echo dateFormatconverter($service_expert_enquiry_today_row['enquiry_cdt']); ?></span></td>
                                        <td>
                                            <span><b>Phone: </b><?php echo $service_expert_enquiry_today_row['enquiry_mobile']; ?></span><br>
                                            <span><b>Email:  </b><?php echo $service_expert_enquiry_today_row['enquiry_email']; ?></span><br>
                                            <span><b>Address: </b><?php echo $service_expert_enquiry_today_row['enquiry_location']; ?></span><br>
                                            <span><b>Preferred date: </b><?php echo dateFormatconverter($service_expert_enquiry_today_row['appointment_date']); ?></span><br>
                                            <span><b>Preferred time: </b><?php echo $service_expert_enquiry_today_row['appointment_time']; ?></span>
                                        </td>
                                        <td><?php echo $service_expert_enquiry_today_row['enquiry_message']; ?></td>
                                        <td><a href="trash_service_expert_enquiry.php?messageenquirymessageenquirymessageenquirymessageenquiry=<?php echo $enquiry_id; ?>" class="db-list-edit"><span class="material-icons">delete</span></a></td>
                                        <td><a href="#" class="db-list-edit cta-blu-sml" data-toggle="modal" data-target="#expstatustoday<?php echo $enquiry_id; ?>">Details</a></td>
                                    </tr>

                                    <?php
                                    $si++;
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                        <!-- END TODAY LEADS -->
                          
                        
                          
                        <!-- FINISHED LEADS -->
                        <div id="lead-fini" class="tab-pane"><br>
                          <h2>Finished leads - <?php echo AddingZero_BeforeNumber(getAllCountFinishedExpertEnquiries()); ?></h2>
                            <?php include "../page_level_message.php"; ?>
                            <table class="responsive-table bordered">
                                <thead>
                                <tr style="">
                                    <th>No</th>
                                    <th>Lead details</th>
                                    <th>Details</th>
                                    <th>Message</th>
                                    <th>Delete</th>
                                    <th>Details</th>
                                </tr>
                                </thead>
                                <tbody>
                                <?php
                                $si = 1;
                                foreach (getAllFinishedExpertEnquiries() as $service_expert_enquiry_row) {

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
                                    <tr>
                                        <td><?php echo $si; ?></td>
                                        <td><img src="../images/user/<?php if (($sender_user_row['profile_image'] == NULL) || empty($sender_user_row['profile_image'])) {
                                                echo $footer_row['user_default_image'];
                                            } else {
                                                echo $sender_user_row['profile_image'];
                                            } ?>"><?php echo $service_expert_enquiry_row['enquiry_name']; ?>
                                            <span>Date: <?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_cdt']); ?></span></td>
                                        <td>
                                            <span><b>Phone: </b><?php echo $service_expert_enquiry_row['enquiry_mobile']; ?></span><br>
                                            <span><b>Email:  </b><?php echo $service_expert_enquiry_row['enquiry_email']; ?></span><br>
                                            <span><b>Address: </b><?php echo $service_expert_enquiry_row['enquiry_location']; ?></span><br>
                                            <span><b>Preferred date: </b><?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></span><br>
                                            <span><b>Preferred time: </b><?php echo $service_expert_enquiry_row['appointment_time']; ?></span>
                                        </td>
                                        <td><?php echo $service_expert_enquiry_row['enquiry_message']; ?></td>
                                        <td><a href="trash_service_expert_enquiry.php?messageenquirymessageenquirymessageenquirymessageenquiry=<?php echo $enquiry_id; ?>" class="db-list-edit"><span class="material-icons">delete</span></a></td>
                                        <td><a href="#" class="db-list-edit cta-blu-sml" data-toggle="modal" data-target="#expstatusfinished<?php echo $enquiry_id; ?>">Details</a></td>
                                    </tr>

                                    <?php
                                    $si++;
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                        <!-- END FINISHED LEADS -->  
                          
                        <!-- PENDING LEADS -->
                        <div id="lead-pend" class="tab-pane"><br>
                          <h2>Pending leads - <?php echo AddingZero_BeforeNumber(getAllCountPendingExpertEnquiries()); ?></h2>
                            <?php include "../page_level_message.php"; ?>
                            <table class="responsive-table bordered">
                                <thead>
                                <tr style="">
                                    <th>No</th>
                                    <th>Lead details</th>
                                    <th>Details</th>
                                    <th>Message</th>
                                    <th>Delete</th>
                                    <th>Details</th>
                                </tr>
                                </thead>
                                <tbody>
                                <?php
                                $si = 1;
                                foreach (getAllPendingExpertEnquiries() as $service_expert_enquiry_row) {

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
                                    <tr>
                                        <td><?php echo $si; ?></td>
                                        <td><img src="../images/user/<?php if (($sender_user_row['profile_image'] == NULL) || empty($sender_user_row['profile_image'])) {
                                                echo $footer_row['user_default_image'];
                                            } else {
                                                echo $sender_user_row['profile_image'];
                                            } ?>"><?php echo $service_expert_enquiry_row['enquiry_name']; ?>
                                            <span>Date: <?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_cdt']); ?></span></td>
                                        <td>
                                            <span><b>Phone: </b><?php echo $service_expert_enquiry_row['enquiry_mobile']; ?></span><br>
                                            <span><b>Email:  </b><?php echo $service_expert_enquiry_row['enquiry_email']; ?></span><br>
                                            <span><b>Address: </b><?php echo $service_expert_enquiry_row['enquiry_location']; ?></span><br>
                                            <span><b>Preferred date: </b><?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></span><br>
                                            <span><b>Preferred time: </b><?php echo $service_expert_enquiry_row['appointment_time']; ?></span>
                                        </td>
                                        <td><?php echo $service_expert_enquiry_row['enquiry_message']; ?></td>
                                        <td><a href="trash_service_expert_enquiry.php?messageenquirymessageenquirymessageenquirymessageenquiry=<?php echo $enquiry_id; ?>" class="db-list-edit"><span class="material-icons">delete</span></a></td>
                                        <td><a href="#" class="db-list-edit cta-blu-sml" data-toggle="modal" data-target="#expstatuspending<?php echo $enquiry_id; ?>">Details</a></td>
                                    </tr>

                                    <?php
                                    $si++;
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                        <!-- END PENDING LEADS --> 
                          
                        <!-- CANCEL LEADS -->
                        <div id="lead-canc" class="tab-pane"><br>
                          <h2>Cancel leads - <?php echo AddingZero_BeforeNumber(getAllCountCancelExpertEnquiries()); ?></h2>
                            <?php include "../page_level_message.php"; ?>
                            <table class="responsive-table bordered">
                                <thead>
                                <tr style="">
                                    <th>No</th>
                                    <th>Lead details</th>
                                    <th>Details</th>
                                    <th>Message</th>
                                    <th>Delete</th>
                                    <th>Details</th>
                                </tr>
                                </thead>
                                <tbody>
                                <?php
                                $si = 1;
                                foreach (getAllCancelExpertEnquiries() as $service_expert_enquiry_row) {

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
                                    <tr>
                                        <td><?php echo $si; ?></td>
                                        <td><img src="../images/user/<?php if (($sender_user_row['profile_image'] == NULL) || empty($sender_user_row['profile_image'])) {
                                                echo $footer_row['user_default_image'];
                                            } else {
                                                echo $sender_user_row['profile_image'];
                                            } ?>"><?php echo $service_expert_enquiry_row['enquiry_name']; ?>
                                            <span>Date: <?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_cdt']); ?></span></td>
                                        <td>
                                            <span><b>Phone: </b><?php echo $service_expert_enquiry_row['enquiry_mobile']; ?></span><br>
                                            <span><b>Email:  </b><?php echo $service_expert_enquiry_row['enquiry_email']; ?></span><br>
                                            <span><b>Address: </b><?php echo $service_expert_enquiry_row['enquiry_location']; ?></span><br>
                                            <span><b>Preferred date: </b><?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></span><br>
                                            <span><b>Preferred time: </b><?php echo $service_expert_enquiry_row['appointment_time']; ?></span>
                                        </td>
                                        <td><?php echo $service_expert_enquiry_row['enquiry_message']; ?></td>
                                        <td><a href="trash_service_expert_enquiry.php?messageenquirymessageenquirymessageenquirymessageenquiry=<?php echo $enquiry_id; ?>" class="db-list-edit"><span class="material-icons">delete</span></a></td>
                                        <td><a href="#" class="db-list-edit cta-blu-sml" data-toggle="modal" data-target="#expstatuscancel<?php echo $enquiry_id; ?>">Details</a></td>
                                    </tr>

                                    <?php
                                    $si++;
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                        <!-- END CANCEl LEADS --> 
                          
                        <!-- Report LEADS -->
                        <div id="lead-repo" class="tab-pane"><br>
                          <h2>Report leads  - <?php echo AddingZero_BeforeNumber(getAllCountReportedExpertEnquiries()); ?></h2>
                            <?php include "../page_level_message.php"; ?>
                            <table class="responsive-table bordered">
                                <thead>
                                <tr style="">
                                    <th>No</th>
                                    <th>Lead details</th>
                                    <th>Details</th>
                                    <th>Message</th>
                                    <th>Delete</th>
                                    <th>Details</th>
                                </tr>
                                </thead>
                                <tbody>
                                <?php
                                $si = 1;
                                foreach (getAllReportedExpertEnquiries() as $service_expert_enquiry_row) {

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
                                    <tr>
                                        <td><?php echo $si; ?></td>
                                        <td><img src="../images/user/<?php if (($sender_user_row['profile_image'] == NULL) || empty($sender_user_row['profile_image'])) {
                                                echo $footer_row['user_default_image'];
                                            } else {
                                                echo $sender_user_row['profile_image'];
                                            } ?>"><?php echo $service_expert_enquiry_row['enquiry_name']; ?>
                                            <span>Date: <?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_cdt']); ?></span></td>
                                        <td>
                                            <span><b>Phone: </b><?php echo $service_expert_enquiry_row['enquiry_mobile']; ?></span><br>
                                            <span><b>Email:  </b><?php echo $service_expert_enquiry_row['enquiry_email']; ?></span><br>
                                            <span><b>Address: </b><?php echo $service_expert_enquiry_row['enquiry_location']; ?></span><br>
                                            <span><b>Preferred date: </b><?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></span><br>
                                            <span><b>Preferred time: </b><?php echo $service_expert_enquiry_row['appointment_time']; ?></span>
                                        </td>
                                        <td><?php echo $service_expert_enquiry_row['enquiry_message']; ?></td>
                                        <td><a href="trash_service_expert_enquiry.php?messageenquirymessageenquirymessageenquirymessageenquiry=<?php echo $enquiry_id; ?>" class="db-list-edit"><span class="material-icons">delete</span></a></td>
                                        <td><a href="#" class="db-list-edit cta-blu-sml" data-toggle="modal" data-target="#expstatusreport<?php echo $enquiry_id; ?>">Details</a></td>
                                    </tr>

                                    <?php
                                    $si++;
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                        <!-- END REPORT LEADS --> 
                    <!-- TAB END -->
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
    </div>
</section>
<!-- END -->

<!-- Today Leads Section Pop up starts -->
<?php
$si = 1;
foreach (getAllTodayExpertEnquiries() as $service_expert_enquiry_today_popup_row) {

    $enquiry_id = $service_expert_enquiry_today_popup_row['enquiry_id'];

    $enquiry_sender_id = $service_expert_enquiry_today_popup_row['enquiry_sender_id'];

    $sender_user_row = getUser($enquiry_sender_id);

    $expert_id = $service_expert_enquiry_today_popup_row['expert_id'];

    $expert_profile_row = getIdExpert($expert_id); //To get Expert Profile Details

    $expert_profile_category_id = $service_expert_enquiry_today_popup_row['enquiry_category']; //Enquiry Category Id

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
        <div class="pop-table">
            <!-- The Modal -->
            <div class="modal fade" id="expstatustoday<?php echo $enquiry_id; ?>">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="log-bor">&nbsp;</div>
                        <span class="udb-inst">Lead details</span>
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <div class="inn">
                            <table class="responsive-table bordered">
                                <tbody>
                                <tr>
                                    <td>User</td>
                                    <td>
                                        <a href="<?php echo $PROFILE_URL . urlModifier($sender_user_row['user_slug']); ?>"
                                           target="_blank"><?php echo $service_expert_enquiry_today_popup_row['enquiry_name']; ?></a>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Enquiry details</td>
                                    <td>
                                        <span><b>Phone: </b><?php echo $service_expert_enquiry_today_popup_row['enquiry_mobile']; ?></span><br>
                                        <span><b>Email: </b><?php echo $service_expert_enquiry_today_popup_row['enquiry_email']; ?></span><br>
                                        <span><b>Address: </b><?php echo $service_expert_enquiry_today_popup_row['enquiry_location']; ?></span><br>
                                        <span><b>Preferred
                                                date: </b><?php echo dateFormatconverter($service_expert_enquiry_today_popup_row['appointment_date']); ?></span><br>
                                        <span><b>Preferred
                                                time: </b><?php echo $service_expert_enquiry_today_popup_row['appointment_time']; ?></span>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Message</td>
                                    <td><?php echo $service_expert_enquiry_today_popup_row['enquiry_message']; ?></td>
                                </tr>
                                <tr>
                                    <td>Requested date</td>
                                    <td><?php echo dateFormatconverter($service_expert_enquiry_today_popup_row['enquiry_cdt']); ?></td>
                                </tr>
                                <?php
                                $enquiry_status = $service_expert_enquiry_today_popup_row['enquiry_status'];
                                if ($enquiry_status == 100) {
                                    ?>
                                    <tr>
                                        <td>Closed date</td>
                                        <td><?php echo dateFormatconverter($service_expert_enquiry_today_popup_row['enquiry_udt']); ?></td>
                                    </tr>
                                    <?php
                                }
                                ?>
                                <tr>
                                    <td>Service category</td>
                                    <td><?php echo $expert_category_name; ?></td>
                                </tr>
                                <tr>
                                    <td>Service status</td>
                                    <td><?php
                                        $enquiry_status = $service_expert_enquiry_today_popup_row['enquiry_status'];
                                        if ($enquiry_status == 100) {
                                            echo "Closed";
                                        } elseif ($enquiry_status == 200) {
                                            echo "New";
                                        } elseif ($enquiry_status == 300) {
                                            echo "On the way";
                                        } elseif ($enquiry_status == 400) {
                                            echo "Pending";
                                        } elseif ($enquiry_status == 500) {
                                            echo "Done";
                                        }
                                        ?></td>
                                </tr>
                                <tr>
                                    <td>Expert approximate arrive time & date</td>
                                    <td><?php echo $service_expert_enquiry_today_popup_row['appointment_time']; ?>
                                        , <?php echo dateFormatconverter($service_expert_enquiry_today_popup_row['appointment_date']); ?></td>
                                </tr>
                                <tr>
                                    <td>Who done this</td>
                                    <td>
                                        <a href="<?php echo $PROFILE_URL . urlModifier($expert_profile_row['user_slug']); ?>"
                                           target="_blank"><?php echo $expert_profile_row['profile_name']; ?></a></td>
                                </tr>
                                <?php
                                if ($star_rate_two != 0) {
                                    ?>
                                    <tr>
                                        <td>Rating</td>
                                        <td><?php echo $star_rate_two; ?> - Best
                                            customer service ever
                                        </td>
                                    </tr>
                                    <?php
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <!--- END --->
        </div>
    </section>
    <!-- END -->
    <?php
}
?>
<!-- Today Lead Section Pop up ends -->

<!-- All Lead Section Pop up starts -->
<?php
$si = 1;
foreach (getAllExpertEnquiries() as $service_expert_enquiry_row) {

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
        <div class="pop-table">
            <!-- The Modal -->
            <div class="modal fade" id="expstatusall<?php echo $enquiry_id; ?>">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="log-bor">&nbsp;</div>
                        <span class="udb-inst">Lead details</span>
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <div class="inn">
                            <table class="responsive-table bordered">
                                <tbody>
                                <tr>
                                    <td>User</td>
                                    <td>
                                        <a href="<?php echo $PROFILE_URL . urlModifier($sender_user_row['user_slug']); ?>"
                                           target="_blank"><?php echo $service_expert_enquiry_row['enquiry_name']; ?></a>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Enquiry details</td>
                                    <td>
                                        <span><b>Phone: </b><?php echo $service_expert_enquiry_row['enquiry_mobile']; ?></span><br>
                                        <span><b>Email: </b><?php echo $service_expert_enquiry_row['enquiry_email']; ?></span><br>
                                        <span><b>Address: </b><?php echo $service_expert_enquiry_row['enquiry_location']; ?></span><br>
                                        <span><b>Preferred
                                                date: </b><?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></span><br>
                                        <span><b>Preferred
                                                time: </b><?php echo $service_expert_enquiry_row['appointment_time']; ?></span>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Message</td>
                                    <td><?php echo $service_expert_enquiry_row['enquiry_message']; ?></td>
                                </tr>
                                <tr>
                                    <td>Requested date</td>
                                    <td><?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_cdt']); ?></td>
                                </tr>
                                <?php
                                $enquiry_status = $service_expert_enquiry_row['enquiry_status'];
                                if ($enquiry_status == 100) {
                                    ?>
                                    <tr>
                                        <td>Closed date</td>
                                        <td><?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_udt']); ?></td>
                                    </tr>
                                    <?php
                                }
                                ?>
                                <tr>
                                    <td>Service category</td>
                                    <td><?php echo $expert_category_name; ?></td>
                                </tr>
                                <tr>
                                    <td>Service status</td>
                                    <td><?php
                                        $enquiry_status = $service_expert_enquiry_row['enquiry_status'];
                                        if ($enquiry_status == 100) {
                                            echo "Closed";
                                        } elseif ($enquiry_status == 200) {
                                            echo "New";
                                        } elseif ($enquiry_status == 300) {
                                            echo "On the way";
                                        } elseif ($enquiry_status == 400) {
                                            echo "Pending";
                                        } elseif ($enquiry_status == 500) {
                                            echo "Done";
                                        }
                                        ?></td>
                                </tr>
                                <tr>
                                    <td>Expert approximate arrive time & date</td>
                                    <td><?php echo $service_expert_enquiry_row['appointment_time']; ?>
                                        , <?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></td>
                                </tr>
                                <tr>
                                    <td>Who done this</td>
                                    <td>
                                        <a href="<?php echo $PROFILE_URL . urlModifier($expert_profile_row['user_slug']); ?>"
                                           target="_blank"><?php echo $expert_profile_row['profile_name']; ?></a></td>
                                </tr>
                                <?php
                                if ($star_rate_two != 0) {
                                    ?>
                                    <tr>
                                        <td>Rating</td>
                                        <td><?php echo $star_rate_two; ?> - Best
                                            customer service ever
                                        </td>
                                    </tr>
                                    <?php
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <!--- END --->
        </div>
    </section>
    <!-- END -->
    <?php
}
?>
<!-- All Lead Section Pop up ends -->

<!-- Finished Lead Section Pop up starts -->
<?php
$si = 1;
foreach (getAllFinishedExpertEnquiries() as $service_expert_enquiry_row) {

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
        <div class="pop-table">
            <!-- The Modal -->
            <div class="modal fade" id="expstatusfinished<?php echo $enquiry_id; ?>">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="log-bor">&nbsp;</div>
                        <span class="udb-inst">Lead details</span>
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <div class="inn">
                            <table class="responsive-table bordered">
                                <tbody>
                                <tr>
                                    <td>User</td>
                                    <td>
                                        <a href="<?php echo $PROFILE_URL . urlModifier($sender_user_row['user_slug']); ?>"
                                           target="_blank"><?php echo $service_expert_enquiry_row['enquiry_name']; ?></a>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Enquiry details</td>
                                    <td>
                                        <span><b>Phone: </b><?php echo $service_expert_enquiry_row['enquiry_mobile']; ?></span><br>
                                        <span><b>Email: </b><?php echo $service_expert_enquiry_row['enquiry_email']; ?></span><br>
                                        <span><b>Address: </b><?php echo $service_expert_enquiry_row['enquiry_location']; ?></span><br>
                                        <span><b>Preferred
                                                date: </b><?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></span><br>
                                        <span><b>Preferred
                                                time: </b><?php echo $service_expert_enquiry_row['appointment_time']; ?></span>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Message</td>
                                    <td><?php echo $service_expert_enquiry_row['enquiry_message']; ?></td>
                                </tr>
                                <tr>
                                    <td>Requested date</td>
                                    <td><?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_cdt']); ?></td>
                                </tr>
                                <?php
                                $enquiry_status = $service_expert_enquiry_row['enquiry_status'];
                                if ($enquiry_status == 100) {
                                    ?>
                                    <tr>
                                        <td>Closed date</td>
                                        <td><?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_udt']); ?></td>
                                    </tr>
                                    <?php
                                }
                                ?>
                                <tr>
                                    <td>Service category</td>
                                    <td><?php echo $expert_category_name; ?></td>
                                </tr>
                                <tr>
                                    <td>Service status</td>
                                    <td><?php
                                        $enquiry_status = $service_expert_enquiry_row['enquiry_status'];
                                        if ($enquiry_status == 100) {
                                            echo "Closed";
                                        } elseif ($enquiry_status == 200) {
                                            echo "New";
                                        } elseif ($enquiry_status == 300) {
                                            echo "On the way";
                                        } elseif ($enquiry_status == 400) {
                                            echo "Pending";
                                        } elseif ($enquiry_status == 500) {
                                            echo "Done";
                                        }
                                        ?></td>
                                </tr>
                                <tr>
                                    <td>Expert approximate arrive time & date</td>
                                    <td><?php echo $service_expert_enquiry_row['appointment_time']; ?>
                                        , <?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></td>
                                </tr>
                                <tr>
                                    <td>Who done this</td>
                                    <td>
                                        <a href="<?php echo $PROFILE_URL . urlModifier($expert_profile_row['user_slug']); ?>"
                                           target="_blank"><?php echo $expert_profile_row['profile_name']; ?></a></td>
                                </tr>
                                <?php
                                if ($star_rate_two != 0) {
                                    ?>
                                    <tr>
                                        <td>Rating</td>
                                        <td><?php echo $star_rate_two; ?> - Best
                                            customer service ever
                                        </td>
                                    </tr>
                                    <?php
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <!--- END --->
        </div>
    </section>
    <!-- END -->
    <?php
}
?>
<!-- Finished Lead Section Pop up ends -->

<!-- Pending Lead Section Pop up starts -->
<?php
$si = 1;
foreach (getAllPendingExpertEnquiries() as $service_expert_enquiry_row) {

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
        <div class="pop-table">
            <!-- The Modal -->
            <div class="modal fade" id="expstatuspending<?php echo $enquiry_id; ?>">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="log-bor">&nbsp;</div>
                        <span class="udb-inst">Lead details</span>
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <div class="inn">
                            <table class="responsive-table bordered">
                                <tbody>
                                <tr>
                                    <td>User</td>
                                    <td>
                                        <a href="<?php echo $PROFILE_URL . urlModifier($sender_user_row['user_slug']); ?>"
                                           target="_blank"><?php echo $service_expert_enquiry_row['enquiry_name']; ?></a>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Enquiry details</td>
                                    <td>
                                        <span><b>Phone: </b><?php echo $service_expert_enquiry_row['enquiry_mobile']; ?></span><br>
                                        <span><b>Email: </b><?php echo $service_expert_enquiry_row['enquiry_email']; ?></span><br>
                                        <span><b>Address: </b><?php echo $service_expert_enquiry_row['enquiry_location']; ?></span><br>
                                        <span><b>Preferred
                                                date: </b><?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></span><br>
                                        <span><b>Preferred
                                                time: </b><?php echo $service_expert_enquiry_row['appointment_time']; ?></span>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Message</td>
                                    <td><?php echo $service_expert_enquiry_row['enquiry_message']; ?></td>
                                </tr>
                                <tr>
                                    <td>Requested date</td>
                                    <td><?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_cdt']); ?></td>
                                </tr>
                                <?php
                                $enquiry_status = $service_expert_enquiry_row['enquiry_status'];
                                if ($enquiry_status == 100) {
                                    ?>
                                    <tr>
                                        <td>Closed date</td>
                                        <td><?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_udt']); ?></td>
                                    </tr>
                                    <?php
                                }
                                ?>
                                <tr>
                                    <td>Service category</td>
                                    <td><?php echo $expert_category_name; ?></td>
                                </tr>
                                <tr>
                                    <td>Service status</td>
                                    <td><?php
                                        $enquiry_status = $service_expert_enquiry_row['enquiry_status'];
                                        if ($enquiry_status == 100) {
                                            echo "Closed";
                                        } elseif ($enquiry_status == 200) {
                                            echo "New";
                                        } elseif ($enquiry_status == 300) {
                                            echo "On the way";
                                        } elseif ($enquiry_status == 400) {
                                            echo "Pending";
                                        } elseif ($enquiry_status == 500) {
                                            echo "Done";
                                        }
                                        ?></td>
                                </tr>
                                <tr>
                                    <td>Expert approximate arrive time & date</td>
                                    <td><?php echo $service_expert_enquiry_row['appointment_time']; ?>
                                        , <?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></td>
                                </tr>
                                <tr>
                                    <td>Who done this</td>
                                    <td>
                                        <a href="<?php echo $PROFILE_URL . urlModifier($expert_profile_row['user_slug']); ?>"
                                           target="_blank"><?php echo $expert_profile_row['profile_name']; ?></a></td>
                                </tr>
                                <?php
                                if ($star_rate_two != 0) {
                                    ?>
                                    <tr>
                                        <td>Rating</td>
                                        <td><?php echo $star_rate_two; ?> - Best
                                            customer service ever
                                        </td>
                                    </tr>
                                    <?php
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <!--- END --->
        </div>
    </section>
    <!-- END -->
    <?php
}
?>
<!-- Pending Lead Section Pop up ends -->

<!-- Cancel Lead Section Pop up starts -->
<?php
$si = 1;
foreach (getAllCancelExpertEnquiries() as $service_expert_enquiry_row) {

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
        <div class="pop-table">
            <!-- The Modal -->
            <div class="modal fade" id="expstatuscancel<?php echo $enquiry_id; ?>">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="log-bor">&nbsp;</div>
                        <span class="udb-inst">Lead details</span>
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <div class="inn">
                            <table class="responsive-table bordered">
                                <tbody>
                                <tr>
                                    <td>User</td>
                                    <td>
                                        <a href="<?php echo $PROFILE_URL . urlModifier($sender_user_row['user_slug']); ?>"
                                           target="_blank"><?php echo $service_expert_enquiry_row['enquiry_name']; ?></a>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Enquiry details</td>
                                    <td>
                                        <span><b>Phone: </b><?php echo $service_expert_enquiry_row['enquiry_mobile']; ?></span><br>
                                        <span><b>Email: </b><?php echo $service_expert_enquiry_row['enquiry_email']; ?></span><br>
                                        <span><b>Address: </b><?php echo $service_expert_enquiry_row['enquiry_location']; ?></span><br>
                                        <span><b>Preferred
                                                date: </b><?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></span><br>
                                        <span><b>Preferred
                                                time: </b><?php echo $service_expert_enquiry_row['appointment_time']; ?></span>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Message</td>
                                    <td><?php echo $service_expert_enquiry_row['enquiry_message']; ?></td>
                                </tr>
                                <tr>
                                    <td>Requested date</td>
                                    <td><?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_cdt']); ?></td>
                                </tr>
                                <?php
                                $enquiry_status = $service_expert_enquiry_row['enquiry_status'];
                                if ($enquiry_status == 100) {
                                    ?>
                                    <tr>
                                        <td>Closed date</td>
                                        <td><?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_udt']); ?></td>
                                    </tr>
                                    <?php
                                }
                                ?>
                                <tr>
                                    <td>Service category</td>
                                    <td><?php echo $expert_category_name; ?></td>
                                </tr>
                                <tr>
                                    <td>Service status</td>
                                    <td><?php
                                        $enquiry_status = $service_expert_enquiry_row['enquiry_status'];
                                        if ($enquiry_status == 100) {
                                            echo "Closed";
                                        } elseif ($enquiry_status == 200) {
                                            echo "New";
                                        } elseif ($enquiry_status == 300) {
                                            echo "On the way";
                                        } elseif ($enquiry_status == 400) {
                                            echo "Pending";
                                        } elseif ($enquiry_status == 500) {
                                            echo "Done";
                                        }
                                        ?></td>
                                </tr>
                                <tr>
                                    <td>Expert approximate arrive time & date</td>
                                    <td><?php echo $service_expert_enquiry_row['appointment_time']; ?>
                                        , <?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></td>
                                </tr>
                                <tr>
                                    <td>Who done this</td>
                                    <td>
                                        <a href="<?php echo $PROFILE_URL . urlModifier($expert_profile_row['user_slug']); ?>"
                                           target="_blank"><?php echo $expert_profile_row['profile_name']; ?></a></td>
                                </tr>
                                <?php
                                if ($star_rate_two != 0) {
                                    ?>
                                    <tr>
                                        <td>Rating</td>
                                        <td><?php echo $star_rate_two; ?> - Best
                                            customer service ever
                                        </td>
                                    </tr>
                                    <?php
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <!--- END --->
        </div>
    </section>
    <!-- END -->
    <?php
}
?>
<!-- Cancel Lead Section Pop up ends -->

<!-- Report Lead Section Pop up starts -->
<?php
$si = 1;
foreach (getAllReportedExpertEnquiries() as $service_expert_enquiry_row) {

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
        <div class="pop-table">
            <!-- The Modal -->
            <div class="modal fade" id="expstatusreport<?php echo $enquiry_id; ?>">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="log-bor">&nbsp;</div>
                        <span class="udb-inst">Lead details</span>
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <div class="inn">
                            <table class="responsive-table bordered">
                                <tbody>
                                <tr>
                                    <td>User</td>
                                    <td>
                                        <a href="<?php echo $PROFILE_URL . urlModifier($sender_user_row['user_slug']); ?>"
                                           target="_blank"><?php echo $service_expert_enquiry_row['enquiry_name']; ?></a>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Enquiry details</td>
                                    <td>
                                        <span><b>Phone: </b><?php echo $service_expert_enquiry_row['enquiry_mobile']; ?></span><br>
                                        <span><b>Email: </b><?php echo $service_expert_enquiry_row['enquiry_email']; ?></span><br>
                                        <span><b>Address: </b><?php echo $service_expert_enquiry_row['enquiry_location']; ?></span><br>
                                        <span><b>Preferred
                                                date: </b><?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></span><br>
                                        <span><b>Preferred
                                                time: </b><?php echo $service_expert_enquiry_row['appointment_time']; ?></span>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Message</td>
                                    <td><?php echo $service_expert_enquiry_row['enquiry_message']; ?></td>
                                </tr>
                                <tr>
                                    <td>Requested date</td>
                                    <td><?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_cdt']); ?></td>
                                </tr>
                                <?php
                                $enquiry_status = $service_expert_enquiry_row['enquiry_status'];
                                if ($enquiry_status == 100) {
                                    ?>
                                    <tr>
                                        <td>Closed date</td>
                                        <td><?php echo dateFormatconverter($service_expert_enquiry_row['enquiry_udt']); ?></td>
                                    </tr>
                                    <?php
                                }
                                ?>
                                <tr>
                                    <td>Service category</td>
                                    <td><?php echo $expert_category_name; ?></td>
                                </tr>
                                <tr>
                                    <td>Service status</td>
                                    <td><?php
                                        $enquiry_status = $service_expert_enquiry_row['enquiry_status'];
                                        if ($enquiry_status == 100) {
                                            echo "Closed";
                                        } elseif ($enquiry_status == 200) {
                                            echo "New";
                                        } elseif ($enquiry_status == 300) {
                                            echo "On the way";
                                        } elseif ($enquiry_status == 400) {
                                            echo "Pending";
                                        } elseif ($enquiry_status == 500) {
                                            echo "Done";
                                        }
                                        ?></td>
                                </tr>
                                <tr>
                                    <td>Expert approximate arrive time & date</td>
                                    <td><?php echo $service_expert_enquiry_row['appointment_time']; ?>
                                        , <?php echo dateFormatconverter($service_expert_enquiry_row['appointment_date']); ?></td>
                                </tr>
                                <tr>
                                    <td>Who done this</td>
                                    <td>
                                        <a href="<?php echo $PROFILE_URL . urlModifier($expert_profile_row['user_slug']); ?>"
                                           target="_blank"><?php echo $expert_profile_row['profile_name']; ?></a></td>
                                </tr>
                                <?php
                                if ($star_rate_two != 0) {
                                    ?>
                                    <tr>
                                        <td>Rating</td>
                                        <td><?php echo $star_rate_two; ?> - Best
                                            customer service ever
                                        </td>
                                    </tr>
                                    <?php
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <!--- END --->
        </div>
    </section>
    <!-- END -->
    <?php
}
?>
<!-- Report Lead Section Pop up ends -->

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="../js/jquery.min.js"></script>
<script src="../js/popper.min.js"></script>
<script src="../js/bootstrap.min.js"></script>
<script src="../js/jquery-ui.js"></script>
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>


</body>

</html>