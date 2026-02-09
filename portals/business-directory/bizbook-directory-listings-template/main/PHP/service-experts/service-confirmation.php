<?php
include "expert-config-info.php";
include "../header.php";

if (isset($_SESSION['user_id'])) {
    $session_user_id = $_SESSION['user_id'];
}
$user_details_row = getUser($session_user_id);

$redirect_url = $webpage_full_link . 'dashboard';  //Redirect Url

if ($_GET['code'] == NULL && empty($_GET['code'])) {

    header("Location: $redirect_url");  //Redirect When code parameter is empty
}

if (isset($_GET['code'])) {

    $enquiry_id = $_GET['code'];

    $expert_enquiry_search_row = getExpertEnquiries($enquiry_id);  //Fetch Enquiry using Enquiry Id

    $expert_id = $expert_enquiry_search_row['expert_id'];

    $expert_profile_row = getIdExpert($expert_id); //To get Expert Profile Details

    $expert_profile_category_id = $expert_enquiry_search_row['enquiry_category']; //Enquiry Category Id

    $expert_enquiry_date = $expert_enquiry_search_row['appointment_date']; //Enquiry Date

    $expert_enquiry_time = $expert_enquiry_search_row['appointment_time']; //Enquiry Time

    $expert_profile_user_id = $expert_profile_row['user_id'];

    $expert_profile_city_id = $expert_profile_row['city_id'];  //User City Id

    $expert_profile_category_row = getExpertCategory($expert_profile_category_id);

    $expert_category_name = $expert_profile_category_row['category_name']; // Enquired Category Name

    $expert_profile_city_row = getExpertCity($expert_profile_city_id);

    $expert_city_name = $expert_profile_city_row['country_name']; //User City Name

    $expert_user_details_row = getUser($expert_profile_user_id);

}

if ($expert_enquiry_search_row['enquiry_sender_id'] != $session_user_id) {

    header("Location: $redirect_url");  //Redirect When this service not belongs to logged in user
}

?>

<!-- START -->
<section>
    <div class="ser-confir">
        <div class="container">
            <div class="row">
                <div class="ser-confir-main">
                    <?php
                    if (isset($_GET['enquiry'])) {
                        ?>
                        <div class="full">
                            <div class="serv-confi-succ">
                                <div class="inn">
                                    <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                                        <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/>
                                        <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
                                    </svg>
                                    <h1><?php echo $BIZBOOK['SERVICE-EXPERT-THANK-YOU-LABEL']; ?></h1>
                                    <p><?php echo $BIZBOOK['SERVICE-EXPERT-THANK-YOU-P-1-LABEL']; ?> <?php echo $expert_profile_row['years_of_experience']; ?><?php echo $BIZBOOK['SERVICE-EXPERT-THANK-YOU-P-2-LABEL']; ?></p>
                                </div>
                            </div>
                        </div>
                        <?php
                    }
                    ?>
                    <div class="lhs">
                        <div class="exp-deta-1">
                            <img src="<?php echo $slash; ?>service-experts/images/services/<?php echo $expert_profile_row['profile_image']; ?>"
                                alt=""/>
                            <h2><?php echo $expert_profile_row['profile_name']; ?></h2>
                            <span class="loc"><?php echo $expert_city_name; ?></span>
                            <p><?php echo $expert_category_name; ?></p>
                        </div>
                        <div class="exp-deta-con-com exp-deta-2">
                            <h4><?php echo $BIZBOOK['SERVICE-EXPERT-APPROX-ARRIVE-TIME']; ?></h4>
                            <p><?php echo $expert_enquiry_search_row['appointment_time']; ?>
                                - <?php echo dateFormatconverter($expert_enquiry_search_row['appointment_date']); ?></p>
                        </div>
                        <div class="exp-deta-con-com exp-deta-3">
                            <h4><?php echo $BIZBOOK['SERVICE-EXPERT-SERVICE-STATUS']; ?></h4>
                            <p><?php
                                $enquiry_status = $expert_enquiry_search_row['enquiry_status'];
                                if ($enquiry_status == 100) {
                                    echo $BIZBOOK['SERVICE-EXPERT-CLOSED-LABEL'];
                                } elseif ($enquiry_status == 200) {
                                    echo $BIZBOOK['SERVICE-EXPERT-NEW-LABEL'];
                                } elseif ($enquiry_status == 300) {
                                    echo $BIZBOOK['SERVICE-EXPERT-ON-THE-WAY-LABEL'];
                                } elseif ($enquiry_status == 400) {
                                    echo $BIZBOOK['SERVICE-EXPERT-PENDING-LABEL'];
                                } elseif ($enquiry_status == 500) {
                                    echo $BIZBOOK['SERVICE-EXPERT-DONE-LABEL'];
                                }
                                ?></p>
                        </div>
                        <div class="exp-deta-con-com exp-deta-4">
                            <h4><?php echo $BIZBOOK['SERVICE-EXPERT-PAYMENT-ACCEPT-LABEL']; ?></h4>
                            <ul>
                                <?php
                                $payment_id = explode(',', $expert_profile_row['payment_id']);
                                foreach ($payment_id as $payment_id_id) {
                                    $payment_row = getExpertPayments($payment_id_id);
                                    ?>
                                    <li><?php echo $payment_row['payment_name']; ?></li>
                                    <?php
                                }
                                ?>
                            </ul>
                        </div>
                    </div>
                    <div class="rhs">
                        <h2><?php echo $BIZBOOK['SERVICE-EXPERT-BOOKING-REFRENCE'];?></h2>
                        <ul>
                            <li><?php echo $BIZBOOK['SERVICES']; ?>: <?php echo $expert_category_name; ?></li>
                            <li><?php echo $BIZBOOK['SERVICE-EXPERT-PREFERRED-DATE-TIME']; ?>: <?php echo $expert_enquiry_search_row['appointment_time']; ?>
                                - <?php echo dateFormatconverter($expert_enquiry_search_row['appointment_date']); ?></li>
                            <li><?php echo $BIZBOOK['MESSAGE']; ?>: <?php echo $expert_enquiry_search_row['enquiry_message']; ?></li>
                        </ul>
                        <?php
                        if($enquiry_status != 100 && $enquiry_status != 500) {
                            ?>
                            <a href="#" data-toggle="modal" data-target="#cancelreq"><?php echo $BIZBOOK['SERVICE-EXPERT-CANCEL-REQUEST']; ?></a>
                            <?php
                        }
                        ?>
                        <a href="#" class="cta-wri-rev" data-toggle="modal" data-target="#expwrirevi"><?php echo $BIZBOOK['LISTING_DETAILS_WRITE_REVIEW']; ?></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->


<?php
include "../footer.php";
?>

<!-- START -->
<section>
    <div class="pop-ups pop-quo">
        <!-- WRITE REVIEW -->
        <div class="modal fade" id="expwrirevi">

            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="exper-rev-box">
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <div class="tit">
                            <h4><?php echo $BIZBOOK['SERVICE-EXPERT-WRITE-A-REVIEW-LABEL']; ?></h4>
                        </div>
                        <div class="prof">
                            <img
                                src="<?php echo $slash; ?>service-experts/images/services/<?php echo $expert_profile_row['profile_image']; ?>"
                                alt="">
                            <h3><?php echo $expert_profile_row['profile_name']; ?></h3>
                            <p><?php echo $BIZBOOK['SERVICE-EXPERT-REVIEW-P-LABEL']; ?></p>
                        </div>
                        <?php if (empty($session_user_id) || $session_user_id == Null || ($expert_profile_user_id == $session_user_id) || ($enquiry_status != 100 && $enquiry_status != 500)) {
                            ?>
                            <?php if (empty($session_user_id) || $session_user_id == Null) {
                                ?>
                                <span style="text-align:center;display: block;color: red;"
                                      id=""><?php echo $BIZBOOK['LISTING_DETAILS_LOGIN_AND_WRITE_REVIEW']; ?></span>
                                <?php
                            }
                            if ($expert_profile_user_id == $session_user_id) { ?>
                                <span style="text-align:center;display: block;color: red;"
                                      id=""><?php echo $BIZBOOK['SERVICE-EXPERT-CANT-REVIEW-OWN-SERVICE']; ?></span>
                                <?php
                            } else {
                                if ($enquiry_status != 100 && $enquiry_status != 500) { ?>
                                    <span style="text-align:center;display: block;color: red;"
                                          id=""><?php echo $BIZBOOK['SERVICE-EXPERT-CANT-REVIEW-DONE-CANCEL']; ?></span>
                                    <?php
                                }
                            }
                        } else {
                            ?>
                            <form class="col" name="expert_review_form" id="expert_review_form" method="post">
                                <input type="hidden" class="form-control" name="expert_id"
                                       value="<?php echo $expert_profile_row['expert_id']; ?>">
                                <input type="hidden" class="form-control" name="expert_user_id"
                                       value="<?php echo $expert_profile_user_id; ?>">
                                <input type="hidden" class="form-control" name="enquiry_id"
                                       value="<?php echo $enquiry_id; ?>">
                                <input name="review_user_id" value="<?php echo $session_user_id; ?>"
                                       type="hidden">
                                <div id="expert_review_success"
                                     style="text-align:center;display: none;color: green;"><?php echo $BIZBOOK['LISTING_DETAILS_REVIEW_SUCCESS_MESSAGE']; ?>
                                </div>
                                <div id="expert_review_fail"
                                     style="text-align:center;display: none;color: red;"><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></div>
                                <div class="rating-new">
                                    <fieldset class="rating">
                                        <input type="radio" id="star5" name="expert_rating"
                                               class="expert_rating" value="5"/>
                                        <label class="full" for="star5" title="Awesome"></label>
                                        <input type="radio" id="star4" name="expert_rating"
                                               class="expert_rating" value="4"/>
                                        <label class="full" for="star4" title="Excellent"></label>
                                        <input type="radio" id="star3"
                                               class="expert_rating" name="expert_rating" value="3"/>
                                        <label class="full" for="star3" title="Good"></label>
                                        <input type="radio" id="star2" name="expert_rating"
                                               class="expert_rating" value="2"/>
                                        <label class="full" for="star2" title="Average"></label>
                                        <input type="radio" id="star1" name="expert_rating"
                                               class="expert_rating" value="1" checked="checked"/>
                                        <label class="full" for="star1" title="Poor"></label>
                                    </fieldset>
                                    <div id="star-value">3 Star</div>
                                </div>
                                <div class="rating-new-msg">
                                    <textarea name="expert_message"
                                              placeholder="<?php echo $BIZBOOK['SERVICE-EXPERT-REVIEW-WRITE-YOUR-COMMENTS-LABEL']; ?>"></textarea>
                                </div>
                                <div class="rating-new-cta">
                                    <span data-dismiss="modal">Not now</span>
                                    <button type="submit" name="expert_review_submit"
                                            id="expert_review_submit"><?php echo $BIZBOOK['SERVICE-EXPERT-REVIEW-SUBMIT-REVIEW']; ?></button>
                                </div>
                            </form>
                        <?php } ?>
                    </div>
                </div>
            </div>

        </div>
        <!-- END -->
        <!-- CANCEL REQUEST -->
        <div class="modal fade" id="cancelreq">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="exper-rev-box">
                        <button type="button" class="close" data-dismiss="modal">&times;</button>
                        <div class="tit">
                            <h4><?php echo $BIZBOOK['SERVICE-EXPERT-CANCEL-REQUEST']; ?></h4>
                        </div>
                        <?php if ((empty($session_user_id) || $session_user_id == Null) || ($expert_enquiry_search_row['enquiry_sender_id'] != $session_user_id)) {
                            ?>
                            <?php if (empty($session_user_id) || $session_user_id == Null) {
                                ?>
                                <span style="text-align:center;display: block;color: red;"
                                      id=""><?php echo $BIZBOOK['SERVICE-EXPERT-LOGIN-AND-CANCEL']; ?></span>
                            <?php }
                            if ($expert_enquiry_search_row['enquiry_sender_id'] != $session_user_id) {
                                ?>
                                <span style="text-align:center;display: block;color: red;"
                                      id=""><?php echo $BIZBOOK['SERVICE-EXPERT-CANT-CANCEL-OTHER-USER']; ?></span>
                                <?php
                            }
                        } else { ?>
                            <form class="col" name="expert_service_cancel_form" id="expert_service_cancel_form"
                                  method="post">
                                <input type="hidden" class="form-control" name="expert_id"
                                       value="<?php echo $expert_profile_row['expert_id']; ?>">
                                <input type="hidden" class="form-control" name="enquiry_id"
                                       value="<?php echo $enquiry_id; ?>">
                                <input name="expert_service_user_id" value="<?php echo $session_user_id; ?>"
                                       type="hidden">
                                <div id="expert_cancel_success"
                                     style="text-align:center;display: none;color: green;"><?php echo $BIZBOOK['SERVICE-EXPERT-CANCEL-SUCCESS-MESSAGE']; ?>
                                </div>
                                <div id="expert_cancel_fail"
                                     style="text-align:center;display: none;color: red;"><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></div>
                                <div class="rating-new-msg">
                                    <textarea name="cancel_message" id="cancel_message" class="cancel_message"
                                              placeholder="<?php echo $BIZBOOK['SERVICE-EXPERT-REVIEW-WRITE-YOUR-COMMENTS-LABEL']; ?>"></textarea>
                                </div>
                                <div class="rating-new-cta">
                                    <span data-dismiss="modal"><?php echo $BIZBOOK['SERVICE-EXPERT-NOT-NOW']; ?></span>
                                    <button type="submit" class="expert_service_cancel_submit"
                                            id="expert_service_cancel_submit" name="expert_service_cancel_submit"><?php echo $BIZBOOK['SERVICE-EXPERT-CONFIRM-CANCEL'];?></button>
                                </div>
                            </form>
                            <?php
                        }
                        ?>
                    </div>
                </div>
            </div>
        </div>
        <!-- END -->
    </div>
</section>
<!-- END -->

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script src="<?php echo $slash; ?>js/select-opt.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>
<script>
    $(document).ready(function () {
        $('input[name="expert_rating"]').change(function () {
            if ($('#star0').prop('checked')) {
                $("#star-value").html('0 Star');
            }
            else if ($('#star1').prop('checked')) {
                $("#star-value").html('1 Star');
            }
            else if ($('#star2').prop('checked')) {
                $("#star-value").html('2 Star');
            }
            else if ($('#star3').prop('checked')) {
                $("#star-value").html('3 Star');
            }
            else if ($('#star4').prop('checked')) {
                $("#star-value").html('4 Star');
            }
            else if ($('#star5').prop('checked')) {
                $("#star-value").html('5 Star');
            }
        });
    });
</script>
</body>

</html>