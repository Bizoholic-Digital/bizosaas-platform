<?php
include "header.php";
?>
<?php if($admin_row['admin_home_options'] != 1){
    header("Location: profile.php");
}
?>
    <!-- START -->
    <section>
        <div class="ad-com">
            <div class="ad-dash leftpadd">
                <div class="ud-cen">
				<div class="log-bor">&nbsp;</div>
				<span class="udb-inst">Home page video</span>
                <div class="ud-cen-s2">
                    <h2>Branding video</h2>
                    <?php include "../page_level_message.php"; ?>
                    
                    <?php $row = getAllFooter();  ?>
                    
                    <form name="home_youtube" id="home_youtube" action="update_home_youtube.php" method="post" enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                        <input type="hidden" autocomplete="off" name="footer_id"
                               value="<?php echo $row['footer_id']; ?>" id="footer_id" class="validate">
                    <div>
                        <!--FILED START-->
                        <div class="row">
                            <div class="col-md-12">
                                <div class="form-group">
                                    <textarea name="admin_home_youtube" class="form-control" placeholder="Youtube video iframe code"><?php echo $row['admin_home_youtube']; ?></textarea>
                                </div>
                            </div>
                        </div>
                        <!--FILED END-->
                        <button type="submit" name="home_youtube" class="db-pro-bot-btn">Save changes</button>
                    </div>
                    </form>
                    <div class="ud-notes">
                        <p><b>Notes:</b> Hi, here you can post your youtube videos from youtube. <br><b>Step 1:</b> Upload your videos to youtube<br><b>Step 2:</b> Publish your videos<br><b>Step 3:</b>Copy the iframe code from your video<br><b>Step 4:</b> Finally paste here.<br></p>
                    </div>
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
    <script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>