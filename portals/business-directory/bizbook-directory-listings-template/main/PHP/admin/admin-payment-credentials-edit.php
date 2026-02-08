<?php
include "header.php";
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
                    <?php
                    $payment_name1 =$_GET['row'];
                    if($payment_name1 == "cod"){

                        $payment_name = "Cash On Delivery";

                    }elseif ($payment_name1 == "paypal"){

                        $payment_name = "PayPal";

                    }elseif ($payment_name1 == "stripe"){

                        $payment_name = "Stripe";
                    }elseif ($payment_name1 == "razor_pay"){

                        $payment_name = "Razor Pay";
                    }elseif ($payment_name1 == "paytm"){

                        $payment_name = "Paytm";
                    }else{
                        $payment_name = "Cash On Delivery";
                    }

                    $row = getAllFooter();
                    ?>
                    <span class="udb-inst"><?php echo $payment_name; ?></span>
                    <div class="log log-1">
                        <div class="login">
                            <h4><?php echo $payment_name; ?> Credentials</h4>
                            <?php include "../page_level_message.php"; ?>

                            <?php if($payment_name1 =="cod") { ?>
                                <form name="payment_credentials" id="payment_credentials"
                                      action="update_payment_credential.php" method="post" enctype="multipart/form-data"
                                      class="cre-dup-form cre-dup-form-show">
                                    <input type="hidden" autocomplete="off" name="footer_id"
                                           value="<?php echo $row['footer_id']; ?>" id="footer_id" class="validate">
                                    <input type="hidden" autocomplete="off" name="footer_path"
                                           value="<?php echo $payment_name1; ?>" id="footer_id" class="validate">
                                    <ul>
                                        <li>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <input type="text" <?php if ($payment_name1 == "cod") { ?> name="" readonly="readonly" value="Free" <?php } ?>
                                                            class="form-control"
                                                            placeholder="Enter your business <?php echo $payment_name; ?> id *"
                                                            required>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <select
                                                            <?php if ($payment_name1 == "cod") { ?> name="admin_cod_status" <?php } ?>
                                                            required="required" class="form-control">
                                                            <option value="">Select status</option>
                                                            <option <?php if ($payment_name1 == "cod") {
                                                                    if ($row['admin_cod_status'] == "Active") { ?> selected="selected"  <?php }
                                                                } ?>>Active
                                                            </option>
                                                            <option
                                                                <?php if ($payment_name1 == "cod") {
                                                                    if ($row['admin_cod_status'] == "InActive") { ?> selected="selected"  <?php }
                                                                } ?>>InActive
                                                            </option>
                                                        </select>
                                                    </div>
                                                </div>
                                            </div>
                                        </li>
                                    </ul>
                                    <button type="submit" name="payment_credential_submit" class="btn btn-primary">
                                        Submit
                                    </button>
                                </form>
                                <?php
                            }
                            ?>
                            <?php if($payment_name1 =="paypal") { ?>
                                <form name="payment_credentials" id="payment_credentials"
                                      action="update_payment_credential.php" method="post" enctype="multipart/form-data"
                                      class="cre-dup-form cre-dup-form-show">
                                    <input type="hidden" autocomplete="off" name="footer_id"
                                           value="<?php echo $row['footer_id']; ?>" id="footer_id" class="validate">
                                    <input type="hidden" autocomplete="off" name="footer_path"
                                           value="<?php echo $payment_name1; ?>" id="footer_id" class="validate">
                                    <ul>
                                        <li>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <input
                                                            type="text" <?php if ($payment_name1 == "paypal") { ?> name="admin_paypal_id" value="<?php echo $row['admin_paypal_id']; ?>" <?php } ?>
                                                            class="form-control"
                                                            placeholder="Enter your business <?php echo $payment_name; ?> id *"
                                                            required>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <select <?php if ($payment_name1 == "paypal") { ?> name="admin_paypal_currency_code"  <?php } ?>
                                                            required="required" class="form-control">
                                                            <option value="">Select Currency Code</option>
                                                            <option value="AUD" <?php if ($row['admin_paypal_currency_code'] == "AUD") { ?> selected="selected"  <?php }?>>Australian dollar</option>
                                                            <option value="BRL" <?php if ($row['admin_paypal_currency_code'] == "BRL") { ?> selected="selected"  <?php }?>>Brazilian real</option>
                                                            <option value="CAD" <?php if ($row['admin_paypal_currency_code'] == "CAD") { ?> selected="selected"  <?php }?>>Canadian dollar</option>
                                                            <option value="CNY" <?php if ($row['admin_paypal_currency_code'] == "CNY") { ?> selected="selected"  <?php }?>>Chinese Renmenbi</option>
                                                            <option value="CZK" <?php if ($row['admin_paypal_currency_code'] == "CZK") { ?> selected="selected"  <?php }?>>Czech koruna</option>
                                                            <option value="DKK" <?php if ($row['admin_paypal_currency_code'] == "DKK") { ?> selected="selected"  <?php }?>>Danish krone</option>
                                                            <option value="EUR" <?php if ($row['admin_paypal_currency_code'] == "EUR") { ?> selected="selected"  <?php }?>>Euro</option>
                                                            <option value="HKD" <?php if ($row['admin_paypal_currency_code'] == "HKD") { ?> selected="selected"  <?php }?>>Hong Kong dollar</option>
                                                            <option value="HUF" <?php if ($row['admin_paypal_currency_code'] == "HUF") { ?> selected="selected"  <?php }?>>Hungarian forint</option>
                                                            <option value="INR" <?php if ($row['admin_paypal_currency_code'] == "INR") { ?> selected="selected"  <?php }?>>Indian rupee</option>
                                                            <option value="ILS" <?php if ($row['admin_paypal_currency_code'] == "ILS") { ?> selected="selected"  <?php }?>>Israeli new shekel</option>
                                                            <option value="JPY" <?php if ($row['admin_paypal_currency_code'] == "JPY") { ?> selected="selected"  <?php }?>>Japanese yen</option>
                                                            <option value="MYR" <?php if ($row['admin_paypal_currency_code'] == "MYR") { ?> selected="selected"  <?php }?>>Malaysian ringgit</option>
                                                            <option value="MXN" <?php if ($row['admin_paypal_currency_code'] == "MXN") { ?> selected="selected"  <?php }?>>Mexican peso</option>
                                                            <option value="TWD" <?php if ($row['admin_paypal_currency_code'] == "TWD") { ?> selected="selected"  <?php }?>>New Taiwan dollar</option>
                                                            <option value="NZD" <?php if ($row['admin_paypal_currency_code'] == "NZD") { ?> selected="selected"  <?php }?>>New Zealand dollar</option>
                                                            <option value="NOK" <?php if ($row['admin_paypal_currency_code'] == "NOK") { ?> selected="selected"  <?php }?>>Norwegian krone</option>
                                                            <option value="PHP" <?php if ($row['admin_paypal_currency_code'] == "PHP") { ?> selected="selected"  <?php }?>>Philippine peso</option>
                                                            <option value="PLN" <?php if ($row['admin_paypal_currency_code'] == "PLN") { ?> selected="selected"  <?php }?>>Polish złoty</option>
                                                            <option value="GBP" <?php if ($row['admin_paypal_currency_code'] == "GBP") { ?> selected="selected"  <?php }?>>Pound sterling</option>
                                                            <option value="RUB" <?php if ($row['admin_paypal_currency_code'] == "RUB") { ?> selected="selected"  <?php }?>>Russian ruble</option>
                                                            <option value="SGD" <?php if ($row['admin_paypal_currency_code'] == "SGD") { ?> selected="selected"  <?php }?>>Singapore dollar</option>
                                                            <option value="SEK" <?php if ($row['admin_paypal_currency_code'] == "SEK") { ?> selected="selected"  <?php }?>>Swedish krona</option>
                                                            <option value="CHF" <?php if ($row['admin_paypal_currency_code'] == "CHF") { ?> selected="selected"  <?php }?>>Swiss franc</option>
                                                            <option value="THB" <?php if ($row['admin_paypal_currency_code'] == "THB") { ?> selected="selected"  <?php }?>>Thai baht</option>
                                                            <option value="USD" <?php if ($row['admin_paypal_currency_code'] == "USD") { ?> selected="selected"  <?php }?>>United States dollar</option>
                                                        </select>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <select <?php if ($payment_name1 == "paypal") { ?> name="admin_paypal_status"  <?php } ?>
                                                            required="required" class="form-control">
                                                            <option value="">Select status</option>
                                                            <option <?php if ($payment_name1 == "paypal") {
                                                                if ($row['admin_paypal_status'] == "Active") { ?> selected="selected"  <?php }
                                                            } ?>>Active
                                                            </option>
                                                            <option <?php if ($payment_name1 == "paypal") {
                                                                if ($row['admin_paypal_status'] == "InActive") { ?> selected="selected"  <?php }
                                                            } ?>>InActive
                                                            </option>
                                                        </select>
                                                    </div>
                                                </div>
                                            </div>
                                        </li>
                                    </ul>
                                    <button type="submit" name="payment_credential_submit" class="btn btn-primary">
                                        Submit
                                    </button>
                                </form>
                                <?php
                            } ?>
                            <?php if($payment_name1 =="stripe") { ?>
                            <form name="payment_credentials" id="payment_credentials" action="update_payment_credential.php" method="post" enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                                <input type="hidden" autocomplete="off" name="footer_id"
                                       value="<?php echo $row['footer_id']; ?>" id="footer_id" class="validate">
                                <input type="hidden" autocomplete="off" name="footer_path"
                                       value="<?php echo $payment_name1; ?>" id="footer_id" class="validate">
                                <ul>
                                    <li>
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <input type="text" <?php if($payment_name1 =="stripe"){ ?> name="admin_stripe_id" value="<?php echo $row['admin_stripe_id']; ?>" <?php } ?>
                                                         class="form-control" placeholder="Enter your business <?php echo $payment_name; ?> Publishable key *" required>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <input type="text" <?php if($payment_name1 =="stripe"){ ?> name="admin_stripe_secret_id" value="<?php echo $row['admin_stripe_secret_id']; ?>" <?php } ?>
                                                           class="form-control" placeholder="Enter your business <?php echo $payment_name; ?> Secret key *" required>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <select <?php if ($payment_name1 == "stripe") { ?> name="admin_stripe_currency_code"  <?php } ?>
                                                        required="required" class="form-control">
                                                        <option value="">Select Currency Code</option>
                                                        <option value="AUD" <?php if ($row['admin_stripe_currency_code'] == "AUD") { ?> selected="selected"  <?php }?>>Australian dollar</option>
                                                        <option value="BRL" <?php if ($row['admin_stripe_currency_code'] == "BRL") { ?> selected="selected"  <?php }?>>Brazilian real</option>
                                                        <option value="CAD" <?php if ($row['admin_stripe_currency_code'] == "CAD") { ?> selected="selected"  <?php }?>>Canadian dollar</option>
                                                        <option value="CNY" <?php if ($row['admin_stripe_currency_code'] == "CNY") { ?> selected="selected"  <?php }?>>Chinese Renmenbi</option>
                                                        <option value="CZK" <?php if ($row['admin_stripe_currency_code'] == "CZK") { ?> selected="selected"  <?php }?>>Czech koruna</option>
                                                        <option value="DKK" <?php if ($row['admin_stripe_currency_code'] == "DKK") { ?> selected="selected"  <?php }?>>Danish krone</option>
                                                        <option value="EUR" <?php if ($row['admin_stripe_currency_code'] == "EUR") { ?> selected="selected"  <?php }?>>Euro</option>
                                                        <option value="HKD" <?php if ($row['admin_stripe_currency_code'] == "HKD") { ?> selected="selected"  <?php }?>>Hong Kong dollar</option>
                                                        <option value="HUF" <?php if ($row['admin_stripe_currency_code'] == "HUF") { ?> selected="selected"  <?php }?>>Hungarian forint</option>
                                                        <option value="INR" <?php if ($row['admin_stripe_currency_code'] == "INR") { ?> selected="selected"  <?php }?>>Indian rupee</option>
                                                        <option value="ILS" <?php if ($row['admin_stripe_currency_code'] == "ILS") { ?> selected="selected"  <?php }?>>Israeli new shekel</option>
                                                        <option value="JPY" <?php if ($row['admin_stripe_currency_code'] == "JPY") { ?> selected="selected"  <?php }?>>Japanese yen</option>
                                                        <option value="MYR" <?php if ($row['admin_stripe_currency_code'] == "MYR") { ?> selected="selected"  <?php }?>>Malaysian ringgit</option>
                                                        <option value="MXN" <?php if ($row['admin_stripe_currency_code'] == "MXN") { ?> selected="selected"  <?php }?>>Mexican peso</option>
                                                        <option value="TWD" <?php if ($row['admin_stripe_currency_code'] == "TWD") { ?> selected="selected"  <?php }?>>New Taiwan dollar</option>
                                                        <option value="NZD" <?php if ($row['admin_stripe_currency_code'] == "NZD") { ?> selected="selected"  <?php }?>>New Zealand dollar</option>
                                                        <option value="NOK" <?php if ($row['admin_stripe_currency_code'] == "NOK") { ?> selected="selected"  <?php }?>>Norwegian krone</option>
                                                        <option value="PHP" <?php if ($row['admin_stripe_currency_code'] == "PHP") { ?> selected="selected"  <?php }?>>Philippine peso</option>
                                                        <option value="PLN" <?php if ($row['admin_stripe_currency_code'] == "PLN") { ?> selected="selected"  <?php }?>>Polish złoty</option>
                                                        <option value="GBP" <?php if ($row['admin_stripe_currency_code'] == "GBP") { ?> selected="selected"  <?php }?>>Pound sterling</option>
                                                        <option value="RUB" <?php if ($row['admin_stripe_currency_code'] == "RUB") { ?> selected="selected"  <?php }?>>Russian ruble</option>
                                                        <option value="SGD" <?php if ($row['admin_stripe_currency_code'] == "SGD") { ?> selected="selected"  <?php }?>>Singapore dollar</option>
                                                        <option value="SEK" <?php if ($row['admin_stripe_currency_code'] == "SEK") { ?> selected="selected"  <?php }?>>Swedish krona</option>
                                                        <option value="CHF" <?php if ($row['admin_stripe_currency_code'] == "CHF") { ?> selected="selected"  <?php }?>>Swiss franc</option>
                                                        <option value="THB" <?php if ($row['admin_stripe_currency_code'] == "THB") { ?> selected="selected"  <?php }?>>Thai baht</option>
                                                        <option value="USD" <?php if ($row['admin_stripe_currency_code'] == "USD") { ?> selected="selected"  <?php }?>>United States dollar</option>
                                                    </select>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-md-12">
                                                <div class="form-group">
                                                    <select
                                                        <?php if($payment_name1 =="stripe"){ ?> name="admin_stripe_status" <?php } ?>
                                                        required="required" class="form-control">
                                                        <option value="">Select status</option>
                                                        <option
                                                            <?php if($payment_name1 =="stripe"){ if($row['admin_stripe_status']=="Active"){ ?> selected="selected"  <?php } }  ?>>Active</option>
                                                        <option
                                                            <?php if($payment_name1 =="stripe"){ if($row['admin_stripe_status']=="InActive"){ ?> selected="selected"  <?php } }  ?>>InActive</option>
                                                    </select>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                </ul>
                                <button type="submit" name="payment_credential_submit" class="btn btn-primary">Submit</button>
                            </form>
                                <?php
                            } ?>
                            <?php if($payment_name1 =="razor_pay") { ?>
                                <form name="payment_credentials" id="payment_credentials" action="update_payment_credential.php" method="post" enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                                    <input type="hidden" autocomplete="off" name="footer_id"
                                           value="<?php echo $row['footer_id']; ?>" id="footer_id" class="validate">
                                    <input type="hidden" autocomplete="off" name="footer_path"
                                           value="<?php echo $payment_name1; ?>" id="footer_id" class="validate">
                                    <ul>
                                        <li>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <input type="text" <?php if($payment_name1 =="razor_pay"){ ?> name="admin_razor_pay_key_id" value="<?php echo $row['admin_razor_pay_key_id']; ?>" <?php } ?>
                                                               class="form-control" placeholder="Enter your business <?php echo $payment_name; ?> key Id *" required>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <input type="text" <?php if($payment_name1 =="razor_pay"){ ?> name="admin_razor_pay_key_id_secret" value="<?php echo $row['admin_razor_pay_key_id_secret']; ?>" <?php } ?>
                                                               class="form-control" placeholder="Enter your business <?php echo $payment_name; ?> Secret key *" required>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <select <?php if ($payment_name1 == "razor_pay") { ?> name="admin_razor_pay_currency_code"  <?php } ?>
                                                            required="required" class="form-control">
                                                            <option value="">Select Currency Code</option>
                                                            <option value="AUD" <?php if ($row['admin_razor_pay_currency_code'] == "AUD") { ?> selected="selected"  <?php }?>>Australian dollar</option>
                                                            <option value="BRL" <?php if ($row['admin_razor_pay_currency_code'] == "BRL") { ?> selected="selected"  <?php }?>>Brazilian real</option>
                                                            <option value="CAD" <?php if ($row['admin_razor_pay_currency_code'] == "CAD") { ?> selected="selected"  <?php }?>>Canadian dollar</option>
                                                            <option value="CNY" <?php if ($row['admin_razor_pay_currency_code'] == "CNY") { ?> selected="selected"  <?php }?>>Chinese Renmenbi</option>
                                                            <option value="CZK" <?php if ($row['admin_razor_pay_currency_code'] == "CZK") { ?> selected="selected"  <?php }?>>Czech koruna</option>
                                                            <option value="DKK" <?php if ($row['admin_razor_pay_currency_code'] == "DKK") { ?> selected="selected"  <?php }?>>Danish krone</option>
                                                            <option value="EUR" <?php if ($row['admin_razor_pay_currency_code'] == "EUR") { ?> selected="selected"  <?php }?>>Euro</option>
                                                            <option value="HKD" <?php if ($row['admin_razor_pay_currency_code'] == "HKD") { ?> selected="selected"  <?php }?>>Hong Kong dollar</option>
                                                            <option value="HUF" <?php if ($row['admin_razor_pay_currency_code'] == "HUF") { ?> selected="selected"  <?php }?>>Hungarian forint</option>
                                                            <option value="INR" <?php if ($row['admin_razor_pay_currency_code'] == "INR") { ?> selected="selected"  <?php }?>>Indian rupee</option>
                                                            <option value="ILS" <?php if ($row['admin_razor_pay_currency_code'] == "ILS") { ?> selected="selected"  <?php }?>>Israeli new shekel</option>
                                                            <option value="JPY" <?php if ($row['admin_razor_pay_currency_code'] == "JPY") { ?> selected="selected"  <?php }?>>Japanese yen</option>
                                                            <option value="MYR" <?php if ($row['admin_razor_pay_currency_code'] == "MYR") { ?> selected="selected"  <?php }?>>Malaysian ringgit</option>
                                                            <option value="MXN" <?php if ($row['admin_razor_pay_currency_code'] == "MXN") { ?> selected="selected"  <?php }?>>Mexican peso</option>
                                                            <option value="TWD" <?php if ($row['admin_razor_pay_currency_code'] == "TWD") { ?> selected="selected"  <?php }?>>New Taiwan dollar</option>
                                                            <option value="NZD" <?php if ($row['admin_razor_pay_currency_code'] == "NZD") { ?> selected="selected"  <?php }?>>New Zealand dollar</option>
                                                            <option value="NOK" <?php if ($row['admin_razor_pay_currency_code'] == "NOK") { ?> selected="selected"  <?php }?>>Norwegian krone</option>
                                                            <option value="PHP" <?php if ($row['admin_razor_pay_currency_code'] == "PHP") { ?> selected="selected"  <?php }?>>Philippine peso</option>
                                                            <option value="PLN" <?php if ($row['admin_razor_pay_currency_code'] == "PLN") { ?> selected="selected"  <?php }?>>Polish złoty</option>
                                                            <option value="GBP" <?php if ($row['admin_razor_pay_currency_code'] == "GBP") { ?> selected="selected"  <?php }?>>Pound sterling</option>
                                                            <option value="RUB" <?php if ($row['admin_razor_pay_currency_code'] == "RUB") { ?> selected="selected"  <?php }?>>Russian ruble</option>
                                                            <option value="SGD" <?php if ($row['admin_razor_pay_currency_code'] == "SGD") { ?> selected="selected"  <?php }?>>Singapore dollar</option>
                                                            <option value="SEK" <?php if ($row['admin_razor_pay_currency_code'] == "SEK") { ?> selected="selected"  <?php }?>>Swedish krona</option>
                                                            <option value="CHF" <?php if ($row['admin_razor_pay_currency_code'] == "CHF") { ?> selected="selected"  <?php }?>>Swiss franc</option>
                                                            <option value="THB" <?php if ($row['admin_razor_pay_currency_code'] == "THB") { ?> selected="selected"  <?php }?>>Thai baht</option>
                                                            <option value="USD" <?php if ($row['admin_razor_pay_currency_code'] == "USD") { ?> selected="selected"  <?php }?>>United States dollar</option>
                                                        </select>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <select
                                                            <?php if($payment_name1 =="razor_pay"){ ?> name="admin_razor_pay_status" <?php } ?>
                                                            required="required" class="form-control">
                                                            <option value="">Select status</option>
                                                            <option
                                                                <?php if($payment_name1 =="razor_pay"){ if($row['admin_razor_pay_status']=="Active"){ ?> selected="selected"  <?php } }  ?>>Active</option>
                                                            <option
                                                                <?php if($payment_name1 =="razor_pay"){ if($row['admin_razor_pay_status']=="InActive"){ ?> selected="selected"  <?php } }  ?>>InActive</option>
                                                        </select>
                                                    </div>
                                                </div>
                                            </div>
                                        </li>
                                    </ul>
                                    <button type="submit" name="payment_credential_submit" class="btn btn-primary">Submit</button>
                                </form>
                                <?php
                            } ?>
                            <?php if($payment_name1 =="paytm") { ?>
                                <form name="payment_credentials" id="payment_credentials" action="update_payment_credential.php" method="post" enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                                    <input type="hidden" autocomplete="off" name="footer_id"
                                           value="<?php echo $row['footer_id']; ?>" id="footer_id" class="validate">
                                    <input type="hidden" autocomplete="off" name="footer_path"
                                           value="<?php echo $payment_name1; ?>" id="footer_id" class="validate">
                                    <ul>
                                        <li>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <input type="text" <?php if($payment_name1 =="paytm"){ ?> name="admin_paytm_merchant_id" value="<?php echo $row['admin_paytm_merchant_id']; ?>" <?php } ?>
                                                               class="form-control" placeholder="Enter your business <?php echo $payment_name; ?> Merchant Id *" required>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <input type="text" <?php if($payment_name1 =="paytm"){ ?> name="admin_paytm_merchant_key" value="<?php echo $row['admin_paytm_merchant_key']; ?>" <?php } ?>
                                                               class="form-control" placeholder="Enter your business <?php echo $payment_name; ?> Merchant key *" required>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <input type="text" <?php if($payment_name1 =="paytm"){ ?> name="admin_paytm_merchant_website" value="<?php echo $row['admin_paytm_merchant_website']; ?>" <?php } ?>
                                                               class="form-control" placeholder="Enter your business <?php echo $payment_name; ?> Merchant Website *" required>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <select disabled <?php if ($payment_name1 == "paytm") { ?> name="admin_paytm_currency_code"  <?php } ?>
                                                            required="required" class="form-control">

                                                            <option disabled value="INR" selected="selected" >Indian rupee</option>

                                                        </select>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col-md-12">
                                                    <div class="form-group">
                                                        <select
                                                            <?php if($payment_name1 =="paytm"){ ?> name="admin_paytm_status" <?php } ?>
                                                            required="required" class="form-control">
                                                            <option value="">Select status</option>
                                                            <option
                                                                <?php if($payment_name1 =="paytm"){ if($row['admin_paytm_status']=="Active"){ ?> selected="selected"  <?php } }  ?>>Active</option>
                                                            <option
                                                                <?php if($payment_name1 =="paytm"){ if($row['admin_paytm_status']=="InActive"){ ?> selected="selected"  <?php } }  ?>>InActive</option>
                                                        </select>
                                                    </div>
                                                </div>
                                            </div>
                                        </li>
                                    </ul>
                                    <button type="submit" name="payment_credential_submit" class="btn btn-primary">Submit</button>
                                </form>
                                <?php
                            } ?>
                            <div class="col-md-12">
                                    <a href="admin-payment-credentials.php" class="skip">Go to Payment Credentials >></a>
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
    <script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
</body>

</html>