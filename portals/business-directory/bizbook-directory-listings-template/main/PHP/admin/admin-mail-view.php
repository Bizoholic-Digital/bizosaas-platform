<?php
include "header.php";
?>

<?php if($admin_row['admin_mail_template_options'] != 1){
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">View Email Template</span>
                <div class="ud-cen-s2 add-list">

                    <div id="email_content" >
                        <?php
                        $mail_id = $_GET['row'];

                        $mail_row = getMailTemplate($mail_id);

                        $row_f = getAllFooter();

                        $mail_template = $mail_row['mail_template'];

                        $website_name = $row_f['website_address'];
                        $footer_copyright = $row_f['footer_copyright'];
                        $admin_primary_email = $row_f['admin_primary_email'];
                        $footer_address = $row_f['footer_address'];

                        echo stripslashes(str_replace(array('\'.$admin_site_name.\'', '\' . $first_name . \'', '\' . $email_id . \''
                        , '\' . $password . \'', '\'.$admin_footer_copyright.\'', '\'.$admin_address.\'', '\'.$webpage_full_link.\''
                        ,'\'.$rec_email_id.\'','\' . $listing_name . \'','\' . $listing_mobile . \'','\' . $listing_email . \''
                        ,'\' . $mobile_number . \'','\' . $event_name . \'','\' . $event_mobile . \'','\' . $event_email . \''
                        ,'\' . $blog_name . \'','\' . $blog_mobile . \'','\' . $blog_email . \''
                        ,'\' . $verify_code . \'','\' . $webpage_full_link_with_verification_link . \''
                        ,'\' . $product_name . \'','\' . $product_mobile . \'','\' . $product_email . \''),
                            array($website_name, 'Johxx', 'axx@gmxx.com', 'casxxz', $footer_copyright, $footer_address
                            , $webpage_full_link,'axx@gmxx.com', 'DirectoryZZ', '987654xxxx', 'axx@gmxx.com','987654xxxx'
                            ,'Eventzz', '987654xxxx', 'axx@gmxx.com', 'Blogzz', '987654xxxx', 'axx@gmxx.com', '12345', $webpage_full_link123, 'Productzz', '987654xxxx', 'axx@gmxx.com'), $mail_template));

                        ?>
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

