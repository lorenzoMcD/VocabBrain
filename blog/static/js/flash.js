// flip the word

window.onload= function() {
    var divs= document.getElementsByTagName('div');
    for (var i= divs.length; i-->0;)
        if (divs[i].className==='term')
            flip(divs[i]);
 };
  

  // flip it back           
function flip(div) {
    var state= false;
    var flipped= div.nextSibling;
    while (flipped.nodeType!==1)
        flipped= flipped.nextSibling;

// Flips on click                   
div.onclick= function() {
    state= !state;
    flipped.style.display= state? 'block' : 'none';
  };
};