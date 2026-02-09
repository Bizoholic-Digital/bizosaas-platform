<?php
//database configuration
if (file_exists('job-config-info.php')) {
    include "job-config-info.php";
}

$category_id = $_POST['category_id'];

//get matched data from Sub - category table

if (getCountJobSubCategoryCategory($category_id) <= 0) {
    ?>

    <?php
} else {
    ?>
    <div class="sub_cat_section filt-com lhs-sub">
        <h4><?php echo $BIZBOOK['ALL-LISTING-SUB-CATEGORY']; ?></h4>
        <ul>
            <?php
            foreach (getCategoryJobSubCategories($category_id) as $sub_category_row) {

                ?>

                <li>
                    <div class="chbox">
                        <input type="checkbox" class="sub_cat_check" name="sub_cat_check"
                               value="<?php echo $sub_category_row['sub_category_id']; ?>"
                               id="<?php echo $sub_category_row['sub_category_name']; ?>"/>
                        <label
                            for="<?php echo $sub_category_row['sub_category_name']; ?>"><?php echo $sub_category_row['sub_category_name']; ?></label>
                    </div>
                </li>

                <?php
            }
            ?>
        </ul>
    </div>
    <?php
}
?>