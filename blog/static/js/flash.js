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
    var fliped= div.nextSibling;
    while (fliped.nodeType!==1)
        fliped= fliped.nextSibling;

// Flips on click                   
div.onclick= function() {
    state= !state;
    fliped.style.display= state? 'block' : 'none';
  };
};