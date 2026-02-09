<?php
include "header.php";
?>

<?php if($admin_row['admin_sub_admin_options'] != 1){
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Sub admins</span>
                <div class="ud-cen-s2">
                    <h2>All Sub Admins</h2>
                    <?php include "../page_level_message.php"; ?>
                    <a href="admin-sub-admin-create.php" class="db-tit-btn">Add new Sub Admin</a>
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>User</th>
                            <th>User Name</th>
                            <th>Password</th>
                            <th>Edit</th>
                            <th>Delete</th>
<!--                            <th>View log</th>-->
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllSubAdmin() as $admin_sql_row) {
                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><img src="../images/user/<?php if(($admin_sql_row['admin_photo'] == NULL) || empty($admin_sql_row['admin_photo'])){  echo $footer_row['user_default_image'];}else{ echo $admin_sql_row['admin_photo']; } ?>" alt=""><?php echo $admin_sql_row['admin_name']; ?>
                                    <span><?php echo dateFormatconverter($admin_sql_row['admin_cdt']); ?></span></td>
                                <td><?php echo $admin_sql_row['admin_email']; ?></td>
                                <td><?php echo "**********"; ?></td>
                                <td><a href="admin-sub-admin-edit.php?row=<?php echo $admin_sql_row['admin_id']; ?>" class="db-list-edit">Edit</a></td>
                                <td><a href="admin-sub-admin-delete.php?row=<?php echo $admin_sql_row['admin_id']; ?>" class="db-list-edit">Delete</a></td>
<!--                                <td><a href="admin-sub-admin-log.html?row=--><?php //echo $admin_sql_row['admin_id']; ?><!--" class="db-list-edit">View log</a></td>-->
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