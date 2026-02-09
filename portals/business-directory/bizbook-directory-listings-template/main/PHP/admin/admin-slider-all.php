<?php
include "header.php";
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">All Slider</span>
                <div class="ud-cen-s2 ad-table-inn">
                    <h2>All Slider Photos</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Slider</th>
                            <th>Link</th>
                            <th>Edit</th>
                            <th>Delete</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si =1;
                        foreach (getAllSlider() as $row) {


                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td>
                                    <img src="../images/slider/<?php echo $row['slider_photo']; ?>" alt="">
                                </td>
                                <td><?php echo $row['slider_link']; ?></td>
                                <td><a href="admin-slider-edit.php?row=<?php echo $row['slider_id']; ?>" class="db-list-edit">Edit</a></td>
                                <td><a href="admin-slider-delete.php?row=<?php echo $row['slider_id']; ?>" class="db-list-edit">Delete</a></td>
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