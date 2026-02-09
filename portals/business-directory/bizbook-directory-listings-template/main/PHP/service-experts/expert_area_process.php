<?php

//database configuration
if (file_exists('expert-config-info.php')) {
    include "expert-config-info.php";
}

$country_id = $_POST['country_id'];

//get matched data from Sub - category table

if (getCountExpertAreaCity($country_id) <= 0) {
    ?>
    <option value=""><?php echo $BIZBOOK['NO_AREA_FOUND_MESSAGE']; ?></option>
    <?php
} else {

    foreach (getAllExpertAreaCity($country_id) as $sub_categories_row) {
        ?>
        <option <?php if ($_SESSION['city_id'] == $sub_categories_row['city_id']) {
            echo "selected";
        } ?>
            value="<?php echo $sub_categories_row['city_id']; ?>"><?php echo $sub_categories_row['city_name']; ?></option>

        <?php
    }
}
?>