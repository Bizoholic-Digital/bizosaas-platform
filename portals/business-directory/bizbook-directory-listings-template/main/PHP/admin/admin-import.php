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
                            <span class="udb-inst">Import</span>
                            <div class="log log-1">
                                <div class="login">
                                    <h4>Import Datas</h4>
                                    <?php include "../page_level_message.php"; ?>
                                    <form name="upload_bulk_form" id="upload_bulk_form" method="post"
                                          action="update_upload_bulk_listings.php" enctype="multipart/form-data">
                                        <ul>
                                            <li>

                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label>Choose import file</label>
                                                            <input type="file" name="file" id="file" class="form-control" required>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                            </li>
                                        </ul>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <button type="submit" name="upload_bulk_submit" class="btn btn-primary">Import Now</button>
                                            </div>
                                            <div class="col-md-12">
                                                <a href="profile.php" class="skip">Go to User Dashboard >></a>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                    </form>
                                    <div class="ud-notes">
                                        <p><b>Notes:</b> Hi, Here you can import your old database files with in a
                                            minutes. If you are ready to import your files means please follow below
                                            instructions
                                        </p>
                                        <ul>
                                            <li>Please export your current files(for safety purposes)</li>
                                            <li>Make sure ready your import files like our database schema(database
                                                table structure)
                                            </li>
                                            <li>Please Convert Excel File To .CSV Format Then Upload</li>
                                            <li>The Uploading CSV File Should Be in This Below Order Only</li>
                                       <li>
                                           <table>
                                               <thead>
                                               <th>Business Type</th>
                                               <th>Phone</th>
                                               <th>Company</th>
                                               <th>Address</th>
                                               <th>City</th>
                                               <th>State</th>
                                               <th>Post_Code</th>
                                               <th>Country</th>
                                               </thead>
                                               <tbody>
                                               <tr>
                                                   <td>Salon</td>
                                                   <td>[1] 416 966 6703</td>
                                                   <td>D HAIR & SKIN CARE SALON</td>
                                                   <td>26 Cumberland St</td>
                                                   <td>TORONTO</td>
                                                   <td>ON</td>
                                                   <td>M6A 2X1</td>
                                                   <td>CANADA</td>
                                               </tr>
                                               <tr>

                                                   <td>Salon</td>
                                                   <td>[1] 416 966 6703</td>
                                                   <td>DEBBIE'S STYLE N PLACE</td>
                                                   <td>26 Cumberland St</td>
                                                   <td>HANOVER</td>
                                                   <td>ON</td>
                                                   <td>N4N 3T8</td>
                                                   <td>CANADA</td>
                                               </tr>
                                               <tr>

                                                   <td>Salon</td>
                                                   <td>[1] 519 364 4382</td>
                                                   <td>THE HAIR HOUSE UNISEX</td>
                                                   <td>2175 Victoria Park Ave</td>
                                                   <td>SCARBOROUGH</td>
                                                   <td>ON</td>
                                                   <td>M1R 1V6</td>
                                                   <td>CANADA</td>
                                               </tr>
                                               </tbody>
                                           </table>
                                        </li>
                                            <li>Cross Check The Uploading .CSV File Muliple Times Before Uploading</li>
                                            <li>The Uploading Time Depends On the Number Of Records You are Uploading Please Wait For Whole Uploade To be Complete!!!</li>


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