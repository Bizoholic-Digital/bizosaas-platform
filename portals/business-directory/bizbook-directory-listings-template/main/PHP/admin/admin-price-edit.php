<?php
include "header.php";
?>
<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">pricing details</span>
                <div class="ud-cen-s2 ud-pro-edit">
                    <h2>Edit pricing details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <table class="responsive-table bordered">
                        <?php
                        $plan_type_id = $_GET['row'];
                        $row = getPlanType($plan_type_id);
                        ?>
                        <form id="plan_type_edit" name="plan_type_edit" method="post" action="update_plan_type.php">
                            <input type="hidden" class="validate" id="plan_type_id" name="plan_type_id"
                                   value="<?php echo $row['plan_type_id']; ?>" required="required">
                            <tbody>
                            <tr>
                                <td>Plan name</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" id="plan_type_name"
                                               name="plan_type_name"
                                               value="<?php echo $row['plan_type_name']; ?>" required="required"
                                               class="form-control">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Price</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="plan_type_price"
                                               name="plan_type_price"
                                               value="<?php echo $row['plan_type_price']; ?>"
                                               onkeypress="return isNumber(event)"
                                               required="required">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Duration</td>
                                <td>
                                    <div class="form-group">
                                        <select id="plan_type_duration" name="plan_type_duration"
                                                required="required" class="form-control">
                                            <option <?php if($row['plan_type_duration']== 1){ echo "selected"; } ?> value="1">1 month</option>
                                            <option <?php if($row['plan_type_duration']== 2){ echo "selected"; } ?> value="2">2 months</option>
                                            <option <?php if($row['plan_type_duration']== 3){ echo "selected"; } ?> value="3">3 months</option>
                                            <option <?php if($row['plan_type_duration']== 6){ echo "selected"; } ?> value="6">6 months</option>
                                            <option <?php if($row['plan_type_duration']== 12){ echo "selected"; } ?> value="12">1 year</option>
                                            <option <?php if($row['plan_type_duration']== 24){ echo "selected"; } ?> value="24">2 years</option>
                                            <option <?php if($row['plan_type_duration']== 36){ echo "selected"; } ?> value="36">3 years</option>
                                            <option <?php if($row['plan_type_duration']== 48){ echo "selected"; } ?> value="48">4 years</option>
                                            <option <?php if($row['plan_type_duration']== 60){ echo "selected"; } ?> value="60">5 years</option>
                                            <option <?php if($row['plan_type_duration']== 72){ echo "selected"; } ?> value="72">6 years</option>
                                            <option <?php if($row['plan_type_duration']== 84){ echo "selected"; } ?> value="84">7 years</option>
                                            <option <?php if($row['plan_type_duration']== 96){ echo "selected"; } ?> value="96">8 years</option>
                                            <option <?php if($row['plan_type_duration']== 108){ echo "selected"; } ?> value="108">9 years</option>
                                            <option <?php if($row['plan_type_duration']== 120){ echo "selected"; } ?> value="120">10 years</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>No of listings</td>
                                <td>
                                    <div class="form-group">
                                        <select id="plan_type_listing_count" name="plan_type_listing_count"
                                                required="required" class="form-control">
                                            <option <?php if($row['plan_type_listing_count']== 1){ echo "selected"; } ?> value="1">1</option>
                                            <option <?php if($row['plan_type_listing_count']== 5){ echo "selected"; } ?> value="5">5</option>
                                            <option <?php if($row['plan_type_listing_count']== 10){ echo "selected"; } ?> value="10">10</option>
                                            <option <?php if($row['plan_type_listing_count']== 15){ echo "selected"; } ?> value="15">15</option>
                                            <option <?php if($row['plan_type_listing_count']== 20){ echo "selected"; } ?> value="20">20</option>
                                            <option <?php if($row['plan_type_listing_count']== 25){ echo "selected"; } ?> value="25">25</option>
                                            <option <?php if($row['plan_type_listing_count']== 30){ echo "selected"; } ?> value="30">30</option>
                                            <option <?php if($row['plan_type_listing_count']== 50){ echo "selected"; } ?> value="50">50</option>
                                            <option <?php if($row['plan_type_listing_count']== 70){ echo "selected"; } ?> value="70">70</option>
                                            <option <?php if($row['plan_type_listing_count']== 100){ echo "selected"; } ?> value="100">100</option>
                                            <option <?php if($row['plan_type_listing_count']== 200){ echo "selected"; } ?> value="200">200</option>
                                            <option <?php if($row['plan_type_listing_count']== 1000){ echo "selected"; } ?> value="1000">Unlimited</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>No of products</td>
                                <td>
                                    <div class="form-group">
                                        <select id="plan_type_product_count" name="plan_type_product_count"
                                                required="required" class="form-control">
                                            <option <?php if($row['plan_type_product_count']== 1){ echo "selected"; } ?> value="1">1</option>
                                            <option <?php if($row['plan_type_product_count']== 5){ echo "selected"; } ?> value="5">5</option>
                                            <option <?php if($row['plan_type_product_count']== 10){ echo "selected"; } ?> value="10">10</option>
                                            <option <?php if($row['plan_type_product_count']== 15){ echo "selected"; } ?> value="15">15</option>
                                            <option <?php if($row['plan_type_product_count']== 20){ echo "selected"; } ?> value="20">20</option>
                                            <option <?php if($row['plan_type_product_count']== 25){ echo "selected"; } ?> value="25">25</option>
                                            <option <?php if($row['plan_type_product_count']== 30){ echo "selected"; } ?> value="30">30</option>
                                            <option <?php if($row['plan_type_product_count']== 50){ echo "selected"; } ?> value="50">50</option>
                                            <option <?php if($row['plan_type_product_count']== 70){ echo "selected"; } ?> value="70">70</option>
                                            <option <?php if($row['plan_type_product_count']== 100){ echo "selected"; } ?> value="100">100</option>
                                            <option <?php if($row['plan_type_product_count']== 200){ echo "selected"; } ?> value="200">200</option>
                                            <option <?php if($row['plan_type_product_count']== 1000){ echo "selected"; } ?> value="1000">Unlimited</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>No of events</td>
                                <td>
                                    <div class="form-group">
                                        <select id="plan_type_event_count" name="plan_type_event_count"
                                                required="required" class="form-control">
                                            <option <?php if($row['plan_type_event_count']== 1){ echo "selected"; } ?> value="1">1</option>
                                            <option <?php if($row['plan_type_event_count']== 5){ echo "selected"; } ?> value="5">5</option>
                                            <option <?php if($row['plan_type_event_count']== 10){ echo "selected"; } ?> value="10">10</option>
                                            <option <?php if($row['plan_type_event_count']== 15){ echo "selected"; } ?> value="15">15</option>
                                            <option <?php if($row['plan_type_event_count']== 20){ echo "selected"; } ?> value="20">20</option>
                                            <option <?php if($row['plan_type_event_count']== 25){ echo "selected"; } ?> value="25">25</option>
                                            <option <?php if($row['plan_type_event_count']== 30){ echo "selected"; } ?> value="30">30</option>
                                            <option <?php if($row['plan_type_event_count']== 50){ echo "selected"; } ?> value="50">50</option>
                                            <option <?php if($row['plan_type_event_count']== 70){ echo "selected"; } ?> value="70">70</option>
                                            <option <?php if($row['plan_type_event_count']== 100){ echo "selected"; } ?> value="100">100</option>
                                            <option <?php if($row['plan_type_event_count']== 200){ echo "selected"; } ?> value="200">200</option>
                                            <option <?php if($row['plan_type_event_count']== 1000){ echo "selected"; } ?> value="1000">Unlimited</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>No of blogs</td>
                                <td>
                                    <div class="form-group">
                                        <select id="plan_type_blog_count" name="plan_type_blog_count"
                                                required="required" class="form-control">
                                            <option <?php if($row['plan_type_blog_count']== 1){ echo "selected"; } ?> value="1">1</option>
                                            <option <?php if($row['plan_type_blog_count']== 5){ echo "selected"; } ?> value="5">5</option>
                                            <option <?php if($row['plan_type_blog_count']== 10){ echo "selected"; } ?> value="10">10</option>
                                            <option <?php if($row['plan_type_blog_count']== 15){ echo "selected"; } ?> value="15">15</option>
                                            <option <?php if($row['plan_type_blog_count']== 20){ echo "selected"; } ?> value="20">20</option>
                                            <option <?php if($row['plan_type_blog_count']== 25){ echo "selected"; } ?> value="25">25</option>
                                            <option <?php if($row['plan_type_blog_count']== 30){ echo "selected"; } ?> value="30">30</option>
                                            <option <?php if($row['plan_type_blog_count']== 50){ echo "selected"; } ?> value="50">50</option>
                                            <option <?php if($row['plan_type_blog_count']== 70){ echo "selected"; } ?> value="70">70</option>
                                            <option <?php if($row['plan_type_blog_count']== 100){ echo "selected"; } ?> value="100">100</option>
                                            <option <?php if($row['plan_type_blog_count']== 200){ echo "selected"; } ?> value="200">200</option>
                                            <option <?php if($row['plan_type_blog_count']== 1000){ echo "selected"; } ?> value="1000">Unlimited</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>No of jobs</td>
                                <td>
                                    <div class="form-group">
                                        <select id="plan_type_job_count" name="plan_type_job_count"
                                                required="required" class="form-control">
                                            <option <?php if($row['plan_type_job_count']== 1){ echo "selected"; } ?> value="1">1</option>
                                            <option <?php if($row['plan_type_job_count']== 5){ echo "selected"; } ?> value="5">5</option>
                                            <option <?php if($row['plan_type_job_count']== 10){ echo "selected"; } ?> value="10">10</option>
                                            <option <?php if($row['plan_type_job_count']== 15){ echo "selected"; } ?> value="15">15</option>
                                            <option <?php if($row['plan_type_job_count']== 20){ echo "selected"; } ?> value="20">20</option>
                                            <option <?php if($row['plan_type_job_count']== 25){ echo "selected"; } ?> value="25">25</option>
                                            <option <?php if($row['plan_type_job_count']== 30){ echo "selected"; } ?> value="30">30</option>
                                            <option <?php if($row['plan_type_job_count']== 50){ echo "selected"; } ?> value="50">50</option>
                                            <option <?php if($row['plan_type_job_count']== 70){ echo "selected"; } ?> value="70">70</option>
                                            <option <?php if($row['plan_type_job_count']== 100){ echo "selected"; } ?> value="100">100</option>
                                            <option <?php if($row['plan_type_job_count']== 200){ echo "selected"; } ?> value="200">200</option>
                                            <option <?php if($row['plan_type_job_count']== 1000){ echo "selected"; } ?> value="1000">Unlimited</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>User Points</td>
                                <td>
                                    <div class="form-group">
                                        <input type="text" class="form-control" id="plan_type_points"
                                               name="plan_type_points"
                                               value="<?php echo $row['plan_type_points']; ?>"
                                               onkeypress="return isNumber(event)"
                                               required="required">
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Get direct leads</td>
                                <td>
                                    <div class="form-group">
                                        <select id="plan_type_direct_lead" name="plan_type_direct_lead" class="form-control">
                                            <option <?php if ($row['plan_type_direct_lead'] == 1) {
                                                echo "selected";
                                            } ?> value="1">Yes</option>
                                            <option <?php if ($row['plan_type_direct_lead'] == 0) {
                                                echo "selected";
                                            } ?> value="0">No</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Email notification(leads)</td>
                                <td>
                                    <div class="form-group">
                                        <select id="plan_type_email_notification" name="plan_type_email_notification" class="form-control">
                                            <option <?php if ($row['plan_type_email_notification'] == 1) {
                                                echo "selected";
                                            } ?> value="1">Yes</option>
                                            <option <?php if ($row['plan_type_email_notification'] == 0) {
                                                echo "selected";
                                            } ?> value="0">No</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Verified listing</td>
                                <td>
                                    <div class="form-group">
                                        <select id="plan_type_verified" name="plan_type_verified" class="form-control">
                                            <option <?php if ($row['plan_type_verified'] == 1) {
                                                echo "selected";
                                            } ?> value="1">Yes</option>
                                            <option <?php if ($row['plan_type_verified'] == 0) {
                                                echo "selected";
                                            } ?> value="0">No</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Trusted listing</td>
                                <td>
                                    <div class="form-group">
                                        <select id="plan_type_trusted" name="plan_type_trusted" class="form-control">
                                            <option <?php if ($row['plan_type_trusted'] == 1) {
                                                echo "selected";
                                            } ?> value="1">Yes</option>
                                            <option <?php if ($row['plan_type_trusted'] == 0) {
                                                echo "selected";
                                            } ?> value="0">No</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Special offers</td>
                                <td>
                                    <div class="form-group">
                                        <select id="plan_type_offers" name="plan_type_offers" class="form-control">
                                            <option <?php if ($row['plan_type_offers'] == 1) {
                                                echo "selected";
                                            } ?> value="1">Yes</option>
                                            <option <?php if ($row['plan_type_offers'] == 0) {
                                                echo "selected";
                                            } ?> value="0">No</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Photos</td>
                                <td>
                                    <div class="form-group">
                                        <select type="number" id="plan_type_photos_count"
                                                name="plan_type_photos_count" class="form-control">
                                            <option <?php if($row['plan_type_photos_count']== 1){ echo "selected"; } ?> value="1">1</option>
                                            <option <?php if($row['plan_type_photos_count']== 2){ echo "selected"; } ?> value="2">2</option>
                                            <option <?php if($row['plan_type_photos_count']== 5){ echo "selected"; } ?> value="5">5</option>
                                            <option <?php if($row['plan_type_photos_count']== 10){ echo "selected"; } ?> value="10">10</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Videos</td>
                                <td>
                                    <div class="form-group">
                                        <select type="number" id="plan_type_videos_count"
                                                name="plan_type_videos_count" class="form-control">
                                            <option <?php if($row['plan_type_videos_count']== 1){ echo "selected"; } ?> value="1">1</option>
                                            <option <?php if($row['plan_type_videos_count']== 2){ echo "selected"; } ?> value="2">2</option>
                                            <option <?php if($row['plan_type_videos_count']== 5){ echo "selected"; } ?> value="5">5</option>
                                            <option <?php if($row['plan_type_videos_count']== 10){ echo "selected"; } ?> value="10">10</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Review control</td>
                                <td>
                                    <div class="form-group">
                                        <select  id="plan_type_ratings" name="plan_type_ratings" class="form-control">
                                            <option <?php if ($row['plan_type_ratings'] == 1) {
                                                echo "selected";
                                            } ?> value="1">Yes</option>
                                            <option <?php if ($row['plan_type_ratings'] == 0) {
                                                echo "selected";
                                            } ?> value="0">No</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>Social media share</td>
                                <td>
                                    <div class="form-group">
                                        <select id="plan_type_social" name="plan_type_social" class="form-control">
                                            <option <?php if ($row['plan_type_social'] == 1) {
                                                echo "selected";
                                            } ?> value="1">Yes</option>
                                            <option <?php if ($row['plan_type_social'] == 0) {
                                                echo "selected";
                                            } ?> value="0">No</option>
                                        </select>
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <button type="submit" name="plan_type_submit" class="db-pro-bot-btn">Submit Changes</button>
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
<script src="../js/jquery-ui.js"></script>
<script src="js/admin-custom.js"></script> <script src="../js/select-opt.js"></script>
</body>

</html>