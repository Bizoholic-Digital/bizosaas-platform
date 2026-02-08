<?php
if ($current_home_page == '1') {
    ?>
    <style>
        .hom-top {
            transition: all 0.5s ease;
            background: none;
            box-shadow: none;
        }

        .top-ser {
            display: none;
        }

        .dmact .top-ser {
            display: block;
        }

        .caro-home {
            margin-top: 90px;
            float: left;
            width: 100%;
        }

        .carousel-item:before {
            background: none;
        }
    </style>
    <?php
} elseif ($current_home_page == '2') {
    ?>
    <style>
         body{background-color:#e8ecf0}
.hom-head{float:left;width:100%;background:url(images/ex2.jpg) no-repeat;position:relative;padding:170px 0 130px;background-size:100%;background-position:center}
.hom-head:before{content:'';position:absolute;width:100%;height:100%;    background: #00000036;left:0;top:0;right:0;bottom:0}
.news-top-menu{position:absolute;left:0;right:0;top: -3px;z-index:10;background:#616161}
.news-hban-box .im img{height:400px}
.news-menu ul li a{color:#fff;font-size:12px;font-weight:500;border-bottom:2px solid #616161}
.news-menu ul li a.act{border-bottom:2px solid #2d344d;background:#525252}
.news-menu ul li a:hover{border-bottom:2px solid #323232;background:#575757}
.land-pack-grid,.land-pack-grid-img img,.land-pack-grid-text{border-radius:15px}
.hom-top{transition:all .5s ease;background:#000;}
.top-ser,.ban-ql,.mob-app{display:none}
.dmact .top-ser{display:block}
.caro-home{margin-top:90px;float:left;width:100%}
.carousel-item:before{background:none}
.hom-head{margin-bottom:0}
.ban-search{background:none;padding:0;border-radius:50px;padding-bottom:10px;box-shadow: none;}
.ban-search ul li.sr-cit{display:block;width:25%}
.ban-search ul li.sr-sea{width:54%;margin:0 1%}
.ban-search ul li.sr-btn{width:19%}
.ban-search ul li input{border-radius:5px}
.ban-search ul li input[type="submit"]{padding:5px;border-radius:5px;background:#2140d7}
.hom-head:after{display:none}
.ban-tit h1{font-weight:500;color:#fff;text-shadow:none;padding-top: 60px;}
.ban-tit h1 b{padding-bottom:15px;color:#fff;text-shadow:none}
.h2-ban-ql ul li div{border:1px solid #d9d9da;background:#fff}
.h2-ban-ql ul li div h5{font-weight:500;color:#383942}
.h2-ban-ql ul li div h5 span{font-weight:700}
.home-tit h2{font-weight:400}
.home-tit h2 span{font-weight:700}
.h2-ban-ql ul li div:hover{background:#d3f0fb;box-shadow:0 14px 22px -13px #0b1017ba}
.land-pack-grid-text{position:relative;-webkit-transition:all .5s ease;-moz-transition:all .5s ease;-o-transition:all .5s ease;transition:all .5s ease;position:absolute;top:0;bottom:0;left:0;right:0;width:100%;height:100%;z-index:2;background:linear-gradient(to top,#000000c7,#00000008)}
.land-pack-grid-text h4{padding:15px;font-size:16px;font-weight:400;text-align:center;bottom:0;position:absolute;width:100%;text-align:center;color:#fff}
.land-pack-grid-text h4 .dir-ho-cat{color:#f6f7f9;font-size:11px;position:relative;width:100%;display:inline-block}
.land-pack-grid-img{background:#333}
.home-tit{padding-top:60px}
.pri .home-tit{padding-top:0}
.news-hom-ban-sli{margin-bottom:30px}
.pri{padding:25px 0 60px;background:#e8ecf0}
.hom2-hom-ban{float:left;width:46%;background-size:cover;margin:0 2%;background:#e6f6fb;padding:30px 100px 30px 30px;border-radius:5px;position:relative}
.hom2-hom-ban:hover a{background:#d6c607}
.hom2-hom-ban h2{font-weight:600;font-size:25px;padding-bottom:5px}
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
.hom2-cus-sli ul li{float:left;width:25%;padding:12px 20px}
.testmo{width:100%;background:#fff;box-shadow:0 1px 7px -3px #161d2926;border-radius:10px 10px 0 0;padding:30px;position:relative;border-radius:10px}
.testmo img{width:64px;height:64px;border-radius:50px;object-fit:cover;margin:-80px 0 0}
.testmo h4{font-size:14px;font-weight:600;margin-bottom:2px;font-family:'Poppins',sans-serif}
.testmo span{font-size:11px;font-weight:400;color:#727688}
.testmo span a{font-weight:500;color:#4caf50;display:block;font-size:12px}
.testmo p{color:#727688;font-size:12px;line-height:20px;margin:0;font-weight:400;height:58px;overflow:hidden;border-top:1px solid #f1eeee;padding-top:15px;margin-top:15px}
.testmo p:before{content:'format_quote';font-size:21px;margin:-25px 0 0;background:#fff}
.hom2-cus{background:#e8ecf0;padding-bottom:70px}
.testmo .rat{padding:2px 2px 2px 10px;display:inline-block;position:absolute;right:30px;top:52px}
.testmo .rat i{color:#FF9800;font-size:17px;width:12px}
.hom2-cus-sli ul{position:relative;overflow:hidden;padding:20px 20px 0}
.hom2-cus .ban-ql{display:block;margin:0;width:100%;padding-top:15px}
.slick-arrow{width:50px;height:50px;border-radius:50px;background:#fff;border:1px solid #ededed;color:#ffffff03;position:absolute;z-index:9;top:38%}
.slick-arrow:before{content:'chevron_left';font-size:27px;top:4px;left:9px}
.slick-prev{left:14px}
.slick-next{right:14px}
.slick-next:before{content:'chevron_right';font-size:27px}
.hom4-prop-box{padding:0;background:#fff;box-shadow:none}
.hom4-prop-box:before{content:'';position:absolute;width:100%;height:100%;left:0;top:0;right:0;bottom:0;background:#333;background:-webkit-linear-gradient(to top,#00000063,#56ccf247);background:linear-gradient(to top,#00000063,#56ccf247);border-radius:10px}
.hom4-prop-box img{width:100%;border-radius:10px 10px 0 0;margin:0;height:175px}
.hom4-prop-box div{padding:25px;position:relative;background:#fff;border-radius:0 0 10px 10px}
.hom4-prop-box .rat{position:relative;top:initial;right:initial;padding:2px 2px 2px 0;display:block;margin:0;height:17px;left:-2px}
.hom4-fea{padding-bottom:40px}
.hom4-fea .hom2-cus-sli ul li{padding:12px 20px}
.hom4-fea .home-tit{margin-bottom:0;padding-top:70px}
.all-serexp .job-box{padding:20px}
.all-serexp .job-box-con span{color:#f58a04}
.all-serexp .serexp-cta-more:hover{background:#f78919}
.job-box-con{position:relative}
.all-serexp .job-box-con h4{font-size:18px}
.all-serexp .job-box-con h5.cate{font-weight:500;color:#fff;display:inline-block;font-size:11px;padding:4px 60px 4px 12px;position:absolute;left:0;top:-21px;background:#587cff;background:-webkit-linear-gradient(to right,#015fdd,#0000000d);background:linear-gradient(to right,#015fdd,#0000000d)}
.job-box{border:0 solid #f0f0f0;padding:30px;box-shadow:none;border-radius:10px}
.job-box:hover{background:#fff;border:0}
@media screen and (max-width: 992px) {
.hom2-hom-ban{width:100%;margin:20px 0}
}
@media screen and (max-width: 767px) {
.ban-tit h1 b{font-size:32px;line-height:38px}
.ind2-home{padding-top:120px}
.ban-search ul li{width:100%!important;margin:0 0 10px!important}
.ban-tit{padding-bottom:30px}
}
@media screen and (max-width: 550px) {
.hom-head .ban-search ul li{width:100%;margin:0 0 15px}
}  
    </style>
    <?php
} elseif ($current_home_page == '3') {
    ?>
    <style>
        body{background-color:#e8ecf0}
        .hom-head:before{float:left;width:100%;background:url(images/ex2.jpg) no-repeat;position:relative;padding:80px 0 0;background-size:100%;background-position:center}
        .hom-head:before{content:'';position:absolute;width:100%;height:100%;background:#00000036;left:0;top:0;right:0;bottom:0}
        .news-top-menu{position:absolute;left:0;right:0;top: -3px;z-index:10;background:#616161}
        .news-hban-box .im img{height:400px}
        .news-menu ul li a{color:#fff;font-size:12px;font-weight:500;border-bottom:2px solid #616161}
        .news-menu ul li a.act{border-bottom:2px solid #2d344d;background:#434859}
        .news-menu ul li a:hover{border-bottom:2px solid #323232;background:#575757}
        .land-pack-grid, .land-pack-grid-img img, .land-pack-grid-text{border-radius: 15px;}
        .hom-top{transition:all .5s ease;background:#000;}
        .top-ser,.ban-ql, .mob-app{display:none}
        .dmact .top-ser{display:block}
        .caro-home{margin-top:90px;float:left;width:100%}
        .carousel-item:before{background:none}
        .hom-head{padding:140px 0 70px;margin-bottom:0}
        .ban-search{background:none;padding:0;border-radius:50px;padding-bottom: 10px;box-shadow: none;}
        .ban-search ul li.sr-cit{display:block;width:25%}
        .ban-search ul li.sr-sea{width:54%;margin:0 1%}
        .ban-search ul li.sr-btn{width:19%}
        .ban-search ul li input{border-radius:5px}
        .ban-search ul li input[type="submit"]{padding:5px;border-radius:5px;background:#2140d7}
        .hom-head:after{display:none}
        .ban-tit h1{font-weight:500;color:#fff;text-shadow:none;    padding-top: 60px;}
        .ban-tit h1 b{padding-bottom:15px;color:#fff;text-shadow:none}
        .h2-ban-ql ul li div{border:1px solid #d9d9da;background:#fff}
        .h2-ban-ql ul li div h5{font-weight:500;color:#383942}
        .h2-ban-ql ul li div h5 span{font-weight:700}
        .home-tit h2{font-weight:400;}
        .home-tit h2 span{font-weight:700}
        .h2-ban-ql ul li div:hover{background:#d3f0fb;box-shadow:0 14px 22px -13px #0b1017ba}
        .land-pack-grid-text{position:relative;-webkit-transition:all .5s ease;-moz-transition:all .5s ease;-o-transition:all .5s ease;transition:all .5s ease;position:absolute;top:0;bottom:0;left:0;right:0;width:100%;height:100%;z-index:2;background:linear-gradient(to top,#000000c7,#00000008)}
        .land-pack-grid-text h4{padding:15px;font-size:16px;font-weight:400;text-align:center;bottom:0;position:absolute;width:100%;text-align:center;color:#fff}
        .land-pack-grid-text h4 .dir-ho-cat{color:#f6f7f9;font-size:11px;position:relative;width:100%;display:inline-block}
        .land-pack-grid-img{background:#333}
        .home-tit{padding-top:60px}
        .news-hom-ban-sli{margin-bottom: 30px;}
        .pri {padding: 75px 0 60px 0;background: #e8ecf0;}
        .hom2-hom-ban{float:left;width:46%;background-size:cover;margin:0 2%;background:#e6f6fb;padding:30px 100px 30px 30px;border-radius:5px;position:relative;}
        .hom2-hom-ban:hover a{background:#d6c607}
        .hom2-hom-ban h2{font-weight:600;font-size:25px;padding-bottom:5px}
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
        .hom2-cus-sli ul li{float:left;width:25%;padding:12px 20px}
        .testmo{width:100%;background:#fff;box-shadow:0 1px 7px -3px #161d2926;border-radius:5px;padding:30px;position:relative}
        .testmo img{width:64px;height:64px;border-radius:50px;object-fit:cover;margin:-80px 0 0}
        .testmo h4{font-size:14px;font-weight:600;margin-bottom:2px;font-family:'Poppins',sans-serif}
        .testmo span{font-size:11px;font-weight:400;color:#727688}
        .testmo span a{font-weight:500;color:#4caf50;display:block;font-size:12px}
        .testmo p{color:#727688;font-size:12px;line-height:20px;margin:0;font-weight:400;height:58px;overflow:hidden;border-top:1px solid #f1eeee;padding-top:15px;margin-top:15px}
        .testmo p:before{content:'format_quote';font-size:21px;margin:-25px 0 0;background:#fff}
        .hom2-cus{background:#e8ecf0;padding-bottom:70px}
        .testmo .rat{padding:2px 2px 2px 10px;display:inline-block;position:absolute;right:30px;top:52px}
        .testmo .rat i{color:#FF9800;font-size:17px;width:12px}
        .hom2-cus-sli ul{position:relative;overflow:hidden;padding:20px 20px 0}
        .slick-arrow{width:50px;height:50px;border-radius:50px;background:#fff;border:1px solid #ededed;color:#ffffff03;position:absolute;z-index:9;top:38%}
        .slick-arrow:before{content:'chevron_left';font-size:27px;top:4px;left:9px}
        .slick-prev{left:14px}
        .slick-next{right:14px}
        .slick-next:before{content:'chevron_right';font-size:27px}
        .hom4-prop-box{padding:0;background:#fff;box-shadow:0 1px 14px -4px #161d2926;border:1px solid #efefef}
        .hom4-prop-box img{width:100%;border-radius:5px 5px 0 0;margin:0;height:185px}
        .hom4-prop-box div{padding:25px}
        .hom4-prop-box .rat{position:relative;top:initial;right:initial;padding:2px 2px 2px 0;display:block;margin:0;height:17px;left:-2px}
        .hom4-fea{padding-bottom:40px}
        .hom4-fea .hom2-cus-sli ul li{padding:12px 20px}
        .hom4-fea .home-tit{margin-bottom: 0px;padding-top: 70px;}
        @media screen and (max-width:992px) {
            .hom2-hom-ban{width:100%;margin:20px 0}
        }
        @media screen and (max-width:767px) {
            .ban-tit h1 b{font-size:32px;line-height:38px}
            .ind2-home{padding-top: 120px;}
            .ban-search ul li{width:100% !important;margin:0 0 10px 0 !important;}
            .ban-tit{padding-bottom: 30px;}
        }
        @media screen and (max-width:550px) {
            .hom-head .ban-search ul li{width:100%;margin:0 0 15px}
        }
    </style>
    <?php
} elseif($current_home_page == '4') {
    ?>
    <style>
        @import "https://fonts.googleapis.com/css2?family=Poppins:wght@500;700&display=swap";
        .hom-head .container{display: none;}
        .hom-top{transition:all .5s ease;background: #000;box-shadow: none}
        .hom-head{background:none !important;padding: 0px;margin: 0px;}
        .hom-head .hom-top .container{display: block;}
        .dmact .top-ser{display:block}
        .hm3-auto-ban{background: url(images/automobile-bg.jpg) no-repeat;background-size: 100%;background-position: center right;padding-top:55px;}
        .h2-ban-ql{display:table}
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
        .hom2-cus-sli ul li{float:left;width:25%;padding:12px 20px}
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
        .hom4-prop-box{padding:0;background:#fff;box-shadow:0 1px 14px -4px #161d2926;border:1px solid #efefef}
        .hom4-prop-box img{width:100%;border-radius:2px;margin:0;height:120px}
        .hom4-prop-box div{padding:25px}
        .hom4-prop-box .rat{position:relative;top:initial;right:initial;padding:2px 2px 2px 0;display:block;margin:0;height:17px;left:-2px}
        .hom4-fea{background:#fff;padding-bottom:40px}
        .hom4-fea .hom2-cus-sli ul li{padding:12px 20px}
        .hom4-fea .home-tit{margin-bottom: 0px;padding-top: 70px;}
        @media screen and (max-width:992px) {
        }
        @media screen and (max-width:767px) {
        }
        @media screen and (max-width:550px) {
        }
    </style>


    <?php
}elseif($current_home_page == '5') {
    ?>
    <style>
        @import "https://fonts.googleapis.com/css2?family=Poppins:wght@500;700&display=swap";
        .hom-head .container{display: none;}
        .hom-top{transition:all .5s ease;background: #000;box-shadow: none}
        .hom-head{background:none !important;padding: 0px;margin: 0px;}
        .hom-head .hom-top .container{display: block;}
        .dmact .top-ser{display:block}
        .hm3-auto-ban{background: url(images/home4.jpg) no-repeat;background-size: 100%;background-position: center right;padding-top:55px;}
        .h2-ban-ql{display:table}
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
        }
        @media screen and (max-width:550px) {
        }
    </style>


    <?php
}elseif($current_home_page == '6') {
    ?>
    <style>
        @import "https://fonts.googleapis.com/css2?family=Poppins:wght@500;700&display=swap";
        .hom-head .container{display: none;}
        .hom-top{transition:all .5s ease;background: #000;box-shadow: none}
        .hom-head{background:none !important;padding: 0px;margin: 0px;}
        .hom-head .hom-top .container{display: block;}
        .dmact .top-ser{display:block}
        .hm3-auto-ban{background: url(images/home5.jpg) no-repeat;background-size: 100%;background-position: center right;padding-top:55px;}
        .h2-ban-ql{display:table}
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
        }
        @media screen and (max-width:550px) {
        }
    </style>

    <?php
}elseif($current_home_page == '7') {
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
    
    <?php
}elseif($current_home_page == '8') {
    ?>
    <style>
        @import "https://fonts.googleapis.com/css2?family=Poppins:wght@500;700&display=swap";
        .hom-head .container{display: none;}
        .hom-top{transition:all .5s ease;background: #000;box-shadow: none}
        .hom-head{background:none !important;padding: 0px;margin: 0px;}
        .hom-head .hom-top .container{display: block;}
        .dmact .top-ser{display:block}
        .hm3-auto-ban{background: url(images/home7.jpg) no-repeat;background-size: 100%;background-position: center right;padding-top:55px;}
        .h2-ban-ql{display:table}
        .hm3-auto-ban .lhs h1{font-size: 50px;}
        .hm3-auto-ban .rhs .hom-col-req .log-bor{display: block;}
        .caro-home{margin-top:90px;float:left;width:100%}
        .carousel-item:before{background:none}
        .hm3-auto-ban .lhs{padding-top:50px;}
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


    <?php
}elseif($current_home_page == '9') {
    ?>
    <style>
        @import "https://fonts.googleapis.com/css2?family=Poppins:wght@500;700&display=swap";
        .hom-head .container{display: none;}
        .hom-top{transition:all .5s ease;background: #000;box-shadow: none}
        .hom-head{background:none !important;padding: 0px;margin: 0px;}
        .hom-head .hom-top .container{display: block;}
        .dmact .top-ser{display:block}
        .hm3-auto-ban{background: url(images/home8.jpg) no-repeat;background-size: 100%;background-position: center right;padding-top:55px;}
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
    
    <?php
}
?>
