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

function r(f){/in/.test(document.readyState)?setTimeout('r('+f+')',9):f()}
r(function(){
    if (!document.getElementsByClassName) {
        // Поддержка IE8
        var getElementsByClassName = function(node, classname) {
            var a = [];
            var re = new RegExp('(^| )'+classname+'( |$)');
            var els = node.getElementsByTagName("*");
            for(var i=0,j=els.length; i < j; i++)
                if(re.test(els[i].className))a.push(els[i]);
            return a;
        }
        var videos = getElementsByClassName(document.body,"youtube");
    } else {
        var videos = document.getElementsByClassName("youtube");
    }
    var nb_videos = videos.length;
    for (var i=0; i < nb_videos; i++) {
        // Находим постер для видео, зная ID нашего видео
        if (videos[i].id.startsWith('http')) {
            videos[i].id = videos[i].id.split('/').slice(-1)[0];
	}
	console.log(videos[i]);
        videos[i].style.backgroundImage = 'url(http://i.ytimg.com/vi/' + videos[i].id + '/sddefault.jpg)';
        // Размещаем над постером кнопку Play, чтобы создать эффект плеера
        var play = document.createElement("div");
        play.setAttribute("class","play");
        videos[i].appendChild(play);
        videos[i].onclick = function() {
            // Создаем iFrame и сразу начинаем проигрывать видео, т.е. атрибут autoplay у видео в значении 1
            var iframe = document.createElement("iframe");
            var iframe_url = "https://www.youtube.com/embed/" + this.id+"?autoplay=1&autohide=1" ;
            if (this.getAttribute("data-params")) iframe_url+='&'+this.getAttribute("data-params");
            iframe.setAttribute("src",iframe_url);
            iframe.setAttribute("frameborder",'0');
            iframe.setAttribute("autoplay",'1');
            iframe.setAttribute("allow",'autoplay;');
            iframe.setAttribute("allowfullscreen",'');
            
            // Высота и ширина iFrame будет как у элемента-родителя
            iframe.style.width  = this.style.width;
            iframe.style.height = this.style.height;
            // Заменяем начальное изображение (постер) на iFrame
            this.parentNode.replaceChild(iframe, this);
        }
    }
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
        infinite: false,
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

    $(".reviews-slider iframe").each(function (idx) {
        $(this).addClass("data-idx-" + idx).data("idx", idx);
    });

    function getPlayer (iframe, onPlayerReady, clonned) {
        var $iframe = $(iframe);
        if ($iframe.data((clonned ? "clonned-" : "") + "player")) {
            var isReady = $iframe.data((clonned ? "clonned-" : "") + "player-ready");
          if (isReady) {
            onPlayerReady && onPlayerReady($iframe.data((clonned ? "clonned-" : "") + "player"));
          }         
            return player;
        }
        else {
            var player = new YT.Player($iframe.get(0), {
            events: {
              'onReady': function () {
                $iframe.data((clonned ? "clonned-" : "") + "player-ready", true);
                onPlayerReady && onPlayerReady(player);
              }
            }
          });        
          $iframe.data((clonned ? "clonned-" : "") + "player", player);
          return player;
        }           
    }

});



function onYouTubeIframeAPIReady(){ // this function is called automatically when Youtube API is loaded (see: https://developers.google.com/youtube/iframe_api_reference)
    var $contentdivs = $('.reviews-slider').find('a.reviews-slider-item__link');
    $contentdivs.each(function(i){ // loop through the content divs
        var $contentdiv = $(this)
        var $youtubeframe = $contentdiv.find('iframe[src*="youtube.com"]:eq(0)') // find Youtube iframe within DIV, if it exists
        console.log($youtubeframe);
        if ($youtubeframe.length == 1){
          var player = new YT.Player($youtubeframe.get(0), { // instantiate a new Youtube API player on each Youtube iframe (its DOM object)
            events: {
              'onReady': function(e){e.target._donecheck=true} // indicate when video has done loading
            }
          })
            $contentdiv.data("youtubeplayer", player) // store Youtube API player inside contentdiv object
        }
    })
};



