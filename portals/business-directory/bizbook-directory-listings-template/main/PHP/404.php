<?php
include "header.php";
?>
    <!-- START -->
	<section class="<?php if($footer_row['admin_language']== 2){ echo "lg-arb";}?> pg-404">
        <div class="container">
            <div class="row">
                <div class="inn1">
                    <b><?php echo $BIZBOOK['404_TEXT']; ?></b>
                    <h1><?php echo $BIZBOOK['404_PAGE_NOT_FOUND']; ?></h1>
                    <p><?php echo $BIZBOOK['404_PAGE_NOT_FOUND_MESSAGE']; ?></p>
                    <a href="<?php echo $webpage_full_link?>" class="btn1"><?php echo $BIZBOOK['404_GO_HOME']; ?></a>
                    <a href="<?php echo $webpage_full_link?>contact-us" class="btn2"><?php echo $BIZBOOK['404_CONTACT_US']; ?></a>
                </div>
                <div class="inn2">
                    
                </div>
            </div>
        </div>
	</section>
	<!--END-->

   
<?php
include "footer.php";
?>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link ='<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url ='<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>
</body>

</html>

