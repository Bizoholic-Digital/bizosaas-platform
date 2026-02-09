<?php
include "header.php";
?>

<?php if ($admin_row['admin_home_options'] != 1) {
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Home Page Top Section </span>
                <div class="ud-cen-s2 hcat-cho">
                    <h2>Home Page Top Section - (For Home Page Variation - 1)</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Title</th>
                            <th>Image</th>
                            <th>Edit</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllHomePageTopSection() as $row) {
                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $row['top_section_title']; ?></td>
                                <td>
                                    <img src="../images/icon/<?php echo $row['top_section_image']; ?>" alt="">
                                </td>
                                <td><a href="admin-home-top-section-edit.php?row=<?php echo $row['top_section_id']; ?>"
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
<?php
if (isset($_GET['pord'])) {
    dbUpdateDrop($conn);
}
?>
</body>

</html>