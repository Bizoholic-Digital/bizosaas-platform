<?php
include "header.php";
?>

<?php if ($footer_row['admin_place_show'] !=1) {
    header("Location: profile.php");
}
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <section class="ud-cen">
                <div class="container">
                    <div class="row">
                        <div class="plac-panl">
                            <div class="log-bor">&nbsp;</div>
                            <span class="udb-inst">Edit This Place</span>
                            <?php
                            $place_ida = $_GET['code'];
                            $place_row = getIdPlaces($place_ida);

                            ?>
                            <div class="log log-1">
                                <div class="login">
                                    <?php include "../page_level_message.php"; ?>
                                    <form name="place_form" id="place_form" method="post" action="update_place.php"
                                          enctype="multipart/form-data">
                                        <input type="hidden" id="place_gallery_image_old"
                                               value="<?php echo $place_row['place_gallery_image']; ?>"
                                               name="place_gallery_image_old"
                                               class="validate">
                                        <input type="hidden" id="place_id"
                                               value="<?php echo $place_row['place_id']; ?>"
                                               name="place_id"
                                               class="validate">
                                        <ul>
                                            <li>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <h6>Place details & Info</h6>
                                                            <label>Place name</label>
                                                            <input type="text" value="<?php echo $place_row['place_name']; ?>" name="place_name" required="required"
                                                                   class="form-control">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <label>Category</label>
                                                            <select name="category_id" required="required"
                                                                    class="chosen-select form-control">
                                                                <option value="">Select place category</option>
                                                                <?php
                                                                foreach (getAllPlaceCategories() as $row) {
                                                                    ?>
                                                                    <option <?php if ($place_row['category_id'] == $row['category_id']) {
                                                                        echo "selected";
                                                                    } ?>
                                                                        value="<?php echo $row['category_id']; ?>"><?php echo $row['category_name']; ?></option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <label>Tag name</label>
                                                            <input type="text" name="place_tags" required="required"
                                                                   class="form-control" value="<?php echo $place_row['place_tags']; ?>"
                                                                   placeholder="Ex: Group of three waterfalls, Best spot in canada">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <label>Status</label>
                                                            <select name="place_status" required="required"
                                                                    class="chosen-select form-control">
                                                                <option <?php if ($place_row['place_status'] == 1) { echo "selected"; } ?> value="1">Active</option>
                                                                <option <?php if ($place_row['place_status'] == 2) { echo "selected"; } ?> value="2">Open</option>
                                                                <option <?php if ($place_row['place_status'] == 3) { echo "selected"; } ?> value="3">Close</option>
                                                                <option <?php if ($place_row['place_status'] == 4) { echo "selected"; } ?> value="4">Temporarily closed</option>
                                                                <option <?php if ($place_row['place_status'] == 5) { echo "selected"; } ?> value="5">Permanently closed</option>
                                                            </select>
                                                        </div>
                                                    </div>
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <label>Tourism fee</label>
                                                            <input type="text" name="place_fee" value="<?php echo $place_row['place_fee']; ?>" required="required"
                                                                   class="form-control">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <label>Open time</label>
                                                            <select name="opening_time" required="required"
                                                                    class="chosen-select form-control">
                                                                <?php
                                                                $time = '4:00'; // start
                                                                for ($i = 0; $i <= 19; $i++) {
                                                                    $prev = date('g:i a', strtotime($time)); // format the start time
                                                                    $next = strtotime('+60mins', strtotime($time)); // add 60 mins
                                                                    $time = date('g:i A', $next); // format the next time
                                                                    ?>
                                                                    <option <?php if ($place_row['opening_time'] == $time) {
                                                                        echo "selected";
                                                                    } ?> value="<?php echo $time; ?>"><?php echo $time; ?></option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                    <div class="col-md-6">
                                                        <div class="form-group">
                                                            <label>Close time</label>
                                                            <select name="closing_time" required="required"
                                                                    class="chosen-select form-control"
                                                                    data-placeholder="Select places">
                                                                <?php
                                                                $time = '5:00'; // start
                                                                for ($i = 0; $i <= 18; $i++) {
                                                                    $prev = date('g:i a', strtotime($time)); // format the start time
                                                                    $next = strtotime('+60mins', strtotime($time)); // add 60 mins
                                                                    $time = date('g:i A', $next); // format the next time
                                                                    ?>
                                                                    <option <?php if ($place_row['closing_time'] == $time) {
                                                                        echo "selected";
                                                                    } ?> value="<?php echo $time; ?>"><?php echo $time; ?></option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->

                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label>Direction(Google map link)</label>
                                                            <input type="text" name="google_map" required="required"
                                                                   value="<?php echo $place_row['google_map']; ?>" placeholder="Ex: https://goo.gl/maps/cUZ39XriLPf9HhKk7"
                                                                   class="form-control">
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <hr>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <h6>Near by services & activity</h6>
                                                            <label>Discover places</label>
                                                            <select name="place_discover[]" multiple="multiple"
                                                                    class="chosen-select form-control"
                                                                    data-placeholder="Select places">
                                                                <?php
                                                                foreach (getExceptPlaces($place_row['place_id']) as $row) {
                                                                    ?>
                                                                    <option <?php $disArray = explode(',', $place_row['place_discover']);
                                                                    foreach($disArray as $dis_Array){
                                                                        if ($row['place_id'] == $dis_Array) {
                                                                            echo "selected";
                                                                        }
                                                                    } ?> value="<?php echo $row['place_id']; ?>"><?php echo $row['place_name']; ?></option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <hr>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label>Related places</label>
                                                            <select name="place_related[]" multiple="multiple"
                                                                    class="chosen-select form-control"
                                                                    data-placeholder="Select places">
                                                                <?php
                                                                foreach (getExceptPlaces($place_row['place_id']) as $row) {
                                                                    ?>
                                                                    <option <?php $relatedArray = explode(',', $place_row['place_related']);
                                                                    foreach($relatedArray as $related_Array){
                                                                        if ($row['place_id'] == $related_Array) {
                                                                            echo "selected";
                                                                        }
                                                                    } ?>
                                                                        value="<?php echo $row['place_id']; ?>"><?php echo $row['place_name']; ?></option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <hr>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label>Top near by Services(Business listings)</label>
                                                            <select name="place_listings[]" multiple="multiple"
                                                                    class="chosen-select form-control"
                                                                    data-placeholder="Select Listings">
                                                                <?php
                                                                foreach (getAllListing() as $row) {
                                                                    ?>
                                                                    <option <?php $relatedArray = explode(',', $place_row['place_listings']);
                                                                    foreach($relatedArray as $related_Array){
                                                                        if ($row['listing_id'] == $related_Array) {
                                                                            echo "selected";
                                                                        }
                                                                    } ?>
                                                                        value="<?php echo $row['listing_id']; ?>"><?php echo $row['listing_name']; ?></option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <hr>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label>Events in this place</label>
                                                            <select name="place_events[]" multiple="multiple"
                                                                    class="chosen-select form-control"
                                                                    data-placeholder="Select Events">
                                                                <?php
                                                                foreach (getAllEvents() as $row) {
                                                                    ?>
                                                                    <option <?php $relatedArray = explode(',', $place_row['place_events']);
                                                                    foreach($relatedArray as $related_Array){
                                                                        if ($row['event_id'] == $related_Array) {
                                                                            echo "selected";
                                                                        }
                                                                    } ?>
                                                                        value="<?php echo $row['event_id']; ?>"><?php echo $row['event_name']; ?></option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <hr>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label>Services Experts in this place</label>
                                                            <select name="place_experts[]"  multiple="multiple"
                                                                    class="chosen-select form-control"
                                                                    data-placeholder="Select Experts">
                                                                <?php
                                                                foreach (getAllExperts() as $row) {
                                                                    ?>
                                                                    <option <?php $relatedArray = explode(',', $place_row['place_experts']);
                                                                    foreach($relatedArray as $related_Array){
                                                                        if ($row['expert_id'] == $related_Array) {
                                                                            echo "selected";
                                                                        }
                                                                    } ?>
                                                                        value="<?php echo $row['expert_id']; ?>"><?php echo $row['profile_name']; ?></option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <hr>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <label>News & Articles in this place</label>
                                                            <select name="places_news[]" multiple="multiple"
                                                                    class="chosen-select form-control"
                                                                    data-placeholder="Select News/Articles">
                                                                <?php
                                                                foreach (getAllNews() as $row) {
                                                                    ?>
                                                                    <option <?php $relatedArray = explode(',', $place_row['places_news']);
                                                                    foreach($relatedArray as $related_Array){
                                                                        if ($row['news_id'] == $related_Array) {
                                                                            echo "selected";
                                                                        }
                                                                    } ?>
                                                                        value="<?php echo $row['news_id']; ?>"><?php echo $row['news_title']; ?></option>
                                                                    <?php
                                                                }
                                                                ?>
                                                            </select>
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <hr>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <h6>Photo gallery</h6>
                                                            <!--FILED END-->
                                                            <div>
                                                                <input type="file" name="place_gallery_image[]" id="place_gallery_image"
                                                                       accept="image/*,.jpg,.jpeg,.png" multiple>
                                                            </div>
                                                            <!--FILED START-->
                                                        </div>
                                                    </div>
                                                </div>
                                                <!--FILED END-->
                                                <hr>
                                                <!--FILED START-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group">
                                                            <h6>What people ask</h6>
                                                            <span class="add-list-add-btn plac-ask-add"
                                                                  title="add new field">+</span>
                                                            <span class="add-list-rem-btn plac-ask-remov"
                                                                  title="remove field">-</span>
                                                        </div>
                                                    </div>
                                                    <ul class="plac-ask-que">
                                                        <?php
                                                        $place_a_row_place_info_question = $place_row['place_info_question'];
                                                        $place_a_row_place_info_answer = $place_row['place_info_answer'];

                                                        $place_a_row_place_info_question_Array = explode(',', $place_a_row_place_info_question);
                                                        $place_a_row_place_info_answer_Array = explode(',', $place_a_row_place_info_answer);

                                                        $zipped = array_map(null, $place_a_row_place_info_question_Array, $place_a_row_place_info_answer_Array);

                                                        foreach($zipped as $tuple) {
                                                            $tuple[0]; // Info question
                                                            $tuple[1]; // Info Answer

                                                            ?>
                                                        <li>
                                                            <div class="col-md-4">
                                                                <div class="form-group">
                                                                    <label>Question:</label>
                                                                    <input type="text" name="place_info_question[]"
                                                                           value="<?php echo $tuple[0]; ?>" class="form-control">
                                                                </div>
                                                            </div>
                                                            <div class="col-md-8">
                                                                <div class="form-group">
                                                                    <label>Answer:</label>
                                                                    <input type="text" name="place_info_answer[]"
                                                                           value="<?php echo $tuple[1]; ?>" class="form-control">
                                                                </div>
                                                            </div>
                                                        </li>
                                                            <?php
                                                        }
                                                        ?>
                                                    </ul>

                                                </div>
                                                <!--FILED END-->

                                                <hr>
                                                <!--FILED END-->
                                                <div class="row">
                                                    <div class="col-md-12">
                                                        <div class="form-group jb-fm-box-hig">
                                                            <h5 data-toggle="collapse" data-target="#jb-expe">SEO
                                                                details</h5>
                                                            <div id="jb-expe" class="collapse coll-box show">
                                                                <input type="text" name="seo_title" class="form-control"
                                                                       value="<?php echo $place_row['seo_title']; ?>" placeholder="SEO Title">
                                                                <hr>
                                                                <input type="text" name="seo_description"
                                                                       class="form-control"
                                                                       value="<?php echo $place_row['seo_description']; ?>" placeholder="Meta descriptions">
                                                                <hr>
                                                                <input type="text" name="seo_keywords"
                                                                       value="<?php echo $place_row['seo_keywords']; ?>" class="form-control" placeholder="Meta keywords">
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        </ul>
                                        <!--FILED START-->
                                        <div class="row">
                                            <div class="col-md-12">
                                                <button type="submit" name="place_submit" class="btn btn-primary">
                                                    Update & Save
                                                </button>
                                            </div>
                                        </div>
                                        <!--FILED END-->
                                    </form>
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
<script src="../js/select-opt.js"></script>
<script type="text/javascript" src="../js/imageuploadify.min.js"></script>
<script src="js/admin-custom.js"></script>
<script type="text/javascript">
    $(document).ready(function () {
        $('input[id="place_gallery_image"]').imageuploadify();
    })
</script>
</body>

</html>