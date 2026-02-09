<?php
include "header.php";
?>

<?php if($admin_row['admin_mail_template_options'] != 1){
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Mail Templates</span>
                <div class="ud-cen-s2">
                    <h2>All Mail Templates</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Topic</th>
                            <th>View</th>
                            <th>Edit</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllMailTemplates() as $row_f) {

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $row_f['mail_template_name']; ?></td>
                                <td><a href="admin-mail-view.php?row=<?php echo $row_f['mail_id']; ?>"
                                       class="db-list-ststus">View</a></td>
                                <td><a href="admin-mail-edit.php?row=<?php echo $row_f['mail_id']; ?>"
                                       class="db-list-edit">Edit</a></td>
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
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>