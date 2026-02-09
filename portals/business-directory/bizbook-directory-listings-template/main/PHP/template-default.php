<?php
include "header.php";

if ($_GET['code'] == NULL && empty($_GET['code'])) {

    header("Location: $redirect_url");  //Redirect When code parameter is empty
}

$page_codea1 = str_replace('-', ' ', $_GET['code']);
$page_codea = str_replace('.php', '', $page_codea1);

$page_row = getActivePageSlug(2,$page_codea); // To Fetch particular General Promotion Data

if ($page_row['page_id'] == NULL && empty($page_row['page_id'])) {


    header("Location: $redirect_url");  //Redirect When No User Found in Table
}

$page_id = $page_row['page_id'];
seopageview($page_id); //Function To Find Page View

if ($page_row['page_css'] != NULL) {
    ?>

    <style>
        <?php echo stripslashes($page_row['page_css']); ?>
    </style>
    <?php
}if ($page_row['page_js'] != NULL) {
    ?>
    <script>
        <?php echo stripslashes($page_row['page_js']); ?>
    </script>
    <?php
}
?>
    <!-- START -->
    <!-- //template-def //template-rhs -->
	<section class="<?php if($footer_row['admin_language']== 2){ echo "lg-arb";}?> abou-pg template-comm template-rhs">
        <div class="container">
            <div class="row">
                <div class="templ-def-cent">
                    <h1><?php echo $page_row['page_name']; ?></h1>
                    <p><?php echo stripslashes($page_row['page_description']); ?></p>
                </div>
                <div class="templ-def-rhs">
                    <?php
                    if($page_row['page_show_listings'] == 1 && $page_row['page_listings'] != NULL) {
                        ?>
                        <div class="box templ-rhs-eve">
                            <div class="hot-page2-hom-pre-head">
                                <h4><?php echo $BIZBOOK['LISTING']; ?></h4>
                            </div>
                            <div class="hot-page2-hom-pre">
                                <ul>
                                    <?php
                                    $page_listings = explode(',', $page_row['page_listings']);
                                    foreach ($page_listings as $listing_id) {
                                        $listing_row = getIdListing($listing_id);
                                        ?>
                                        <li>
                                            <div class="hot-page2-hom-pre-1">
                                                <img src="<?php echo $slash; ?><?php if ($listing_row['profile_image'] != NULL || !empty($listing_row['profile_image'])) {
                                                    echo "images/listings/" . $listing_row['profile_image'];
                                                } else {
                                                    echo "images/listings/hot4.jpg";
                                                } ?>" alt="">
                                            </div>
                                            <div class="hot-page2-hom-pre-2">
                                                <h5><?php echo $listing_row['listing_name']; ?></h5>
                                                <span><?php echo $listing_row['listing_address']; ?></span>
                                            </div>
                                            <a href="<?php echo $LISTING_URL.urlModifier($listing_row['listing_slug']); ?>" class="fclick"></a>
                                        </li>
                                        <?php
                                    }
                                    ?>
                                </ul>
                            </div>
                        </div>
                        <?php
                    } if($page_row['page_show_products'] == 1 && $page_row['page_products'] != NULL) {
                    ?>
                    <div class="box templ-rhs-eve">
                         <div class="hot-page2-hom-pre-head">
                            <h4><?php echo $BIZBOOK['PRODUCTS']; ?></h4>
                        </div>
                        <div class="hot-page2-hom-pre">
                            <ul>
                                <?php
                                $page_products = explode(',', $page_row['page_products']);
                                foreach ($page_products as $product_id) {
                                $productrow = getIdProduct($product_id);
                                ?>
                                <li>
                                    <div class="hot-page2-hom-pre-1">
                                        <img src="<?php echo $slash; ?><?php if ($productrow['gallery_image'] != NULL || !empty($productrow['gallery_image'])) {
                                            echo "images/products/" . array_shift(explode(',', $productrow['gallery_image']));
                                        } else {
                                            echo "images/products/hot4.jpg";
                                        } ?>" alt="">
                                    </div>
                                    <div class="hot-page2-hom-pre-2">
                                        <h5><?php echo $productrow['product_name']; ?></h5>
                                        <span><b class="pro-off"><?php echo $footer_row['currency_symbol']; ?><?php echo $productrow['product_price']; ?></b></span>
                                    </div>
                                    <a href="<?php echo $PRODUCT_URL.urlModifier($productrow['product_slug']); ?>" class="fclick"></a>
                                </li>
                                    <?php
                                }
                                ?>
                            </ul>
                        </div>
                    </div>
                        <?php
                    } if($page_row['page_show_blogs'] == 1 && $page_row['page_blogs'] != NULL) {
                    ?>
                    <div class="box templ-rhs-eve">
                         <div class="hot-page2-hom-pre-head">
                            <h4><?php echo $BIZBOOK['BLOG_POSTS']; ?></h4>
                        </div>
                        <div class="hot-page2-hom-pre">
                            <ul>
                                <?php
                                $page_blogs = explode(',', $page_row['page_blogs']);
                                foreach ($page_blogs as $blog_id) {
                                    $blogrow = getBlog($blog_id);
                                    ?>
                                    <li>
                                        <div class="hot-page2-hom-pre-1">
                                            <img src="<?php echo $slash; ?>images/blogs/<?php echo $blogrow['blog_image']; ?>" alt="">
                                        </div>
                                        <div class="hot-page2-hom-pre-2">
                                            <h5><?php echo $blogrow['blog_name']; ?></h5>
                                            <span><?php  echo dateFormatconverter($blogrow['blog_cdt']); ?></span>
                                        </div>
                                        <a href="<?php echo $BLOG_URL.urlModifier($blogrow['blog_slug']); ?>" class="fclick"></a>
                                    </li>
                                    <?php
                                }
                                ?>
                            </ul>
                        </div>
                    </div>
                        <?php
                    } if($page_row['page_show_events'] == 1 && $page_row['page_events'] != NULL) {
                        ?>
                        <div class="box templ-rhs-eve">
                            <div class="hot-page2-hom-pre-head">
                                <h4><?php echo $BIZBOOK['EVENTS']; ?></h4>
                            </div>
                            <div class="hot-page2-hom-pre">
                                <ul>
                                    <?php
                                    $page_events = explode(',', $page_row['page_events']);
                                    foreach ($page_events as $event_id) {
                                        $eventrow = getEvent($event_id);
                                    ?>
                                    <li>
                                        <div class="hot-page2-hom-pre-1">
                                            <img src="<?php echo $slash; ?>images/events/<?php echo $eventrow['event_image']; ?>" alt="">
                                        </div>
                                        <div class="hot-page2-hom-pre-2">
                                            <h5><?php echo $eventrow['event_name']; ?></h5>
                                            <span><?php echo $eventrow['event_address']; ?></span>
                                        </div>
                                        <a href="<?php echo $EVENT_URL.urlModifier($eventrow['event_slug']); ?>" class="fclick"></a>
                                    </li>
                                        <?php
                                    }
                                    ?>
                                </ul>
                            </div>
                        </div>
                        <?php
                    }
                    ?>
                    <div class="box templ-rhs-eve">
                         <div class="hot-page2-hom-pre-head">
                            <h4><?php echo $BIZBOOK['LEAD-SEND-ENQUIRY']; ?></h4>
                        </div>
                        <div class="templ-rhs-form">
                            <div id="home_enq_success" class="log"
                             style="display: none;">
                            <p><?php echo $BIZBOOK['ENQUIRY_SUCCESSFUL_MESSAGE']; ?></p>
                        </div>
                        <div id="home_enq_fail" class="log" style="display: none;">
                            <p><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></p>
                        </div>
                        <div id="home_enq_same" class="log" style="display: none;">
                            <p><?php echo $BIZBOOK['ENQUIRY_OWN_LISTING_MESSAGE']; ?></p>
                        </div>
                        <form name="home_enquiry_form" id="home_enquiry_form" method="post"
                              enctype="multipart/form-data">
                            <input type="hidden" class="form-control" name="listing_id" value="0" placeholder="" required>
                            <input type="hidden" class="form-control" name="listing_user_id" value="0" placeholder="" required>
                            <input type="hidden" class="form-control" name="enquiry_sender_id" value="" placeholder="" required>
                            <input type="hidden" class="form-control"
                                   name="enquiry_source"
                                   value="<?php if (isset($_GET["src"])) {
                                       echo $_GET["src"];
                                   } else {
                                       echo "Website";
                                   }; ?>" placeholder="" required>
                            <div class="form-group">
                                <input type="text" name="enquiry_name" value="" required="required" class="form-control" placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>">
                            </div>
                            <div class="form-group">
                                <input type="email" class="form-control" placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>" required="required" value="" name="enquiry_email" pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$" title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>">
                            </div>
                            <div class="form-group">
                                <input type="text" class="form-control" value="" name="enquiry_mobile"
                                       placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>" pattern="[7-9]{1}[0-9]{9}"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>" required="">
                            </div>
                            <div class="form-group">
                                <select name="enquiry_category" id="enquiry_category" class="form-control">
                                    <option value=""><?php echo $BIZBOOK['SELECT_CATEGORY']; ?></option>
                                    <?php
                                    foreach (getAllCategories() as $categories_row) {
                                        ?>
                                        <option
                                            value="<?php echo $categories_row['category_id']; ?>"><?php echo $categories_row['category_name']; ?></option>
                                        <?php
                                    }
                                    ?>
                                </select>
                            </div>
                            <div class="form-group">
                        <textarea class="form-control" rows="3" name="enquiry_message"
                                  placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                            </div>
                            <input type="hidden" id="source">
                            <button type="submit" id="home_enquiry_submit" name="home_enquiry_submit"
                                    class="btn btn-primary"><?php echo $BIZBOOK['SUBMIT']; ?></button>
                        </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
	</section>
	<!--END-->

<?php
if($page_row['page_seo_schema'] != NULL) {
    ?>
    <!-- WEBSITE SCHEMA STARTS -->
    <h2 style="display: none"><?php echo $page_row['page_seo_schema']; ?></h2>
    <!-- WEBSITE SCHEMA ENDS -->
    <?php
}
?>
   
<?php
include "footer.php";
?>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>
</body>

</html>