/**
 * Created by Vignesh on 10/06/2021.
 */

<!--    Expert Filter Script Starts-->


// $("input[type='checkbox'], input[type='radio']").on( "click", expertFilter() );
// $("select").on( "change", expertFilter() );


$(" .availability_check ,.expert_veri ,.rating_check, .expert_ser_cou").on("click", expertFilter);
$(".cat_check, .city_check").on("change", expertFilter);
$(document).on('change', 'input[type="checkbox"]', expertFilter);
$(document).on('change', 'input[type="radio"]', expertFilter);

function expertFilter() {

    // $(".all-expert-total").css("opacity",0);


    var mainarray = [];

    //To get Category values from All expert page starts

    var cat_check = [];
    $('#cat_check :selected').each(function () {
        // $('input[name="cat_check"]:checked').each(function(){
        cat_check.push($(this).val());
    });

    var cat_checklist = "/" + cat_check;

    //To get Category values from All expert page ends


    //To get Availability values from All expert page starts

    var expert_avail_check = [];
    $('input[name="expert_avail"]:checked').each(function () {
        expert_avail_check.push($(this).val());

    });

    var expert_avail_checklist = "&availability=" + expert_avail_check;

    //To get Availability values from All expert page ends

    //To get expert verified from All expert page starts

    var expert_veri = [];
    $('input[name="expert_veri"]:checked').each(function () {
        expert_veri.push($(this).val());

    });

    var expert_veri_list = "&verified=" + expert_veri;

    //To get expert verified from All expert page ends

    var city_check = [];
    $('#city_check :selected').each(function () {
        city_check.push($(this).val());

    });
    var city_checklist = "&city=" + city_check;


    //To get Rating values from All expert page starts

    var expert_rat = [];
    $('input[name="expert_rat"]:checked').each(function () {
        expert_rat.push($(this).val());
    });
    var expert_ratlist = "&ratings=" + expert_rat;

    //To get Rating values from All expert page ends

    //To get Sort values from All expert page starts

    var expert_ser_cou = [];
    $('input[name="expert_ser_cou"]:checked').each(function () {
        expert_ser_cou.push($(this).val());
    });
    var expert_ser_cou_list = "&sort_by=" + expert_ser_cou;

    //To get Sort values from All expert page ends


    // var main_string = cat_checklist+sub_cat_checklist+expert_typelist+city_checklist+expert_salarylist;
    var main_string = expert_avail_checklist + expert_ratlist + city_checklist + expert_veri_list + expert_ser_cou_list;
    main_string = main_string.substring(1, main_string.length);


    if (webpage_full_link != null) {
        var link = webpage_full_link + 'all-service-experts';
    } else {
        var link = 'all-service-experts';
    }

    window.location.href = link + cat_checklist + '?' + main_string;


    //$.ajax({
    //    type: "POST",
    //    url: link,
    //    data: main_string,
    //    cache: false,
    //    success: function(html){
    //        $(".all-expert-total").html(html);
    //        $(".all-expert-total").css("opacity",1);
    //    }
    //});


}

<!--    expert Page Filter Script Ends-->