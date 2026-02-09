<?php
include "header.php";
?>
<?php if($admin_row['admin_country_options'] != 1){
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <section class="login-reg">
                <div class="container">
                    <div class="row">
                        <div class="login-main add-list add-ncate">
                            <div class="log-bor">&nbsp;</div>
                            <span class="udb-inst">Delete search query</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Search query</h4>
                                    <?php
                                    $search_list_id = $_GET['row'];
                                    $details_row = getSearch($search_list_id);
                                    ?>
                                    <?php include "../page_level_message.php"; ?>
                                    <form name="search_list_form" action="trash_search_list.php" id="search_list_form" method="post" enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                                        <input type="hidden" id="search_list_id" value="<?php echo $details_row['search_list_id']; ?>"
                                               name="search_list_id" class="validate">
                                        <ul>
                                            <li>
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <input type="text" readonly="readonly" value="<?php echo $details_row['search_title']; ?>" name="search_title" class="form-control" placeholder="Search text *" required>
                                                        </div><hr>
                                                        <div class="form-group">
                                                            <input type="text" readonly="readonly" value="<?php echo $details_row['search_tag_line']; ?>" name="search_tag_line" class="form-control" placeholder="Tag line for search *" required>
                                                        </div><hr>
                                                        <div class="form-group">
                                                            <input type="text" readonly="readonly" value="<?php echo $details_row['search_list_link']; ?>" name="search_list_link" class="form-control" placeholder="Search link *" required>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        </ul>
                                        <button type="submit" name="search_list_submit" class="btn btn-primary">Delete</button>
                                    </form>

                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

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