var ChartColor = ["#5D62B4", "#54C3BE", "#EF726F", "#F9C446", "rgb(93.0, 98.0, 180.0)", "#21B7EC", "#04BCCC"];
var primaryColor = getComputedStyle(document.body).getPropertyValue('--primary');
var secondaryColor = getComputedStyle(document.body).getPropertyValue('--secondary');
var successColor = getComputedStyle(document.body).getPropertyValue('--success');
var warningColor = getComputedStyle(document.body).getPropertyValue('--warning');
var dangerColor = getComputedStyle(document.body).getPropertyValue('--danger');
var infoColor = getComputedStyle(document.body).getPropertyValue('--info');
var darkColor = getComputedStyle(document.body).getPropertyValue('--dark');
var lightColor = getComputedStyle(document.body).getPropertyValue('--light');

(function($) {
  'use strict';
  $(function() {
    var body = $('body');
    var contentWrapper = $('.content-wrapper');
    var scroller = $('.container-scroller');
    var footer = $('.footer');
    var sidebar = $('.sidebar');

    //Add active class to nav-link based on url dynamically
    //Active class can be hard coded directly in html file also as required

    function addActiveClass(element) {
      if (current === "") {
        //for root url
        if (element.attr('href').indexOf("index.html") !== -1) {
          element.parents('.nav-item').last().addClass('active');
          if (element.parents('.sub-menu').length) {
            element.closest('.collapse').addClass('show');
            element.addClass('active');
          }
        }
      } else {
        //for other url
        if (element.attr('href').indexOf(current) !== -1) {
          element.parents('.nav-item').last().addClass('active');
          if (element.parents('.sub-menu').length) {
            element.closest('.collapse').addClass('show');
            element.addClass('active');
          }
          if (element.parents('.submenu-item').length) {
            element.addClass('active');
          }
        }
      }
    }

    var current = location.pathname.split("/").slice(-1)[0].replace(/^\/|\/$/g, '');
    $('.nav li a', sidebar).each(function() {
      var $this = $(this);
      addActiveClass($this);
    })

    $('.horizontal-menu .nav li a').each(function() {
      var $this = $(this);
      addActiveClass($this);
    })

    //Close other submenu in sidebar on opening any

    sidebar.on('show.bs.collapse', '.collapse', function() {
      sidebar.find('.collapse.show').collapse('hide');
    });


    //Change sidebar and content-wrapper height
    applyStyles();

    function applyStyles() {
      //Applying perfect scrollbar
      if (!body.hasClass("rtl")) {
        if (body.hasClass("sidebar-fixed")) {
          var fixedSidebarScroll = new PerfectScrollbar('#sidebar .nav');
        }
      }
    }

    body.toggleClass(window.localStorage.ToggleClass)
    $('[data-toggle="minimize"]').on("click", function() {
      if (document.body.classList.toString() == 'sidebar-icon-only') {
        document.body.classList.remove('sidebar-icon-only');
        body.toggleClass('sidebar-hidden');
        window.localStorage.ToggleClass = 'sidebar-hidden';
      } else {
        document.body.classList.remove('sidebar-hidden');
        body.toggleClass('sidebar-icon-only');
        window.localStorage.ToggleClass = 'sidebar-icon-only';
      }
    });

    // icon moon_sun
    let icon_txt = localStorage.getItem("data-icon")
    let icon = JSON.parse(icon_txt)
    const element_icon = document.querySelectorAll('.nav-item .count-indicator i')[0]
    const element_conten = document.querySelector('.content-wrapper')
    const text_pageTitle = document.querySelector('.page-title')
    const text_breadcrumb = document.querySelector('.breadcrumb')
    
    if(element_icon.classList.toString() == 'bx bx-moon bx-tada-hover') {
      // icon
      element_icon.classList.add(''+icon.icon,''+icon.animation)
      // content
      element_conten.classList.add(localStorage.content)
      // text
      text_pageTitle.classList.add(localStorage.text)
      text_breadcrumb.classList.add(localStorage.text)
    }
    if(element_icon.classList.toString() == 'bx bx-sun bx-spin-hover') {
      // icon
      element_icon.classList.add(''+icon.icon,''+icon.animation)
      // content
      element_conten.classList.remove(localStorage.content)
      // text 
      text_pageTitle.classList.remove(localStorage.text)
      text_breadcrumb.classList.remove(localStorage.text)
    }

    $(".tab-icon").on("click", function(){
      const element_icon = document.querySelectorAll('.nav-item .count-indicator i')[0]
      const element_conten = document.querySelector('.content-wrapper')
      const text_pageTitle = document.querySelector('.page-title')
      const text_breadcrumb = document.querySelector('.breadcrumb')

      // console.log(element)
      if(element_icon.classList.toString() == 'bx bx-moon bx-tada-hover'){
        // icon
        element_icon.classList.remove('bx-moon', 'bx-tada-hover')
        element_icon.classList.add('bx-sun','bx-spin-hover')
        // content
        element_conten.classList.add('dark')
        localStorage.content = 'dark'
        // text
        text_pageTitle.classList.add('text-white')
        text_breadcrumb.classList.add('text-white')
        localStorage.text = 'text-white'
        
        const data_icon = { icon: "bx-sun", animation: "bx-spin-hover" }
        const obj_icon = JSON.stringify(data_icon)
        localStorage.setItem("data-icon", obj_icon)
      }else if(element_icon.classList.toString() == 'bx bx-sun bx-spin-hover' || element_icon.classList.toString() == 'bx bx-moon bx-tada-hover bx-sun bx-spin-hover'){
        // icon
        element_icon.classList.remove('bx-sun','bx-spin-hover')
        element_icon.classList.add('bx-moon', 'bx-tada-hover')
        // content
        element_conten.classList.remove('dark')
        localStorage.content = 'none'
         // text
         text_pageTitle.classList.remove('text-white')
         text_breadcrumb.classList.remove('text-white')
         localStorage.text = 'none'
        
        const data_icon = { icon: "bx-moon", animation: "bx-tada-hover" }
        const obj_icon = JSON.stringify(data_icon)
        localStorage.setItem("data-icon", obj_icon)
      }
    });

    // icon show pas
    $('.eye_input').on('click', function(){
      var eyes = document.querySelectorAll('.eye_input i')
      var password = document.getElementById('password')
      if(eyes[0].classList.toString == 'mdi mdi-eye' || password.type === "password"){
        eyes[0].classList.remove('mdi', 'mdi-eye')
        eyes[0].classList.add('bx','bx-low-vision')
        password.type ="text"
      }else{
        eyes[0].classList.remove('bx','bx-low-vision')
        eyes[0].classList.add('mdi', 'mdi-eye')
        password.type = "password"
      }
    })

    //checkbox and radios
    $(".form-check label,.form-radio label").append('<i class="input-helper"></i>');

    //fullscreen
    $("#fullscreen-button").on("click", function toggleFullScreen() {
      if ((document.fullScreenElement !== undefined && document.fullScreenElement === null) || (document.msFullscreenElement !== undefined && document.msFullscreenElement === null) || (document.mozFullScreen !== undefined && !document.mozFullScreen) || (document.webkitIsFullScreen !== undefined && !document.webkitIsFullScreen)) {
        if (document.documentElement.requestFullScreen) {
          document.documentElement.requestFullScreen();
        } else if (document.documentElement.mozRequestFullScreen) {
          document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullScreen) {
          document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
        } else if (document.documentElement.msRequestFullscreen) {
          document.documentElement.msRequestFullscreen();
        }
      } else {
        if (document.cancelFullScreen) {
          document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
          document.webkitCancelFullScreen();
        } else if (document.msExitFullscreen) {
          document.msExitFullscreen();
        }
      }
    })
    // if ($.cookie('purple-free-banner')!="true") {
    //   document.querySelector('#proBanner').classList.add('d-flex');
    //   document.querySelector('.navbar').classList.remove('fixed-top');
    // }
    // else {
    //   document.querySelector('#proBanner').classList.add('d-none');
    //   document.querySelector('.navbar').classList.add('fixed-top');
    // }
    
    if ($( ".navbar" ).hasClass( "fixed-top" )) {
      document.querySelector('.page-body-wrapper').classList.remove('pt-0');
      document.querySelector('.navbar').classList.remove('pt-5');
    }
    else {
      document.querySelector('.page-body-wrapper').classList.add('pt-0');
      document.querySelector('.navbar').classList.add('pt-5');
      document.querySelector('.navbar').classList.add('mt-3');
      
    }
    // document.querySelector('#bannerClose').addEventListener('click',function() {
    //   document.querySelector('#proBanner').classList.add('d-none');
    //   document.querySelector('#proBanner').classList.remove('d-flex');
    //   document.querySelector('.navbar').classList.remove('pt-5');
    //   document.querySelector('.navbar').classList.add('fixed-top');
    //   document.querySelector('.page-body-wrapper').classList.add('proBanner-padding-top');
    //   document.querySelector('.navbar').classList.remove('mt-3');
    //   var date = new Date();
    //   date.setTime(date.getTime() + 24 * 60 * 60 * 1000); 
    //   $.cookie('purple-free-banner', "true", { expires: date });
    // });
  });
})(jQuery);