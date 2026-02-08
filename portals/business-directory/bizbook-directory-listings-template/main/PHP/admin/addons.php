<?php
include "header.php";
?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash adda-oly leftpadd">

<!--            User Welcome Div starts -->

            <div class="ad-dash-s1">
                <div class="cd-cen-intr-inn cd-cen-intr-inn2">
                <h2>Welcome to <b>Bizbook Add-Ons</b></h2>
                <p>It's more simplify your work with additional awesome features.</p>
                </div>
            </div>

<!--User Welcome Div ends -->

            <div class="biz-updates">
                <div class="inn">
                <table class="responsive-table bordered">
                        <thead>
                        <tr>
                            <th>#</th>
                            <th>Addon</th>
                            <th>Access</th>
                            <th>Activate date</th>
                            <th>Expairy date</th>
                            <th>Status</th>
                            <th>Plan</th>
                            <th>Demo</th>
                            <th>Buy Addons</th>
                        </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>1</td>
                                <td>Bizbook Lead Manager</td>
                                <td><a href="../admin/lead-manager/" class="btn-sml btn-c-blu" target="_blank">Go to my addon</a></td>
                                <td>02 Jan 2021</td>
                                <td>24 Feb 2021</td>
                                <td><span class="txt-clr-gre">Active</span></td>
                                <td>Monthly</td>
                                <td><a href="" class="btn-sml btn-c-gre" target="_blank">Demo</a></td>
                                <td><a href="" class="btn-sml btn-c-red" target="_blank">Buy now</a></td>
                            </tr>
                            <tr>
                                <td>2</td>
                                <td>Bizbook Visitors Manager</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td><a href="" class="btn-sml btn-c-gre" target="_blank">Demo</a></td>
                                <td><a href="" class="btn-sml btn-c-red" target="_blank">Buy now</a></td>
                            </tr>
                            <tr>
                                <td>3</td>
                                <td>Bizbook Support Manager</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td><a href="" class="btn-sml btn-c-gre" target="_blank">Demo</a></td>
                                <td><a href="" class="btn-sml btn-c-red" target="_blank">Buy now</a></td>
                            </tr>
                            <tr>
                                <td>4</td>
                                <td>Bizbook Mobile App</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td><a href="" class="btn-sml btn-c-gre" target="_blank">Demo</a></td>
                                <td><a href="" class="btn-sml btn-c-red" target="_blank">Buy now</a></td>
                            </tr>
                        </tbody>
                    </table>
            </div>
                <div class="ud-notes">
                    <p><b>Notes:</b> Enter your purchase code to the below box and activate your Bizbook Directory template. Once you use your purchase code for your domain means you can't use  the same purchase code to anothor domain. Your purchase code only for one domain not for multi-domain use.</p>
                </div>
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