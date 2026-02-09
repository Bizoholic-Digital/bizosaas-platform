<?php
include "header.php";

$actual_link = "http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";

?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Admin Promote <?php echo $type; ?></span>
                <div class="ud-cen-s2 ud-pro-edit">
                    <h2>Promote Your <?php echo $type; ?></h2>
                    <?php include "../page_level_message.php"; ?>

                    <table class="responsive-table bordered">
                        <form name="create_promote_form" id="create_promote_form" method="post"
                              action="insert_new_promote.php" enctype="multipart/form-data">
                            <input type="hidden" value="<?php echo $user_id; ?>" name="user_id" id="user_id" class="validate">
                            <input type="hidden" value="" name="ad_total_days" id="ad_total_days" class="validate">
                            <input type="hidden" value="" name="ad_cost_per_day" id="ad_cost_per_day" class="validate">
                            <input type="hidden" value="1" name="adposi" id="adposi" class="validate">
                            <input type="hidden" value="" name="ad_total_cost" id="ad_total_cost" class="validate">
                            <input type="hidden" value="<?php echo $actual_link; ?>" name="url" id="url"
                                   class="validate">
                            <input type="hidden" value="1" name="type_value" id="type_value" class="validate">

                            <tbody>

                            <tr>
                                <td>
                                    <select name="type_id" required="required"
                                            id="type_id" class=" form-control">
                                        <option value="">Choose Listing</option>
                                        <?php
                                        foreach (getAllListing() as $listing_row) {
                                            ?>
                                            <option <?php if ($_SESSION['listing_id'] == $listing_row['listing_id']) {
                                                echo "selected";
                                            } ?>
                                                value="<?php echo $listing_row['listing_id']; ?>">
                                                <?php echo $listing_row['listing_name']; ?></option>
                                            <?php
                                        }
                                        ?>
                                    </select>
                                </td>
                            </tr>


                            <tr>

                                <td>
                                    <div class="form-group">
                                        <input id="start-date" name="ad_start_date" required="required" type="date" class="form-control">
                                    </div>
                                </td>
                            </tr>

                            <tr>

                                <td>
                                    <div class="form-group">
                                        <input id="end-date" name="ad_end_date" type="date" required="required" class="form-control">
                                    </div>
                                </td>
                            </tr>

                            <tr>

                                <td>
                                    <div class="row">
                                        <div class="col-md-12">
                                            <div style="display:block" class="ad-pri-cal">
                                                <ul>
                                                    <li>
                                                        <div>
                                                            <span>Total days</span>
                                                            <h5 class="ad-tdays">0</h5>
                                                        </div>
                                                    </li>
                                                    <li>
                                                        <div>
                                                            <span>Cost Per Day</span>
                                                            <h5><b class="ad-pocost">1</b></h5>
                                                        </div>
                                                    </li>
                                                    <li>
                                                        <div>
                                                            <span>Total Points</span>
                                                            <h5><b class="ad-tcost">0</b></h5>
                                                        </div>
                                                    </li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </td>
                            </tr>

                            <tr>
                                <td>
                                    <button type="submit" name="create_promote_submit" class="db-pro-bot-btn">Submit
                                    </button>
                                </td>
                                <td></td>
                            </tr>

                            </tbody>
                        </form>
                    </table>
                </div>


            </div>

        </div>
    </div>
</section>
<!-- END -->

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="../js/jquery.min.js"></script>
<script src="../js/popper.min.js"></script>
<script src="../js/bootstrap.min.js"></script>
<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js"></script>
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
<script>
    //ADS TOTAL DAYS CALCULATION
    $("#start-date, #end-date").change(function () {
        var firstDate = $("#start-date").val();
        var secondDate = $("#end-date").val();
        var millisecondsPerDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
        var startDay = new Date(firstDate);
        var endDay = new Date(secondDate);
        var diffDays = Math.abs((startDay.getTime() - endDay.getTime()) / (millisecondsPerDay));
        $(".ad-tdays").text(diffDays);
        $("#ad_total_days").val(diffDays);
        // var adpocost = $('#adposi').find('option:selected', this).attr('mytag');
        var adpocost = $('#adposi').val();
        $(".ad-pocost").text(adpocost);
        $("#ad_cost_per_day").val(adpocost);
        var totcost = diffDays * adpocost;
        $(".ad-tcost").text(totcost);
        $("#ad_total_cost").val(totcost);
    });
</script>
</body>

</html>