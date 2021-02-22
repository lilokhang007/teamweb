/* Function to hide navbar when scroll is larger than 80 px*/
window.onscroll = function() {
      if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
        document.getElementById("nav").style.top = "-80px";
      } else {
        document.getElementById("nav").style.top = "0";
      }
      prevScrollpos = currentScrollPos;
}