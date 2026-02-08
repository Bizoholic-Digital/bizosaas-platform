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

//To check the listings count with current plan starts

$plan_type_listing_count = $user_plan_type['plan_type_listing_count'];
$listing_count_user = getCountUserListing($_SESSION['user_id']);

if ($listing_count_user >= $plan_type_listing_count) {

    $_SESSION['status_msg'] = $BIZBOOK['LISTINGS_LIMIT_EXCEED_MESSAGE'];

    header('Location: db-all-listing');
}
//To check the listings count with current plan ends
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
                <span class="steps"><?php echo $BIZBOOK['CREATE_NEW']; ?></span>
                <div class="log">
                    <div class="login">

                        <h4><?php echo $BIZBOOK['ADD_NEW_LISTING']; ?></h4>
                        <div class="row cre-dup">
                            <div class="col-md-6">
                                <a href="add-listing-step-1"><?php echo $BIZBOOK['CREATE_SCRATCH_LISTING_LABEL']; ?></a>
                            </div>
                            <div class="col-md-6">
                                <span
                                    class="cre-dup-btn"><?php echo $BIZBOOK['CREATE_DUPLICATE_LISTING_LABEL']; ?></span>
                            </div>
                        </div>
                        <form name="duplicate_listing_form" action="duplicate_listing_insert.php"
                              id="duplicate_listing_form" method="post" class="cre-dup-form cre-dup-form-show">
                            <!--FILED START-->
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group">
                                        <select name="listing_id" id="listing_id" class="chosen-select form-control"
                                                required="required">
                                            <option value="" disabled
                                                    selected><?php echo $BIZBOOK['LISTING_NAME']; ?></option>
                                            <?php
                                            $user_id = $_SESSION['user_id'];
                                            $listsql = "SELECT * FROM " . TBL . "listings  WHERE  listing_is_delete != '2' AND user_id = $user_id  ORDER BY listing_id DESC";

                                            $listrs = mysqli_query($conn, $listsql);

                                            $list_count = mysqli_num_rows($listrs);

                                            while ($listrow = mysqli_fetch_array($listrs)) {
                                                ?>
                                                <option
                                                    value="<?php echo $listrow['listing_code']; ?>"><?php echo $listrow['listing_name']; ?></option>
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
                                        <input type="text" name="listing_name" required="required" class="form-control"
                                               placeholder="<?php echo $BIZBOOK['NEW_LISTING_NAME_STAR']; ?>">
                                    </div>
                                </div>
                            </div>
                            <!--FILED END-->
                            <button type="submit" name="listing_submit"
                                    class="btn btn-primary"><?php echo $BIZBOOK['CREATE_NOW']; ?></button>
                        </form>
                        <div class="col-md-12">
                            <a href="dashboard" class="skip"><?php echo $BIZBOOK['GO_TO_USER_DASHBOARD']; ?> >></a>
                        </div>
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