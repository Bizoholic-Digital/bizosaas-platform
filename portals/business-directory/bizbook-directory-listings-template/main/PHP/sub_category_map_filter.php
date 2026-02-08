<?php

//database configuration
if (file_exists('config/info.php')) {
    include('config/info.php');
}

$category_id = $_POST['category_id'];


//get matched data from Sub - category table

if (getCountSubCategoryCategory($category_id) <= 0) {
    ?>

    <?php
} else {
    ?>
    <div class="sub_cat_section1 map-fi-com map-fi-subcate" style="width: 100%;">
        <select name="sub_cat_check" id="sub_cat_check1" class="sub_cat_check">
            <?php
            foreach (getCategorySubCategories($category_id) as $sub_category_row) {
                ?>
                <option value="<?php echo $sub_category_row['sub_category_id']; ?>">
                    <?php echo $sub_category_row['sub_category_name']; ?></option>
                <?php
            }
            ?>
        </select>
    </div>
    <?php

}
?>