<?php
include "header.php";
?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash adda-oly leftpadd">

<!--            User Welcome Div starts -->

            <div class="ad-dash-s1">
                <div class="cd-cen-intr-inn cd-cen-intr-inn1">
                <h2>Welcome to <b>Bizbook updates</b></h2>
                <p>You can you can easy to update your template with our update wizard.</p>
                </div>
            </div>

<!--User Welcome Div ends -->
            <div class="update-panel">
                <iframe src="https://directoryfinder.net/bizbook-updates/bizbook-update.html" title="Iframe Example"></iframe>
            </div>
            
            
        </div>
    </div>
</section>

<!-- END -->

<!-- END -->

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="../js/jquery.min.js"></script>
<script src="../js/popper.min.js"></script>
<script src="../js/bootstrap.min.js"></script>
<script src="../js/jquery-ui.js"></script>
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
<?php httpPost("http://directoryfinder.net/updation/updation_wizard.php",$data_array); ?>
</body>

</html>