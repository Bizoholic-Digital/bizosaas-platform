<?php
/**
 * Created by Vignesh.
 * User: Vignesh
 */

if (file_exists('config/info.php')) {
    include('config/info.php');
}

if(isset($_GET['approveclaimrequestapproveclaimrequestapproveclaimrequestapproveclaimrequestapproveclaimrequest'])){

    $sender_id = $_GET['approveclaimrequestapproveclaimrequestapproveclaimrequestapproveclaimrequestapproveclaimrequest'];
    $listing_id = $_GET['listing_id'];
    $claim_id = $_GET['claim_id'];


    $listing_qry =
        "UPDATE  " . TBL . "listings  SET user_id='" . $sender_id . "' where listing_id='" . $listing_id . "'";

    $listing_res = mysqli_query($conn,$listing_qry);

    $listing_qry1 =
        "UPDATE  " . TBL . "claim_listings  SET claim_status= 1 where claim_listing_id='" . $claim_id . "'";

    $listing_res1 = mysqli_query($conn,$listing_qry1);

    $sql = "SELECT * FROM  " . TBL . "users where user_id='" . $sender_id . "'";
    $rs = mysqli_query($conn, $sql);
    $user_row = mysqli_fetch_array($rs);

    $sql1 = "SELECT * FROM  " . TBL . "listings where listing_id='" . $listing_id . "'";
    $rs1 = mysqli_query($conn, $sql1);
    $liiiist_row = mysqli_fetch_array($rs1);

    $user_email_id = $user_row['email_id'];
    $first_name = $user_row['first_name'];

    $listing_name = $liiiist_row['listing_name'];



    if ($listing_res) {

        //****************************    Admin Primary email fetch starts    *************************

        $admin_primary_email_fetch = mysqli_query($conn, "SELECT * FROM " . TBL . "footer  WHERE footer_id = '1' ");
        $admin_primary_email_fetchrow = mysqli_fetch_array($admin_primary_email_fetch);
        $admin_primary_email = $admin_primary_email_fetchrow['admin_primary_email'];
        $admin_footer_copyright = $admin_primary_email_fetchrow['footer_copyright'];
        $admin_site_name = $admin_primary_email_fetchrow['website_address'];
        $admin_address = $admin_primary_email_fetchrow['footer_address'];

        //****************************    Admin Primary email fetch ends    *************************

        $admin_email = $admin_primary_email; // Admin Email Id


//****************************    Client email starts    *************************

        $to1 = $user_email_id;
        $subject1 = "$admin_site_name Claim This Business - Approved";



        $message1 = '<style type="text/css" rel="stylesheet" media="all">
    /* Base ------------------------------ */
    
    @import url("https://fonts.googleapis.com/css?family=Nunito+Sans:400,700&display=swap");
    body{width:100%!important;height:100%;margin:0;-webkit-text-size-adjust:none}
a{color:#3869D4}
a img{border:none}
td{word-break:break-word}
.preheader{display:none!important;visibility:hidden;mso-hide:all;font-size:1px;line-height:1px;max-height:0;max-width:0;opacity:0;overflow:hidden}
body,td,th{font-family:"Nunito Sans",Helvetica,Arial,sans-serif}
h1{margin-top:0;color:#333;font-size:22px;font-weight:700;text-align:left}
h2{margin-top:0;color:#333;font-size:16px;font-weight:700;text-align:left}
h3{margin-top:0;color:#333;font-size:14px;font-weight:700;text-align:left}
td,th{font-size:16px}
p,ul,ol,blockquote{margin:.4em 0 1.1875em;font-size:16px;line-height:1.625}
p.sub{font-size:13px}
.align-right{text-align:right}
.align-left{text-align:left}
.align-center{text-align:center}
.button{background-color:#3869D4;border-top:10px solid #3869D4;border-right:18px solid #3869D4;border-bottom:10px solid #3869D4;border-left:18px solid #3869D4;display:inline-block;color:#FFF;text-decoration:none;border-radius:3px;box-shadow:0 2px 3px rgba(0,0,0,0.16);-webkit-text-size-adjust:none;box-sizing:border-box}
.button--green{background-color:#22BC66;border-top:10px solid #22BC66;border-right:18px solid #22BC66;border-bottom:10px solid #22BC66;border-left:18px solid #22BC66}
.button--red{background-color:#FF6136;border-top:10px solid #FF6136;border-right:18px solid #FF6136;border-bottom:10px solid #FF6136;border-left:18px solid #FF6136}
@media only screen and (max-width: 500px) {
.button{width:100%!important;text-align:center!important}
}
.attributes{margin:0 0 21px}
.attributes_content{background-color:#F4F4F7;padding:16px}
.attributes_item{padding:0}
.related{width:100%;margin:0;padding:25px 0 0;-premailer-width:100%;-premailer-cellpadding:0;-premailer-cellspacing:0}
.related_item{padding:10px 0;color:#CBCCCF;font-size:15px;line-height:18px}
.related_item-title{display:block;margin:.5em 0 0}
.related_item-thumb{display:block;padding-bottom:10px}
.related_heading{border-top:1px solid #CBCCCF;text-align:center;padding:25px 0 10px}
.discount{width:100%;margin:0;padding:24px;-premailer-width:100%;-premailer-cellpadding:0;-premailer-cellspacing:0;background-color:#F4F4F7;border:2px dashed #CBCCCF}
.discount_heading{text-align:center}
.discount_body{text-align:center;font-size:15px}
.social{width:auto}
.social td{padding:0;width:auto}
.social_icon{height:20px;margin:0 8px 10px;padding:0}
.purchase{width:100%;margin:0;padding:35px 0;-premailer-width:100%;-premailer-cellpadding:0;-premailer-cellspacing:0}
.purchase_content{width:100%;margin:0;padding:25px 0 0;-premailer-width:100%;-premailer-cellpadding:0;-premailer-cellspacing:0}
.purchase_item{padding:10px 0;color:#51545E;font-size:15px;line-height:18px}
.purchase_heading{padding-bottom:8px;border-bottom:1px solid #EAEAEC}
.purchase_heading p{margin:0;color:#85878E;font-size:12px}
.purchase_footer{padding-top:15px;border-top:1px solid #EAEAEC}
.purchase_total{margin:0;text-align:right;font-weight:700;color:#333}
.purchase_total--label{padding:0 15px 0 0}
body{background-color:#F4F4F7;color:#51545E}
p{color:#51545E}
p.sub{color:#6B6E76}
.email-wrapper{width:100%;margin:0;padding:0;-premailer-width:100%;-premailer-cellpadding:0;-premailer-cellspacing:0;background-color:#F4F4F7}
.email-content{width:100%;margin:0;padding:0;-premailer-width:100%;-premailer-cellpadding:0;-premailer-cellspacing:0}
.email-masthead{padding:25px 0;text-align:center}
.email-masthead_logo{width:94px}
.email-masthead_name{font-size:16px;font-weight:700;color:#A8AAAF;text-decoration:none;text-shadow:0 1px 0 #fff}
.email-body{width:100%;margin:0;padding:0;-premailer-width:100%;-premailer-cellpadding:0;-premailer-cellspacing:0;background-color:#FFF}
.email-body_inner{width:570px;margin:0 auto;padding:0;-premailer-width:570px;-premailer-cellpadding:0;-premailer-cellspacing:0;background-color:#FFF}
.email-footer{width:570px;margin:0 auto;padding:0;-premailer-width:570px;-premailer-cellpadding:0;-premailer-cellspacing:0;text-align:center}
.email-footer p{color:#6B6E76}
.body-action{width:100%;margin:30px auto;padding:0;-premailer-width:100%;-premailer-cellpadding:0;-premailer-cellspacing:0;text-align:center}
.body-sub{margin-top:25px;padding-top:25px;border-top:1px solid #EAEAEC}
.content-cell{padding:35px}
@media only screen and (max-width: 600px) {
.email-body_inner,.email-footer{width:100%!important}
}
@media (prefers-color-scheme: dark) {
body,.email-body,.email-body_inner,.email-content,.email-wrapper,.email-masthead,.email-footer{background-color:#333!important;color:#FFF!important}
p,ul,ol,blockquote,h1,h2,h3{color:#FFF!important}
.attributes_content,.discount{background-color:#222!important}
.email-masthead_name{text-shadow:none!important}
}
    </style>
   
    <style type="text/css">
      .f-fallback  {
        font-family: Arial, sans-serif;
      }
    </style>
 
  </head>
  <body>
<span class="preheader">Thanks for trying out [Product Name]. We’ve pulled together some information and resources to help you get started.</span>
<table class="email-wrapper" width="100%" cellpadding="0" cellspacing="0" role="presentation">
    <tr>
        <td align="center">
            <table class="email-content" width="100%" cellpadding="0" cellspacing="0" role="presentation">
                <tr>
                    <td class="email-masthead">
                        <a href="' . $webpage_full_link . '" class="f-fallback email-masthead_name">
                            ' . $admin_site_name . '
                        </a>
                    </td>
                </tr>
                <!-- Email Body -->
                <tr>
                    <td class="email-body" width="100%" cellpadding="0" cellspacing="0">
                        <table class="email-body_inner" align="center" width="570" cellpadding="0" cellspacing="0" role="presentation">
                            <!-- Body content -->
                            <tr>
                                <td class="content-cell">
                                    <div class="f-fallback">
                                        <h1>Hi, ' . $first_name . '!</h1>
                                        <p>Your New Claim Request for your ' . $listing_name . ' .</p>
                                        <!-- Action -->
                                        <p>Our Admin team verified & Approved your request,Please log into your dashboard to edit your ' . $listing_name . ' .</p >
                                        <!-- Action -->
                                        <table class="body-action" align="center" width="100%" cellpadding="0" cellspacing="0" role="presentation">
                                            <tr>
                                                <td align="center">
                                                    <table width="100%" border="0" cellspacing="0" cellpadding="0" role="presentation">
                                                        <tr>
                                                            <td align="center">
                                                                <a href="' . $webpage_full_link . '" class="f-fallback button" target="_blank">Access your dashboard</a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                        <p>If you have any questions, feel free to <a href="mailto:{{support_email}}">email our customer success team</a>. (We\'re lightning quick at replying .)</p >
                                        <p> Thanks,
                                            <br > ' . $admin_site_name . ' Team</p>
                                        <p><strong>P.S.</strong> Need immediate help getting started? Check out our <a href="' . $webpage_full_link . '">help documentation</a>. Or, just reply to this email, the [Product Name] support team is always ready to help!</p>
                                        <!-- Sub copy -->
                                        <table class="body-sub" role="presentation">
                                            <tr>
                                                <td>
                                                    <p class="f-fallback sub">If you’re having trouble with the button above, copy and paste the URL below into your web browser.</p>
                                                    <p class="f-fallback sub">' . $webpage_full_link . '</p>
                                                </td>
                                            </tr>
                                        </table>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <table class="email-footer" align="center" width="570" cellpadding="0" cellspacing="0" role="presentation">
                            <tr>
                                <td class="content-cell" align="center">
                                    <p class="f-fallback sub align-center">&copy; ' . $admin_footer_copyright . ' ' . $admin_site_name . '. All rights reserved.</p>
                                    <p class="f-fallback sub align-center">
                                        ' . $admin_site_name . '
                                        <br>' . $admin_address . '
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
</body>';


        $headers1 = "From: " . "$admin_email" . "\r\n";
        $headers1 .= "Reply-To: " . "$admin_email" . "\r\n";
        $headers1 .= "MIME-Version: 1.0\r\n";
        $headers1 .= "Content-Type: text/html; charset=utf-8\r\n";


        mail($to1, $subject1, $message1, $headers1); //Client email

        $_SESSION['status_msg'] = "Claim Request has been Approved Successfully!!!";

        header('Location: admin-claim-listing.php');
    } else {

        $_SESSION['status_msg'] = "Oops!! Something Went Wrong Try Later!!!";

        header('Location: admin-claim-listing.php');
    }


}else{
    header('Location: admin-claim-listing.php');
    exit();
}