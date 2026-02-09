<?php
include "header.php";

if ($_GET['code'] == NULL && empty($_GET['code'])) {

    header("Location: $redirect_url");  //Redirect When code parameter is empty
}

//$page_codea = $_GET['code'];
$page_codea1 = str_replace('-', ' ', $_GET['code']);
$page_codea = str_replace('.php', '', $page_codea1);

$page_row = getActivePageSlug(3,$page_codea); // To Fetch particular Ebook Data

if ($page_row['page_id'] == NULL && empty($page_row['page_id'])) {


    header("Location: $redirect_url");  //Redirect When No User Found in Table
}

$page_id = $page_row['page_id'];
seopageview($page_id); //Function To Find Page View

if ($page_row['page_css'] != NULL) {
?>
    
    <style>
        <?php echo stripslashes($page_row['page_css']); ?>
    </style>
<?php
}if ($page_row['page_js'] != NULL) {
    ?>
    <script>
        <?php echo stripslashes($page_row['page_js']); ?>
    </script>
    <?php
}
?>
<!-- START -->
<section>
    <!-- START -->
    <div class="ebk-ban">
        <div class="container">
            <div class="row">
                <div class="lhs">
                    <h1><?php echo $page_row['page_name']; ?></h1>
                    <p><?php echo $page_row['page_name_2']; ?></p>
                    <a href="<?php echo $page_row['page_download_link']; ?>" class="btn"><?php echo $BIZBOOK['E-BOOK-DOWNLOAD-NOW']; ?></a>
                </div>
                <div class="rhs">
                    <img src="<?php echo $slash; ?>images/services/<?php echo $page_row['page_image']; ?>">
                </div>
            </div>
        </div>
    </div>
    <!-- END -->
    <!-- START -->
    <div class="ebk-con">
        <div class="container">
            <div class="row">
                <div class="lhs">
                    <?php include "page_level_message.php"; ?>
                <form name="feedback_form" id="feedback_form" method="post" action="feedback_submit.php" enctype="multipart/form-data">
                    <h4><?php echo $BIZBOOK['E-BOOK-DOWNLOAD-REQUEST']; ?></h4>
                    <div class="form-group">
                        <input type="text" placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>" name="feedback_name" id="feedback_name" class="form-control" required="required">
                    </div>
                    <div class="form-group">
                        <input type="email" class="form-control" placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>" required="required"
                               name="feedback_email"
                               pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$"
                               title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>">
                    </div>
                    <div class="form-group">
                        <input type="text" onkeypress="return isNumber(event)" class="form-control" id="feedback_mobile" name="feedback_mobile"
                               placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>" pattern="[7-9]{1}[0-9]{9}"
                               title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>" required="">
                    </div>
                    <div class="form-group">
                        <textarea name="feedback_message" id="feedback_message" required="required" placeholder="<?php echo $BIZBOOK['LEAD-WRITE-YOUR-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                    </div>
                    <button type="submit" id="feedback_submit" name="feedback_submit"
                            class="btn btn-primary">
                        <?php echo $BIZBOOK['LEAD-SUBMIT-FEEDBACK']; ?>
                    </button>
                </form>
                </div>
                <div class="rhs">
                    <h4><?php echo $BIZBOOK['ABOUT']; ?> <?php echo $page_row['page_name']; ?></h4>
                    <p><?php echo stripslashes($page_row['page_description']); ?></p>
                </div>
            </div>
        </div>
    </div>
    <!-- END -->
</section>
<!-- END -->


<?php
if($page_row['page_seo_schema'] != NULL) {
    ?>
    <!-- WEBSITE SCHEMA STARTS -->
    <h2 style="display: none"><?php echo $page_row['page_seo_schema']; ?></h2>
    <!-- WEBSITE SCHEMA ENDS -->
    <?php
}
?>

<?php
include "footer.php";
?>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>
</body>

</html>