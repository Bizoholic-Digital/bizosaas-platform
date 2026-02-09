<?php
include "header.php";
?>

<?php if ($admin_row['admin_import_options'] != 1) {
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
                        <div class="login-main add-list posr">
                            <div class="log-bor">&nbsp;</div>
                            <span class="udb-inst">Export</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Export Datas</h4>
                                    <form>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <a href="export_all_database.php"> <button type="button" class="btn btn-primary">Click here to export all
                                                    files
                                                </button></a>
                                            </div>
                                            <div class="col-md-12">
                                                <a href="profile.php" class="skip">Go to User Dashboard >></a>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                    </form>
                                    <div class="ud-notes">
                                        <p><b>Notes:</b> Hi, Here you can import your old database files with in a
                                            minutes. If yourare ready to import your files means please follow below
                                            instructions
                                        </p>
                                        <ul>
                                            <li>Please export your current files(for safety purposes)</li>
                                            <li>Make sure ready your import files like our database schema(database
                                                table structure)
                                            </li>
                                        </ul>
                                    </div>
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