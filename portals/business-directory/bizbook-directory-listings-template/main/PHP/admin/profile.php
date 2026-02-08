<?php
include "header.php";
?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash adda-oly leftpadd">

            <!--            User Welcome Div starts -->

            <div class="ad-dash-s1">
                <div class="cd-cen-intr-inn">
                    <h2>Hi Welcome <b><?php echo $admin_row['admin_name']; ?></b></h2>
                    <p>Stay up to date reports in your listing, products, events and blog reports here</p>
                </div>
            </div>

            <!--            User Welcome Div ends -->

            <div class="ad-dash-s2">
                <ul>
                    <li>
                        <div>
                            <img src="../images/icon/ic-1.png" alt="">
                            <h2 class="count1"><?php echo AddingZero_BeforeNumber(getCountUser()); ?></h2>
                            <h4>All Users</h4>
                            <a href="admin-all-users.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div>
                            <img src="../images/icon/shop.png" alt="">
                            <h2 class="count1"><?php echo AddingZero_BeforeNumber(getCountListing()); ?></h2>
                            <h4>All Listing</h4>
                            <a href="admin-all-listings.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div>
                            <img src="../images/icon/calendar.png" alt="">
                            <h2 class="count1"><?php echo AddingZero_BeforeNumber(getCountEvent()); ?></h2>
                            <h4>All Events</h4>
                            <a href="admin-event.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div>
                            <img src="../images/icon/cart.png" alt="">
                            <h2 class="count1"><?php echo AddingZero_BeforeNumber(getCountProduct()); ?></h2>
                            <h4>All Products</h4>
                            <a href="admin-all-products.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div>
                            <img src="../images/icon/blog1.png" alt="">
                            <h2 class="count1"><?php echo AddingZero_BeforeNumber(getCountBlog()); ?></h2>
                            <h4>All Blog Posts</h4>
                            <a href="admin-all-blogs.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div>
                            <img src="../images/icon/expert.png" alt="">
                            <h2 class="count1"><?php echo AddingZero_BeforeNumber(getCountAllExperts()); ?></h2>
                            <h4>Service Experts</h4>
                            <a href="expert-users.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div>
                            <img src="../images/icon/employee.png" alt="">
                            <h2 class="count1"><?php echo AddingZero_BeforeNumber(getCountJob()); ?></h2>
                            <h4>Job posts</h4>
                            <a href="job-all.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div>
                            <img src="../images/icon/coupons.png" alt="">
                            <h2 class="count1"><?php echo AddingZero_BeforeNumber(getCountCoupon()); ?></h2>
                            <h4>Coupon & Deals</h4>
                            <a href="admin-coupons.php" class="fclick"></a>
                        </div>
                    </li>
                </ul>
            </div>

            <div class="ad-dash-s4">
                <ul>
                    <li>
                        <div class="cor-1">
                            <h4>New Users</h4>
                            <h2>User requests</h2>
                            <span><?php echo AddingZero_BeforeNumber(getCountInactiveUser()); ?></span>
                            <p>This count for today how many get quote and enquiry you got it.</p>
                            <a href="admin-new-user-requests.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div class="cor-2">
                            <h4>Leads</h4>
                            <h2>Leads & Enquiry</h2>
                            <span><?php echo AddingZero_BeforeNumber(getCountEnquiries()); ?></span>
                            <p>This count for last month get quote and enquiry you got it.</p>
                            <a href="admin-all-enquiry.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div class="cor-3">
                            <h4>Enquiry</h4>
                            <h2>Ad Request</h2>
                            <span><?php echo AddingZero_BeforeNumber(getCountAds()); ?></span>
                            <p>This count for total get quote and enquiry leads you got it till to end.</p>
                            <a href="admin-ads-request.php" class="fclick"></a>
                        </div>
                    </li>
                </ul>
            </div>
            
            <!-- EARNING CHART -->
            <div class="das-com das-chart-pay">
                <div class="chartin">
                    <div class="chart-tit">
                        <div class="lhs">
                            <h4><b>Earnings</b> last 30 days </h4>
                        </div>
                        <div class="rhs">
                            <ul>
                                <?php
                                $all_total_payment_sum_row = getSumTransaction();
                                $all_total_payment_sum = $all_total_payment_sum_row['total']; // All Total Amount

                                $all_30_payment_sum_row = getSumTransactionlast30days();
                                $all_30_payment_sum = $all_30_payment_sum_row['total']; // Last 30 Days Amount
                                ?>
                                <li><span>Total earning: <b>$<?php echo AddingZero_BeforeNumber($all_total_payment_sum); ?></b></span></li>
                                <li><span>Last 30 days earning: <b>$<?php echo AddingZero_BeforeNumber($all_30_payment_sum); ?></b></span></li>
                            </ul>
                        </div>
                    </div>
                    <canvas id="Chart_payments"></canvas>
                </div>
            </div>
            <!-- END EARNING CHART -->


            <div class="ad-dash-s3">
                <ul>
                    <li>
                        <div class="ad-cou">
                            <div>
                                <span><?php echo $name[3]['name']; ?> Users</span>
                                <h4><?php echo AddingZero_BeforeNumber(getCountServiceUser(4)); ?></h4>
                            </div>
                            <div>
                                <img src="../images/icon/ic-9.png" alt="">
                            </div>
                            <a href="admin-premium-plus-users.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div class="ad-cou">
                            <div>
                                <span><?php echo $name[2]['name']; ?> Users</span>
                                <h4><?php echo AddingZero_BeforeNumber(getCountServiceUser(3)); ?></h4>
                            </div>
                            <div>
                                <img src="../images/icon/ic-8.png" alt="">
                            </div>
                            <a href="admin-premium-users.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div class="ad-cou">
                            <div>
                                <span><?php echo $name[1]['name']; ?> Users</span>
                                <h4><?php echo AddingZero_BeforeNumber(getCountServiceUser(2)); ?></h4>
                            </div>
                            <div>
                                <img src="../images/icon/ic-10.png" alt="">
                            </div>
                            <a href="admin-standard-users.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div class="ad-cou">
                            <div>
                                <span><?php echo $name[0]['name']; ?> Users</span>
                                <h4><?php echo AddingZero_BeforeNumber(getCountServiceUser(1)); ?></h4>
                            </div>
                            <div>
                                <img src="../images/icon/ic-11.png" alt="">
                            </div>
                            <a href="admin-free-users.php" class="fclick"></a>
                        </div>
                    </li>
                </ul>
            </div>

            
            
            <!-- COUNT & LEAD CHART -->
            <div class="das-com das-chart-user">
                <div class="lhs chartin char-lhs">
                    <div class="chart-tit">
                        <div class="lhs">
                            <h4><b>Registered users</b></h4>
                        </div>
                        <div class="rhs">
                            <ul>
                                <li><span>All users: <b><?php echo AddingZero_BeforeNumber(getCountUser()); ?></b></span></li>
                                <li><span>Last 30 days: <b><?php echo AddingZero_BeforeNumber(getCountUserlast30days()); ?></b></span></li>
                            </ul>
                        </div>
                    </div>
                    <canvas id="Chart_users"></canvas>
                </div>
                <div class="rhs chartin char-rhs">
                    <div class="chart-tit">
                        <div class="lhs">
                            <h4><b>Leads & enquiry</b></h4>
                        </div>
                        <div class="rhs">
                            <ul>
                                <li><span>All leads: <b><?php echo AddingZero_BeforeNumber(getCountEnquiries()); ?></b></span></li>
                                <li><span>Last 30 days: <b><?php echo AddingZero_BeforeNumber(getCountEnquirieslast30days()); ?></b></span></li>
                            </ul>
                        </div>
                    </div>
                    <canvas id="Chart_leads"></canvas>
                </div>
            </div>

            <div class="ad-dash-s3 ad-dash-s5">
                <ul>
                    <li>
                        <div class="ad-cou">
                            <div>
                                <img src="../images/icon/ic-14.png" alt="">
                            </div>
                            <div>
                                <span>Category</span>
                                <h4><?php echo AddingZero_BeforeNumber(getCountCategory()); ?></h4>
                            </div>
                            <a href="admin-all-category.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div class="ad-cou">
                            <div>
                                <img src="../images/icon/ic-12.png" alt="">
                            </div>
                            <div>
                                <span>Sub Category</span>
                                <h4><?php echo AddingZero_BeforeNumber(getSubCountCategory()); ?></h4>
                            </div>
                            <a href="admin-all-category.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div class="ad-cou">
                            <div>
                                <img src="../images/icon/ic-13.png" alt="">
                            </div>
                            <div>
                                <span>Cities</span>
                                <h4><?php echo AddingZero_BeforeNumber(getCountCity()); ?></h4>
                            </div>
                            <a href="admin-all-city.php" class="fclick"></a>
                        </div>
                    </li>
                    <li>
                        <div class="ad-cou">
                            <div>
                                <img src="../images/icon/ic-15.png" alt="">
                            </div>
                            <div>
                                <span>Notifications Send</span>
                                <h4><?php echo AddingZero_BeforeNumber(getCountNotification()); ?></h4>
                            </div>
                            <a href="admin-notification-all.php" class="fclick"></a>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</section>

<!-- END -->

<!-- END -->

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="../js/jquery.min.js"></script>
<script src="../js/popper.min.js"></script>
<script src="../js/bootstrap.min.js"></script>
<script src="../js/jquery-ui.js"></script>
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
<?php httpPost("http://directoryfinder.net/updation/updation_wizard.php", $data_array); ?>
<script src="js/Chart.js"></script>

<script>
    //CHART PAYMENT

    //Function to get transaction table to get chart X values and point values starts

    <?php
    // Organise the array by date
    $dates = [];
    $total1 = [];
    $date1 = [];

    foreach (getAllSumTransactionLast(30) as $day) {
        $dates[$day['Dates']] = $day['count'];

    }

    // Loop through the last 30 days and match each iteration with the data
    $d = new DateTime();
    for ($i = 0; $i < 30; $i++) {

        $date = $d->format('d/m/Y');

        // If there's no data for the specified date, use zero
        $total = isset($dates[$date]) ? $dates[$date] : 0;

        //echo '<p>' . $total . ' on ' . $date . '</p>';
        $total1[] = $total;
        $date = $d->format('j');
        $date1[] = $date;
        $d->modify('-1 day');

    }
    $result = implode(",", array_reverse($total1));
    $date_result = implode(",", array_reverse($date1));
    ?>

    //Function to get transaction table to get chart X values and point values ends

    var xValues = [<?php echo $date_result; ?>];
    var yValues = [<?php echo $result; ?>];

    new Chart("Chart_payments", {
        type: "line",
        data: {
            labels: xValues,
            datasets: [{
                fill: false,
                lineTension: 0,
                backgroundColor: "#02b842",
                borderColor: "#65fc9a",
                data: yValues
            }]
        },
        options: {
            responsive: true,
            legend: {display: false},
            scales: {
                yAxes: [{ticks: {min: 0, max: 10000}}]
            }
        }
    });

    //CHART users

    //Function to get user table to get chart X values and point values starts

    <?php
    // Organise the array by date
    $dates = [];
    $total1 = [];
    $date1 = [];

    foreach (getAllCountUserLast(30) as $day) {
        $dates[$day['Dates']] = $day['count'];

    }

    // Loop through the last 30 days and match each iteration with the data
    $d = new DateTime();
    for ($i = 0; $i < 30; $i++) {

        $date = $d->format('d/m/Y');

        // If there's no data for the specified date, use zero
        $total = isset($dates[$date]) ? $dates[$date] : 0;

        //echo '<p>' . $total . ' on ' . $date . '</p>';
        $total1[] = $total;
        $date = $d->format('j');
        $date1[] = $date;
        $d->modify('-1 day');

    }
    $result = implode(",", array_reverse($total1));
    $date_result = implode(",", array_reverse($date1));
    ?>

    //Function to get user table to get chart X values and point values ends

    var xValues = [<?php echo $date_result; ?>];
    var yValues = [<?php echo $result; ?>];

    new Chart("Chart_users", {
        type: "line",
        data: {
            labels: xValues,
            datasets: [{
                fill: false,
                lineTension: 0,
                backgroundColor: "#fe386f",
                borderColor: "#ffc6d6",
                data: yValues
            }]
        },
        options: {
            responsive: true,
            legend: {display: false},
            scales: {
                yAxes: [{ticks: {min: 0, max: 25}}]
            }
        }
    });

    //CHART LEADS

    //Function to get enquiry table to get chart X values and point values starts

    <?php
    // Organise the array by date
    $dates = [];
    $total1 = [];
    $date1 = [];

    foreach (getAllCountEnquiriesLast(30) as $day) {
        $dates[$day['Dates']] = $day['count'];

    }

    // Loop through the last 30 days and match each iteration with the data
    $d = new DateTime();
    for ($i = 0; $i < 30; $i++) {

        $date = $d->format('d/m/Y');

        // If there's no data for the specified date, use zero
        $total = isset($dates[$date]) ? $dates[$date] : 0;

        //echo '<p>' . $total . ' on ' . $date . '</p>';
        $total1[] = $total;
        $date = $d->format('j');
        $date1[] = $date;
        $d->modify('-1 day');

    }
    $result = implode(",", array_reverse($total1));
    $date_result = implode(",", array_reverse($date1));
    ?>

    //Function to get enquiry table to get chart X values and point values ends

    var xValues = [<?php echo $date_result; ?>];
    var yValues = [<?php echo $result; ?>];

    new Chart("Chart_leads", {
        type: "line",
        data: {
            labels: xValues,
            datasets: [{
                fill: false,
                lineTension: 0,
                backgroundColor: "#f1bb51",
                borderColor: "#fae9c8",
                data: yValues
            }]
        },
        options: {
            responsive: true,
            legend: {display: false},
            scales: {
                yAxes: [{ticks: {min: 0, max: 100}}]
            }
        }
    });
</script>

</body>

</html>