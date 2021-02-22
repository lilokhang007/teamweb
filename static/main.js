// When the user scrolls down 80px from the top of the document, resize the navbar's padding and the logo's font size
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  var child = document.getElementById('nav').getElementsByTagName('*');

  if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
    for (var i=0, len=child.length|0; i<len; i=i+1|0) {
        child[i].style.height = "0px";
    }
  } else {
    for (var i=0, len=child.length|0; i<len; i=i+1|0) {
        child[i].style.height = "80px";
    }
  }
}