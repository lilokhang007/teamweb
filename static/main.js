/* Function to hide navbar when scroll is larger than 80 px*/
window.onscroll = function() {
      var height = parseFloat(document.getElementById("nav").getBoundingClientRect().height);
      console.log(height);
      if (height == 80 && (document.body.scrollTop > height || document.documentElement.scrollTop > height)) {
        document.getElementById("nav").style.top = "-80px";
      } else {
        document.getElementById("nav").style.top = "0";
      }
}

$(window).load(function () {
    var ANIMATE_DURATION = 300;
    var WAIT_DURATION = 5000;
    $('body').delay(WAIT_DURATION) //wait 5 seconds
        .animate({
            'scrollTop': $('#second').offset().top
        }, ANIMATE_DURATION);
});