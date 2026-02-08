<?php
if ($current_home_page == '4' || $current_home_page == '5' || $current_home_page == '6' || $current_home_page == '7' || $current_home_page == '8' || $current_home_page == '9') {
    ?>
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
                    centerMode: false
                }
            }]

        });
        
        <?php
        if ($current_home_page == '5') {
        ?>
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
        <?php } ?>

    </script>
    <?php
}
    ?>
