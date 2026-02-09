<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}

include "dashboard_left_pane.php";

if (file_exists('config/general_user_authentication.php')) {
    include('config/general_user_authentication.php');
}

if (file_exists('config/product_page_authentication.php')) {
    include('config/product_page_authentication.php');
}
?>
    <!--CENTER SECTION-->
    <div class="ud-main">
   <div class="ud-main-inn ud-no-rhs">
    <div class="ud-cen">
        <div class="log-bor">&nbsp;</div>
        <span class="udb-inst"><?php echo $BIZBOOK['ALL_PRODUCTS']; ?></span>
        <?php include('config/user_activation_checker.php'); ?>
        <div class="ud-cen-s2">
            <h2><?php echo $BIZBOOK['PRODUCT_DETAILS']; ?></h2>
            <?php include "page_level_message.php"; ?>
            <a href="add-new-product" class="db-tit-btn"><?php echo $BIZBOOK['ADD_NEW_PRODUCT']; ?></a>
            <table class="responsive-table bordered">
                <thead>
                <tr>
                    <th><?php echo $BIZBOOK['S_NO']; ?></th>
                    <th><?php echo $BIZBOOK['PRODUCT_NAME']; ?></th>
                    <th><?php echo $BIZBOOK['VIEWS']; ?></th>
                    <th><?php echo $BIZBOOK['STATUS']; ?></th>
                    <th><?php echo $BIZBOOK['EDIT']; ?></th>
                    <th><?php echo $BIZBOOK['DELETE']; ?></th>
                    <th><?php echo $BIZBOOK['PREVIEW']; ?></th>
                </tr>
                </thead>
                <tbody>
                <?php

                $si = 1;
                foreach (getAllProductUser($_SESSION['user_id']) as $productrow) {

                    $reviewproduct_id = $productrow['product_id'];

                    ?>
                    <tr>
                        <td><?php echo $si; ?></td>
                        <td><img
                                src="<?php if ($productrow['gallery_image'] != NULL || !empty($productrow['gallery_image'])) {
                                    echo "images/products/" . array_shift(explode(',', $productrow['gallery_image']));
                                } else {
                                    echo "images/products/hot4.jpg";
                                } ?>"><?php echo $productrow['product_name']; ?> <span><?php echo dateFormatconverter($productrow['product_cdt']); ?></span></td>
                        <td><span class="db-list-rat"><?php echo product_pageview_count($productrow['product_id']); ?></span></td>
                        <td><span class="db-list-ststus"><?php echo $productrow['product_status']; ?></span></td>
                        <td><a href="edit-product?code=<?php echo $productrow['product_code']; ?>" class="db-list-edit"><?php echo $BIZBOOK['EDIT']; ?></a></td>
                        <td><a href="delete-product?code=<?php echo $productrow['product_code']; ?>" class="db-list-edit"><?php echo $BIZBOOK['DELETE']; ?></a></td>
                        <td><a href="<?php echo $PRODUCT_URL.urlModifier($productrow['product_slug']); ?>" class="db-list-edit" target="_blank"><?php echo $BIZBOOK['PREVIEW']; ?></a></td>
                    </tr>

                    <?php
                    $si++;
                }
                ?>

                </tbody>
            </table>
        </div>
    </div>
    <!--RIGHT SECTION-->
<?php
include "dashboard_right_pane.php";
?>