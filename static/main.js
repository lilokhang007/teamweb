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
