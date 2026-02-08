<?php
include "header.php";
?>

<?php if ($admin_row['admin_seo_setting_options'] != 1) {
    header("Location: profile.php");
}
?>

<!-- START -->
<section xmlns="http://www.w3.org/1999/html">
    <div class="ad-com pg-com">
        <div class="ad-dash leftpadd">
            <div class="ud-cen">
                <?php
                $category_id = $_GET['row'];
                $row = getCategory($category_id);
                ?>
                <form name="seo_category_form" id="seo_category_form" method="post" action="update_seo_category.php"
                      enctype="multipart/form-data" class="cre-dup-form cre-dup-form-show">
                    <input type="hidden" class="validate" id="category_id" name="category_id"
                           value="<?php echo $row['category_id']; ?>" required="required">
                    <div class="pg-cen">
                        <div class="s-com pg-tit">
                            <h1>Edit category SEO options</h1>
                            <?php include "../page_level_message.php"; ?>
                            <div class="form-group">
                                <input type="text" required="required" class="form-control" value="<?php echo $row['category_name']; ?>"
                                       disabled>
                            </div>
                        </div>
                        <div class="s-com pg-edita">
                            <h6>About this category</h6>
                            <div class="form-group">
                                <textarea class="form-control" id="category_description" name="category_description"
                                          placeholder="Details about the category"><?php echo $row['category_description']; ?></textarea>
                            </div>
                        </div>
                        <div class="s-com pg-cen-tab pg-seo">
                            <h4>SEO settings</h4>
                            <div class="inn">
                                <div class="form-group">
                                    <label>Page title</label>
                                    <input type="text" name="category_seo_title" value="<?php echo $row['category_seo_title']; ?>"  class="form-control">
                                </div>
                                <div class="form-group">
                                    <label>Page keywords</label>
                                    <input type="text" name="category_seo_keywords" value="<?php echo $row['category_seo_keywords']; ?>"  class="form-control">
                                </div>
                                <div class="form-group">
                                    <label>Page descriptions</label>
                                    <input type="text" name="category_seo_description" value="<?php echo $row['category_seo_description']; ?>"  class="form-control">
                                </div>
                            </div>
                        </div>
                        <div class="s-com pg-cen-tab pg-adv-seo">
                            <h4>FAQ</h4>
                            <div class="inn">
                                <ul class="nav nav-tabs" role="tablist">
                                    <li class="nav-item"><a class="nav-link active" data-toggle="tab" href="#faq1">FAQ
                                            1</a></li>
                                    <li class="nav-item"><a class="nav-link" data-toggle="tab" href="#faq2">FAQ 2</a>
                                    </li>
                                    <li class="nav-item"><a class="nav-link" data-toggle="tab" href="#faq3">FAQ 3</a>
                                    </li>
                                    <li class="nav-item"><a class="nav-link" data-toggle="tab" href="#faq4">FAQ 4</a>
                                    </li>
                                    <li class="nav-item"><a class="nav-link" data-toggle="tab" href="#faq5">FAQ 5</a>
                                    </li>
                                    <li class="nav-item"><a class="nav-link" data-toggle="tab" href="#faq6">FAQ 6</a>
                                    </li>
                                    <li class="nav-item"><a class="nav-link" data-toggle="tab" href="#faq7">FAQ 7</a>
                                    </li>
                                    <li class="nav-item"><a class="nav-link" data-toggle="tab" href="#faq8">FAQ 8</a>
                                    </li>
                                </ul>
                                <div class="tab-content">
                                    <!--- FAQ START --->
                                    <div id="faq1" class="tab-pane fade in active show">
                                        <div class="form-group">
                                            <label>Faq 1</label>
                                            <input type="text" name="category_faq_1_ques" value="<?php echo $row['category_faq_1_ques']; ?>" class="form-control"
                                                   placeholder="Question"><br>
                                            <textarea class="form-control" name="category_faq_1_ans" placeholder="answer"><?php echo $row['category_faq_1_ans']; ?></textarea>
                                        </div>
                                    </div>
                                    <!--- FAQ END --->
                                    <!--- FAQ START --->
                                    <div id="faq2" class="tab-pane fade">
                                        <div class="form-group">
                                            <label>Faq 2</label>
                                            <input type="text" name="category_faq_2_ques" value="<?php echo $row['category_faq_2_ques']; ?>" class="form-control"
                                                   placeholder="Question"><br>
                                            <textarea class="form-control" name="category_faq_2_ans" placeholder="answer"><?php echo $row['category_faq_2_ans']; ?></textarea>
                                        </div>
                                    </div>
                                    <!--- FAQ END --->
                                    <!--- FAQ START --->
                                    <div id="faq3" class="tab-pane fade">
                                        <div class="form-group">
                                            <label>Faq 3</label>
                                            <input type="text" name="category_faq_3_ques" value="<?php echo $row['category_faq_3_ques']; ?>" class="form-control"
                                                   placeholder="Question"><br>
                                            <textarea class="form-control" name="category_faq_3_ans" placeholder="answer"><?php echo $row['category_faq_3_ans']; ?></textarea>
                                        </div>
                                    </div>
                                    <!--- FAQ END --->
                                    <!--- FAQ START --->
                                    <div id="faq4" class="tab-pane fade">
                                        <div class="form-group">
                                            <label>Faq 4</label>
                                            <input type="text" name="category_faq_4_ques" value="<?php echo $row['category_faq_4_ques']; ?>" class="form-control"
                                                   placeholder="Question"><br>
                                            <textarea class="form-control" name="category_faq_4_ans" placeholder="answer"><?php echo $row['category_faq_4_ans']; ?></textarea>
                                        </div>
                                    </div>
                                    <!--- FAQ END --->
                                    <!--- FAQ START --->
                                    <div id="faq5" class="tab-pane fade">
                                        <div class="form-group">
                                            <label>Faq 5</label>
                                            <input type="text" name="category_faq_5_ques" value="<?php echo $row['category_faq_5_ques']; ?>" class="form-control"
                                                   placeholder="Question"><br>
                                            <textarea class="form-control" name="category_faq_5_ans" placeholder="answer"><?php echo $row['category_faq_5_ans']; ?></textarea>
                                        </div>
                                    </div>
                                    <!--- FAQ END --->
                                    <!--- FAQ START --->
                                    <div id="faq6" class="tab-pane fade">
                                        <div class="form-group">
                                            <label>Faq 6</label>
                                            <input type="text" name="category_faq_6_ques" value="<?php echo $row['category_faq_6_ques']; ?>" class="form-control"
                                                   placeholder="Question"><br>
                                            <textarea class="form-control" name="category_faq_6_ans" placeholder="answer"><?php echo $row['category_faq_6_ans']; ?></textarea>
                                        </div>
                                    </div>
                                    <!--- FAQ END --->
                                    <!--- FAQ START --->
                                    <div id="faq7" class="tab-pane fade">
                                        <div class="form-group">
                                            <label>Faq 7</label>
                                            <input type="text" name="category_faq_7_ques" value="<?php echo $row['category_faq_7_ques']; ?>" class="form-control"
                                                   placeholder="Question"><br>
                                            <textarea class="form-control" name="category_faq_7_ans" placeholder="answer"><?php echo $row['category_faq_7_ans']; ?></textarea>
                                        </div>
                                    </div>
                                    <!--- FAQ END --->
                                    <!--- FAQ START --->
                                    <div id="faq8" class="tab-pane fade">
                                        <div class="form-group">
                                            <label>Faq 8</label>
                                            <input type="text" name="category_faq_8_ques" value="<?php echo $row['category_faq_8_ques']; ?>" class="form-control"
                                                   placeholder="Question"><br>
                                            <textarea class="form-control" name="category_faq_8_ans" placeholder="answer"><?php echo $row['category_faq_8_ans']; ?></textarea>
                                        </div>
                                    </div>
                                    <!--- FAQ END --->
                                </div>
                            </div>
                        </div>
                        <div class="s-com pg-cen-tab pg-adv-seo">
                            <h4>Advance SEO settings</h4>
                            <div class="inn">
                                <div class="form-group">
                                    <label>Google schema</label>
                                    <textarea name="category_google_schema" class="form-control"><?php echo $row['category_google_schema']; ?></textarea>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="pg-rhs">
                        <div class="box pub">
                            <h3>Publish</h3>
                            <div class="inn">
                                <ul>
                                    <li>
                                        <button type="submit" name="seo-submit" class="btn-pub">Save changes</button>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </form>

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
<script src="../js/select-opt.js"></script>
<script src="js/admin-custom.js"></script>
<script src="../js/select-opt.js"></script>
<script src="ckeditor/ckeditor.js"></script>
<script>
    CKEDITOR.replace('category_description');
</script>
</body>

</html>