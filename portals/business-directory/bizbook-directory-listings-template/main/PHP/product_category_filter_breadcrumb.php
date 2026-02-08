<?php

//database configuration
if (file_exists('config/info.php')) {
    include('config/info.php');
}

$category_id = $_POST['category_id'];


//get matched data from Sub - category table

if (getCountCategoryProductCategory($category_id) <= 0) {
    ?>
    <div class="row">
        <h1><?php echo $BIZBOOK['ALL_CATEGORIES']; ?></h1>

        <ul>
            <li><a href="index"><?php echo $BIZBOOK['HOME']; ?></a></li>
            <li><a href="all-products"><?php echo $BIZBOOK['ALL_CATEGORY']; ?></a></li>

        </ul>
    </div>
    <?php
} else {
    ?>

    <div class="row">
        <?php
        $category_name = getProductCategoryName($category_id);

        $category_slug = getProductCategorySlug($category_id);
        ?>
        <h1><?php echo $category_name; ?></h1>

        <ul>
            <li><a href="index"><?php echo $BIZBOOK['HOME']; ?></a></li>
            <li><a href="all-products"><?php echo $BIZBOOK['ALL_CATEGORY']; ?></a></li>
            <li>
                <a href="<?php echo $ALL_PRODUCTS_URL . urlModifier($category_slug); ?>"><?php echo $category_name; ?></a>
            </li>

        </ul>
    </div>

    <?php
}
?>