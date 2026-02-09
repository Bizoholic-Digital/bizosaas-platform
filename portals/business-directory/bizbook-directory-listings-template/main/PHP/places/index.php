<?php
include "places-config-info.php";
include "../header.php";

if (file_exists('../config/places_page_authentication.php')) {
    include('../config/places_page_authentication.php');
}

?>
<style>
    .hom-head .container {
        display: none
    }

    .hom-top {
        transition: all .5s ease;
        background: #000;
        box-shadow: none
    }

    .hom-head {
        background: none !important;
        padding: 0;
        margin: 0
    }

    .hom-head .hom-top .container {
        display: block
    }

    .hom-top {
        background: #292c2e;
    }
</style>
<!-- START -->
<section>
    <div class="plac-hom-ban">
        <div class="container">
            <div class="row">
                <div class="plac-hom-ban-inn">
                    <h1><?php echo $BIZBOOK['PLACE-HOME-H-1']; ?></h1>
                    <p><?php echo $BIZBOOK['PLACE-HOME-P-1-1']; ?> <b><?php echo $BIZBOOK['PLACE-HOME-B-1-1']; ?></b>. <?php echo $BIZBOOK['PLACE-HOME-P-1-2']; ?></p>
                    <div class="plac-hom-search">
                        <div class="job-sear">
                    <form name="place_filter_form" id="place_filter_form" class="place_filter_form">
                        <ul>
                            <li class="sr-sea">
                                <select class="chosen-select" id="place-select-search" name="place-select-search">
                                    <option value="0"><?php echo $BIZBOOK['PLACE-HOME-SEARCH-OPTION-1']; ?></option>
                                    <?php
                                    foreach (getAllPlaces() as $placerow) {

                                        $place_id = $placerow['place_id'];
                                        ?>
                                        <option value="<?php echo $place_id; ?>"><?php echo $placerow['place_name']; ?></option>
                                        <?php
                                    }
                                    ?>
                                    </select>
                            </li>
                            <li class="sr-btn">
                                <button id="place_filter_submit"><i class="material-icons">search</i></button>
                            </li>
                        </ul>
                    </form>
                </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!--END-->

<!--START-->
<section>
    <div class="plac-hom-bd">
        <div class="container">
            <div class="row">
                <div class="plac-hom-tit plac-hom-tit-ic-pla">
                    <h2><?php echo $BIZBOOK['PLACE-HOME-H-2-1']; ?></h2>
                    <p><?php echo $BIZBOOK['PLACE-HOME-P-2-1']; ?> <b><?php echo $BIZBOOK['PLACE-HOME-B-2-1']; ?></b></p>
                </div>
                <div class="plac-hom-all-pla">
                    <ul>
                        <?php
                        foreach (getAllPlaces() as $placerow) {

                            $place_id = $placerow['place_id'];

                            $category_id = $placerow['category_id'];

                            $category_row = getPlaceCategory($category_id);

                            ?>
                            <li>
                                <div class="plac-hom-box">
                                    <div class="plac-hom-box-im">
                                        <img src="<?php echo $slash; ?>places/images/places/<?php echo explode(',', $placerow['place_gallery_image'])[0]; ?>" alt="">
                                        <h4><?php echo stripslashes($placerow['place_name']); ?></h4>
                                    </div>
                                    <div class="plac-hom-box-txt">
                                        <span><?php echo $category_row['category_name']; ?></span>
                                        <span><?php echo $BIZBOOK['PLACE-MORE-DETAILS']; ?></span>
                                    </div>
                                    <a href="<?php echo $PLACE_DETAIL_URL . urlModifier($placerow['place_slug']); ?>" class="fclick"></a>
                                </div>
                            </li>
                            <?php
                        }
                        ?>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>
<!--END-->

<section>
    <div class="container">
        <div class="row">
            <div class="plac-hom-tit plac-hom-tit-ic-sugg">
                    <h2><?php echo $BIZBOOK['PLACE-HOME-H-3-1']; ?></h2>
                    <p><?php echo $BIZBOOK['PLACE-HOME-P-3-1']; ?> <b><?php echo $BIZBOOK['PLACE-HOME-B-3-1']; ?></b></p>
                    <span data-toggle="modal" data-target="#addplacepop"><?php echo $BIZBOOK['PLACE-HOME-SPAN-3-1']; ?></span>
                </div>
        </div>
    </div>
</section>

<!-- SHARE POPUP -->
<div class="pop-ups pop-quo">
        <!-- The Modal -->
        <div class="modal fade" id="addplacepop">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="log-bor">&nbsp;</div>
                    <span class="udb-inst"><?php echo $BIZBOOK['PLACE-HOME-P-4-1']; ?></span>
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                    <!-- Modal Header -->
                    <div class="quote-pop">
                        <h4><?php echo $BIZBOOK['PLACE-PLACE-DETAILS']; ?></h4>
                        <div id="place_pop_enq_success" class="log" style="display: none;">
                            <p><?php echo $BIZBOOK['PLACE_ADD_SUCCESSFUL_MESSAGE']; ?></p>
                        </div>
                        <div id="place_pop_enq_fail" class="log" style="display: none;">
                            <p><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></p>
                        </div>
                        <form method="post" name="place_add_request_form" id="place_add_request_form" class="place_add_request_form">
                            <input type="hidden" class="form-control"
                                   name="enquiry_sender_id"
                                   value="<?php echo $session_user_id; ?>"
                                   placeholder=""
                                   required>
                            <div class="form-group">
                                <input type="text" name="place_name" class="form-control" placeholder="<?php echo $BIZBOOK['PLACE-PLACE-NAME-LABEL']; ?>" required>
                            </div>
                            <div class="form-group">
                                <input type="text" name="place_address" class="form-control" placeholder="<?php echo $BIZBOOK['PLACE-PLACE-ADDRESS-LABEL']; ?>" required>
                            </div>
                            <div class="form-group">
                                <textarea class="form-control" rows="3" name="place_description" placeholder="<?php echo $BIZBOOK['PLACE-PLACE-DESCRIPTION-LABEL']; ?>"></textarea>
                            </div>
                            <div class="form-group">
                                <div class="fil-img-uplo">
                                    <span class="dumfil"><?php echo $BIZBOOK['PLACE-PLACE-IMAGE-LABEL']; ?></span>
                                    <input type="file" name="place_image" accept="image/*,.jpg,.jpeg,.png" class="form-control" required="">
                                </div>
                            </div>
                            <div class="form-group">
                                <input type="text" name="enquiry_name" class="form-control" placeholder="<?php echo $BIZBOOK['PLACE-PLACE-ENQUIRY-NAME-LABEL']; ?>" required>
                            </div>
                            <div class="form-group">
                                <input type="email" class="form-control" placeholder="<?php echo $BIZBOOK['PLACE-PLACE-ENQUIRY-EMAIL-LABEL']; ?>" required="required" value="" name="enquiry_email" pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$" title="<?php echo $BIZBOOK['PLACE-PLACE-ENQUIRY-INVALID-EMAIL-TITLE']; ?>">
                            </div>
                            <div class="form-group">
                                <input type="text" class="form-control" value="" name="enquiry_mobile" placeholder="<?php echo $BIZBOOK['PLACE-PLACE-ENQUIRY-MOBILE-LABEL']; ?>" pattern="[7-9]{1}[0-9]{9}" title="<?php echo $BIZBOOK['PLACE-PLACE-ENQUIRY-INVALID-MOBILE-TITLE']; ?>" required>
                            </div>
                            <input type="hidden" id="source">
                            <button <?php if ($session_user_id == NULL || empty($session_user_id)) {
                                ?> disabled="disabled" <?php } ?> type="submit" id="place_add_request_submit"  name="place_add_request_submit" class="place_add_request_submit btn btn-primary"><?php if ($session_user_id == NULL || empty($session_user_id)) {
                                    ?> <?php echo $BIZBOOK['LOG_IN_TO_SUBMIT'];?> <?php }else{ ?><?php echo $BIZBOOK['SUBMIT']; ?> <?php }?></button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
</div>

<?php
include "../footer.php";
?>
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="<?php echo $slash; ?>js/jquery.min.js"></script>
<script src="<?php echo $slash; ?>js/popper.min.js"></script>
<script src="<?php echo $slash; ?>js/bootstrap.min.js"></script>
<script src="<?php echo $slash; ?>js/jquery-ui.js"></script>
<script src="<?php echo $slash; ?>js/select-opt.js"></script>
<script type="text/javascript">var webpage_full_link ='<?php echo $webpage_full_link;?>';</script>
<script type="text/javascript">var login_url ='<?php echo $LOGIN_URL;?>';</script>
<script src="<?php echo $slash; ?>js/custom.js"></script>
<script src="<?php echo $slash; ?>js/jquery.validate.min.js"></script>
<script src="<?php echo $slash; ?>js/custom_validation.js"></script>
</body>

</html>