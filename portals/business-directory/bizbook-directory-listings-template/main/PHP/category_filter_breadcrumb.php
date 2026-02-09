<?php

//database configuration
if (file_exists('config/info.php')) {
    include('config/info.php');
}

$category_id = $_POST['category_id'];


//get matched data from category table

if ((getCountCategoryCategory($category_id) <= 0) || $category_id == NULL){
    ?>
    <div class="row">
        <h1><?php echo $BIZBOOK['ALL_CATEGORIES']; ?></h1>

        <ul>
            <li><a href="<?php echo $webpage_full_link; ?>"><?php echo $BIZBOOK['HOME']; ?></a></li>
            <li><a href="<?php echo $webpage_full_link.'all-listing'; ?>"><?php echo $BIZBOOK['ALL_CATEGORY']; ?></a></li>

        </ul>
    </div>
    <?php
} else {
    ?>

    <div class="row">
        <?php
        $category_name = getCategoryName($category_id);
        $category_slug = getCategorySlug($category_id);
        ?>
        <h1><?php echo $category_name; ?></h1>

        <ul>
            <li><a href="<?php echo $webpage_full_link; ?>"><?php echo $BIZBOOK['HOME']; ?></a></li>
            <li><a href="<?php echo $webpage_full_link.'all-listing'; ?>"><?php echo $BIZBOOK['ALL_CATEGORY']; ?></a></li>
            <li>
                <a href="<?php echo $ALL_LISTING_URL . urlModifier($category_slug); ?>"><?php echo $category_name; ?></a>
            </li>

        </ul>
    </div>

    <?php

}

?>