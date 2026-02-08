<?php
include "header.php";
?>

<?php if ($footer_row['admin_news_show'] !=1 || $admin_row['admin_news_options'] != 1) {
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Social Media - News</span>
                <div class="ud-cen-s2 hcat-cho">
                    <h2>Social Media - News</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Name</th>
                            <th>Count</th>
                            <th>Status</th>
                            <th>Edit</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllNewsSocialMedia() as $row) {

                            $social_media_id = $row['social_media_id'];

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $row['social_media_name']; ?></td>
                                <td><?php echo $row['social_media_count']; ?></td>
                                <td><?php
                                        $social_media_status = $row['social_media_status'];
                                        if ($social_media_status == 1) {
                                            echo "Active";
                                        } else{
                                            echo "Inactive";
                                        } ?></td>
                                <td><a href="news-home-social-media-edit.php?row=<?php echo $social_media_id; ?>" class="db-list-edit">Edit</a></td>
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
<script src="js/admin-custom.js"></script> <script src="http://harvesthq.github.io/chosen/chosen.jquery.js"></script>

</body>

</html>