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
                <span class="udb-inst">Home page category</span>
                <div class="ud-cen-s2 hcat-cho">
                    <h2>Home page category</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Category Name</th>
                            <th>Image</th>
                            <th>Edit</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;

                        foreach (getAllTopCategories() as $row) {

                            $category_name = $row['category_name'];

                            $category_sql_row = getCategory($category_name);

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $category_sql_row['category_name']; ?></td>
                                <td>
                                    <img src="../images/services/<?php echo $row['category_image']; ?>" alt="">
                                </td>
                                <td><a href="admin-home-category-edit.php?row=<?php echo $row['category_id']; ?>"
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