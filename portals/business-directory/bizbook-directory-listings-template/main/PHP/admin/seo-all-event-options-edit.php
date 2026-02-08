<?php
include "header.php";
?>

<?php if ($admin_row['admin_seo_setting_options'] != 1) {
    header("Location: profile.php");
}
?>

<!-- START -->
<section xmlns="http://www.w3.org/1999/html">
    <div class="ad-com pg-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <?php
                $event_id = $_GET['row'];
                $row = getEvent($event_id);
                ?>
                <form name="all_event_form" id="all_event_form" method="post" action="update_seo_event.php"
                      enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                    <input type="hidden" class="validate" id="event_id" name="event_id"
                           value="<?php echo $row['event_id']; ?>" required="required">
                    <div class="pg-cen">
                        <div class="s-com pg-tit">
                            <h1>Edit Event SEO options</h1>
                            <?php include "../page_level_message.php"; ?>
                            <div class="form-group">
                                <input type="text" required="required" class="form-control" value="<?php echo $row['event_name']; ?>"
                                       disabled>
                            </div>
                        </div>
                        <div class="s-com pg-cen-tab pg-seo">
                            <h4>SEO settings</h4>
                            <div class="inn">
                                <div class="form-group">
                                    <label>Page title</label>
                                    <input type="text" name="seo_title" value="<?php echo $row['seo_title']; ?>"  class="form-control">
                                </div>
                                <div class="form-group">
                                    <label>Page keywords</label>
                                    <input type="text" name="seo_keywords" value="<?php echo $row['seo_keywords']; ?>"  class="form-control">
                                </div>
                                <div class="form-group">
                                    <label>Page descriptions</label>
                                    <input type="text" name="seo_description" value="<?php echo $row['seo_description']; ?>"  class="form-control">
                                </div>
                            </div>
                        </div>

                    </div>
                    <div class="pg-rhs">
                        <div class="box pub">
                            <h3>Publish</h3>
                            <div class="inn">
                                <ul>
                                    <li>
                                        <button type="submit" name="event-seo-submit" class="btn-pub">Save changes</button>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </form>

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
<script src="../js/select-opt.js"></script>
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
</body>

</html>