<?php
include "header.php";

if (file_exists('config/user_authentication.php')) {
    include('config/user_authentication.php');
}
include "dashboard_left_pane.php";

if (file_exists('config/general_user_authentication.php')) {
    include('config/general_user_authentication.php');
}

if (file_exists('config/blog_page_authentication.php')) {
    include('config/blog_page_authentication.php');
}
?>
    <!--CENTER SECTION-->
    <div class="ud-main">
   <div class="ud-main-inn ud-no-rhs">
    <div class="ud-cen">
        <div class="log-bor">&nbsp;</div>
        <span class="udb-inst"><?php echo $BIZBOOK['BLOG_POSTS']; ?></span>
        <?php include('config/user_activation_checker.php'); ?>
        <div class="ud-cen-s2">
            <h2><?php echo $BIZBOOK['BLOG_DETAILS']; ?></h2>
            <?php include "page_level_message.php"; ?>
            <a href="create-new-blog-post" class="db-tit-btn"><?php echo $BIZBOOK['ADD_NEW_POST']; ?></a>
            <table class="responsive-table bordered">
                <thead>
                <tr>
                    <th><?php echo $BIZBOOK['S_NO']; ?></th>
                    <th><?php echo $BIZBOOK['POST_NAME']; ?></th>
                    <th><?php echo $BIZBOOK['VIEWS']; ?></th>
                    <th><?php echo $BIZBOOK['EDIT']; ?></th>
                    <th><?php echo $BIZBOOK['DELETE']; ?></th>
                    <th><?php echo $BIZBOOK['PREVIEW']; ?></th>
                </tr>
                </thead>
                <tbody>
                <?php
                $si = 1;
                foreach (getAllUserBlogs($_SESSION['user_id']) as $blogrow) {
                    
                    ?>
                    <tr>
                        <td><?php echo $si; ?></td>
                        <td><?php echo $blogrow['blog_name']; ?> <span><?php echo dateFormatconverter($blogrow['blog_cdt']); ?></span></td>
                        <td><span class="db-list-rat"><?php  echo blog_pageview_count($blogrow['blog_id']); ?></span></td>
                        <td><a href="edit-blog-post?code=<?php echo $blogrow['blog_id']; ?>" class="db-list-edit"><?php echo $BIZBOOK['EDIT']; ?></a></td>
                        <td><a href="delete-blog-post?code=<?php echo $blogrow['blog_id']; ?>" class="db-list-edit"><?php echo $BIZBOOK['DELETE']; ?></a></td>
                        <td><a href="<?php echo $BLOG_URL.urlModifier($blogrow['blog_slug']); ?>" class="db-list-edit" target="_blank"><?php echo $BIZBOOK['PREVIEW']; ?></a></td>
                    </tr>
                    <?php
                    $si++;
                }
                ?>

                </tbody>
            </table>
        </div>
    </div>
<?php
include "dashboard_right_pane.php";
?>