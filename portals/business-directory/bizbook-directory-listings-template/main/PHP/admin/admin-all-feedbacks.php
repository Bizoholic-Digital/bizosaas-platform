<?php
include "header.php";
?>

<?php if($admin_row['admin_listing_options'] != 1){
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">All Feedback</span>
                <div class="ud-cen-s2">
                    <h2>All Feedback details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Name</th>
                            <th>Mobile</th>
                            <th>Email Id</th>
                            <th>Message</th>
                            <th>Date</th>
                            <th>Delete</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php

                        $si = 1;
                        foreach (getAllMessages() as $claimrow) {

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $claimrow['sender_name']; ?></td>
                                <td><?php echo $claimrow['sender_mobile']; ?></td>
                                <td><?php echo $claimrow['sender_email']; ?></td>
                                <td><?php echo $claimrow['message']; ?></td>
                                <td><span class="db-list-rat"><?php  echo dateFormatconverter($claimrow['message_cdt']); ?></span></td>
                                <td><a href="trash-feedback.php?trashfeedbacktrashfeedbacktrashfeedbacktrashfeedbacktrashfeedback=<?php echo $claimrow['message_id']; ?>" class="db-list-edit">Delete</a></td>
                            </tr>
                            <?php
                            $si++;
                        }
                        ?>
                        </tbody>
                    </table>
                </div>

            </div>
            <div class="ad-pgnat">
                <ul class="pagination">
                    <li class="page-item"><a class="page-link" href="#">Previous</a></li>
                    <li class="page-item active"><a class="page-link" href="#">1</a></li>
                    <li class="page-item"><a class="page-link" href="#">2</a></li>
                    <li class="page-item"><a class="page-link" href="#">3</a></li>
                    <li class="page-item"><a class="page-link" href="#">Next</a></li>
                </ul>
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