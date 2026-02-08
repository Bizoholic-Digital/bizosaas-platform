<?php
include "header.php";
?>

<?php if($admin_row['admin_seo_setting_options'] != 1){
    header("Location: profile.php");
}
?>

<!-- START -->
<section>
    <div class="ad-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <div class="log-bor">&nbsp;</div>
                <span class="udb-inst">Pages</span>
                <div class="ud-cen-s2">
                    <h2>Meta details</h2>
                    <?php include "../page_level_message.php"; ?>
                    <div class="ad-int-sear">
                        <input type="text" id="pg-sear" placeholder="Search this page..">
                    </div>
                    <table class="responsive-table bordered" id="pg-resu">
                        <thead>
                        <tr>
                            <th>No</th>
                            <th>Page</th>
                            <th>Last edit</th>
                            <th>Edit</th>
                            <th>Preview</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php
                        $si = 1;
                        foreach (getAllSeo() as $row) {

                            if($row['seo_page_name'] == 'Home Page'){
                                $url = '';
                            }elseif($row['seo_page_name'] == 'All Services'){
                                $url = 'all-category';
                            }elseif($row['seo_page_name'] == 'All Events'){
                                $url = 'events';
                            }elseif($row['seo_page_name'] == 'All Products'){
                                $url = 'all-products';
                            }elseif($row['seo_page_name'] == 'All Blog Posts'){
                                $url = 'blog-posts';
                            }elseif($row['seo_page_name'] == 'All Jobs'){
                                $url = 'all-jobs/';
                            }elseif($row['seo_page_name'] == 'All Service Experts'){
                                $url = 'all-service-experts/';
                            }elseif($row['seo_page_name'] == 'Community'){
                                $url = 'community';
                            }elseif($row['seo_page_name'] == 'Pricing Details'){
                                $url = 'pricing-details';
                            }elseif($row['seo_page_name'] == 'Sign In'){
                                $url = 'login';
                            }elseif($row['seo_page_name'] == 'About Us'){
                                $url = 'about';
                            }elseif($row['seo_page_name'] == 'FAQ'){
                                $url = 'faq';
                            }elseif($row['seo_page_name'] == 'Feedback'){
                                $url = 'feedback';
                            }elseif($row['seo_page_name'] == 'Contact Us'){
                                $url = 'contact-us';
                            }

                            ?>
                            <tr>
                                <td><?php echo $si; ?></td>
                                <td><?php echo $row['seo_page_name']; ?></td>
                                <td><?php echo dateFormatconverter($row['seo_page_edit_cdt']); ?></td>
                                <td><a href="seo-meta-tags-edit.php?row=<?php echo $row['seo_page_id']; ?>" class="db-list-edit">Edit</a></td>
                                <td><a href="<?php echo $webpage_full_link.$url; ?>" class="db-list-edit" target="_blank">Preview</a>
                                </td>
                            </tr>
                            <?php
                            $si++;
                        }
                        ?>
                        </tbody>
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