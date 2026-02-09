<?php
include "header.php";
?>
<?php if($admin_row['admin_invoice_options'] != 1){
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Create Invoices</span>
                <div class="ud-cen-s2 add-list">
                    <div id="content2" contenteditable="true">
                        <div class="pdf-main">
                            <div class="inn">
                                <div class="head">
                                    <h2>Premium Plus - Invoice</h2>
                                </div>
                                <div class="con">
                                    <p>Your are the golden member of the worlds No:1 business directory portal
                                        website.</p>
                                    <table class="table table-hover">
                                        <tbody>
                                        <tr>
                                            <td>User</td>
                                            <td>:</td>
                                            <td>Andriya jue</td>
                                        </tr>
                                        <tr>
                                            <td>Plan type</td>
                                            <td>:</td>
                                            <td>Premium Plus</td>
                                        </tr>
                                        <tr>
                                            <td>Amount paid</td>
                                            <td>:</td>
                                            <td><?php echo $footer_row['currency_symbol'];?>250</td>
                                        </tr>
                                        <tr>
                                            <td>Email id</td>
                                            <td>:</td>
                                            <td>andriya@business.com</td>
                                        </tr>
                                        <tr>
                                            <td>Payment type</td>
                                            <td>:</td>
                                            <td>Cash on delivery</td>
                                        </tr>
                                        <tr>
                                            <td>Profile</td>
                                            <td>:</td>
                                            <td>www.businessdire.com/profile/andriya</td>
                                        </tr>
                                        <tr>
                                            <td>Address</td>
                                            <td>:</td>
                                            <td>28800 Orchard Lake Road, Suite 180 Farmington Hills, U.S.A.</td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                                <div class="but">
                                    <p>Your are the golden member of worlds No:1 business directory portal website.</p>
                                </div>
                                <div class="foot">
                                    <p>Thank you for a member of <?php echo $footer_row['website_address']; ?></p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button class="btn-mpdf" id="downloadPDF">Click to Download PDF</button>
                    <div class="ud-notes">
                        <p><b>Notes:</b> Hi, here you can able to edit all text and title also. You just click the text
                            and change it and click "Click to download pdf" button to generate your invoice.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="../js/jquery.min.js"></script>
<script src="js/dom-to-image.min.js"></script>
<script src="js/jspdf.min.js"></script>
<script src="../js/popper.min.js"></script>
<script src="../js/bootstrap.min.js"></script>
<script src="../js/jquery-ui.js"></script>
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>