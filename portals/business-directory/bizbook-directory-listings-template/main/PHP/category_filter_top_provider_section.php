<?php

//database configuration
if (file_exists('config/info.php')) {
    include('config/info.php');
}

$category_id = $_POST['category_id'];

$category_search_query = "AND FIND_IN_SET($category_id, category_id)";

//get matched data from category table

if ((getCountCategoryCategory($category_id) <= 0) || $category_id == NULL){
    ?>
    
    <?php
} else {
    ?>

    <ul>
        <?php
        $nearby_listsql = "SELECT " . TBL . "listings.*, " . TBL . "users.user_plan FROM " . TBL . "listings

                                            LEFT JOIN " . TBL . "users ON " . TBL . "listings.user_id = " . TBL . "users.user_id  WHERE " . TBL . "listings.listing_status= 'Active'

                                            AND " . TBL . "listings.listing_is_delete != '2' $category_search_query $sub_category_search_query

                                            ORDER BY " . TBL . "users.user_plan DESC," . TBL . "listings.listing_id DESC LIMIT 5 ";

        $nearby_listrs = mysqli_query($conn, $nearby_listsql);
        while ($nearby_listrow = mysqli_fetch_array($nearby_listrs)) {
            ?>
            <li>
                <div class="near-bx">
                    <div class="ne-1">
                        <img
                            src="<?php echo $webpage_full_link; ?><?php if ($nearby_listrow['profile_image'] != NULL || !empty($nearby_listrow['profile_image'])) {
                                echo "images/listings/" . $nearby_listrow['profile_image'];
                            } else {
                                echo "images/listings/hot4.jpg";
                            } ?>">
                    </div>
                    <div class="ne-2">
                        <h5><?php echo $nearby_listrow['listing_name']; ?></h5>
                        <p><?php echo $BIZBOOK['CITY'].':'; ?> <?php echo $nearby_listrow['listing_address']; ?></p>
                    </div>
                    <div class="ne-3">
                        <span>5.0</span>
                    </div>
                    <a href="<?php echo $LISTING_URL . urlModifier($nearby_listrow['listing_slug']); ?>"><?php echo $listrow['listing_name']; ?></a>
                </div>
            </li>
            <?php
        }
        ?>
    </ul>

    <?php

}

?>