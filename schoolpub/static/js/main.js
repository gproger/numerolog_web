// header fixed
function headerFixed() {
    main_h = $('.intro').outerHeight();
    new_main_h = 0;
    if ($(window).scrollTop() > new_main_h){
        $('.js-header-sticky').addClass('is-fixed');
    } else{
        $('.js-header-sticky').removeClass('is-fixed');
    }
}

$(window).on('scroll', function(){
    headerFixed();
});

$(document).ready(function(){
    // header fixed
    headerFixed();


    // target link
    $('.js-scroll').on('click', function (event){
        event.preventDefault();
        var id2 = $(this).attr('href'),
            top_1_2 = $(id2).offset().top,
            top_2_2 = top_1_2 - 69;
        $('body, html').animate({scrollTop: top_2_2}, 650);
    });


    // close nav
    $('.nav__link').on('click', function (event){
        $('body').removeClass('is-hidden');
        $('.js-mobile-toggle').removeClass('is-active');
        $('.header__nav').removeClass('is-show');
    });


    // toggle mobile
    $('.js-mobile-toggle').click(function(){
        $('body').toggleClass('is-hidden');
        $(this).toggleClass('is-active');
        $('.header__nav').toggleClass('is-show');
    });


    // video play
    $('.js-video-play').click(function(){  
        $(this).addClass('is-hidden');
        $(this).siblings('.video__player').get(0).play();
    });


    // slider SLICK
    $('.js-reviews-slider-init').slick({
        adaptiveHeight: true,
        slidesToShow: 3,
        slidesToScroll: 1,
        dots: true,
        arrows: false,
        speed: 600,
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2
                }
            },
            {
                breakpoint: 421,
                settings: {
                    slidesToShow: 1
                }
            }
        ]
    });
});