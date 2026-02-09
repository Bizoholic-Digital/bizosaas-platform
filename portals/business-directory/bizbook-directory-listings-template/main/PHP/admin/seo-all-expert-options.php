<?php
include "header.php";
?>

<?php if ($admin_row['admin_seo_setting_options'] != 1) {
    header("Location: profile.php");
}
?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">All Service Experts SEO</span>
                <div class="ud-cen-s2">
                    <h2>All Service Experts SEO details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Expert Name</th>
                            <th>SEO score</th>
                            <th>Edit</th>
                            <th>Preview</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllExperts() as $row) {

                            $expert_id = $row['expert_id'];

                            $percentage = round(getExpertsSeoScore($expert_id));

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $row['profile_name']; ?></td>
                                <td>
                                    <div class="progress">
                                        <div class="progress-bar bg-success progress-bar-striped"
                                             style="width:<?php echo $percentage; ?>%">
                                            <?php echo $percentage; ?>%
                                        </div>
                                    </div>
                                </td>
                                <td><a href="seo-all-expert-options-edit.php?row=<?php echo $row['expert_id']; ?>"
                                       class="db-list-edit">Edit</a></td>
                                <td>
                                    <a href="<?php echo $SERVICE_EXPERT_URL . urlModifier($row['expert_slug']); ?>"
                                       class="db-list-edit"
                                       target="_blank">Preview</a>
                                </td>
                            </tr>
                            <?php
                            $si++;
                        }
                        ?>
                        </tbody>
                    </table>
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
</body>

</html>