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
                <span class="udb-inst">Service experts</span>
                <div class="ud-cen-s2">
                    <!-- TAB START -->
                    <!-- Nav tabs -->
                    <ul class="nav nav-tabs" role="tablist">
                        <li class="nav-item">
                            <a class="nav-link active" data-toggle="tab" href="#home">Top experts</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#lead-all">All experts</a>
                        </li>
<!--                        <li class="nav-item">-->
<!--                            <a class="nav-link" data-toggle="tab" href="#lead-canc">Report experts</a>-->
<!--                        </li>-->
                    </ul>

                    <!-- Tab panes -->
                    <div class="tab-content">
                        <!-- TODAY LEADS -->
                        <div id="home" class="tab-pane active"><br>
                            <h2>Top experts - <?php echo AddingZero_BeforeNumber(getCountAllTopExperts()); ?></h2>
                            <?php include "../page_level_message.php"; ?>
                            <table class="responsive-table bordered">
                                <thead>
                                <tr style="">
                                    <th>No</th>
                                    <th>User</th>
                                    <th>Services done</th>
                                    <th>Type</th>
                                    <th>Review</th>
                                    <th>Edit</th>
                                    <th>Delete</th>
                                    <th>Details</th>
                                </tr>
                                </thead>
                                <tbody>
                                <?php
                                $si = 1;
                                foreach (getAllTopExperts() as $expert_profile_row) {

                                    $expert_id = $expert_profile_row['expert_id'];

                                    $user_id = $expert_profile_row['user_id'];

                                    $expert_user_row = getUser($user_id);

                                    $user_plan = $expert_user_row['user_plan'];

                                    $plan_type_row = getPlanType($user_plan);

                                    // Service Expert Rating. for Rating of Star Starts

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

// Service Expert Rating. for Rating of Star Ends

                                    ?>
                                    <tr style="">
                                        <td><?php echo $si; ?></td>
                                        <td><img
                                                src="../images/user/<?php if (($expert_user_row['profile_image'] == NULL) || empty($expert_user_row['profile_image'])) {
                                                    echo $footer_row['user_default_image'];
                                                } else {
                                                    echo $expert_user_row['profile_image'];
                                                } ?>"><?php echo $expert_profile_row['profile_name']; ?>
                                            <span>Date: <?php echo dateFormatconverter($expert_profile_row['expert_cdt']); ?></span>
                                        </td>
                                        <td><span
                                                class="db-list-rat"><?php echo AddingZero_BeforeNumber(getIdCountFinishedExpertEnquiries($expert_id)); ?></span>
                                        </td>
                                        <td><span class="db-list-rat"><?php if ($user_plan == 0) {
                                                    echo "Free";
                                                } else {
                                                    echo $plan_type_row['plan_type_name'];
                                                } ?></span></td>
                                        <td><span class="db-list-rat"><?php
                                                if ($star_rate_two != 0) {
                                                    echo $star_rate_two;
                                                }else{
                                                    echo "N/A"; }?></span></td>
                                        <td><a href="expert-edit-profile.php?code=<?php echo $expert_id; ?>" class="db-list-edit"><span
                                                    class="material-icons">edit</span></a></td>
                                        <td><a href="expert-delete-profile.php?code=<?php echo $expert_id; ?>" class="db-list-edit"><span class="material-icons">delete</span></a>
                                        </td>
                                        <td><a href="#" class="db-list-edit cta-blu-sml" data-toggle="modal"
                                               data-target="#expstatustop<?php echo $expert_id; ?>">Details</a></td>
                                    </tr>
                                    <?php
                                    $si++;
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                        <!-- END TODAY LEADS -->

                        <!-- ALL LEADS -->
                        <div id="lead-all" class="tab-pane"><br>
                            <h2>All Experts - <?php echo AddingZero_BeforeNumber(getCountAllExperts()); ?></h2>
                            <?php include "../page_level_message.php"; ?>
                            <table class="responsive-table bordered">
                                <thead>
                                <tr style="">
                                    <th>No</th>
                                    <th>User</th>
                                    <th>Services done</th>
                                    <th>Type</th>
                                    <th>Review</th>
                                    <th>Edit</th>
                                    <th>Delete</th>
                                    <th>Details</th>
                                </tr>
                                </thead>
                                <tbody>
                                <?php
                                $si = 1;
                                foreach (getAllExperts() as $expert_profile_row) {

                                    $expert_id = $expert_profile_row['expert_id'];

                                    $user_id = $expert_profile_row['user_id'];

                                    $expert_user_row = getUser($user_id);

                                    $user_plan = $expert_user_row['user_plan'];

                                    $plan_type_row = getPlanType($user_plan);

                                    // Service Expert Rating. for Rating of Star Starts

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

// Service Expert Rating. for Rating of Star Ends

                                    ?>
                                    <tr style="">
                                        <td><?php echo $si; ?></td>
                                        <td><img
                                                src="../images/user/<?php if (($expert_user_row['profile_image'] == NULL) || empty($expert_user_row['profile_image'])) {
                                                    echo $footer_row['user_default_image'];
                                                } else {
                                                    echo $expert_user_row['profile_image'];
                                                } ?>"><?php echo $expert_profile_row['profile_name']; ?>
                                            <span>Date: <?php echo dateFormatconverter($expert_profile_row['expert_cdt']); ?></span>
                                        </td>
                                        <td><span
                                                class="db-list-rat"><?php echo AddingZero_BeforeNumber(getIdCountFinishedExpertEnquiries($expert_id)); ?></span>
                                        </td>
                                        <td><span class="db-list-rat"><?php if ($user_plan == 0) {
                                                    echo "Free";
                                                } else {
                                                    echo $plan_type_row['plan_type_name'];
                                                } ?></span></td>
                                        <td><span class="db-list-rat"><?php
                                                if ($star_rate_two != 0) {
                                                    echo $star_rate_two;
                                                }else{
                                                echo "N/A"; }?></span></td>
                                        <td><a href="expert-edit-profile.php?code=<?php echo $expert_id; ?>" class="db-list-edit"><span
                                                    class="material-icons">edit</span></a></td>
                                        <td><a href="expert-delete-profile.php?code=<?php echo $expert_id; ?>" class="db-list-edit"><span class="material-icons">delete</span></a>
                                        </td>
                                        <td><a href="#" class="db-list-edit cta-blu-sml" data-toggle="modal"
                                               data-target="#expstatusall<?php echo $expert_id; ?>">Details</a></td>
                                    </tr>
                                    <?php
                                    $si++;
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                        <!-- END All LEADS -->

                        <!-- CANCEL LEADS -->
                        <div id="lead-canc" class="tab-pane"><br>
                            <h2>Reported Experts - 18</h2>
                            <?php include "../page_level_message.php"; ?>
                            <table class="responsive-table bordered">
                                <thead>
                                <tr style="">
                                    <th>No</th>
                                    <th>User</th>
                                    <th>Services done</th>
                                    <th>Type</th>
                                    <th>Review</th>
                                    <th>Edit</th>
                                    <th>Delete</th>
                                    <th>Details</th>
                                </tr>
                                </thead>
                                <tbody>
                                <?php
                                $si = 1;
                                foreach (getAllExperts() as $expert_profile_row) {

                                    $expert_id = $expert_profile_row['expert_id'];

                                    $expert_user_row = getUser($expert_id);

                                    $expert_profile_category_id = $expert_profile_row['enquiry_category']; //Enquiry Category Id

                                    $expert_profile_category_row = getExpertCategory($expert_profile_category_id);

                                    $expert_category_name = $expert_profile_category_row['category_name']; // Enquired Category Name


                                    ?>
                                    <tr style="">
                                        <td><?php echo $si; ?></td>
                                        <td><img
                                                src="../images/user/<?php if (($expert_user_row['profile_image'] == NULL) || empty($expert_user_row['profile_image'])) {
                                                    echo $footer_row['user_default_image'];
                                                } else {
                                                    echo $expert_user_row['profile_image'];
                                                } ?>"><?php echo $expert_profile_row['profile_name']; ?>
                                            <span>Date: <?php echo dateFormatconverter($expert_profile_row['expert_cdt']); ?></span>
                                        </td>
                                        <td><span class="db-list-rat">50</span></td>
                                        <td><span class="db-list-rat">Premium</span></td>
                                        <td><span class="db-list-rat">4.0</span></td>
                                        <td><a href="#" class="db-list-edit"><span
                                                    class="material-icons">edit</span></a></td>
                                        <td><a href="#" class="db-list-edit"><span class="material-icons">delete</span></a>
                                        </td>
                                        <td><a href="#" class="db-list-edit cta-blu-sml" data-toggle="modal"
                                               data-target="#expstatus">Details</a></td>
                                    </tr>
                                    <?php
                                    $si++;
                                }
                                ?>
                                </tbody>
                            </table>
                        </div>
                        <!-- END CANCEl LEADS -->
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

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="../js/jquery.min.js"></script>
<script src="../js/popper.min.js"></script>
<script src="../js/bootstrap.min.js"></script>
<script src="../js/jquery-ui.js"></script>
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>

<!-- Top Experts Section Pop up starts -->
<?php
$si = 1;
foreach (getAllTopExperts() as $expert_profile_row) {

    $expert_id = $expert_profile_row['expert_id'];

    $user_id = $expert_profile_row['user_id'];

    $expert_user_row = getUser($user_id);

    $user_plan = $expert_user_row['user_plan'];

    $plan_type_row = getPlanType($user_plan);

    $expert_profile_category_id = $expert_profile_row['category_id'];

    $expert_profile_city_id = $expert_profile_row['city_id'];

    $expert_profile_category_row = getExpertCategory($expert_profile_category_id);

    $expert_category_name = $expert_profile_category_row['category_name'];

    $expert_profile_city_row = getExpertCity($expert_profile_city_id);

    $expert_city_name = $expert_profile_city_row['country_name'];

    //To calculate the expiry date from user created date starts

    $start_date_timestamp = strtotime($expert_user_row['user_cdt']);
    $plan_type_duration = $plan_type_row['plan_type_duration'];

    $expiry_date_timestamp = strtotime("+$plan_type_duration months", $start_date_timestamp);

    $expiry_date = date("Y-m-d h:i:s", $expiry_date_timestamp);

    //To calculate the expiry date from user created date ends

    ?>
    <!-- START -->
    <section>
        <div class="pop-table">
            <!-- The Modal -->
            <div class="modal fade" id="expstatustop<?php echo $expert_id; ?>">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="log-bor">&nbsp;</div>
                        <span class="udb-inst">Expert details</span>
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <div class="inn">
                            <table class="responsive-table bordered">
                                <tbody>
                                <tr>
                                    <td>User</td>
                                    <td>
                                        <a href="<?php echo $SERVICE_EXPERT_URL . urlModifier($expert_profile_row['expert_slug']); ?>"
                                           target="_blank"><?php echo $expert_profile_row['profile_name']; ?></a></td>
                                </tr>
                                <tr>
                                    <td>Profile image</td>
                                    <td>
                                        <a href="../service-experts/images/services/<?php echo $expert_profile_row['profile_image']; ?>"
                                           target="_blank"><img
                                                src="../service-experts/images/services/<?php echo $expert_profile_row['profile_image']; ?>"></a>
                                    </td>
                                </tr>
                                <tr>
                                    <td>User type</td>
                                    <td><?php if ($user_plan == 0) {
                                            echo "Free";
                                        } else {
                                            echo $plan_type_row['plan_type_name'];
                                        } ?></td>
                                </tr>
                                <tr>
                                    <td>Last payment</td>
                                    <td><span class="db-list-rat"><?php if ($plan_type_row['plan_type_price'] == 0) {
                                                echo "FREE";
                                            } else {
                                                echo $footer_row['currency_symbol'] . '' . $plan_type_row['plan_type_price'];
                                            } ?></span></td>
                                </tr>
                                <tr>
                                    <td>Plan start date</td>
                                    <td><?php if ($expert_user_row['payment_status'] == 'Paid') {
                                            echo dateFormatconverter($expert_user_row['user_cdt']);
                                        } else {
                                            echo "N/A";
                                        } ?></td>
                                </tr>
                                <tr>
                                    <td>Plan end date</td>
                                    <td><?php if ($expert_user_row['payment_status'] == 'Paid') {
                                            echo dateFormatconverter($expiry_date);
                                        } else {
                                            echo "N/A";
                                        } ?></td>
                                </tr>
                                <tr>
                                    <td>Work profession</td>
                                    <td><?php echo $expert_category_name; ?></td>
                                </tr>
                                <tr>
                                    <td>City</td>
                                    <td><?php echo $expert_city_name; ?></td>
                                </tr>
                                <tr>
                                    <td>Year of experience</td>
                                    <td><?php echo $expert_profile_row['years_of_experience']; ?></td>
                                </tr>
                                <tr>
                                    <td>Service start time</td>
                                    <td><?php echo $expert_profile_row['available_time_start']; ?></td>
                                </tr>
                                <tr>
                                    <td>Service close time</td>
                                    <td><?php echo $expert_profile_row['available_time_end']; ?></td>
                                </tr>
                                <tr>
                                    <td>Base fare</td>
                                    <td><?php echo $footer_row['currency_symbol']; ?><?php echo $expert_profile_row['base_fare']; ?></td>
                                </tr>
                                <tr>
                                    <td>Services can do</td>
                                    <td><?php
                                        $sub_category = explode(',', $expert_profile_row['sub_category_id']);
                                        foreach ($sub_category as $sub_category_id) {
                                            $sub_category_name = getExpertSubCategory($sub_category_id);
                                            ?>
                                            <?php echo $sub_category_name['sub_category_name'] . ' ,'; ?>
                                            <?php
                                        }
                                        ?></td>
                                </tr>
                                <tr>
                                    <td>Service Areas</td>
                                    <td><?php
                                        $area_set = explode(',', $expert_profile_row['area_id']);
                                        foreach ($area_set as $area_set_id) {
                                            $area_name = getExpertArea($area_set_id);
                                            ?>
                                            <?php echo $area_name['city_name'] . ' ,'; ?>
                                            <?php
                                        }
                                        ?></td>
                                </tr>
                                <tr>
                                    <td>Experience details</td>
                                    <td>
                                        <ul>
                                            <?php
                                            if ($expert_profile_row['experience_1'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['experience_1']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['experience_2'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['experience_2']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['experience_3'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['experience_3']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['experience_4'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['experience_4']; ?></li>
                                                <?php
                                            }
                                            ?>
                                        </ul>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Education and Qualifications</td>
                                    <td>
                                        <ul>
                                            <?php
                                            if ($expert_profile_row['education_1'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['education_1']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['education_2'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['education_2']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['education_3'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['education_3']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['education_4'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['education_4']; ?></li>
                                                <?php
                                            }
                                            ?>
                                        </ul>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Additional information</td>
                                    <td>
                                        <ul>
                                            <?php
                                            if ($expert_profile_row['additional_info_1'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['additional_info_1']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['additional_info_2'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['additional_info_2']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['additional_info_3'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['additional_info_3']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['additional_info_4'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['additional_info_4']; ?></li>
                                                <?php
                                            }
                                            ?>
                                        </ul>
                                    </td>
                                </tr>
                                <tr>
                                    <td>ID proof</td>
                                    <td>
                                        <a href="../service-experts/images/services/<?php echo $expert_profile_row['id_proof']; ?>"
                                           target="_blank"><img
                                                src="../service-experts/images/services/<?php echo $expert_profile_row['id_proof']; ?>"></a>
                                    </td>
                                </tr>
                                <!--                                <tr>-->
                                <!--                                    <td>Address</td>-->
                                <!--                                    <td>-->
                                <!--                                        <ul>-->
                                <!--                                            <li>Temporary address: 28800 Orchard Lake Road, Suite 180 Farmington Hills,-->
                                <!--                                                U.S.A.-->
                                <!--                                            </li>-->
                                <!--                                            <li>Permanent address: 28800 Orchard Lake Road, Suite 180 Farmington Hills,-->
                                <!--                                                U.S.A.-->
                                <!--                                            </li>-->
                                <!--                                        </ul>-->
                                <!--                                    </td>-->
                                <!--                                </tr>-->
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
<!-- Top Experts Section Pop up ends -->

<!-- All Experts Section Pop up starts -->
<?php
$si = 1;
foreach (getAllExperts() as $expert_profile_row) {

    $expert_id = $expert_profile_row['expert_id'];

    $user_id = $expert_profile_row['user_id'];

    $expert_user_row = getUser($user_id);

    $user_plan = $expert_user_row['user_plan'];

    $plan_type_row = getPlanType($user_plan);

    $expert_profile_category_id = $expert_profile_row['category_id'];

    $expert_profile_city_id = $expert_profile_row['city_id'];

    $expert_profile_category_row = getExpertCategory($expert_profile_category_id);

    $expert_category_name = $expert_profile_category_row['category_name'];

    $expert_profile_city_row = getExpertCity($expert_profile_city_id);

    $expert_city_name = $expert_profile_city_row['country_name'];

    //To calculate the expiry date from user created date starts

    $start_date_timestamp = strtotime($expert_user_row['user_cdt']);
    $plan_type_duration = $plan_type_row['plan_type_duration'];

    $expiry_date_timestamp = strtotime("+$plan_type_duration months", $start_date_timestamp);

    $expiry_date = date("Y-m-d h:i:s", $expiry_date_timestamp);

    //To calculate the expiry date from user created date ends

    ?>
    <!-- START -->
    <section>
        <div class="pop-table">
            <!-- The Modal -->
            <div class="modal fade" id="expstatusall<?php echo $expert_id; ?>">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="log-bor">&nbsp;</div>
                        <span class="udb-inst">Expert details</span>
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <div class="inn">
                            <table class="responsive-table bordered">
                                <tbody>
                                <tr>
                                    <td>User</td>
                                    <td>
                                        <a href="<?php echo $SERVICE_EXPERT_URL . urlModifier($expert_profile_row['expert_slug']); ?>"
                                           target="_blank"><?php echo $expert_profile_row['profile_name']; ?></a></td>
                                </tr>
                                <tr>
                                    <td>Profile image</td>
                                    <td>
                                        <a href="../service-experts/images/services/<?php echo $expert_profile_row['profile_image']; ?>"
                                           target="_blank"><img
                                                src="../service-experts/images/services/<?php echo $expert_profile_row['profile_image']; ?>"></a>
                                    </td>
                                </tr>
                                <tr>
                                    <td>User type</td>
                                    <td><?php if ($user_plan == 0) {
                                            echo "Free";
                                        } else {
                                            echo $plan_type_row['plan_type_name'];
                                        } ?></td>
                                </tr>
                                <tr>
                                    <td>Last payment</td>
                                    <td><span class="db-list-rat"><?php if ($plan_type_row['plan_type_price'] == 0) {
                                                echo "FREE";
                                            } else {
                                                echo $footer_row['currency_symbol'] . '' . $plan_type_row['plan_type_price'];
                                            } ?></span></td>
                                </tr>
                                <tr>
                                    <td>Plan start date</td>
                                    <td><?php if ($expert_user_row['payment_status'] == 'Paid') {
                                            echo dateFormatconverter($expert_user_row['user_cdt']);
                                        } else {
                                            echo "N/A";
                                        } ?></td>
                                </tr>
                                <tr>
                                    <td>Plan end date</td>
                                    <td><?php if ($expert_user_row['payment_status'] == 'Paid') {
                                            echo dateFormatconverter($expiry_date);
                                        } else {
                                            echo "N/A";
                                        } ?></td>
                                </tr>
                                <tr>
                                    <td>Work profession</td>
                                    <td><?php echo $expert_category_name; ?></td>
                                </tr>
                                <tr>
                                    <td>City</td>
                                    <td><?php echo $expert_city_name; ?></td>
                                </tr>
                                <tr>
                                    <td>Year of experience</td>
                                    <td><?php echo $expert_profile_row['years_of_experience']; ?></td>
                                </tr>
                                <tr>
                                    <td>Service start time</td>
                                    <td><?php echo $expert_profile_row['available_time_start']; ?></td>
                                </tr>
                                <tr>
                                    <td>Service close time</td>
                                    <td><?php echo $expert_profile_row['available_time_end']; ?></td>
                                </tr>
                                <tr>
                                    <td>Base fare</td>
                                    <td><?php echo $footer_row['currency_symbol']; ?><?php echo $expert_profile_row['base_fare']; ?></td>
                                </tr>
                                <tr>
                                    <td>Services can do</td>
                                    <td><?php
                                        $sub_category = explode(',', $expert_profile_row['sub_category_id']);
                                        foreach ($sub_category as $sub_category_id) {
                                            $sub_category_name = getExpertSubCategory($sub_category_id);
                                            ?>
                                            <?php echo $sub_category_name['sub_category_name'] . ' ,'; ?>
                                            <?php
                                        }
                                        ?></td>
                                </tr>
                                <tr>
                                    <td>Service Areas</td>
                                    <td><?php
                                        $area_set = explode(',', $expert_profile_row['area_id']);
                                        foreach ($area_set as $area_set_id) {
                                            $area_name = getExpertArea($area_set_id);
                                            ?>
                                            <?php echo $area_name['city_name'] . ' ,'; ?>
                                            <?php
                                        }
                                        ?></td>
                                </tr>
                                <tr>
                                    <td>Experience details</td>
                                    <td>
                                        <ul>
                                            <?php
                                            if ($expert_profile_row['experience_1'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['experience_1']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['experience_2'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['experience_2']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['experience_3'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['experience_3']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['experience_4'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['experience_4']; ?></li>
                                                <?php
                                            }
                                            ?>
                                        </ul>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Education and Qualifications</td>
                                    <td>
                                        <ul>
                                            <?php
                                            if ($expert_profile_row['education_1'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['education_1']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['education_2'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['education_2']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['education_3'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['education_3']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['education_4'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['education_4']; ?></li>
                                                <?php
                                            }
                                            ?>
                                        </ul>
                                    </td>
                                </tr>
                                <tr>
                                    <td>Additional information</td>
                                    <td>
                                        <ul>
                                            <?php
                                            if ($expert_profile_row['additional_info_1'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['additional_info_1']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['additional_info_2'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['additional_info_2']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['additional_info_3'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['additional_info_3']; ?></li>
                                                <?php
                                            }
                                            if ($expert_profile_row['additional_info_4'] != NULL) {
                                                ?>
                                                <li><?php echo $expert_profile_row['additional_info_4']; ?></li>
                                                <?php
                                            }
                                            ?>
                                        </ul>
                                    </td>
                                </tr>
                                <tr>
                                    <td>ID proof</td>
                                    <td>
                                        <a href="../service-experts/images/services/<?php echo $expert_profile_row['id_proof']; ?>"
                                           target="_blank"><img
                                                src="../service-experts/images/services/<?php echo $expert_profile_row['id_proof']; ?>"></a>
                                    </td>
                                </tr>
                                <!--                                <tr>-->
                                <!--                                    <td>Address</td>-->
                                <!--                                    <td>-->
                                <!--                                        <ul>-->
                                <!--                                            <li>Temporary address: 28800 Orchard Lake Road, Suite 180 Farmington Hills,-->
                                <!--                                                U.S.A.-->
                                <!--                                            </li>-->
                                <!--                                            <li>Permanent address: 28800 Orchard Lake Road, Suite 180 Farmington Hills,-->
                                <!--                                                U.S.A.-->
                                <!--                                            </li>-->
                                <!--                                        </ul>-->
                                <!--                                    </td>-->
                                <!--                                </tr>-->
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
<!-- All Experts Section Pop up ends -->
</body>

</html>