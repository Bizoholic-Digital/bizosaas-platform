<?php
include "header.php";
?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <section class="login-reg">
                <div class="container">
                    <div class="row">
                        <div class="login-main add-list posr">
                            <div class="log-bor">&nbsp;</div>
                            <span class="udb-inst">Delete Slider</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Delete this slider photo</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <?php
                                    $slider_id = $_GET['row'];
                                    $row = getSlider($slider_id);
                                    ?>
                                    <form name="delete_ads_form" id="delete_ads_form" method="post" action="trash_slider.php" enctype="multipart/form-data">
                                        <input type="hidden" class="validate" id="slider_id" name="slider_id" value="<?php echo $row['slider_id']; ?>" required="required">
                                        <input type="hidden" class="validate" id="slider_photo_old" name="slider_photo_old" value="<?php echo $row['slider_photo']; ?>" required="required">

                                        <ul>
                                            <li>

                                                <!--FILED START-->
                                                <div class="row">

                                                        <div class="form-group">
                                                            <img style="width: 200px;height: 100px" src="../images/slider/<?php echo $row['slider_photo']; ?>" readonly="readonly" class="form-control"/>
                                                        </div>

                                                </div>
                                                <!--FILED END-->

                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <textarea readonly="readonly"  id="slider_link"  name="slider_link" class="form-control" placeholder="Advertisement External link" required><?php echo $row['slider_link']; ?></textarea>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                
                                            </li>
                                        </ul>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <button type="submit" name="delete_slider_submit" class="btn btn-primary">Delete this Slider</button>
                                            </div>
                                            <div class="col-md-12">
                                                <a href="profile.php" class="skip">Go to User Dashboard >></a>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                    </form>
                                    <div class="ud-notes">
                                        <p><b>Notes:</b> Hi, Before submit your <b>Ads</b> please check the <b>available date</b> because previous Ads running in same date. Kindly check this manually</p>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </section>

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