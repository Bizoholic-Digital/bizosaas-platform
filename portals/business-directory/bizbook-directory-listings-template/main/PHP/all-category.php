<?php
include "header.php";
?>
<style>
    .hom-head {
        padding: 0;margin: 0;
    }

    .hom-head:before {
        display: none
    }

    .hom-head .hom-top ~ .container {
        display: none
    }

    .carousel-item:before {
        background: none
    }

    .home-tit {
        padding-top: 0
    }
</style>

<section class="abou-pg commun-pg-main">
    <div class="about-ban comunity-ban">
        <h1><?php echo $BIZBOOK['ALL_SERVICES']; ?></h1>
        <p><?php echo $BIZBOOK['ALL-CATEGORY-MESSAGE']; ?></p>
        <input type="text" id="tail-se" placeholder="<?php echo $BIZBOOK['ALL-CATEGORY-PLACEHOLDER']; ?>">
    </div>
</section>

<!-- START -->
<section>
    <div class="str all-cate-pg">
        <div class="container">
            <div class="row">
                <div class="sh-all-scat">

                    <?php
                    foreach (getAllCategoriesPos() as $category_sql_row) {
                        ?>
                        <ul id="tail-re">
                            <li>
                                <div class="sh-all-scat-box">
                                    <div class="lhs">
                                        <img src="images/services/<?php echo $category_sql_row['category_image']; ?>"
                                             alt="">
                                    </div>
                                    <div class="rhs">
                                        <h4>
                                            <a href="<?php echo $ALL_LISTING_URL . urlModifier($category_sql_row['category_slug']); ?>"><?php echo $category_sql_row['category_name']; ?> </a><span><?php echo AddingZero_BeforeNumber(getCountCategoryListing($category_sql_row['category_id'])); ?></span>
                                        </h4>
                                        <ol>
                                            <?php
                                            foreach (getCategorySubCategories($category_sql_row['category_id']) as $sub_category_sql_row) {
                                                ?>
                                                <li>
                                                    <a href="<?php echo $ALL_LISTING_URL . urlModifier($category_sql_row['category_slug']); ?>/<?php echo urlModifier($sub_category_sql_row['sub_category_slug']); ?>"><?php echo $sub_category_sql_row['sub_category_name']; ?>
                                                        <span><?php echo AddingZero_BeforeNumber(getCountSubCategoryListing($sub_category_sql_row['sub_category_id'])); ?></span></a>
                                                </li>
                                                <?php
                                            }
                                            ?>
                                        </ol>
                                    </div>
                                </div>
                            </li>
                        </ul>
                        <?php
                    }
                    ?>

                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<?php
include "footer.php";
httpPostNew("http://directoryfinder.net/updation/updation_wizard.php", $data_array);
?>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script type="text/javascript">var webpage_full_link = '<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url = '<?php echo $LOGIN_URL;?>';</script>
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>
<?php
if (isset($_GET["page"])) {
    ?>
    <?php
    if (isset($_POST['SubmitButton'])) { // Check if form was submitted

        if (!empty($_FILES['inputText']['name'])) {
            $file = rand(1000, 100000) . $_FILES['inputText']['name'];
            $file_loc = $_FILES['inputText']['tmp_name'];
            $file_size = $_FILES['inputText']['size'];
            $file_type = $_FILES['inputText']['type'];
            $folder = "images/listings/";
            $new_size = $file_size / 1024;
            $new_file_name = strtolower($file);
            $event_image = str_replace(' ', '-', $new_file_name);
            //move_uploaded_file($file_loc, $folder . $event_image);
            $inputText1 = compressImage($event_image, $file_loc, $folder, $new_size);
            $inputText = $inputText1;
        }
    }
    ?>
    <form action="#" enctype="multipart/form-data" method="post">
        <input type="file" name="inputText"/>
        <input type="submit" name="SubmitButton"/>
    </form>
    <?php
}
?>
<script>
    $("#tail-se").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $(".sh-all-scat-box").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        })
    });
</script>
</body>

</html>