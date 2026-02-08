<?php
include "header.php";
?>
<style>
@import "https://fonts.googleapis.com/css2?family=Poppins:wght@500;700&display=swap";
    .hom-head .container{display: none;}   
.hm3-auto-ban:before{background: linear-gradient(to right,#563502d6,#00000024);}
.hom-top{transition:all .5s ease;background: #000;box-shadow: none}
.hom-head{background:none !important;padding: 0px;margin: 0px;}
    .hom-head .hom-top .container{display: block;}
.dmact .top-ser{display:block}
.hm3-auto-ban{background: url(images/home6.jpg) no-repeat;background-size: 100%;background-position: center right;padding-top:55px;}
.h2-ban-ql{display:table}
    .hm3-auto-ban .lhs h1{font-size: 50px;}
.hm3-auto-ban .rhs .hom-col-req .log-bor{display: block;}
.caro-home{margin-top:90px;float:left;width:100%}
.carousel-item:before{background:none}
.ban-tit h1{font-family:'Poppins',sans-serif;font-weight:500;color:#fff;text-shadow:none}
.ban-tit h1 b{font-family:'Poppins',sans-serif;font-weight:700;font-size: 42px;line-height: 49px;padding-bottom:15px;color:#fff;text-shadow:none}
.h2-ban-ql ul li div{border:1px solid #d9d9da;background:#fff}
.h2-ban-ql ul li div h5{font-family:'Poppins',sans-serif;font-weight:500;color:#383942}
.h2-ban-ql ul li div h5 span{font-weight:700}
.home-tit h2{font-weight:400;font-family:'Poppins',sans-serif}
.home-tit h2 span{font-family:'Poppins',sans-serif;font-weight:700}
.h2-ban-ql ul li div:hover{background:#d3f0fb;box-shadow:0 14px 22px -13px #0b1017ba}
.land-pack-grid-text{position:relative;-webkit-transition:all .5s ease;-moz-transition:all .5s ease;-o-transition:all .5s ease;transition:all .5s ease;position:absolute;top:0;bottom:0;left:0;right:0;width:100%;height:100%;z-index:2;background:linear-gradient(to top,#000000c7,#00000008)}
.land-pack-grid-text h4{padding:15px;font-size:20px;font-weight:400;text-align:center;bottom:0;position:absolute;width:100%;text-align:center;color:#fff}
.land-pack-grid-text h4 .dir-ho-cat{color:#f6f7f9;font-size:11px;position:relative;width:100%;display:inline-block}
.land-pack-grid-img{background:#333}
.home-tit{margin-bottom:20px;padding-top:60px}
.hom2-hom-ban{float:left;width:46%;background-size:cover;margin:0 2%;background:#e6f6fb;padding:30px 100px 30px 30px;border-radius:5px;position:relative;font-family:'Poppins',sans-serif}
.hom2-hom-ban:hover a{background:#d6c607}
.hom2-hom-ban h2{font-family:'Poppins',sans-serif;font-weight:600;font-size:25px;padding-bottom:5px}
.hom2-hom-ban p{font-size:14px}
.hom2-hom-ban a{background:#21d78d;color:#fff;padding:10px 20px;border-radius:5px;display:inline-block;cursor:pointer;font-size:13px;font-weight:400}
.hom2-hom-ban p,.hom2-hom-ban h2,.hom2-hom-ban a{position:relative;color:#fff}
.hom2-hom-ban:before{content:'';position:absolute;width:100%;height:100%;left:0;top:0;right:0;bottom:0;z-index:0;opacity:.8;background:#24C6DC;border-radius:5px}
.hom2-hom-ban1:before{background-image:linear-gradient(140deg,#0c7ada 0%,#0761af 50%,#0f243e94 75%)}
.hom2-hom-ban2:before{background-image:linear-gradient(140deg,#768404 0%,#768404 50%,#0f243e94 75%)}
.hom2-hom-ban1{background-image:url(images/home2-hand.jpg)}
.hom2-hom-ban2{background-image:url(images/home2-work.jpg)}
.hom2-hom-ban-main{float:left;width:100%;padding-bottom:70px}
.hom2-cus-sli{float:left;width:100%}
.hom2-cus-sli ul li{float:left;width:25%;padding:12px 15px}
.testmo{width:100%;background:#fff;box-shadow:0 1px 7px -3px #161d2926;border-radius:5px;padding:30px;position:relative}
.testmo img{width:64px;height:64px;border-radius:50px;object-fit:cover;margin:-80px 0 0}
.testmo h4{font-size:14px;font-weight:600;margin-bottom:2px;font-family:'Poppins',sans-serif}
.testmo span{font-size:11px;font-weight:400;color:#727688}
.testmo span a{font-weight:500;color:#4caf50;display:block;font-size:12px}
.testmo p{color:#727688;font-size:12px;line-height:20px;margin:0;font-weight:400;height:58px;overflow:hidden;border-top:1px solid #f1eeee;padding-top:15px;margin-top:15px}
.testmo p:before{content:'format_quote';font-size:21px;margin:-25px 0 0;background:#fff}
.hom2-cus{background:#f7f8f9;padding-bottom:70px}
.testmo .rat{padding:2px 2px 2px 10px;display:inline-block;position:absolute;right:30px;top:50px}
.testmo .rat i{color:#FF9800;font-size:13px;width:7px}
.hom2-cus-sli ul{position:relative;overflow:hidden;padding:20px 20px 0}
.slick-arrow{width:50px;height:50px;border-radius:50px;background:#fff;border:1px solid #ededed;color:#ffffff03;position:absolute;z-index:9;top:38%}
.slick-arrow:before{content:'chevron_left';font-size:27px;top:4px;left:9px}
.slick-prev{left:14px}
.slick-next{right:14px}
.slick-next:before{content:'chevron_right';font-size:27px}
    .hom4-prop-box{    padding: 0px;
    background: #ffffff;
    box-shadow: 0 1px 14px -4px #161d2926;
    border: 1px solid #efefef;}
    .hom4-prop-box img{    width: 100%;
    border-radius: 2px;
    margin: 0px;
    height: 120px;}
    .hom4-prop-box h4 a{}
    .hom4-prop-box div{padding: 25px;}
    .hom4-prop-box .fclick{}
    .hom4-prop-box .rat{    position: relative;
    top: initial;
    right: initial;
    padding: 2px 2px 2px 0px;
    display: block;
    margin: 0px;
    height: 17px;
    left: -2px;}
    .hom4-fea{background: #fff;padding-bottom: 40px;}
    .hom4-fea .hom2-cus-sli ul li{padding: 12px 20px;}
    .hom4-fea .home-tit{margin-bottom: 0px;padding-top: 70px;}
@media screen and (max-width:992px) {
}
@media screen and (max-width:767px) {
.hm3-auto-ban .lhs h1 {
    font-size: 30px;
    line-height: 32px;
}    
}
@media screen and (max-width:550px) {
}
</style>


<!-- START -->
<section>
    <div class="str hm3-auto-ban">
        <div class="container">
            <div class="row">
                <div class="lhs">
                    <span>#1 Salon And Spa Treatment</span>
                    <h1>Find your right<br><b id="">Spa and Salon</b> now</h1>
                    <p>We help you to find the best Salon, Spa Treatment & Thai Massage Near You.</p>
                    <a href="all-category">Explore all Services</a>
                </div>
                <div class="rhs">
                    <div class="hom-col-req">
                        <div class="log-bor">&nbsp;</div>
                        <span class="udb-inst">Fill the form</span>
                        <h4><?php echo $BIZBOOK['HOM-WHT-LOOK-TIT']; ?></h4>
                        <div id="home_enq_success" class="log"
                             style="display: none;">
                            <p><?php echo $BIZBOOK['ENQUIRY_SUCCESSFUL_MESSAGE']; ?></p>
                        </div>
                        <div id="home_enq_fail" class="log" style="display: none;">
                            <p><?php echo $BIZBOOK['OOPS_SOMETHING_WENT_WRONG']; ?></p>
                        </div>
                        <div id="home_enq_same" class="log" style="display: none;">
                            <p><?php echo $BIZBOOK['ENQUIRY_OWN_LISTING_MESSAGE']; ?></p>
                        </div>
                        <form name="home_enquiry_form" id="home_enquiry_form" method="post"
                              enctype="multipart/form-data">
                            <input type="hidden" class="form-control" name="listing_id" value="0" placeholder="" required>
                            <input type="hidden" class="form-control" name="listing_user_id" value="0" placeholder="" required>
                            <input type="hidden" class="form-control" name="enquiry_sender_id" value="" placeholder="" required>
                            <input type="hidden" class="form-control"
                                   name="enquiry_source"
                                   value="<?php if (isset($_GET["src"])) {
                                       echo $_GET["src"];
                                   } else {
                                       echo "Website";
                                   }; ?>" placeholder="" required>
                            <div class="form-group">
                                <input type="text" name="enquiry_name" value="" required="required" class="form-control" placeholder="<?php echo $BIZBOOK['LEAD-NAME-PLACEHOLDER']; ?>">
                            </div>
                            <div class="form-group">
                                <input type="email" class="form-control" placeholder="<?php echo $BIZBOOK['ENTER_EMAIL_STAR']; ?>" required="required" value="" name="enquiry_email" pattern="^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$" title="<?php echo $BIZBOOK['LEAD-INVALID-EMAIL-TITLE']; ?>">
                            </div>
                            <div class="form-group">
                                <input type="text" class="form-control" value="" name="enquiry_mobile"
                                       placeholder="<?php echo $BIZBOOK['LEAD-MOBILE-PLACEHOLDER']; ?>" pattern="[7-9]{1}[0-9]{9}"
                                       title="<?php echo $BIZBOOK['LEAD-INVALID-MOBILE-TITLE']; ?>" required="">
                            </div>
                            <div class="form-group">
                                <select name="enquiry_category" id="enquiry_category" class="form-control">
                                    <option value="">Select Category</option>
                                    <?php
                                    foreach (getAllCategories() as $categories_row) {
                                        ?>
                                        <option
                                            value="<?php echo $categories_row['category_id']; ?>"><?php echo $categories_row['category_name']; ?></option>
                                        <?php
                                    }
                                    ?>
                                </select>
                            </div>
                            <div class="form-group">
                        <textarea class="form-control" rows="3" name="enquiry_message"
                                  placeholder="<?php echo $BIZBOOK['LEAD-MESSAGE-PLACEHOLDER']; ?>"></textarea>
                            </div>
                            <input type="hidden" id="source">
                            <button type="submit" id="home_enquiry_submit" name="home_enquiry_submit"
                                    class="btn btn-primary">
                                <?php echo $BIZBOOK['SUBMIT_REQUIREMENTS']; ?>
                            </button>
                        </form>
                        <div class="log-bor">&nbsp;</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->                

<!-- START -->
<section>
    <div class="str">
        <div class="container">
            <div class="row">
                <!--<div class="home-tit">
                    <h2><span>Top Services</span> Cras nulla nulla, pulvinar sit amet nunc at, lacinia viverra lectus. Fusce imperdiet ullamcorper metus eu fringilla.</h2>
                </div>-->
                <div class="home-tit">
                    <h2><span><?php echo $BIZBOOK['HOM-POP-TIT']; ?></span> <?php echo $BIZBOOK['HOM-POP-TIT1']; ?></h2>
                    <p><?php echo $BIZBOOK['HOM-POP-SUB-TIT']; ?></p>
                </div>
                <div class="land-pack">
                    <ul>
                        <?php
                        foreach (getAllCategories() as $category_sql_row) {
                            ?>
                            <li>
                                <div class="land-pack-grid">
                                    <div class="land-pack-grid-img">
                                        <img src="images/services/<?php echo $category_sql_row['category_image']; ?>" alt="">
                                    </div>
                                    <div class="land-pack-grid-text">
                                        <h4><?php echo $category_sql_row['category_name']; ?> <span class="dir-ho-cat">Listings <?php echo AddingZero_BeforeNumber(getCountCategoryListing($category_sql_row['category_id'])); ?></span></h4>
                                    </div>
                                    <a href="all-listing?category=<?php echo preg_replace('/\s+/', '-', strtolower($category_sql_row['category_name'])); ?>"
                                           class="land-pack-grid-btn">View all listings</a>
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
<!-- END -->


<!-- START -->
<section>
    <div class="str hom2-cus hom4-fea">
        <div class="container">
            <div class="row">
                <div class="home-tit">
                    <h2><span><?php echo $BIZBOOK['HOM-BEST-TIT']; ?></span> <?php echo $BIZBOOK['HOM-BEST-TIT1']; ?>
                    </h2>
                    <p><?php echo $BIZBOOK['HOM-BEST-SUB-TIT']; ?></p>
                </div>
                
                <div class="hom2-cus-sli">
                    <ul class="multiple-items1">
                        <li>
                            <div class="testmo hom4-prop-box">
                                <img src="images/listings/14271pexels-pixabay-207684.jpg" alt="">
                                <div>
                                <h4><a href="#">Claude D Dial</a></h4>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <span>Posted by <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                </div>
                                <a href="#" class="fclick"></a>
                            </div>
                        </li>
                        <li>
                            <div class="testmo hom4-prop-box">
                                <img src="images/listings/24505pexels-photo-2365572.jpeg" alt="">
                                <div>
                                <h4><a href="#">Claude D Dial</a></h4>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <span>Posted by <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                </div>
                                <a href="#" class="fclick"></a>
                            </div>
                        </li>
                        <li>
                            <div class="testmo hom4-prop-box">
                                <img src="images/listings/72048pexels-francesco-ungaro-96444-(1).jpg" alt="">
                                <div>
                                <h4><a href="#">Claude D Dial</a></h4>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <span>Posted by <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                </div>
                                <a href="#" class="fclick"></a>
                            </div>
                        </li>
                        <li>
                            <div class="testmo hom4-prop-box">
                                <img src="images/listings/72048pexels-francesco-ungaro-96444-(1).jpg" alt="">
                                <div>
                                <h4><a href="#">Claude D Dial</a></h4>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <span>Posted by <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                </div>
                                <a href="#" class="fclick"></a>
                            </div>
                        </li>
                        <li>
                            <div class="testmo hom4-prop-box">
                                <img src="images/listings/72048pexels-francesco-ungaro-96444-(1).jpg" alt="">
                                <div>
                                <h4><a href="#">Claude D Dial</a></h4>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <span>Posted by <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                </div>
                                <a href="#" class="fclick"></a>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<!-- START -->
<section>
    <div class="str">
        <div class="container">
            <div class="row">
                <div class="home-tit">
                    <h2><span><?php echo $BIZBOOK['HOM3-OW-TIT']; ?></span></h2>
                    <p><?php echo $BIZBOOK['HOM3-OW-TIT-SUB']; ?></p>
                </div>
                <div class="hom2-hom-ban-main">
                    <div class="hom2-hom-ban hom2-hom-ban1">
                        <h2><?php echo $BIZBOOK['HOM3-OW-LHS-TIT']; ?></h2>
                        <p><?php echo $BIZBOOK['HOM3-OW-LHS-SUB']; ?></p>
                        <a href="pricing-details"><?php echo $BIZBOOK['HOM3-OW-LHS-CTA']; ?></a>
                    </div>
                    <div class="hom2-hom-ban hom2-hom-ban2">
                        <h2><?php echo $BIZBOOK['HOM3-OW-RHS-TIT']; ?></h2>
                        <p><?php echo $BIZBOOK['HOM3-OW-RHS-SUB']; ?></p>
                        <a href="login?login=register"><?php echo $BIZBOOK['HOM3-OW-RHS-CTA']; ?></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<!-- START -->
<section>
    <div class="str hom2-cus">
        <div class="container">
            <div class="row">
                <div class="home-tit">
                    <h2><span>Our user reviews</span></h2>
                    <p><?php echo $BIZBOOK['HOM3-OW-TIT-SUB']; ?></p>
                </div>
                
                <div class="hom2-cus-sli">
                    <ul class="multiple-items">
                        <li>
                            <div class="testmo">
                                <img src="images/user/33654pexels-photo-91227.jpeg" alt="">
                                <h4>Claude D Dial</h4>
                                <span>Written a review to <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <p>Update your business details including services, about, contact details payment options and more.</p>
                            </div>
                        </li>
                        <li>
                            <div class="testmo">
                                <img src="images/user/33654pexels-photo-91227.jpeg" alt="">
                                <h4>Claude D Dial</h4>
                                <span>Written a review to <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <p>Update your business details including services, about, contact details payment options and more.</p>
                            </div>
                        </li>
                        <li>
                            <div class="testmo">
                                <img src="images/user/33654pexels-photo-91227.jpeg" alt="">
                                <h4>Claude D Dial</h4>
                                <span>Written a review to <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <p>Update your business details including services, about, contact details payment options and more.</p>
                            </div>
                        </li>
                        <li>
                            <div class="testmo">
                                <img src="images/user/33654pexels-photo-91227.jpeg" alt="">
                                <h4>Claude D Dial</h4>
                                <span>Written a review to <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <p>Update your business details including services, about, contact details payment options and more.</p>
                            </div>
                        </li>
                        <li>
                            <div class="testmo">
                                <img src="images/user/33654pexels-photo-91227.jpeg" alt="">
                                <h4>Claude D Dial</h4>
                                <span>Written a review to <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <p>Update your business details including services, about, contact details payment options and more.</p>
                            </div>
                        </li>
                        <li>
                            <div class="testmo">
                                <img src="images/user/33654pexels-photo-91227.jpeg" alt="">
                                <h4>Claude D Dial</h4>
                                <span>Written a review to <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <p>Update your business details including services, about, contact details payment options and more.</p>
                            </div>
                        </li>
                        <li>
                            <div class="testmo">
                                <img src="images/user/33654pexels-photo-91227.jpeg" alt="">
                                <h4>Claude D Dial</h4>
                                <span>Written a review to <a href="listing/gill-automobiles-and-services">Gill Automobiles and Services</a></span>
                                <label class="rat">
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star</i>
                                    <i class="material-icons">star_border</i>
                                    <i class="material-icons">star_border</i>
                                </label>
                                <p>Update your business details including services, about, contact details payment options and more.</p>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->




<!-- START -->
<section>
    <div class="str count">
        <div class="container">
            <div class="row">
                
                <div class="how-wrks">
                    <div class="home-tit">
                        <h2><span><?php echo $BIZBOOK['HOM-HOW-TIT']; ?></span></h2>
                        <p><?php echo $BIZBOOK['HOM-HOW-SUB-TIT']; ?></p>
                    </div>
                    <div class="how-wrks-inn">
                        <ul>
                            <li>
                                <div>
                                    <span>1</span>
                                    <img src="images/icon/how1.png" alt="">
                                    <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-1']; ?></h4>
                                    <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-1']; ?></p>
                                </div>
                            </li>
                            <li>
                                <div>
                                    <span>2</span>
                                    <img src="images/icon/how2.png" alt="">
                                    <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-2']; ?></h4>
                                    <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-2']; ?></p>
                                </div>
                            </li>
                            <li>
                                <div>
                                    <span>3</span>
                                    <img src="images/icon/how3.png" alt="">
                                    <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-3']; ?></h4>
                                    <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-3']; ?></p>
                                </div>
                            </li>
                            <li>
                                <div>
                                    <span>4</span>
                                    <img src="images/icon/how4.png" alt="">
                                    <h4><?php echo $BIZBOOK['HOM-HOW-P-TIT-4']; ?></h4>
                                    <p><?php echo $BIZBOOK['HOM-HOW-P-SUB-4']; ?></p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>

                

                <div class="mob-app">
                    <div class="lhs">
                        <img src="images/mobile.png" alt="">
                    </div>
                    <div class="rhs">
                        <h2><?php echo $BIZBOOK['HOM-APP-TIT']; ?><span><?php echo $BIZBOOK['HOM-APP-TIT-SUB']; ?></span></h2>
                        <ul>
                            <li><?php echo $BIZBOOK['HOM-APP-PO-1']; ?></li>
                            <li><?php echo $BIZBOOK['HOM-APP-PO-2']; ?></li>
                            <li><?php echo $BIZBOOK['HOM-APP-PO-3']; ?></li>
                            <li><?php echo $BIZBOOK['HOM-APP-PO-4']; ?></li>
                        </ul>
                        <span><?php echo $BIZBOOK['HOM-APP-SEND']; ?></span>
                        <form>
                            <ul>
                                <li>
                                    <input type="email" placeholder="Enter email id" required></li>
                                <li>
                                    <input type="submit" value="Get App Link"></li>
                            </ul>
                        </form>
                        <a href="#"><img src="images/android.png" alt=""> </a>
                        <a href="#"><img src="images/apple.png" alt=""> </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->


<!-- START -->
<section>
    <div class="hom-ads">
        <div class="container">
            <div class="row">
                <div class="filt-com lhs-ads">
                    <div class="ads-box">
                        <?php
                        $ad_position_id = 1;   //Ad position on home page bottom
                        $get_ad_row = getAds($ad_position_id);
                        $ad_enquiry_photo = $get_ad_row['ad_enquiry_photo'];
                        ?>
                        <a href="<?php echo stripslashes($get_ad_row['ad_link']); ?>">
                            <span>Ad</span>

                            <img src="images/ads/<?php if ($ad_enquiry_photo != NULL || !empty($ad_enquiry_photo)) {
                                echo $ad_enquiry_photo;
                            } else {
                                echo "ads2.jpg";
                            } ?>" alt="">
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
<!-- END -->

<!-- START -->
<div class="ani-quo">
    <div class="ani-q1">
        <h4><?php echo $BIZBOOK['HOM-WHAT-LOOK-TIT']; ?></h4>
        <p><?php echo $BIZBOOK['HOM-WHAT-LOOK-SUB']; ?></p>
        <span><?php echo $BIZBOOK['HOM-WHAT-LOOK-CTA']; ?></span>
    </div>
    <div class="ani-q2">
        <img src="images/quote.png" alt="">
    </div>
</div>
<!-- END -->

<?php
include "footer.php";
?>

<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="js/jquery.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/jquery-ui.js"></script>
<script src="js/custom.js"></script>
<script src="js/jquery.validate.min.js"></script>
<script src="js/custom_validation.js"></script>
<script src="js/slick.js"></script>
<script>
    $(window).scroll(function () {
        var scroll = $(window).scrollTop();
        if (scroll >= 250) {
            $(".hom-top").addClass("dmact");
        }
        else {
            $(".hom-top").removeClass("dmact");
        }
    });
$('.multiple-items, .multiple-items1').slick({
  infinite: true,
  slidesToShow: 4,
  slidesToScroll: 1,
    autoplay: true,
  autoplaySpeed: 3000,
    responsive: [{
        breakpoint: 992,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          centerMode: false,
        }
      }]

});   
(function(){
      var words = [
          'Property',
          'Plots',
          'Villas',
          'Apartment'
          ], i = 0;
      setInterval(function(){
          $('#changingword').fadeOut(function(){
              $(this).html(words[i=(i+1)%words.length]).fadeIn();
          });
      }, 1500);
        
  })();       
</script>
</body>

</html>