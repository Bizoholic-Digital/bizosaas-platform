<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

if (file_exists('config/general_user_authentication.php')) {
    include('config/general_user_authentication.php');
}

if (file_exists('config/listing_page_authentication.php')) {
    include('config/listing_page_authentication.php');
}

if ($_GET['row'] == NULL && empty($_GET['row'])) {

    header("Location: db-all-listing");
}

if (!isset($_SESSION['listing_codea']) || empty($_SESSION['listing_codea'])) {
    $listing_codea = $_GET['row'];
} else {
    $listing_codea = $_SESSION['listing_codea'];
}

?>
<!-- START -->
<!--PRICING DETAILS-->
<section class="<?php if ($footer_row['admin_language'] == 2) {
    echo "lg-arb";
} ?> login-reg">
    <div class="container">
        <div class="row">
            <div class="add-list-ste">
                <div class="add-list-ste-inn">
                    <ul>
                        <li>
                            <a href="edit-listing-step-1?row=<?php echo $listing_codea; ?>">
                                <span><?php echo $BIZBOOK['STEP1']; ?></span>
                                <b><?php echo $BIZBOOK['BASIC_INFO']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="edit-listing-step-2?row=<?php echo $listing_codea; ?>">
                                <span><?php echo $BIZBOOK['STEP2']; ?></span>
                                <b><?php echo $BIZBOOK['SERVICES']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="edit-listing-step-3?row=<?php echo $listing_codea; ?>">
                                <span><?php echo $BIZBOOK['STEP3']; ?></span>
                                <b><?php echo $BIZBOOK['OFFERS']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="edit-listing-step-4?row=<?php echo $listing_codea; ?>">
                                <span><?php echo $BIZBOOK['STEP4']; ?></span>
                                <b><?php echo $BIZBOOK['MAP']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="edit-listing-step-5?row=<?php echo $listing_codea; ?>" class="act">
                                <span><?php echo $BIZBOOK['STEP5']; ?></span>
                                <b><?php echo $BIZBOOK['OTHER']; ?></b>
                            </a>
                        </li>
                        <li>
                            <a href="edit-listing-step-6?row=<?php echo $listing_codea; ?>">
                                <span><?php echo $BIZBOOK['STEP6']; ?></span>
                                <b><?php echo $BIZBOOK['DONE']; ?></b>
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="login-main add-list">
                <div class="log-bor">&nbsp;</div>
                <span class="steps"><?php echo $BIZBOOK['STEP5']; ?></span>
                <div class="log">
                    <div class="login add-lis-oth">

                        <h4><?php echo $BIZBOOK['OTHER_INFORMATIONS']; ?></h4>
                        <span class="add-list-add-btn lis-add-oad" title="add new offer">+</span>
                        <span class="add-list-rem-btn lis-add-ore" title="remove offer">-</span>
                        <?php
                        $listings_a_row = getListing($listing_codea);
                        ?>
                        <form action="listing_update.php" class="listing_form_5" id="listing_form_5"
                              name="listing_form_5" method="post" enctype="multipart/form-data">
                            <input type="hidden" id="src_path" value="edit-5"
                                   name="src_path" class="validate">
                            <input type="hidden" id="listing_codea" value="<?php echo $listing_codea; ?>"
                                   name="listing_codea" class="validate">
                            <input type="hidden" id="listing_code"
                                   value="<?php echo $listings_a_row['listing_code']; ?>"
                                   name="listing_code" class="validate">
                            <input type="hidden" id="listing_id" value="<?php echo $listings_a_row['listing_id']; ?>"
                                   name="listing_id" class="validate">
                            <ul>
                                <?php
                                $listings_a_row_listing_info_question = $listings_a_row['listing_info_question'];
                                $listings_a_row_listing_info_answer = $listings_a_row['listing_info_answer'];

                                $listings_a_row_listing_info_question_Array = explode(',', $listings_a_row_listing_info_question);
                                $listings_a_row_listing_info_answer_Array = explode(',', $listings_a_row_listing_info_answer);

                                $zipped = array_map(null, $listings_a_row_listing_info_question_Array, $listings_a_row_listing_info_answer_Array);

                                foreach ($zipped as $tuple) {
                                    $tuple[0]; // Info question
                                    $tuple[1]; // Info Answer

                                    ?>
                                    <li>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-5">
                                                <div class="form-group">
                                                    <input type="text" class="form-control"
                                                           name="listing_info_question[]"
                                                           value="<?php echo $tuple[0]; ?>"
                                                           placeholder="<?php echo $BIZBOOK['OTHER_INFORMATIONS_PLACEHOLDER_LEFT']; ?>">
                                                </div>
                                            </div>
                                            <div class="col-md-2">
                                                <div class="form-group">
                                                    <i class="material-icons">arrow_forward</i>
                                                </div>
                                            </div>
                                            <div class="col-md-5">
                                                <div class="form-group">
                                                    <input type="text" class="form-control"
                                                           name="listing_info_answer[]" value="<?php echo $tuple[1]; ?>"
                                                           placeholder="<?php echo $BIZBOOK['OTHER_INFORMATIONS_PLACEHOLDER_RIGHT']; ?>">
                                                </div>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                    </li>
                                    <?php
                                }
                                ?>


                            </ul>
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-6">
                                    <a href="edit-listing-step-4?row=<?php echo $_SESSION['listing_codea']; ?>">
                                        <button type="button"
                                                class="btn btn-primary"><?php echo $BIZBOOK['PREVIOUS']; ?></button>
                                    </a>
                                </div>
                                <div class="col-md-6">
                                    <button type="submit" name="listing_submit"
                                            class="btn btn-primary"><?php echo $BIZBOOK['SAVE_AND_EXIT']; ?></button>
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
<?php
include "footer.php";
?>


<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
</body>

</html>