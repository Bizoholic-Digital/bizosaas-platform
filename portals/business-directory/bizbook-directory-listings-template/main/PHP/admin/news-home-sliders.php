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
                <span class="udb-inst">Home page Slider News</span>
                <div class="ud-cen-s2 hcat-cho">
                    <h2>Slider News</h2>
                    <?php include "../page_level_message.php"; ?>
                    <a href="news-home-sliders-add.php" class="db-tit-btn">Add new slider news</a>
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>News posts</th>
                            <th>Edit</th>
                            <th>Delete</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllNewsSlider() as $row) {

                        $news_id = $row['news_id'];

                        $news_slider_id = $row['news_slider_id'];

                        $news_sql_row = getIdNews($news_id);

                        ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo stripslashes($news_sql_row['news_title']); ?></td>
                                <td><a href="news-home-sliders-edit.php?row=<?php echo $news_slider_id; ?>" class="db-list-edit">Edit</a></td>
                                <td><a href="news-home-sliders-delete.php?row=<?php echo $news_slider_id; ?>" class="db-list-edit">Delete</a></td>
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